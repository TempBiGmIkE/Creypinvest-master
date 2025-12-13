from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from users.models import Profile


class InvestmentPlan(models.Model):
    """
    Investment plans tailored to different investor profiles.
    Supports diversified crypto and real-world assets.
    """
    
    PLAN_CATEGORIES = (
        ('starter', 'Starter - Beginner Investors'),
        ('couples', 'Couples - Joint Investment'),
        ('retirement', 'Retirement - Long-term Growth'),
        ('education', 'Education Fund - Child\'s Future'),
        ('travel', 'Travel Fund - Adventure Fund'),
        ('emergency', 'Emergency Fund - Safety Net'),
        ('wealth', 'Wealth Building - Premium'),
        ('crypto', 'Crypto Growth - High Risk/Reward'),
    )
    
    RISK_LEVELS = (
        ('low', 'Low Risk - Conservative'),
        ('moderate', 'Moderate Risk - Balanced'),
        ('high', 'High Risk - Aggressive Growth'),
    )
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=PLAN_CATEGORIES)
    description = models.TextField()
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS)
    
    # Investment amounts
    minimum_investment = models.DecimalField(max_digits=15, decimal_places=2, default=100)
    recommended_investment = models.DecimalField(max_digits=15, decimal_places=2)
    maximum_investment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Returns and performance
    expected_annual_return = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="Expected annual return percentage (0-100%)"
    )
    historical_performance = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Historical average annual return percentage"
    )
    
    # Asset allocation
    crypto_allocation = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        help_text="Percentage allocated to cryptocurrencies"
    )
    real_estate_allocation = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        help_text="Percentage allocated to real estate/property"
    )
    stocks_allocation = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        help_text="Percentage allocated to stocks"
    )
    bonds_allocation = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        help_text="Percentage allocated to bonds"
    )
    cash_allocation = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        help_text="Percentage allocated to cash/stablecoins"
    )
    
    # Plan duration
    recommended_duration_months = models.IntegerField(
        help_text="Recommended investment period in months"
    )
    early_withdrawal_penalty = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Penalty percentage for early withdrawal"
    )
    
    # Features
    is_automated_rebalancing = models.BooleanField(default=True)
    is_tax_optimized = models.BooleanField(default=False)
    allows_monthly_contribution = models.BooleanField(default=True)
    allows_lump_sum = models.BooleanField(default=True)
    
    # Metrics and metadata
    management_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.5,
        help_text="Annual management fee percentage"
    )
    current_aum = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        help_text="Current assets under management"
    )
    number_of_investors = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'minimum_investment']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['risk_level']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    
    def get_asset_allocation(self):
        """Returns asset allocation as a dictionary."""
        return {
            'crypto': self.crypto_allocation,
            'real_estate': self.real_estate_allocation,
            'stocks': self.stocks_allocation,
            'bonds': self.bonds_allocation,
            'cash': self.cash_allocation,
        }
    
    def validate_allocation(self):
        """Validate that asset allocations sum to 100%."""
        total = (
            self.crypto_allocation +
            self.real_estate_allocation +
            self.stocks_allocation +
            self.bonds_allocation +
            self.cash_allocation
        )
        return total == 100


class UserInvestmentSubscription(models.Model):
    """
    Track user subscriptions to investment plans.
    """
    
    SUBSCRIPTION_STATUS = (
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='investment_subscriptions')
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.PROTECT, related_name='subscriptions')
    
    initial_investment = models.DecimalField(max_digits=15, decimal_places=2)
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    total_contributed = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_returns = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS, default='active')
    
    subscription_start_date = models.DateTimeField(auto_now_add=True)
    planned_end_date = models.DateTimeField()
    actual_end_date = models.DateTimeField(null=True, blank=True)
    
    monthly_contribution = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Monthly recurring contribution amount"
    )
    next_contribution_date = models.DateTimeField(null=True, blank=True)
    
    # Performance tracking
    roi_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    last_rebalance_date = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('user_profile', 'plan')
        ordering = ['-subscription_start_date']
    
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.plan.name}"
    
    def calculate_roi(self):
        """Calculate return on investment percentage."""
        if self.initial_investment > 0:
            roi = ((self.current_value - self.initial_investment) / self.initial_investment) * 100
            self.roi_percentage = roi
            return roi
        return 0
    
    def get_duration_remaining(self):
        """Get remaining duration in days."""
        if self.status == 'active':
            remaining = (self.planned_end_date - timezone.now()).days
            return max(0, remaining)
        return 0


class PlanPortfolioAsset(models.Model):
    """
    Individual assets held within an investment plan portfolio.
    Tracks specific cryptocurrencies, stocks, ETFs, real estate properties, etc.
    """
    
    ASSET_TYPES = (
        ('crypto', 'Cryptocurrency'),
        ('stock', 'Stock/ETF'),
        ('bond', 'Bond/Fixed Income'),
        ('real_estate', 'Real Estate/Property'),
        ('commodity', 'Commodity'),
        ('cash', 'Cash/Stablecoin'),
    )
    
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE, related_name='portfolio_assets')
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    symbol = models.CharField(max_length=20, help_text="e.g., BTC, AAPL, SPY")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    allocation_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Percentage of plan allocated to this asset"
    )
    
    current_price = models.DecimalField(max_digits=15, decimal_places=8)
    price_updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    added_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['plan', '-allocation_percentage']
    
    def __str__(self):
        return f"{self.plan.name} - {self.symbol} ({self.allocation_percentage}%)"


class MonthlyCotributionSchedule(models.Model):
    """
    Track monthly contribution schedules for recurring investments.
    """
    
    subscription = models.ForeignKey(
        UserInvestmentSubscription,
        on_delete=models.CASCADE,
        related_name='contribution_schedules'
    )
    
    contribution_amount = models.DecimalField(max_digits=15, decimal_places=2)
    scheduled_date = models.DateField()
    actual_contribution_date = models.DateField(null=True, blank=True)
    actual_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('skipped', 'Skipped'),
        ),
        default='scheduled'
    )
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['scheduled_date']
    
    def __str__(self):
        return f"{self.subscription} - {self.scheduled_date}"


class InvestmentPlanPromotionGrant(models.Model):
    """
    Promotion grants and incentives for different investment plans.
    E.g., "First-time investors get 5% bonus", "Referral grants", etc.
    """
    
    GRANT_TYPES = (
        ('welcome_bonus', 'Welcome Bonus'),
        ('referral', 'Referral Bonus'),
        ('milestone', 'Milestone Reward'),
        ('seasonal', 'Seasonal Promotion'),
        ('loyalty', 'Loyalty Reward'),
    )
    
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE, related_name='grants')
    grant_type = models.CharField(max_length=20, choices=GRANT_TYPES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    grant_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Fixed bonus amount in USD"
    )
    grant_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Percentage-based bonus (e.g., 5% of investment)"
    )
    
    minimum_investment_required = models.DecimalField(max_digits=15, decimal_places=2)
    maximum_grant_per_user = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-valid_from']
    
    def __str__(self):
        return f"{self.plan.name} - {self.name}"
    
    def is_valid_now(self):
        """Check if grant is currently active."""
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_until
    
    def calculate_grant_amount(self, investment_amount):
        """Calculate the grant amount for a given investment."""
        if not self.is_valid_now():
            return 0
        
        if self.grant_amount:
            grant = min(self.grant_amount, investment_amount)
        elif self.grant_percentage:
            grant = (investment_amount * self.grant_percentage) / 100
        else:
            grant = 0
        
        if self.maximum_grant_per_user:
            grant = min(grant, self.maximum_grant_per_user)
        
        return grant
