from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

# criando o app do site
app = Flask(__name__)

# configura o banco de dados e também cria o banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# é uma chave de segurança que garante a segurança do meu app
app.config["SECRET_KEY"] = "287414e2f37ddf4ae8be22503b94bd08"

# criando variável para mostrar o caminho do upload de uma imagem para o static
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

# criando o banco de dados para o app
database = SQLAlchemy(app)


# iniciando biblioteca que irá realizar a criptografía
bcrypt = Bcrypt(app)

# iniciando biblioteca que irá ser responsável pelo login
login_manager = LoginManager(app)

# Vai redirecionar o usuário para a 'homepage', caso ele não tenha realizado o login
login_manager.login_view = "homepage"

from fakepinterest import routes