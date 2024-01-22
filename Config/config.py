import os

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'this is important secret_key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_DATABASE_URI='mysql://root:1223@localhost/db_toplist'
