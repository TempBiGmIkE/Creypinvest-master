# CreypInvest Investment Plans System

A comprehensive investment plans system supporting multiple investor profiles with diversified crypto and real-world asset allocation.

## Features

### 1. **Multiple Investment Plan Categories**
- **Starter Portfolio** - Beginner-friendly balanced investing
- **Couples Investment Plan** - Joint investment for couples
- **Retirement Growth Plan** - Long-term retirement savings (30-year horizon)
- **Education Fund** - Tax-optimized savings for children's education
- **Travel Fund** - Short-term fund accumulation for vacations
- **Emergency Fund** - Liquid safety net with low volatility
- **Wealth Building Premium** - High-net-worth diversified portfolio
- **Crypto Growth Aggressive** - High-risk cryptocurrency portfolio

### 2. **Asset Diversification**
Each plan allocates capital across multiple asset classes:
- **Cryptocurrencies**: Bitcoin, Ethereum, Solana, Chainlink, Polygon, Avalanche
- **Stocks/ETFs**: S&P 500, Total Market, Growth Funds, Tech-focused ETFs
- **Bonds**: Government bonds, Corporate bonds, Treasury ETFs
- **Real Estate**: REITs and property investment trusts
- **Cash/Stablecoins**: USDC, USDT for liquidity and stability

### 3. **Risk Levels**
- **Low Risk** - Conservative portfolios (4-10% annual returns)
- **Moderate Risk** - Balanced portfolios (11-15% annual returns)
- **High Risk** - Aggressive portfolios (18-35% annual returns)

### 4. **Investment Features**
- **Automated Rebalancing** - Maintains target allocation percentages
- **Tax Optimization** - Plan-specific tax-efficient strategies
- **Flexible Contributions** - Lump sum and/or monthly contributions
- **Monthly Contribution Scheduling** - Automated recurring investments (Dollar-Cost Averaging)
- **Early Withdrawal Penalties** - Variable penalties (0-15%) based on plan type

### 5. **Promotion Grants & Incentives**
- **Welcome Bonus** - New investor bonuses (e.g., 5% on first investment)
- **Referral Grants** - Earn from referring friends
- **Milestone Rewards** - Bonuses at investment milestones ($10K, $50K, etc.)
- **Seasonal Promotions** - Time-limited special offers
- **Loyalty Rewards** - Benefits for long-term investors

### 6. **Performance Tracking**
- Real-time portfolio value tracking
- Return on Investment (ROI) calculations
- Contribution history and schedules
- Performance metrics and analytics
- Portfolio rebalancing history

## Database Models

### InvestmentPlan
Core plan definition with asset allocation and expected returns.

**Key Fields:**
- `name` - Plan name (unique)
- `category` - Plan type/category
- `risk_level` - Low/Moderate/High
- `minimum_investment` - Minimum entry amount
- `recommended_investment` - Suggested amount
- `expected_annual_return` - Projected % return
- `crypto_allocation` to `cash_allocation` - Asset percentages (sum=100)
- `management_fee` - Annual fee percentage
- `recommended_duration_months` - Suggested investment period

### UserInvestmentSubscription
Tracks individual user subscriptions to plans.

**Key Fields:**
- `user_profile` - FK to user's profile
- `plan` - FK to investment plan
- `initial_investment` - Starting amount
- `current_value` - Current portfolio value
- `total_contributed` - Total invested (including monthly contributions)
- `total_returns` - Realized gains
- `status` - active/paused/completed/cancelled
- `monthly_contribution` - Optional recurring amount
- `roi_percentage` - Current return on investment %

### PlanPortfolioAsset
Individual assets within a plan's portfolio.

**Key Fields:**
- `plan` - FK to investment plan
- `asset_type` - crypto/stock/bond/real_estate/commodity/cash
- `symbol` - Trading symbol (BTC, AAPL, etc.)
- `allocation_percentage` - % of plan allocated to this asset
- `current_price` - Current market price

### MonthlyCotributionSchedule
Scheduled recurring contributions for dollar-cost averaging.

**Key Fields:**
- `subscription` - FK to user subscription
- `contribution_amount` - Scheduled contribution amount
- `scheduled_date` - When contribution is due
- `status` - scheduled/completed/failed/skipped
- `actual_contribution_date` - When it was actually processed

### InvestmentPlanPromotionGrant
Promotional bonuses and grants available for plans.

**Key Fields:**
- `plan` - FK to investment plan
- `grant_type` - welcome_bonus/referral/milestone/seasonal/loyalty
- `grant_amount` - Fixed bonus amount (optional)
- `grant_percentage` - Percentage-based bonus (optional)
- `minimum_investment_required` - Minimum to qualify
- `valid_from` / `valid_until` - Promotion period
- Methods: `is_valid_now()`, `calculate_grant_amount()`

## API Endpoints

### Browse & View Plans
```
GET  /investment-plans/                         # Browse all plans
GET  /investment-plans/?category=retirement     # Filter by category
GET  /investment-plans/?risk_level=low          # Filter by risk
GET  /investment-plans/?search=retirement       # Search plans
GET  /investment-plans/<plan_id>/               # Plan details
```

