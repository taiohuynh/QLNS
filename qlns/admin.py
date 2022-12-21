from qlns.models import Category, Product, Tag
from qlns import db, app, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask import request


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class ProductView(ModelView):
    column_searchable_list = ['name', 'author']
    column_filters = ['name', 'price']
    can_view_details = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = {
        'name': 'Tên Sách',
        'author': 'Tác Giả',
        'price': 'Giá'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'author': CKTextAreaField
    }

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):
        stats = dao.stats_revenue(kw=request.args.get('kw'),
                                  from_date=request.args.get('from_date'),
                                  to_date=request.args.get('to_date'))
        return self.render('admin/stats.html', stats=stats)


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_product_by_cate()
        return self.render('admin/index.html', stats=stats)


admin = Admin(app=app, name='QUẢN TRỊ BÁN SÁCH', template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(ModelView(Category, db.session, name='Danh mục'))
admin.add_view(ModelView(Tag, db.session, name='Tag'))
admin.add_view(ProductView(Product, db.session, name='Sách'))
admin.add_view(StatsView(name='Thông kê'))
