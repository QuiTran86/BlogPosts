import os


class Config:
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    FLASKY_ADMIN = os.getenv('FLASKY_ADMIN')

    FLASKY_MAIL_SENDER = os.getenv('FLASKY_MAIL_SENDER')
    FLASKY_MAIL_SUBJECT_PREFIX = os.getenv('FLASKY_MAIL_SUBJECT_PREFIX')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')

    FLASKY_POST_PER_PAGES = 10
    FLASKY_FOLLOWERS_PERPAGE = 10

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_DEV_URI')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_TEST_URI')


config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig
}
