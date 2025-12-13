# 🚀 Quick Start Guide - Investment Plans

## Installation & Setup (5 minutes)

```bash
# 1. Activate environment and unset remote DB
source env/Scripts/activate
unset DATABASE_URL
export DATABASE_URL=""

# 2. Run migrations (already done)
python manage.py migrate

# 3. Seed sample plans (already done)
python manage.py seed_investment_plans

# 4. Start dev server
python manage.py runserver
```

## Admin Access

**URL**: http://localhost:8000/admin  
**Username**: jordan  
**Password**: Password123!

---

## Investment Plans Overview

### 🌱 Starter Portfolio
- **Min**: $100 | **Rec**: $500
- **Return**: 12.5% | **Risk**: Moderate
- **Best for**: Beginners
- **Assets**: 30% Crypto + 40% Stocks + 20% Bonds + 10% Cash

### 👥 Couples Investment Plan
- **Min**: $1,000 | **Rec**: $5,000
- **Return**: 14.0% | **Risk**: Moderate
- **Best for**: Joint investments
- **Assets**: 25% Crypto + 45% Stocks + 20% Bonds + 10% Real Estate

### 🏖️ Retirement Growth Plan
- **Min**: $5,000 | **Rec**: $15,000
- **Return**: 9.0% | **Risk**: Low
- **Best for**: Long-term (30 years)
- **Assets**: 10% Crypto + 40% Stocks + 40% Bonds + 10% Cash

### 🎓 Education Fund Plan
- **Min**: $500 | **Rec**: $2,000
- **Return**: 11.5% | **Risk**: Moderate
- **Best for**: Child's education (15 years)
- **Assets**: 20% Crypto + 50% Stocks + 20% Bonds + 10% Cash
- **Feature**: Tax-optimized

### ✈️ Travel Fund Plan
- **Min**: $200 | **Rec**: $1,000
- **Return**: 13.0% | **Risk**: Moderate
- **Best for**: Saving for vacations (24 months)
- **Assets**: 35% Crypto + 35% Stocks + 20% Bonds + 10% Cash

### 🛡️ Emergency Fund Safety Net
- **Min**: $100 | **Rec**: $1,000
- **Return**: 5.5% | **Risk**: Low
- **Best for**: Liquid emergency savings
- **Assets**: 50% Stablecoins + 30% Bonds + 15% Stocks + 5% Crypto
- **No withdrawal penalty**

### 💎 Wealth Building Premium
- **Min**: $50,000 | **Rec**: $100,000
- **Return**: 18.5% | **Risk**: High
- **Best for**: High-net-worth individuals
- **Assets**: 40% Crypto + 35% Stocks + 15% Bonds + 10% Real Estate
- **Features**: Tax-optimized, automated rebalancing

### 🚀 Crypto Growth Aggressive
- **Min**: $500 | **Rec**: $5,000
- **Return**: 35.0% | **Risk**: High
- **Best for**: Risk-seeking investors
- **Assets**: 85% Crypto (BTC, ETH, SOL, AVAX) + 10% Stocks + 5% Cash

---

## Featured Assets

### Cryptocurrencies
- Bitcoin (BTC) - $45,000
- Ethereum (ETH) - $2,500
- Solana (SOL) - $110
- Chainlink (LINK) - $28
- Polygon (MATIC) - $1.20
- Avalanche (AVAX) - $85

### Stablecoins
- USD Coin (USDC) - $1.00
- Tether (USDT) - $1.00

### Stock ETFs
- SPY - S&P 500
- VTI - Total Market
- QQQ - Nasdaq 100
- VOO - Vanguard S&P 500
- VUG - Vanguard Growth

### Bond ETFs
- AGG - Bloomberg Aggregate
- BND - Total Bond Market
- TLT - 20+ Year Treasury
- SHV - Short-term Treasury
- VGIT - Intermediate Treasury

### Real Estate
- REIT - Real Estate Investment Trust

---

## Promotional Grants

### 🎉 New Investor Welcome
- **Plan**: Starter
- **Bonus**: 5% of investment
- **Min**: $100 | **Max**: $500 bonus
- **Duration**: 90 days

### 🤝 Couples Referral
- **Plan**: Couples
- **Bonus**: $200 per referral
- **Min Investment**: $1,000
- **Duration**: 12 months

### 🏆 Milestone Reward
- **Plan**: Crypto Growth
- **Bonus**: $500 for $10K investment
- **Duration**: 6 months

---

## User Workflow

