class Config(object):
    DEBUG = False
    SECRET_KEY = '7\xe9\xcf\x17\x11\x92I|\xbc\x85\xc8\xc1u\x18\xbb\xec\xc9\xe2\xbb,\x9fX'
    SESSION_COOKIE_NAME = 'votingApp'
    ALLOW_RESULTS = False
    LOG_FORMAT = '%(asctime)s %(message)s'
    LOG_FILENAME = 'extras/dev.log'

class ProductionConfig(Config):
    USERNAME = 'admin'
    PASSWORD = 'admin'
    ADMIN_COUPON = 'admin'
    SQLALCHEMY_DATABASE_URI = 'mysql://election:election@localhost/election'

class DevelopmentConfig(Config):
    DEBUG = True
    USERNAME = 'admin'
    PASSWORD = 'admin'
    ADMIN_COUPON = 'admin'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:prakhar@localhost/election'
    LOG_FILENAME = 'extras/dev.log'

