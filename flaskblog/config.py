import os


class Config:
    # get the unique code from python terminal using module : "import os,secrets"
    # then in the terminal type "secrets.token_hex(16)
    # SECRET_KEY = os.environ.get('c49d4965dd07b994a1a65683d869297c')
    SECRET_KEY = 'c49d4965dd07b994a1a65683d869297c'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


    # flask mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    # MAIL_USERNAME = os.environ.get('USER_NAME')
    MAIL_USERNAME = 'put your email'
    # MAIL_PASSWORD = os.environ.get('USER_PASSWORD')
    MAIL_PASSWORD = 'put email password'
