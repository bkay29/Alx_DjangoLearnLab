# bookshelf — groups & permissions

This app defines a `Book` model and custom permissions used to restrict access.

## Custom permissions
Defined in `bookshelf.models.Book.Meta.permissions`:
- `can_view`
- `can_create`
- `can_edit`
- `can_delete`

## Groups
We use three groups:
- `Viewers` → `can_view`
- `Editors` → `can_create`, `can_edit`, `can_view`
- `Admins` → all four permissions

You can create groups via admin or run:


## How to protect views
Use `@permission_required('bookshelf.can_edit', raise_exception=True)` for function views,
or `PermissionRequiredMixin` with `permission_required = 'bookshelf.can_edit'` for CBVs.

## Quick setup
1. `python manage.py makemigrations bookshelf`
2. `python manage.py migrate`
3. `python manage.py createsuperuser`
4. `python manage.py create_groups` (or create groups in admin)
5. Create test users in admin and add them to the relevant group


# bookshelf — groups & permissions

This app defines a `Book` model and custom permissions used to restrict access.

## Custom permissions
Defined in `bookshelf.models.Book.Meta.permissions`:
- `can_view`
- `can_create`
- `can_edit`
- `can_delete`

## Groups
We use three groups:
- `Viewers` → `can_view`
- `Editors` → `can_create`, `can_edit`, `can_view`
- `Admins` → all four permissions

You can create groups via admin or run:
```bash
python manage.py create_groups


---

## Security Measures Implemented

To protect against common web vulnerabilities, the following security best practices were added:

### Django Settings (`settings.py`)
- `DEBUG = False` in production → prevents leaking sensitive debug info.
- `SECURE_BROWSER_XSS_FILTER = True` → enables X-XSS-Protection header to block reflective XSS.
- `SECURE_CONTENT_TYPE_NOSNIFF = True` → prevents MIME-type sniffing.
- `X_FRAME_OPTIONS = "DENY"` → prevents clickjacking by blocking framing.
- `CSRF_COOKIE_SECURE = True` → ensures CSRF cookie is sent only over HTTPS.
- `SESSION_COOKIE_SECURE = True` → ensures session cookies are sent only over HTTPS.
- `SESSION_COOKIE_HTTPONLY = True` → prevents JavaScript from accessing session cookie.
- `SECURE_SSL_REDIRECT = True` (production only) → forces all HTTP requests to HTTPS.
- **Content Security Policy (CSP)** via `django-csp` middleware:
  - `CSP_DEFAULT_SRC = ("'self'",)` → only allow resources from same origin.
  - `CSP_SCRIPT_SRC = ("'self'",)` → only allow scripts from same origin.
  - `CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")` → allow styles from same origin (inline styles permitted only where necessary).

### Forms & Templates
- All templates that render forms explicitly include `{% csrf_token %}` to protect against CSRF.
- `BookForm` and `ExampleForm` handle user input via Django’s form validation and `cleaned_data` (no direct use of raw request data).
- `ConfirmDeleteForm` ensures delete actions are confirmed through a CSRF-protected POST, instead of unsafe GET requests.

### Views (`views.py`)
- ORM methods (`Book.objects.filter`, `Book.objects.create`, etc.) are used instead of raw SQL, preventing SQL injection.
- Direct request data (`request.POST` / `request.GET`) is validated or handled safely via forms.
- Permissions enforced using `@permission_required` decorators (`can_view`, `can_create`, `can_edit`, `can_delete`).

---

## Testing Approach

### Manual Security Tests
1. **CSRF Protection**
   - Verified forms reject submissions without a `{% csrf_token %}`.
   - Confirmed delete action requires a POST with CSRF token (no accidental deletes via link).

2. **XSS Protection**
   - Tried submitting `<script>alert(1)</script>` as book title/author.  
   - Verified the script was escaped and not executed (thanks to Django auto-escaping + CSP headers).

3. **SQL Injection**
   - Tried search query with `"' OR 1=1 --"` in the `q` parameter.  
   - Verified ORM safely parameterized the query and returned only expected results.

4. **Permissions**
   - Logged in as different group users (Viewer, Editor, Admin).  
   - Verified each group only had access to views they were granted.

5. **HTTPS / Cookie Security**
   - Confirmed cookies (`sessionid`, `csrftoken`) had `Secure` and `HttpOnly` flags when running under HTTPS.

---

