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
