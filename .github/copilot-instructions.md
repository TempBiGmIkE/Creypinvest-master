## Copilot instructions for Creypinvest (concise)

Purpose: help AI coding assistants be productive in this Django monolith by documenting the project's structure, workflows, and discoverable conventions.

- Big picture
  - This is a single Django project (root package `creyp`) composed of several apps: `core`, `users`, `dashboard`, and `site_admin`.
  - Templates live under `templates/` and per-app `templates/` folders. Static source files are in `static/` and collected to `static-root/`.
  - `creyp/settings.py` loads a `.env` file and supports two deployment modes: local static files (Whitenoise) or S3-backed storage controlled by the `USE_S3` env var.

- Important files to inspect when changing behavior
  - `creyp/settings.py` — central feature flags (USE_S3, DEBUG), database (dj_database_url) and email/S3 env var usage.
  - `creyp/storage_backends.py` — custom storage classes (StaticStorage, PublicMediaStorage, CachedS3BotoStorage) used when `USE_S3` is truthy.
  - `users/forms.py` — custom signup flow: `CustomSignupForm` saves `profile.phone_number` and `profile.ip_address` from `request.META['REMOTE_ADDR']`.
  - `creyp/urls.py` — top-level routes: referral path `r/<username>/`, `auth/account/` (django-allauth), and a non-standard dashboard-denial path. Use it as an example of URL patterns.
  - `manage.py` — standard Django CLI entrypoint.

- Developer workflows (exact commands that work in this repo)
  - Activate the bundled venv (Windows bash): `source env/Scripts/activate` (the repo contains `env/` in the workspace).
  - Install dependencies: `python -m pip install -r requirements.txt`.
  - Run migrations: `python manage.py migrate`.
  - Create admin: `python manage.py createsuperuser`.
  - Run development server: `python manage.py runserver`.
  - Serve static locally in DEBUG: settings already append static() helpers in `creyp/urls.py` when DEBUG is true.
  - Collect static for production: `python manage.py collectstatic --noinput` (ensure env variables for S3 are set if using S3).

- Environment variables to know (used directly in code)
  - `DEBUG`, `USE_S3` — feature flags in `creyp/settings.py` (note: DEBUG is read from .env via dotenv).
  - DB connection: `dj_database_url` will override `DATABASES` from `DATABASE_URL`.
  - S3: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_DEFAULT_ACL`.
  - Email: `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` (settings use Gmail SMTP by default in `creyp/settings.py`).

- Project-specific conventions and patterns
  - django-allauth is the canonical auth flow. App-level customizations are in `users/` (see `users/forms.py`) and templates under `templates/account` and `templates/socialaccount`.
  - Static/media behavior is conditional: if `USE_S3` is truthy, code expects S3-backed storage classes under `creyp.storage_backends` (see `creyp/storage_backends.py`); otherwise static is served from `static-root` and `MEDIA_ROOT = media-root`.
  - Templates sometimes reference `user.socialaccount_set` for avatar URLs (see `dashboard/templates/dashboard_base.html`). Use the socialaccount helpers already present in templates.
  - Settings intentionally add `allauth.account.middleware.AccountMiddleware` only when `DEBUG` is True.

- Integration points and cross-component communication
  - `users.forms.CustomSignupForm.save` writes to `user.profile` — profile model is populated elsewhere (search `models.py` in `users` or `core`). Be careful when changing signup logic.
  - External integrations: Google and Apple social logins (providers configured in `creyp/settings.py`), optional AWS S3 storage, and Gmail SMTP.
  - Database URL overrides are applied via `dj_database_url.config()` so CI/hosting will likely provide `DATABASE_URL`.

- Quick examples to reference in changes
  - To use the public media storage class in code: DEFAULT_FILE_STORAGE = "creyp.storage_backends.PublicMediaStorage" (set in `creyp/settings.py` when `USE_S3` is enabled).
  - Custom signup saves IP: `profile.ip_address = request.META['REMOTE_ADDR']` (see `users/forms.py`).
  - Route examples: referral `path('r/<str:username>/', referral_view, name="refer")` and allauth inclusion `path('auth/account/', include('allauth.urls'))` (see `creyp/urls.py`).

- Safety notes (what you can rely on / watch for)
  - `SECRET_KEY` is present in `creyp/settings.py` (hard-coded). Do not assume it's secure — prefer using `.env` overrides for secrets when making production changes.
  - ALLOWED_HOSTS is set to `['*']` in the repository; change this before production deployment.

- Where to run tests and checks
  - Django tests: `python manage.py test` (apps include `core`, `users`, `dashboard`, `site_admin`).

If something in these instructions is unclear or you want additional guidance (example PR templates, preferred code style, or extra safety checks), tell me which area to expand and I will update this file.