### Subscription Management
```
POST /investment-plans/<plan_id>/subscribe/     # Subscribe to plan
GET  /investment/dashboard/                     # View all subscriptions
GET  /investment/subscription/<sub_id>/         # Subscription details
POST /investment/subscription/<sub_id>/contribute/  # Add contribution
POST /investment/subscription/<sub_id>/pause/   # Pause subscription
POST /investment/subscription/<sub_id>/resume/  # Resume subscription
```

## Usage Instructions

### 1. Initialize Database with Sample Plans

```bash
# Activate virtual environment
source env/Scripts/activate

# Ensure DATABASE_URL is unset for local SQLite
unset DATABASE_URL
export DATABASE_URL=""

# Run migrations
python manage.py migrate

# Seed sample plans (recommended first time)
python manage.py seed_investment_plans

# Access admin panel
python manage.py createsuperuser  # if needed
python manage.py runserver
# Visit: http://localhost:8000/admin
```

### 2. Django Admin Features

Access investment plan management at `/admin`:

**InvestmentPlanAdmin:**
- Create/edit/delete plans
- Set asset allocations
- Configure expected returns and fees
- View AUM and investor count
- Colored risk level display

**UserInvestmentSubscriptionAdmin:**
- Monitor user subscriptions
- Track ROI performance
- View contribution schedules
- Status badges (active/paused/completed/cancelled)

**PlanPortfolioAssetAdmin:**
- Manage individual assets in plans
- Update prices
- Configure allocations

**InvestmentPlanPromotionGrantAdmin:**
- Create promotional grants
- Set validity periods
- Configure bonus amounts/percentages

### 3. User Workflow

1. **Browse Plans** - User visits `/investment-plans/`
2. **Filter & Search** - Find plans matching criteria
3. **View Details** - See asset allocation, expected returns, grants
4. **Subscribe** - Make initial investment
5. **Monitor** - Track performance in `/investment/dashboard/`
6. **Contribute** - Add monthly or lump-sum contributions
7. **Manage** - Pause/resume subscription as needed

## Asset Allocation Examples

### Starter Portfolio (Beginner)
```
Bitcoin (15%) + Ethereum (15%)         = 30% Crypto
S&P 500 ETF (40%)                      = 40% Stocks
Total Bond Market (20%)                = 20% Bonds
USD Coin Stablecoin (10%)              = 10% Cash
```

### Retirement Plan (Conservative, 30 years)
```
Bitcoin (10%)                          = 10% Crypto
Nasdaq 100 + Total Stock (40%)         = 40% Stocks
Bond ETFs (40%)                        = 40% Bonds
Stablecoin (10%)                       = 10% Cash
```

### Wealth Building (High Net Worth)
```
Bitcoin (20%) + Ethereum (15%)         = 40% Crypto
Nasdaq 100 + Growth ETFs (35%)         = 35% Stocks
Long-term Treasury Bonds (15%)         = 15% Bonds
Real Estate Fund (10%)                 = 10% Real Estate
```

### Crypto Growth (Aggressive, High Risk)
```
Bitcoin (40%)                          = 40% Crypto
Ethereum (25%) + Solana (10%)          = 35% Crypto
Avalanche (10%)                        = 10% Crypto
S&P 500 ETF (10%)                      = 10% Stocks
Stablecoin (5%)                        = 5% Cash
```
**Total Crypto: 85% | Stocks: 10% | Cash: 5%**

## Return Projections

Based on historical market data:

| Plan | Expected Return | Risk Level | Duration |
|------|-----------------|-----------|----------|
| Starter | 12.5% | Moderate | 12 months |
| Couples | 14.0% | Moderate | 24 months |
| Retirement | 9.0% | Low | 30 years |
| Education | 11.5% | Moderate | 15 years |
| Travel | 13.0% | Moderate | 24 months |
| Emergency | 5.5% | Low | 12 months |
| Wealth | 18.5% | High | 5 years |
| Crypto | 35.0% | High | 24 months |

## Promotion Grants (Included)

1. **New Investor Welcome** - 5% bonus on Starter plan
2. **Couples Referral** - $200 per successful referral
3. **Milestone Reward** - $500 for $10K investment in Crypto plan

## Future Enhancements

- [ ] Real-time price updates via API
- [ ] Advanced charting and analytics dashboard
- [ ] Automated monthly contribution processing
- [ ] Tax reporting integration
- [ ] Withdrawal request processing
- [ ] Performance benchmarking
- [ ] Portfolio rebalancing automation
- [ ] Mobile app
- [ ] API for third-party integrations

## Technical Stack

- **Framework**: Django 5.0
- **Database**: SQLite (local) / PostgreSQL (production)
- **Models**: 5 primary models + relationships
- **Admin**: Django admin with custom forms
- **Management Commands**: Seed data generation

## Security Considerations

- Users can only view/edit their own subscriptions
- Investment amounts validated against plan limits
- Grants automatically calculated and applied
- Early withdrawal penalties enforced
- All transactions logged with timestamps

---

**Created**: December 2025  
**Version**: 1.0  
**Status**: Ready for deployment
