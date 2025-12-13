from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Avg, Count
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from creyp.utils import send_contact_us_email, set_cookie_function
from users.models import Profile
from users.decorators import update_user_ip
from core.models import (
    InvestmentPlan,
    UserInvestmentSubscription,
    PlanPortfolioAsset,
    InvestmentPlanPromotionGrant,
)


# ============================================================================
# Investment Plans Views
# ============================================================================

@update_user_ip
def investment_plans_browse_view(request):
    """Browse all available investment plans."""
    
    # Get filter parameters
    category = request.GET.get('category')
    risk_level = request.GET.get('risk_level')
    search = request.GET.get('search')
    
    plans = InvestmentPlan.objects.filter(is_active=True)
    
    # Apply filters
    if category:
        plans = plans.filter(category=category)
    if risk_level:
        plans = plans.filter(risk_level=risk_level)
    if search:
        plans = plans.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Add user's current subscriptions to context
    user_subscriptions = []
    if request.user.is_authenticated:
        user_subscriptions = UserInvestmentSubscription.objects.filter(
            user_profile=request.user.profile,
            status__in=['active', 'paused']
        )
    
    context = {
        'title': 'Investment Plans',
        'plans': plans,
        'user_subscriptions': user_subscriptions,
    }
    
    return render(request, 'investment/plans_browse.html', context)


@update_user_ip
def investment_plan_detail_view(request, plan_id):
    """View detailed information about a specific investment plan."""
    
    plan = get_object_or_404(InvestmentPlan, id=plan_id, is_active=True)
    assets = plan.portfolio_assets.filter(is_active=True)
    promotions = plan.grants.filter(
        is_active=True,
        valid_from__lte=timezone.now(),
        valid_until__gte=timezone.now()
    )
    
    # Check if user already has this subscription
    has_subscription = False
    if request.user.is_authenticated:
        has_subscription = UserInvestmentSubscription.objects.filter(
            user_profile=request.user.profile,
            plan=plan,
            status__in=['active', 'paused']
        ).exists()
    
    context = {
        'title': f'{plan.name} - Investment Plan',
        'plan': plan,
        'assets': assets,
        'promotions': promotions,
        'has_subscription': has_subscription,
    }
    
    return render(request, 'investment/plan_detail.html', context)


@login_required
@update_user_ip
def subscribe_to_plan_view(request, plan_id):
    """Subscribe user to an investment plan."""
    
    plan = get_object_or_404(InvestmentPlan, id=plan_id, is_active=True)
    
    # Check if user already has this subscription
    existing = UserInvestmentSubscription.objects.filter(
        user_profile=request.user.profile,
        plan=plan,
        status__in=['active', 'paused']
    ).first()
    
    if existing:
        return redirect('plan_detail', plan_id=plan_id)
    
    if request.method == 'POST':
        initial_investment = request.POST.get('initial_investment')
        monthly_contribution = request.POST.get('monthly_contribution')
        
        try:
            initial_investment = Decimal(initial_investment)
            
            # Validate investment amount
            if initial_investment < plan.min_investment:
                error = f'Minimum investment is ${plan.min_investment}'
                return render(request, 'investment/subscribe_plan.html', {
                    'plan': plan,
                    'form': {'initial_investment': {'errors': [error]}},
                })
            
            # Create subscription
            duration_days = plan.investment_duration * 30
            planned_end_date = timezone.now() + timedelta(days=duration_days)
            
            subscription = UserInvestmentSubscription.objects.create(
                user_profile=request.user.profile,
                plan=plan,
                initial_investment=initial_investment,
                current_value=initial_investment,
                total_contributed=initial_investment,
                planned_end_date=planned_end_date,
            )
            
            # Add monthly contribution if provided
            if monthly_contribution:
                subscription.monthly_contribution = Decimal(monthly_contribution)
                subscription.next_contribution_date = timezone.now() + timedelta(days=30)
                subscription.save()
            
            # Apply grants if available
            applicable_grants = plan.grants.filter(
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_until__gte=timezone.now(),
                minimum_investment_required__lte=initial_investment
            )
            
            total_grant = Decimal(0)
            for grant in applicable_grants:
                grant_amount = grant.calculate_grant_amount(initial_investment)
                if grant_amount > 0:
                    total_grant += grant_amount
            
            # Add grant to subscription
            if total_grant > 0:
                subscription.current_value += total_grant
                subscription.total_contributed += total_grant
                subscription.save()
            
            return redirect('investment_dashboard')
        
        except (ValueError, TypeError):
            error = 'Invalid investment amount'
            return render(request, 'investment/subscribe_plan.html', {
                'plan': plan,
                'form': {'initial_investment': {'errors': [error]}},
            })
    
    # Get active promotions
    promotions = plan.grants.filter(
        is_active=True,
        valid_from__lte=timezone.now(),
        valid_until__gte=timezone.now()
    )
    
    context = {
        'title': f'Subscribe to {plan.name}',
        'plan': plan,
        'promotions': promotions,
        'form': {},
    }
    return render(request, 'investment/subscribe_plan.html', context)


