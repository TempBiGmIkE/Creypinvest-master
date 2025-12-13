from django.contrib import admin
from django.utils.html import format_html
from core.models import (
    InvestmentPlan,
    UserInvestmentSubscription,
    PlanPortfolioAsset,
    MonthlyCotributionSchedule,
    InvestmentPlanPromotionGrant,
)


@admin.register(InvestmentPlan)
class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category_display',
        'risk_level_display',
        'minimum_investment',
        'expected_return_display',
        'allocation_summary',
        'is_active',
    )
    list_filter = ('category', 'risk_level', 'is_active', 'is_automated_rebalancing')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'current_aum', 'number_of_investors')
    
    fieldsets = (
        ('Plan Information', {
            'fields': ('name', 'category', 'description', 'risk_level', 'is_active')
        }),
        ('Investment Amounts', {
            'fields': ('minimum_investment', 'recommended_investment', 'maximum_investment')
        }),
        ('Performance', {
            'fields': ('expected_annual_return', 'historical_performance', 'management_fee')
        }),
        ('Asset Allocation', {
            'fields': (
                'crypto_allocation',
                'real_estate_allocation',
                'stocks_allocation',
                'bonds_allocation',
                'cash_allocation',
            )
        }),
        ('Plan Features', {
            'fields': (
                'recommended_duration_months',
                'early_withdrawal_penalty',
                'is_automated_rebalancing',
                'is_tax_optimized',
                'allows_monthly_contribution',
                'allows_lump_sum',
            )
        }),
        ('Metrics', {
            'fields': ('current_aum', 'number_of_investors', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def category_display(self, obj):
        return obj.get_category_display()
    category_display.short_description = 'Category'
    
    def risk_level_display(self, obj):
        colors = {
            'low': '#28a745',
            'moderate': '#ffc107',
            'high': '#dc3545',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.risk_level, '#000'),
            obj.get_risk_level_display()
        )
    risk_level_display.short_description = 'Risk Level'
    
    def expected_return_display(self, obj):
        return f"{obj.expected_annual_return}%"
    expected_return_display.short_description = 'Expected Return'
    
    def allocation_summary(self, obj):
        parts = []
        if obj.crypto_allocation > 0:
            parts.append(f"C:{obj.crypto_allocation}%")
        if obj.real_estate_allocation > 0:
            parts.append(f"RE:{obj.real_estate_allocation}%")
        if obj.stocks_allocation > 0:
            parts.append(f"S:{obj.stocks_allocation}%")
        if obj.bonds_allocation > 0:
            parts.append(f"B:{obj.bonds_allocation}%")
        if obj.cash_allocation > 0:
            parts.append(f"Ca:{obj.cash_allocation}%")
        return " | ".join(parts) if parts else "No allocation"
    allocation_summary.short_description = 'Asset Allocation'


@admin.register(UserInvestmentSubscription)
class UserInvestmentSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user_profile',
        'plan',
        'initial_investment_display',
        'current_value_display',
        'status_badge',
        'roi_display',
        'subscription_start_date',
    )
    list_filter = ('status', 'plan__category', 'plan__risk_level', 'subscription_start_date')
    search_fields = ('user_profile__user__username', 'plan__name')
    readonly_fields = ('subscription_start_date', 'roi_percentage')
    
    fieldsets = (
        ('User & Plan', {
            'fields': ('user_profile', 'plan')
        }),
        ('Investment Details', {
            'fields': (
                'initial_investment',
                'current_value',
                'total_contributed',
                'total_returns',
                'roi_percentage',
            )
        }),
        ('Subscription', {
            'fields': (
                'status',
                'subscription_start_date',
                'planned_end_date',
                'actual_end_date',
            )
        }),
        ('Contributions', {
            'fields': (
                'monthly_contribution',
                'next_contribution_date',
            ),
            'classes': ('collapse',)
        }),
        ('Rebalancing', {
            'fields': ('last_rebalance_date',),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def initial_investment_display(self, obj):
        return f"${obj.initial_investment:,.2f}"
    initial_investment_display.short_description = 'Initial Investment'
    
    def current_value_display(self, obj):
        return f"${obj.current_value:,.2f}"
    current_value_display.short_description = 'Current Value'
    
    def status_badge(self, obj):
        colors = {
            'active': '#28a745',
            'paused': '#ffc107',
            'completed': '#007bff',
            'cancelled': '#dc3545',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#999'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def roi_display(self, obj):
        roi = obj.calculate_roi()
        color = '#28a745' if roi >= 0 else '#dc3545'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.2f}%</span>',
            color,
            roi
        )
    roi_display.short_description = 'ROI'


@admin.register(PlanPortfolioAsset)
class PlanPortfolioAssetAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'asset_type', 'plan', 'allocation_percentage', 'current_price', 'is_active')
    list_filter = ('asset_type', 'plan', 'is_active')
    search_fields = ('symbol', 'name', 'plan__name')
    
    fieldsets = (
        ('Asset Information', {
            'fields': ('plan', 'asset_type', 'symbol', 'name', 'description')
        }),
        ('Allocation & Pricing', {
            'fields': ('allocation_percentage', 'current_price', 'price_updated_at')
        }),
        ('Status', {
            'fields': ('is_active', 'added_date'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('price_updated_at', 'added_date')


@admin.register(MonthlyCotributionSchedule)
class MonthlyCotributionScheduleAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'contribution_amount', 'scheduled_date', 'status', 'actual_contribution_date')
    list_filter = ('status', 'scheduled_date')
    search_fields = ('subscription__user_profile__user__username', 'subscription__plan__name')
    
    fieldsets = (
        ('Subscription', {
            'fields': ('subscription',)
        }),
        ('Scheduled Contribution', {
            'fields': ('contribution_amount', 'scheduled_date')
        }),
        ('Actual Contribution', {
            'fields': ('actual_contribution_date', 'actual_amount', 'status')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )


@admin.register(InvestmentPlanPromotionGrant)
class InvestmentPlanPromotionGrantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'grant_type',
        'plan',
        'grant_display',
        'valid_from',
        'valid_until',
        'is_active',
    )
    list_filter = ('grant_type', 'plan', 'is_active', 'valid_from')
    search_fields = ('name', 'description', 'plan__name')
    
    fieldsets = (
        ('Grant Information', {
            'fields': ('plan', 'grant_type', 'name', 'description', 'is_active')
        }),
        ('Grant Amount', {
            'fields': ('grant_amount', 'grant_percentage', 'minimum_investment_required', 'maximum_grant_per_user')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)
    
    def grant_display(self, obj):
        if obj.grant_amount:
            return f"${obj.grant_amount:,.2f}"
        elif obj.grant_percentage:
            return f"{obj.grant_percentage}%"
        return "N/A"
    grant_display.short_description = 'Grant Amount'
