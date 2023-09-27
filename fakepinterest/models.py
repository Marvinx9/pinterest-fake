# criar a estrutura do banco de dados

from fakepinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin

# retorna quem é o meu usuário por meio do banco de dados, utilizando o id_usuario para consulta
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


# UserMixin, diz qual a classe irá gerenciar a estrutura de login
# criando uma tabela no meu banco de dados para armazenamento de dados dos usuários
# database.Column -> cria as colunas do banco de dados
class Usuario(database.Model, UserMixin):
    # primary key serve para indicar que o id é uma chave que é a chave principal
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
# serve para indicar dentro da tabela de usuarios, qual foto estou a procura da tabela de fotos
# o parâmetro backref serve como um relationship reverso, ou seja consigo encontrar o usuário
# de uma foto a partir de uma foto da tabela de (Foto)
    fotos = database.relationship("Foto", backref="usuario", lazy=True) #lazy serve para otimizar a busca dentro do banco de dados


# criando uma tabela no meu banco de dados para armazenar as postagens dos usuários
class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
# a imagem é um texto, porque a informação que irei guardar no meu banco de dados é o local onde minha imagem pode ser acessada
    imagem = database.Column(database.String, default="default.png")
# datatime é usado para pegar a informação de tempo no momento do commit da foto no formato utc
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
# chave estrangeira, a variável fotos da classe Usuario vai buscar uma local da imagem de uma foto
# que contém o mesmo id que tenha na classe Fotos
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)