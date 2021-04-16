# from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.base import AdminIndexView, expose, Admin
from models import UserModel
from flask_login import current_user
from flask import redirect, url_for

class AppModelView(ModelView):
    # full reference
    # https://flask-admin.readthedocs.io/en/latest/introduction/#customizing-builtin-views
    can_view_details = True

    def is_accessible(self):
        # return is_authorized() for example
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('myadmin.html', user=current_user)

def create_admin(app, db):
    admin = Admin(app, name='Admin', template_mode='bootstrap3', index_view=MyAdminView())
    admin.add_view(AppModelView(UserModel, db.session, name='Users'))
    return admin