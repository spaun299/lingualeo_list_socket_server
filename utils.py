from concurrent.futures import ThreadPoolExecutor
import tornado.gen
import shelve
import os

pool = ThreadPoolExecutor(max_workers=5)


@tornado.gen.coroutine
def call_blocking_func_async(func, *args, **kwargs):
    result = yield pool.submit(func, *args, **kwargs)
    return result


def __get_shelve_filename():
    return '%s/shelve_session' % os.path.dirname(
        os.path.abspath(__file__))


def shelve_save(**kwargs):
    file_name = __get_shelve_filename()
    db = False
    try:
        db = shelve.open(file_name, protocol=2, writeback=True)
        db.update(dict(**kwargs))
    finally:
        if db is not False:
            db.close()
            return 'Saved successfully'


def shelve_get(key):
    file_name = __get_shelve_filename()
    try:
        db = shelve.open(file_name, protocol=2)
        obj = db.get(key)
    finally:
        db.close()
    return obj
