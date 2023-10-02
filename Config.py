import os # os = operating system, helps locate the env file
#in our env it treats everything liek a dictionary, thats why we need to put .get('SQLALCHEMY_DATABASE_URL')

class Config:
  PROPAGATE_EXCEPTIONS = True
  API_TITLE = 'Hand Therapy Rest Api'
  API_VERSION = 'v1'
  OPENAPI_VERSION = '3.0.3'
  OPENAPI_URL_PREFIX = '/'
  OPENAPI_SWAGGER_UI_PATH = '/'
  OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
  SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URL')
  JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
  # jwt_secret_key: we pick our own secure secret key. When JWT generates access token for user, it signs it with our secret_key. SO if a hacker or something decodes secret key or generates their own & hacks in, they need to have our secret key
  # you do os.environ.get when you want to use something sensitive, because we want that info to be pulled from a file that is in our gitignore so that it doesnt get posted all over github