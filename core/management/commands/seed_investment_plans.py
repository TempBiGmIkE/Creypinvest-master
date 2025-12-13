from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from core.models import InvestmentPlan, PlanPortfolioAsset, InvestmentPlanPromotionGrant


class Command(BaseCommand):
    help = 'Seed the database with sample investment plans'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating investment plans...'))

        # Delete existing plans to avoid duplicates
        InvestmentPlan.objects.all().delete()

        plans_data = [
            {
                'name': 'Starter Portfolio',
                'category': 'starter',
                'description': 'Perfect for beginners with limited capital. A balanced portfolio mixing crypto (30%), stocks (40%), bonds (20%), and cash (10%).',
                'risk_level': 'moderate',
                'minimum_investment': Decimal('100'),
                'recommended_investment': Decimal('500'),
                'expected_annual_return': Decimal('12.5'),
                'historical_performance': Decimal('11.8'),
                'crypto_allocation': 30,
                'stocks_allocation': 40,
                'bonds_allocation': 20,
                'cash_allocation': 10,
                'recommended_duration_months': 12,
                'management_fee': Decimal('1.5'),
                'assets': [
                    {'symbol': 'BTC', 'name': 'Bitcoin', 'asset_type': 'crypto', 'allocation': 15, 'price': Decimal('45000.00')},
                    {'symbol': 'ETH', 'name': 'Ethereum', 'asset_type': 'crypto', 'allocation': 15, 'price': Decimal('2500.00')},
                    {'symbol': 'SPY', 'name': 'S&P 500 ETF', 'asset_type': 'stock', 'allocation': 40, 'price': Decimal('450.00')},
                    {'symbol': 'BND', 'name': 'Total Bond Market ETF', 'asset_type': 'bond', 'allocation': 20, 'price': Decimal('82.50')},
                    {'symbol': 'USDC', 'name': 'USD Coin (Stablecoin)', 'asset_type': 'cash', 'allocation': 10, 'price': Decimal('1.00')},
                ]
            },
            {
                'name': 'Couples Investment Plan',
                'category': 'couples',
                'description': 'Designed for couples looking to invest together. Provides steady growth with moderate risk for joint goals.',
                'risk_level': 'moderate',
                'minimum_investment': Decimal('1000'),
                'recommended_investment': Decimal('5000'),
                'expected_annual_return': Decimal('14.0'),
                'historical_performance': Decimal('13.2'),
                'crypto_allocation': 25,
                'stocks_allocation': 45,
                'bonds_allocation': 20,
                'real_estate_allocation': 10,
                'recommended_duration_months': 24,
                'management_fee': Decimal('1.2'),
                'assets': [
                    {'symbol': 'BTC', 'name': 'Bitcoin', 'asset_type': 'crypto', 'allocation': 15, 'price': Decimal('45000.00')},
                    {'symbol': 'LINK', 'name': 'Chainlink', 'asset_type': 'crypto', 'allocation': 10, 'price': Decimal('28.00')},
                    {'symbol': 'VOO', 'name': 'Vanguard S&P 500 ETF', 'asset_type': 'stock', 'allocation': 30, 'price': Decimal('420.00')},
                    {'symbol': 'VTI', 'name': 'Vanguard Total Stock Market', 'asset_type': 'stock', 'allocation': 15, 'price': Decimal('240.00')},
                    {'symbol': 'AGG', 'name': 'Bloomberg Aggregate Bond ETF', 'asset_type': 'bond', 'allocation': 20, 'price': Decimal('105.00')},
                    {'symbol': 'REIT', 'name': 'Real Estate Investment Trust', 'asset_type': 'real_estate', 'allocation': 10, 'price': Decimal('75.00')},
                ]
            },
            {
                'name': 'Retirement Growth Plan',
                'category': 'retirement',
                'description': 'Long-term retirement planning with conservative growth. Focuses on stable assets with lower volatility.',
                'risk_level': 'low',
                'minimum_investment': Decimal('5000'),
                'recommended_investment': Decimal('15000'),
                'expected_annual_return': Decimal('9.0'),
                'historical_performance': Decimal('8.5'),
                'crypto_allocation': 10,
                'stocks_allocation': 40,
                'bonds_allocation': 40,
                'cash_allocation': 10,
                'recommended_duration_months': 360,  # 30 years
                'early_withdrawal_penalty': Decimal('10.0'),
                'management_fee': Decimal('0.8'),
                'assets': [
                    {'symbol': 'BTC', 'name': 'Bitcoin', 'asset_type': 'crypto', 'allocation': 10, 'price': Decimal('45000.00')},
                    {'symbol': 'QQQ', 'name': 'Nasdaq 100 ETF', 'asset_type': 'stock', 'allocation': 20, 'price': Decimal('380.00')},
                    {'symbol': 'VTI', 'name': 'Vanguard Total Stock Market', 'asset_type': 'stock', 'allocation': 20, 'price': Decimal('240.00')},
                    {'symbol': 'BND', 'name': 'Total Bond Market', 'asset_type': 'bond', 'allocation': 35, 'price': Decimal('82.50')},
                    {'symbol': 'TLT', 'name': 'iShares 20+ Year Treasury', 'asset_type': 'bond', 'allocation': 5, 'price': Decimal('95.00')},
                    {'symbol': 'USDC', 'name': 'USD Coin', 'asset_type': 'cash', 'allocation': 10, 'price': Decimal('1.00')},
                ]
            },
            {
                'name': 'Education Fund Plan',
                'category': 'education',
                'description': 'Save for your child\'s education with a balanced growth strategy. Tax-optimized for education expenses.',
                'risk_level': 'moderate',
                'minimum_investment': Decimal('500'),
                'recommended_investment': Decimal('2000'),
                'expected_annual_return': Decimal('11.5'),
                'historical_performance': Decimal('10.8'),
                'crypto_allocation': 20,
                'stocks_allocation': 50,
                'bonds_allocation': 20,
                'cash_allocation': 10,
                'is_tax_optimized': True,
                'recommended_duration_months': 180,  # 15 years
                'management_fee': Decimal('1.0'),
                'assets': [
                    {'symbol': 'BTC', 'name': 'Bitcoin', 'asset_type': 'crypto', 'allocation': 12, 'price': Decimal('45000.00')},
                    {'symbol': 'ETH', 'name': 'Ethereum', 'asset_type': 'crypto', 'allocation': 8, 'price': Decimal('2500.00')},
                    {'symbol': 'SPY', 'name': 'S&P 500 ETF', 'asset_type': 'stock', 'allocation': 35, 'price': Decimal('450.00')},
                    {'symbol': 'VUG', 'name': 'Vanguard Growth ETF', 'asset_type': 'stock', 'allocation': 15, 'price': Decimal('320.00')},
                    {'symbol': 'BND', 'name': 'Bond ETF', 'asset_type': 'bond', 'allocation': 20, 'price': Decimal('82.50')},
                    {'symbol': 'USDC', 'name': 'Stablecoin', 'asset_type': 'cash', 'allocation': 10, 'price': Decimal('1.00')},
                ]
            },
            {
                'name': 'Travel Fund Plan',
                'category': 'travel',
                'description': 'Accumulate funds for your dream vacation or adventure. Flexible withdrawal with moderate growth.',
                'risk_level': 'moderate',
                'minimum_investment': Decimal('200'),
                'recommended_investment': Decimal('1000'),
                'expected_annual_return': Decimal('13.0'),
                'historical_performance': Decimal('12.5'),
                'crypto_allocation': 35,
                'stocks_allocation': 35,
                'bonds_allocation': 20,
                'cash_allocation': 10,
                'recommended_duration_months': 24,
                'allows_monthly_contribution': True,
                'management_fee': Decimal('1.3'),
                'assets': [
                    {'symbol': 'BTC', 'name': 'Bitcoin', 'asset_type': 'crypto', 'allocation': 20, 'price': Decimal('45000.00')},
                    {'symbol': 'SOL', 'name': 'Solana', 'asset_type': 'crypto', 'allocation': 15, 'price': Decimal('110.00')},
                    {'symbol': 'VTI', 'name': 'Total Market ETF', 'asset_type': 'stock', 'allocation': 25, 'price': Decimal('240.00')},
                    {'symbol': 'VGIT', 'name': 'Growth-focused ETF', 'asset_type': 'stock', 'allocation': 10, 'price': Decimal('85.00')},
                    {'symbol': 'BND', 'name': 'Bond ETF', 'asset_type': 'bond', 'allocation': 20, 'price': Decimal('82.50')},
                ]
            },
            {
                'name': 'Emergency Fund Safety Net',
                'category': 'emergency',
                'description': 'Build a safety net with liquid, stable assets. Low risk with high accessibility.',
                'risk_level': 'low',
                'minimum_investment': Decimal('100'),
                'recommended_investment': Decimal('1000'),
                'expected_annual_return': Decimal('5.5'),
                'crypto_allocation': 5,
                'stocks_allocation': 15,
                'bonds_allocation': 30,
                'cash_allocation': 50,
                'recommended_duration_months': 12,
                'early_withdrawal_penalty': Decimal('0.0'),
                'management_fee': Decimal('0.5'),
                'assets': [
                    {'symbol': 'USDC', 'name': 'USD Coin (Stablecoin)', 'asset_type': 'cash', 'allocation': 50, 'price': Decimal('1.00')},
                    {'symbol': 'USDT', 'name': 'Tether (Stablecoin)', 'asset_type': 'cash', 'allocation': 5, 'price': Decimal('1.00')},
                    {'symbol': 'AGG', 'name': 'Bond ETF', 'asset_type': 'bond', 'allocation': 30, 'price': Decimal('105.00')},
                    {'symbol': 'SHV', 'name': 'Short-term Treasury ETF', 'asset_type': 'bond', 'allocation': 10, 'price': Decimal('110.00')},
                    {'symbol': 'BTC', 'name': 'Bitcoin (Small allocation)', 'asset_type': 'crypto', 'allocation': 5, 'price': Decimal('45000.00')},
                ]
            },
            {
                'name': 'Wealth Building Premium',
                'category': 'wealth',
                'description': 'Premium plan for high-net-worth individuals. Diversified across all asset classes with advanced strategies.',
                'risk_level': 'high',
                'minimum_investment': Decimal('50000'),
                'recommended_investment': Decimal('100000'),
                'expected_annual_return': Decimal('18.5'),
                'historical_performance': Decimal('17.8'),
                'crypto_allocation': 40,
                'stocks_allocation': 35,
                'bonds_allocation': 15,
                'real_estate_allocation': 10,
                'is_automated_rebalancing': True,
                'is_tax_optimized': True,
                'recommended_duration_months': 60,
                'management_fee': Decimal('0.9'),
                'assets': [
                    {'symbol': 'BTC', 'name': 'Bitcoin', 'asset_type': 'crypto', 'allocation': 20, 'price': Decimal('45000.00')},
                    {'symbol': 'ETH', 'name': 'Ethereum', 'asset_type': 'crypto', 'allocation': 15, 'price': Decimal('2500.00')},
                    {'symbol': 'MATIC', 'name': 'Polygon', 'asset_type': 'crypto', 'allocation': 5, 'price': Decimal('1.20')},
                    {'symbol': 'QQQ', 'name': 'Nasdaq 100', 'asset_type': 'stock', 'allocation': 20, 'price': Decimal('380.00')},
                    {'symbol': 'VUG', 'name': 'Growth ETF', 'asset_type': 'stock', 'allocation': 15, 'price': Decimal('320.00')},
                    {'symbol': 'TLT', 'name': 'Long-term Treasury', 'asset_type': 'bond', 'allocation': 15, 'price': Decimal('95.00')},
                    {'symbol': 'REIT', 'name': 'Real Estate Fund', 'asset_type': 'real_estate', 'allocation': 10, 'price': Decimal('75.00')},
                ]
            },
            {
                'name': 'Crypto Growth Aggressive',
                'category': 'crypto',
                'description': 'For adventurous investors seeking high returns. Concentrated in cryptocurrencies and blockchain assets.',
                'risk_level': 'high',
                'minimum_investment': Decimal('500'),
                'recommended_investment': Decimal('5000'),
                'expected_annual_return': Decimal('35.0'),
                'historical_performance': Decimal('32.5'),
                'crypto_allocation': 85,
                'stocks_allocation': 10,
                'bonds_allocation': 0,
                'cash_allocation': 5,
                'recommended_duration_months': 24,
                'early_withdrawal_penalty': Decimal('15.0'),
                'management_fee': Decimal('2.0'),
                'assets': [
                    {'symbol': 'BTC', 'name': 'Bitcoin', 'asset_type': 'crypto', 'allocation': 40, 'price': Decimal('45000.00')},
                    {'symbol': 'ETH', 'name': 'Ethereum', 'asset_type': 'crypto', 'allocation': 25, 'price': Decimal('2500.00')},
                    {'symbol': 'SOL', 'name': 'Solana', 'asset_type': 'crypto', 'allocation': 10, 'price': Decimal('110.00')},
                    {'symbol': 'AVAX', 'name': 'Avalanche', 'asset_type': 'crypto', 'allocation': 10, 'price': Decimal('85.00')},
                    {'symbol': 'SPY', 'name': 'S&P 500 ETF', 'asset_type': 'stock', 'allocation': 10, 'price': Decimal('450.00')},
                    {'symbol': 'USDC', 'name': 'Stablecoin Reserve', 'asset_type': 'cash', 'allocation': 5, 'price': Decimal('1.00')},
                ]
            },
        ]

        created_count = 0
        for plan_data in plans_data:
            assets = plan_data.pop('assets')
            plan = InvestmentPlan.objects.create(**plan_data)
            
            # Create portfolio assets
            for asset_data in assets:
                asset_dict = {
                    'plan': plan,
                    'asset_type': asset_data['asset_type'],
                    'symbol': asset_data['symbol'],
                    'name': asset_data['name'],
                    'allocation_percentage': Decimal(str(asset_data['allocation'])),
                    'current_price': Decimal(str(asset_data['price'])),
                }
                PlanPortfolioAsset.objects.create(**asset_dict)
            
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'✓ Created {plan.name}'))

        # Create sample grants
        self.stdout.write(self.style.SUCCESS('\nCreating promotion grants...'))
        
        starter_plan = InvestmentPlan.objects.get(name='Starter Portfolio')
        couples_plan = InvestmentPlan.objects.get(name='Couples Investment Plan')
        crypto_plan = InvestmentPlan.objects.get(name='Crypto Growth Aggressive')

        grants = [
            {
                'plan': starter_plan,
                'grant_type': 'welcome_bonus',
                'name': 'New Investor Welcome Bonus',
                'description': 'Get 5% bonus on your first investment',
                'grant_percentage': Decimal('5'),
                'minimum_investment_required': Decimal('100'),
                'maximum_grant_per_user': Decimal('500'),
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=90),
            },
            {
                'plan': couples_plan,
                'grant_type': 'referral',
                'name': 'Couples Referral Bonus',
                'description': 'Earn $200 for each friend who subscribes',
                'grant_amount': Decimal('200'),
                'minimum_investment_required': Decimal('1000'),
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=365),
            },
            {
                'plan': crypto_plan,
                'grant_type': 'milestone',
                'name': 'Milestone Reward - $10K',
                'description': 'Invest $10,000 and get $500 bonus',
                'grant_amount': Decimal('500'),
                'minimum_investment_required': Decimal('10000'),
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=180),
            },
        ]

        for grant_data in grants:
            InvestmentPlanPromotionGrant.objects.create(**grant_data)
            self.stdout.write(self.style.SUCCESS(f'✓ Created {grant_data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created {created_count} investment plans!'))
