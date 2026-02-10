# Vercel Deployment Checklist for CreypInvest Django Application

## Pre-Deployment Setup

### 1. Environment & Dependencies
- [ ] Update Python version to 3.11 or higher in `vercel.json`
- [ ] Install all requirements: `pip install -r requirements.txt`
- [ ] Create `.env` file in root with all required environment variables
- [ ] Copy `.env.example` for reference: `cp .env.example .env`
- [ ] Test locally: `python manage.py runserver`

### 2. Database Configuration (CRITICAL for Vercel)
#### ⚠️ Important: SQLite does NOT work on Vercel (ephemeral filesystem)
- [ ] Create a PostgreSQL database (recommended):
  - [ ] Use Vercel PostgreSQL (https://vercel.com/docs/storage/postgres)
  - [ ] OR use external provider (AWS RDS, Railway, Supabase, etc.)
- [ ] Get `DATABASE_URL` connection string
- [ ] Set `DATABASE_URL` in Vercel environment variables
- [ ] Remove/backup local `db.sqlite3` before deploying
- [ ] Test database connection: `psql $DATABASE_URL`

### 3. Static Files & Media Configuration
#### Option A: Using AWS S3 (Recommended for production)
- [ ] Create AWS S3 bucket for static/media files
- [ ] Create IAM user with S3 permissions
- [ ] Set `USE_S3=True` in environment variables
- [ ] Add AWS credentials:
  - [ ] `AWS_ACCESS_KEY_ID`
  - [ ] `AWS_SECRET_ACCESS_KEY`
  - [ ] `AWS_STORAGE_BUCKET_NAME`
  - [ ] `AWS_DEFAULT_ACL`
- [ ] Test locally with S3: `DEBUG=False python manage.py collectstatic`

#### Option B: Using Vercel Blob Storage
- [ ] Install blob storage SDK: `pip install vercel-blob`
- [ ] Configure blob storage endpoints
- [ ] Update storage backend settings

### 4. Secret Key & Security
- [ ] Generate a new `SECRET_KEY` (use Django secret key generator)
- [ ] Set `SECRET_KEY` in environment variables
- [ ] Ensure `DEBUG=False` in production environment
- [ ] Set `ALLOWED_HOSTS` with your domain(s)
- [ ] Set `CSRF_TRUSTED_ORIGINS` with your domain(s)
- [ ] Enable HTTPS enforcement

### 5. Authentication & Social Login
#### Google OAuth
- [ ] Create Google OAuth credentials at https://console.cloud.google.com/
- [ ] Authorized redirect URIs: `https://yourdomain.com/auth/account/google/callback/`
- [ ] Set environment variables (if needed for dynamic config)

#### Apple Sign-In
- [ ] Configure Apple Developer account
- [ ] Register Service ID and Signing Key
- [ ] Set authorized URLs

#### Email Verification
- [ ] Set up Gmail SMTP (or other email service):
  - [ ] `EMAIL_HOST_USER`: Gmail address
  - [ ] `EMAIL_HOST_PASSWORD`: App-specific password (not Gmail password)
- [ ] Verify email backend works: `python manage.py shell`

### 6. Django Migrations & Setup
- [ ] Run migrations locally first: `python manage.py migrate`
- [ ] Create a backup of production database after first deploy
- [ ] In Vercel, migrations run via build command in `vercel.json`
- [ ] Create superuser in production:
  ```bash
  vercel env pull
  python manage.py createsuperuser --settings=creyp.settings
  ```

### 7. Vercel Project Setup
- [ ] Create Vercel account at https://vercel.com
- [ ] Connect GitHub repository to Vercel
- [ ] Configure build settings:
  - [ ] Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
  - [ ] Install Command: `pip install -r requirements.txt`
  - [ ] Output Directory: `.vercel/output/static`
  - [ ] Root Directory: `./`

### 8. Environment Variables in Vercel
Add all these to Vercel project settings (Settings → Environment Variables):

```
DEBUG=False
SECRET_KEY=<your-generated-secret-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/dbname
USE_S3=True
AWS_ACCESS_KEY_ID=<your-key>
AWS_SECRET_ACCESS_KEY=<your-secret>
AWS_STORAGE_BUCKET_NAME=<your-bucket>
AWS_DEFAULT_ACL=public-read
EMAIL_HOST_USER=<your-email@gmail.com>
EMAIL_HOST_PASSWORD=<your-app-password>
```

### 9. File Structure Verification
Ensure these files exist:
- [ ] `vercel.json` - Vercel configuration
- [ ] `api/index.py` - WSGI entry point for Vercel
- [ ] `api/wsgi.py` - Alternative WSGI entry point
- [ ] `manage.py` - Django management script
- [ ] `requirements.txt` - Python dependencies
- [ ] `.env.example` - Environment variable template
- [ ] `creyp/wsgi.py` - Original Django WSGI

### 10. Testing Before Deployment
- [ ] Run tests: `python manage.py test`
- [ ] Check for errors: `python manage.py check --deploy`
- [ ] Run management command seed (if needed): `python manage.py seed_investment_plans`
- [ ] Test locally with production settings:
  ```bash
  DEBUG=False python manage.py runserver
  ```

### 11. Domain & HTTPS
- [ ] Point domain to Vercel nameservers or configure DNS
- [ ] Wait for DNS propagation (typically 24-48 hours)
- [ ] Vercel auto-provisions SSL certificate
- [ ] Enable automatic HTTPS redirect in Vercel settings

### 12. First Deployment
- [ ] Push code to GitHub repository
- [ ] Vercel automatically starts deployment
- [ ] Monitor build logs for errors
- [ ] Check deployed URL: `https://yourdomain.com/`
- [ ] Test main pages:
  - [ ] Homepage: `/`
  - [ ] Login: `/auth/account/login/`
  - [ ] Dashboard: `/dashboard/` (login required)
  - [ ] Admin: `/admin/`
  - [ ] Investment Plans: `/site/investment-plans/`

### 13. Post-Deployment Verification
- [ ] Verify static files load: Check browser DevTools Network tab
- [ ] Test form submissions work
- [ ] Test file uploads (if applicable)
- [ ] Check email notifications send correctly
- [ ] Test social authentication (Google, Apple)
- [ ] Verify CSRF protection works
- [ ] Check database queries work
- [ ] Monitor error logs in Vercel dashboard

### 14. Monitoring & Maintenance
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Monitor application logs via Vercel dashboard
- [ ] Set up alerts for deployment failures
- [ ] Regular database backups (if using external DB)
- [ ] Monitor static file delivery and caching
- [ ] Set up SSL certificate auto-renewal
- [ ] Regular security updates to dependencies

### 15. Performance Optimization
- [ ] Enable caching headers in `vercel.json`
- [ ] Use CDN for static files (CloudFront with S3)
- [ ] Enable database query caching
- [ ] Minify CSS/JS files
- [ ] Optimize image sizes
- [ ] Enable gzip compression
- [ ] Monitor response times

## Troubleshooting Common Deployment Issues

### Issue: "No such table / column" database errors
**Solution:** Ensure `DATABASE_URL` is set correctly and migrations ran during build

### Issue: Strange port errors (8000, 5000)
**Solution:** Remove `ALLOWED_HOSTS = ["127.0.0.1:8000"]` type settings

### Issue: CSRF verification failures
**Solution:** Ensure `CSRF_TRUSTED_ORIGINS` includes your domain and uses HTTPS

### Issue: Static files not loading (404 errors)
**Solution:** 
- Ensure collectstatic runs in build command
- Use S3 for static files (recommended)
- Check file permissions in S3

### Issue: Social authentication not working
**Solution:** Verify OAuth callback URLs match deployed domain exactly

### Issue: Email not sending
**Solution:** Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are set

## Important Notes

1. **SQLite ❌**: Vercel uses an ephemeral filesystem. SQLite files will be deleted after each deploy. **Must use external database.**

2. **Media Files ❌**: Same issue as SQLite. Use S3 or Vercel Blob storage.

3. **Environment Variables 🔒**: Never commit `.env` to GitHub. Use Vercel dashboard only.

4. **Build Time**: Keep under 5 minutes. Optimize if needed.

5. **Serverless Function Limitations**: 
   - Max 10 seconds execution time per request
   - Limited memory (variables depend on plan)
   - Cold start delays possible

6. **Database Costs**: External database (PostgreSQL) adds monthly cost

7. **Domain Setup**: Use Vercel's default domain first to test, then add custom domain

## Deployment Checklist Summary by Priority

### 🔴 Critical (Must do before deploying)
- [ ] Database configured and accessible
- [ ] SECRET_KEY set in environment
- [ ] DEBUG=False in production
- [ ] AWS S3 or blob storage configured for files
- [ ] ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS set

### 🟡 Important (Highly recommended)
- [ ] Email configuration tested
- [ ] Static files collect successfully
- [ ] Migrations run without errors
- [ ] Local testing with production settings

### 🟢 Nice to have
- [ ] Monitoring/logging set up
- [ ] Performance optimization
- [ ] Backup strategy in place

## Quick Deploy Commands

```bash
# Pull environment variables
vercel env pull

# Run migrations locally
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test production settings locally
DEBUG=False python manage.py runserver

# Deploy to Vercel
git push origin main
# (Vercel auto-deploys on push)

# View deployment logs
vercel logs

# Rollback to previous deployment
vercel rollback
```

## Support & Resources

- **Vercel Django Docs**: https://vercel.com/guides/deploying-django
- **Django Deployment Checklist**: https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
- **Vercel Support**: https://vercel.com/support
- **Vercel Status Page**: https://www.vercelstatus.com/

---

**Last Updated**: February 10, 2026
**Django Version**: 4.0.4+
**Python Version**: 3.11+
**Status**: Ready for Production Deployment ✅
