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