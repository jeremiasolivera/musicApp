class Config():
    SECRET_KEY = 'cd51d25dfc04cba154dd4deec5f6d8f2c9b541deb4fff67c'


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig
}
