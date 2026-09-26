from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.core.config import settings
from app.db.session import engine
from app.models import User, ActivityType, UnitType, ActivityTypeUnitType

class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if (username == settings.SQLADMIN_USERNAME
            and 
            password == settings.SQLADMIN_PASSWORD):
            request.session.update({"admin": username})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
    async def authenticate(self, request: Request) -> bool:
        return request.session.get("admin") is not None

# /admin-muistilista, kun lisäät uuden ORM-mallin:
# 1. Tee sille ModelView tähän tiedostoon (column_list, searchable, sortable).
# 2. Rekisteröi se create_admin():ssa: admin.add_view(...).
# 3. Pidä salaisuudet (password_hash, tokenit) poissa: column_list, column_details_exclude_list, form_excluded_columns.
# 4. Tarkista /admin ennen demoa.


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    column_list = [User.id, User.email, User.display_name, User.created_at]
    column_details_exclude_list = [User.password_hash]
    column_searchable_list = [User.email]
    column_sortable_list = [User.id, User.email, User.created_at]
    form_excluded_columns = [User.password_hash]
    can_create = False



class ActivityTypeAdmin(ModelView, model=ActivityType):
    name = "Activity type"
    name_plural = "Activity types"
    column_list = [
        ActivityType.id,
        ActivityType.name,
        ActivityType.slug,
        ActivityType.is_system,
        ActivityType.user_id,
    ]
    column_searchable_list = [ActivityType.name, ActivityType.slug]
    column_sortable_list = [ActivityType.id, ActivityType.name]


class UnitTypeAdmin(ModelView, model=UnitType):
    name = "Unit type"
    name_plural = "Unit types"
    column_list = [UnitType.id, UnitType.name, UnitType.slug, UnitType.is_system]
    column_searchable_list = [UnitType.name, UnitType.slug]
    column_sortable_list = [UnitType.id, UnitType.name]


class ActivityTypeUnitTypeAdmin(ModelView, model=ActivityTypeUnitType):
    name = "Activity-unit link"
    name_plural = "Activity-unit links"
    column_list = [
        ActivityTypeUnitType.id,
        ActivityTypeUnitType.activity_type,
        ActivityTypeUnitType.unit_type,
        ActivityTypeUnitType.per_set,
        ActivityTypeUnitType.is_required,
        ActivityTypeUnitType.sort_order,
    ]


def create_admin(app) -> Admin:
    admin = Admin(
        app,
        engine,
        authentication_backend=AdminAuth(secret_key=settings.SQLADMIN_SECRET_KEY),
    )
    admin.add_view(UserAdmin)
    admin.add_view(ActivityTypeAdmin)
    admin.add_view(UnitTypeAdmin)
    admin.add_view(ActivityTypeUnitTypeAdmin)
    return admin