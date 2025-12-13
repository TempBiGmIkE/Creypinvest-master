from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django_countries import countries
from users.models import Wallet, Profile, Transaction, AdminWallet
from users.decorators import update_user_ip, deposit_before


@update_user_ip
@deposit_before
def dashboard_home_view(request):
    if request.user.is_authenticated:
        if not Wallet.objects.filter(user=request.user.profile):
            Wallet.objects.create(user=request.user.profile)
        qs = Wallet.objects.filter(user=request.user.profile).first()
        bal = str(qs.balance).split(".")
        first_bal = bal[0]
        second_bal = bal[1] if len(bal) > 1 else "00"
        transactions = Transaction.objects.filter(wallet=request.user.profile.wallet)
        amount_invested = float(qs.amount_invested)
        if amount_invested == 0:
            for transaction in (
                transactions.exclude(status="pending")
                .exclude(status="processing")
                .exclude(status="confirming")
                .exclude(status="error")
                .exclude(status="failed")
            ):
                amount_invested += float(transaction.amount)

        context = {
            "title": "Dashboard",
            "crumbs": ["Dashboard"],
            "bal": qs.balance,
            "first_bal": first_bal,
            "amount_invested": amount_invested,
            "second_bal": second_bal,
            "crumbs_count": 1,
            "transactions": transactions.exclude(status="hidden"),
        }
        return render(request, "dashboard/dashboard_home.html", context)
    else:
        return redirect("/auth/account/login?next=/dashboard/")


@update_user_ip
def dashboard_profile_view(request):
    if request.user.is_authenticated:
        if not Wallet.objects.filter(user=request.user.profile):
            Wallet.objects.create(user=request.user.profile)
        context = {
            "title": "Profile",
            "crumbs": ["Profile"],
            "crumbs_count": 2,
            "countries": countries,
        }
        return render(request, "dashboard/dashboard_profile.html", context)
    else:
        return redirect("/auth/account/login?next=/dashboard/profile/")


@update_user_ip
def dashboard_profile_auth_view(request):
    if request.method == "POST":
        form = request.POST
        profile_image = form.get("profile_image")
        if "profile_image" in request.FILES:
            profile_image = request.FILES["profile_image"]
        # KYC / documents
        kyc_file = None
        financial_file = None
        loan_file = None
        if "kyc_doc" in request.FILES:
            kyc_file = request.FILES["kyc_doc"]
        if "financial_doc" in request.FILES:
            financial_file = request.FILES["financial_doc"]
        if "loan_doc" in request.FILES:
            loan_file = request.FILES["loan_doc"]
        full_name = form.get("full_name").strip()
        full_name_list = full_name.split(" ")
        full_name = []
        for name in full_name_list:
            full_name.append(name.strip())
        email = form.get("email").strip()
        phone_number = form.get("phone_number").strip()
        gender = form["gender"]
        country = form["country"]

        user = request.user
        user_ = User.objects.filter(username=user.username).first()
        user_profile = Profile.objects.filter(user=user).first()

        try:
            if len(full_name) > 1:
                user_.first_name = full_name[0]
                user_profile.first_name = full_name[0]
                user_.last_name = full_name[1]
                user_profile.last_name = full_name[1]
            elif len(full_name) == 1:
                user_.first_name = full_name[0]
                user_profile.first_name = full_name[0]

        except:
            user_.first_name = ""
            user_profile.first_name = ""

            user_.last_name = ""
            user_profile.last_name = ""

        user_.email = email

        # deleting old uploaded image.
        # image_path = user_profile.image
        # if os.path.exists(image_path):
        #     os.remove(image_path)

        user_profile.email = email
        user_profile.image = profile_image
        user_profile.phone_number = phone_number
        user_profile.gender = gender
        user_profile.country = country

        # Handle KYC uploads (create KycDocument records)
        try:
            from users.models import KycDocument
            if kyc_file:
                KycDocument.objects.create(profile=user_profile, document_type="id", file=kyc_file)
            if financial_file:
                KycDocument.objects.create(profile=user_profile, document_type="financial", file=financial_file)
            if loan_file:
                KycDocument.objects.create(profile=user_profile, document_type="loan", file=loan_file)
        except Exception:
            # If anything goes wrong creating documents, ignore to not break profile update
            pass

        user_.save()
        user_profile.save()

        return redirect(
            "/dashboard/profile/?success=yes&msg=your+profile+has+been+updated"
        )
    return redirect("dashboard-profile")


@update_user_ip
@deposit_before
def dashboard_payments_view(request):
    if request.user.is_authenticated:
        if not Wallet.objects.filter(user=request.user.profile):
            Wallet.objects.create(user=request.user.profile)
        qs = Wallet.objects.filter(user=request.user.profile).first()
        bal = str(qs.balance).split(".")
        first_bal = bal[0]
        second_bal = bal[1] if len(bal) > 1 else "00"
        transactions = Transaction.objects.filter(wallet=request.user.profile.wallet)
        amount_invested = float(qs.amount_invested)
        if amount_invested == 0:
            for transaction in (
                transactions.exclude(status="pending")
                .exclude(status="processing")
                .exclude(status="confirming")
                .exclude(status="error")
                .exclude(status="failed")
            ):
                amount_invested += float(transaction.amount)
        context = {
            "title": "Payments",
            "crumbs": ["Payment"],
            "bal": qs.balance,
            "first_bal": first_bal,
            "amount_invested": amount_invested,
            "second_bal": second_bal,
            "crumbs_count": 2,
            "transactions": transactions.exclude(status="hidden"),
        }
        return render(request, "dashboard/dashboard_payments.html", context)
    else:
        return redirect("/auth/account/login?next=/dashboard/payments/")


@update_user_ip
@deposit_before
def dashboard_referral_view(request):
    if request.user.is_authenticated:
        user = request.user
        if not Wallet.objects.filter(user=request.user.profile):
            Wallet.objects.create(user=request.user.profile)
        refers = {"clicks": f"{user.profile.refer_clicks}"}
        context = {
            "title": "Referral",
            "crumbs": ["Referral"],
            "crumbs_count": 2,
            "refers": refers,
        }
        return render(request, "dashboard/dashboard_referral.html", context)
    else:
        return redirect("/auth/account/login?next=/dashboard/referral/")