@login_required
@update_user_ip
def investment_dashboard_view(request):
    """User's investment dashboard with all subscriptions."""
    
    subscriptions = UserInvestmentSubscription.objects.filter(
        user_profile=request.user.profile,
        status__in=['active', 'paused']
    )
    
    # Calculate totals
    total_invested = subscriptions.aggregate(Sum('total_contributed'))['total_contributed__sum'] or Decimal(0)
    current_value = subscriptions.aggregate(Sum('current_value'))['current_value__sum'] or Decimal(0)
    total_gain = current_value - total_invested
    
    # Calculate overall ROI
    overall_roi = Decimal(0)
    if total_invested > 0:
        overall_roi = (total_gain / total_invested) * 100
    
    # Get recent contributions
    from core.models import MonthlyCotributionSchedule
    recent_contributions = MonthlyCotributionSchedule.objects.filter(
        subscription__user_profile=request.user.profile
    ).order_by('-scheduled_date')[:10]
    
    # Get monthly contributions total
    monthly_contributions = subscriptions.aggregate(Sum('monthly_contribution'))['monthly_contribution__sum'] or Decimal(0)
    
    context = {
        'title': 'Investment Dashboard',
        'subscriptions': subscriptions,
        'total_invested': total_invested,
        'current_value': current_value,
        'total_gain': total_gain,
        'overall_roi': overall_roi,
        'subscription_count': subscriptions.count(),
        'monthly_contributions': monthly_contributions,
        'recent_contributions': recent_contributions,
    }
    
    return render(request, 'investment/dashboard.html', context)


@login_required
@update_user_ip
def subscription_detail_view(request, subscription_id):
    """View detailed information about a specific subscription."""
    
    subscription = get_object_or_404(
        UserInvestmentSubscription,
        id=subscription_id,
        user_profile=request.user.profile
    )
    
    # Get contribution schedule
    contributions = subscription.contribution_schedules.all()
    
    # Calculate metrics
    roi = subscription.calculate_roi()
    remaining_days = subscription.get_duration_remaining()
    
    context = {
        'title': f'{subscription.plan.name} - Investment Details',
        'subscription': subscription,
        'plan': subscription.plan,
        'portfolio_assets': subscription.plan.portfolio_assets.filter(is_active=True),
        'contributions': contributions,
        'roi': roi,
        'remaining_days': remaining_days,
        'asset_allocation': subscription.plan.get_asset_allocation(),
    }
    
    return render(request, 'investment/subscription_detail.html', context)


@login_required
@update_user_ip
def add_contribution_view(request, subscription_id):
    """Add additional contribution to an active subscription."""
    
    subscription = get_object_or_404(
        UserInvestmentSubscription,
        id=subscription_id,
        user_profile=request.user.profile,
        status='active'
    )
    
    if request.method == 'POST':
        contribution_amount = request.POST.get('contribution_amount')
        
        try:
            contribution_amount = Decimal(contribution_amount)
            
            if contribution_amount <= 0:
                return render(request, 'investment/add_contribution.html', {
                    'subscription': subscription,
                    'error': 'Contribution must be greater than 0',
                })
            
            # Add contribution
            subscription.total_contributed += contribution_amount
            subscription.current_value += contribution_amount
            subscription.save()
            
            return redirect('subscription_detail', subscription_id=subscription_id)
        
        except (ValueError, TypeError):
            return render(request, 'investment/add_contribution.html', {
                'subscription': subscription,
                'error': 'Invalid contribution amount',
            })
    
    context = {
        'title': f'Add Contribution - {subscription.plan.name}',
        'subscription': subscription,
    }
    return render(request, 'investment/add_contribution.html', context)


