import tornado.websocket
import tornado.web
import tornado.gen
from utils import shelve_save, shelve_get
import config
import time


class Base(tornado.websocket.WebSocketHandler):

    def get_current_user(self):
        return self.get_secure_cookie('user')


class AdminLogin(Base):

    def get(self):
        self.render('admin/login.html')

    def post(self):
        if self.get_argument('name', None) == 'admin' and \
                        self.get_argument('password', None) == '111':
            self.set_secure_cookie('user', 'admin')
            self.redirect('/admin')
            return
        self.redirect(self.request.path)


class Admin(Base):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        data = dict(version=shelve_get('version'))
        self.render('admin/admin_panel.html', data=data)

    @tornado.gen.coroutine
    def post(self):
        required_fields = ('version', )
        print(self.get_argument('version'))
        save_dict = {}
        for field in required_fields:
            save_dict[field] = self.get_argument(field)
        shelve_save(**save_dict)
        self.application.version = self.get_argument('version')
        self.redirect(self.request.path)


class CheckForUpdates(Base):

    def check_origin(self, origin):
        return True

    def open(self):
        print('Open socket')
        self.write_message('Current version is %s' % self.application.version)

    def on_message(self, message):
        self.write_message(self.application.version)

    def on_close(self):
        print('Web socket closed.')
