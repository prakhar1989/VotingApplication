class Config(object):
    DEBUG = False
    SECRET_KEY = '7\xe9\xcf\x17\x11\x92I|\xbc\x85\xc8\xc1u\x18\xbb\xec\xc9\xe2\xbb,\x9fX'
    SESSION_COOKIE_NAME = 'votingApp'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:prakhar@localhost/voting_app'

class DevelopmentConfig(Config):
    DEBUG = True
    USERNAME = 'admin'
    PASSWORD = 'admin'
    ADMIN_COUPON = 'admin'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:prakhar@localhost/election'

