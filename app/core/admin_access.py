from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request

class AdminModelView(ModelView):
    # def is_accessible(self):
    #     return current_user.is_authenticated and (
    #         current_user.role == 'admin' or current_user.username == "admin"
    #     )

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))
    
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and (
            current_user.role == 'admin' or current_user.username == "admin"
        )