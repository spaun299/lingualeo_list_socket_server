import tornado.ioloop
from handlers import CheckForUpdates, AdminLogin, Admin
import tornado.web
import tornado.httpserver
from config import DEBUG, STATIC_PATH, TEMPLATE_PATH
from utils import shelve_get


class Application(tornado.web.Application):

    def __init__(self):
        self.handlers = [(r'/', CheckForUpdates),
                         (r'/admin/login', AdminLogin),
                         (r'/admin', Admin)]
        self.settings = dict(
            template_path=TEMPLATE_PATH,
            static_path=STATIC_PATH,
            cookie_secret='ss1sx!sd15cx1vfgsdf453s2~1`!s=d453',
            login_url='/admin/login',
            debug=DEBUG
        )
        self.version = shelve_get('version')
        super(Application, self).__init__(handlers=self.handlers, **self.settings)

if __name__ == '__main__':
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
