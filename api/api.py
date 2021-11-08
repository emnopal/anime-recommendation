import sys
sys.path.append('..')

from Deployment import app # noqa


def testing():
    return app.test()