1. **Browse Plans**: `/investment-plans/`
2. **Filter & Search**: By category, risk level, or keywords
3. **View Details**: Full asset allocation and grants
4. **Subscribe**: Set initial investment amount
5. **Track Progress**: View ROI in `/investment/dashboard/`
6. **Add Contributions**: Monthly or lump-sum
7. **Manage**: Pause or resume anytime

---

## Admin Features

### InvestmentPlanAdmin
- ✅ Create new plans with any asset allocation
- ✅ Risk level badges (color-coded)
- ✅ Asset allocation summary
- ✅ Return projection configuration
- ✅ Fee and duration settings
- ✅ Active/inactive toggle

### UserInvestmentSubscriptionAdmin
- ✅ Monitor all user subscriptions
- ✅ Status badges (active/paused/completed/cancelled)
- ✅ ROI color-coded (green for gains, red for losses)
- ✅ Contribution schedule management
- ✅ Monthly contribution configuration

### PlanPortfolioAssetAdmin
- ✅ Add/remove assets from plans
- ✅ Update current prices
- ✅ Adjust allocation percentages
- ✅ Toggle asset active/inactive

### InvestmentPlanPromotionGrantAdmin
- ✅ Create time-limited promotions
- ✅ Fixed amount or percentage bonuses
- ✅ Minimum investment thresholds
- ✅ Maximum grant caps
- ✅ Type selection (welcome, referral, milestone, etc.)

---

## Database Models

```
InvestmentPlan
├── name (unique)
├── category (8 types)
├── risk_level (low/moderate/high)
├── asset allocations (crypto, stocks, bonds, real_estate, cash)
├── expected returns and fees
├── features (rebalancing, tax optimization, etc.)
└── portfolio_assets (many-to-many via PlanPortfolioAsset)

UserInvestmentSubscription
├── user_profile (FK)
├── plan (FK)
├── initial_investment
├── current_value
├── total_contributed
├── monthly_contribution (optional)
├── status (active/paused/completed/cancelled)
└── contribution_schedules (one-to-many)

PlanPortfolioAsset
├── plan (FK)
├── asset_type
├── symbol
├── allocation_percentage
└── current_price

MonthlyCotributionSchedule
├── subscription (FK)
├── contribution_amount
├── scheduled_date
└── status

InvestmentPlanPromotionGrant
├── plan (FK)
├── grant_type
├── grant_amount or grant_percentage
├── validity period
└── minimum_investment_required
```

---

## Common Tasks

### Create a New Investment Plan
1. Go to Admin → Investment Plans → Add
2. Fill in name, category, risk level
3. Set investment limits (min, recommended, max)
4. Configure asset allocation (must sum to 100%)
5. Set expected return and fees
6. Click Save

### Add Assets to a Plan
1. Go to Admin → Plan Portfolio Assets → Add
2. Select plan
3. Choose asset type and symbol
4. Set allocation percentage
5. Enter current price
6. Save

### Create a Promotion Grant
1. Go to Admin → Promotion Grants → Add
2. Select plan and grant type
3. Set bonus amount or percentage
4. Set validity dates
5. Configure minimum investment
6. Save

### View Subscriber Performance
1. Go to Admin → User Investment Subscriptions
2. Click on a subscription to view:
   - Initial investment
   - Current value
   - ROI percentage
   - Contribution history
   - Monthly contribution setup

---

## Troubleshooting

**Issue**: Models not migrating  
**Solution**: Run `python manage.py migrate core`

**Issue**: Admin shows no plans  
**Solution**: Run `python manage.py seed_investment_plans`

**Issue**: 404 on investment URLs  
**Solution**: Check `core/urls.py` is updated with investment routes

**Issue**: Users can't subscribe  
**Solution**: Check user is logged in and has profile created

---

## Performance Metrics (Sample Data)

| Metric | Value |
|--------|-------|
| Total Plans | 8 |
| Total Assets | 40+ |
| Asset Classes | 6 |
| Promotion Grants | 3 |
| Sample Subscriptions | 0 (ready for user data) |
| AUM Range | $100 - $100,000+ |
| Management Fees | 0.5% - 2.0% |

---

## Support

**Documentation**: See `INVESTMENT_PLANS_README.md`  
**Implementation**: See `IMPLEMENTATION_SUMMARY.md`  
**Admin**: Go to `/admin`  
**User Dashboard**: Go to `/investment/dashboard/`

---

**Created**: December 2025  
**Status**: ✅ Ready for Production  
**Version**: 1.0