@login_required
@update_user_ip
def pause_subscription_view(request, subscription_id):
    """Pause an active subscription."""
    
    subscription = get_object_or_404(
        UserInvestmentSubscription,
        id=subscription_id,
        user_profile=request.user.profile,
        status='active'
    )
    
    if request.method == 'POST':
        subscription.status = 'paused'
        subscription.save()
        return redirect('investment_dashboard')
    
    context = {
        'title': 'Pause Subscription',
        'subscription': subscription,
    }
    return render(request, 'investment/pause_subscription.html', context)


@login_required
@update_user_ip
def resume_subscription_view(request, subscription_id):
    """Resume a paused subscription."""
    
    subscription = get_object_or_404(
        UserInvestmentSubscription,
        id=subscription_id,
        user_profile=request.user.profile,
        status='paused'
    )
    
    if request.method == 'POST':
        subscription.status = 'active'
        subscription.save()
        return redirect('investment_dashboard')
    
    context = {
        'title': 'Resume Subscription',
        'subscription': subscription,
    }
    return render(request, 'investment/resume_subscription.html', context)


# ============================================================================
# Original Views
# ============================================================================

def error_404_view(request, exception):
    return render(request, "pages/errors/404.html")

@update_user_ip
def dashboard_denial_view(request):
    return render(request, "pages/errors/dashboard_denial.html")

@update_user_ip
def index(request):
    return render(request, "pages/index.html")

@update_user_ip
def referral_view(request, username):
    cookie = request.COOKIES.get("_refered_by", None) == None
    user = request.user
    is_user = str(request.user.username) == str(username)
    context = {}
    if not user.is_authenticated:
        if cookie == True:
            context = {
                "username": username,
                "title": "Congratulation",
                "message": f"You were been referred by {username}, now signup and deposit above $1,000 to get $100 has welcoming gift!",
                "btn": "signup"
            }
            res = render(request, "pages/referral.html", context)
            set_cookie_function("_refered_by", str(username),
                                max_age=500*1900, response=res)
            qs = Profile.objects.filter(user__username=username).first()
            qs.refer_clicks = qs.refer_clicks + 1
            qs.save()
        else:
            try:
                context = {
                    "username": username,
                    "title": "Hey!",
                    "message": f"You have already been referred by {request.COOKIES['_refered_by']}, just create an account and deposit above $1,000 then get your $100 welcoming gift!",
                    "btn": "signup"
                }
            except:
                context = {
                    "username": username,
                    "title": "Hey!",
                    "message": f"You have already been referred, just create an account and deposit above $1,000 then get your $100 welcoming gift!",
                    "btn": "signup"
                }
            res = render(request, "pages/referral.html", context)
    elif user.is_authenticated:
        if is_user:
            context = {
                "username": username,
                "title": f"Sorry {user.username}",
                "message": "You can not refer yourself",
                "btn": "back"
            }
            res = render(request, "pages/referral.html", context)
        else:
            return redirect("dashboard-home")
    return res

@update_user_ip
def about(request):
    return render(request, "pages/about.html", {"type": "About CreypInvest Inc.", "crumbs": ["About Us"]})

@update_user_ip
def contact(request):
    return render(request, "pages/contact.html", {"type": "Contact Support Team At CreypInvest Inc.", "crumbs": ["Contact Us"]})

@update_user_ip
def send_contact_email(request):
    res = render(request, "pages/message_page.html",
                 {"title": "Oops", "msg": "Sorry, something is wrong with the server but you can mail us at <a href='mailto:creypinvest@gmail.com'>creypinvest@gmail.com</a>"})
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        body = request.POST.get("message")
        try:
            send_contact_us_email(request, name, phone,
                                  email, subject, body, toAdmin=True)
            send_contact_us_email(request, name, phone, email, "Email Has Been Recieved",
                                  "Your Email Has Been Received, We Will Get Back To You A Soon As Possible")
            res = render(request, "pages/message_page.html",
                         {"title": "Yay!", "msg": "Your mail has been sent to us"})
        except:
            res = render(request, "pages/message_page.html", {
                         "title": "Oops", "msg": "Sorry, something is wrong with the server but you can mail us at <a href='mailto:creypinvest@gmail.com'>creypinvest@gmail.com</a>"})
    return res
