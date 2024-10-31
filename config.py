import os

SECRET_KEY = 'apredendocodigoflask'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'root',
        servidor = 'localhost',
        database = 'cliente'
    )
    
UPLOAD_PASTA = os.path.dirname(os.path.abspath(__file__)) + '/uploads'