from webapp2 import Route
from webapp2_extras import routes

from handlers.admin import base


class RankBase(base.AdminHandler):

    templatedir = 'rank'

    def __init__(self, *args, **kwargs):
        super(RankBase, self).__init__(*args, **kwargs)
        from lib.forms import Rank as RankForm
        self.form = RankForm

        from models.account import Rank as RankModel
        self.model = RankModel


class RankList(RankBase, base.List):
    title = 'Rank'


class RankCreate(RankBase, base.Create):

    def createitem(self, form):
        newentry = self.model(
            name=form.cleaneddata['title'],
            placement=form.cleaneddata['placement'])
        newentry.description = form.cleaneddata['body']
        return newentry    


class RankEdit(RankBase, base.Edit):

    def formcontext(self, item):
        formcontext = {
            'title': item.name,
            'body': item.description,
            'placement': item.placement,
        }
        return formcontext

    def updateitem(self, item, form):
        item.name = form.cleaneddata['title']
        item.description = form.cleaneddata['body']
        item.placement = form.cleaneddata['placement']
        return item


class RankDelete(RankBase, base.Delete):
    pass


class UserBase(base.AdminHandler):

    templatedir = 'user'

    def __init__(self, *args, **kwargs):
        super(UserBase, self).__init__(*args, **kwargs)
        from lib.forms import AdminAccount as UserForm
        self.form = UserForm

        from models.account import User as UserModel
        self.model = UserModel


class UserList(UserBase, base.List):
    title = 'User'
    create = False


class UserEdit(UserBase, base.Edit):

    def formcontext(self, item):
        formcontext = {
            'name': item.name,
            'about': item.description,
            'isadmin': item.siteadmin,
        }
        return formcontext

    def updateitem(self, item, form):
        item.name = form.cleaneddata['name']
        item.description = form.cleaneddata['about']
        item.siteadmin = form.cleaneddata['isadmin']
        return item


class UserDelete(UserBase, base.Delete):
    pass


routes = [
    routes.PathPrefixRoute(r'/ranks', [
        Route(r'/', RankList, name='admin-rank-list'),
        Route(r'/create', RankCreate, name='admin-rank-create'),
        Route(r'/edit/<itemkey>', RankEdit, name='admin-rank-edit'),
        Route(r'/delete/<itemkey>', RankDelete, name='admin-rank-delete'),
    ]),
    routes.PathPrefixRoute(r'/users', [
        Route(r'/', UserList, name='admin-user-list'),
        Route(r'/edit/<itemkey>', UserEdit, name='admin-user-edit'),
        Route(r'/delete/<itemkey>', UserDelete, name='admin-user-delete'),
    ]),
]