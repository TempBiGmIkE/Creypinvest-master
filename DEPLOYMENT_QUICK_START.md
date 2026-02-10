# Quick Vercel Deployment Guide - CreypInvest

## 5-Minute Setup

### Step 1: Database Setup (Most Critical!)
```bash
# Create PostgreSQL database
# Option 1: Vercel Postgres (recommended)
# Go to https://vercel.com/docs/storage/postgres

# Option 2: External provider (Railway, Supabase, AWS RDS)
# Get your DATABASE_URL connection string
```

### Step 2: AWS S3 Setup (For static files & media)
```bash
# Create S3 bucket
# Create IAM user with S3 permissions
# Get credentials
```

### Step 3: Environment Variables
Create a `.env` file with:
```
DEBUG=False
SECRET_KEY=your-new-secret-key-here-do-not-reuse
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/db
USE_S3=True
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_DEFAULT_ACL=public-read
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

### Step 4: Test Locally
```bash
# Test with production settings
DEBUG=False python manage.py runserver

# Verify static files collect
python manage.py collectstatic --noinput
```

### Step 5: Deploy to Vercel
```bash
# Push to GitHub
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main

# Go to https://vercel.com
# Connect your GitHub repository
# Add environment variables in Vercel dashboard
# Vercel auto-deploys!
```

### Step 6: Post-Deployment
```bash
# Get environment and run migrations
vercel env pull
python manage.py migrate --settings=creyp.settings --database default

# Create superuser in production
python manage.py createsuperuser --settings=creyp.settings

# Verify deployment
# Test at https://yourdomain.com
# Admin at https://yourdomain.com/admin/
```

## Vercel Configuration Files Created

✅ **vercel.json** - Deployment configuration
✅ **api/index.py** - WSGI entry point
✅ **api/wsgi.py** - Alternative entry point
✅ **.env.example** - Environment variable template

## Key Files Modified

✅ **creyp/settings.py** - Updated for production & Vercel

## Important Warnings

⚠️ **SQLite will NOT work on Vercel** - Must use PostgreSQL or other external database
⚠️ **Files uploaded will be deleted** - Use AWS S3 or similar for file storage
⚠️ **10-second timeout per request** - Optimize long-running operations
⚠️ **Never commit .env to GitHub** - Use Vercel dashboard for secrets

## If Something Goes Wrong

```bash
# View deployment logs
vercel logs

# Check build logs
vercel logs --follow

# Rollback to previous version
vercel rollback

# Force rebuild
vercel rebuild
```

## Next: Full Deployment Checklist

For comprehensive checklist with all steps, see:
👉 **[VERCEL_DEPLOYMENT_CHECKLIST.md](VERCEL_DEPLOYMENT_CHECKLIST.md)**

---

**Status**: Ready for deployment ✅
