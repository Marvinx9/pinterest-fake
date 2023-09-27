# criar as rotas do site
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.templates.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename


@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin=FormLogin()
# verificando se o usuario enviou dados para login válidos
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
# verificando se a senha que o usuario inserio é igual a senha que temos armazenada no banco de dados
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=formlogin)

@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    formcriarconta=FormCriarConta()
# verifica se o botão de criarconta foi submetido, e se está válido, caso positivo, podemos criar o usuário no banco de dados
    if formcriarconta.validate_on_submit():
# encriptar a senha do usuário para que ninguem possa ter acesso a essa senha, porque o bcrypt usa a SECRET_KEY que foi criada
# na página init, como parámetro para criar a criptografia
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data,
                          email=formcriarconta.email.data,
                          senha=senha)
 # adicionando os dados do usuário no meu banco de dados
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=formcriarconta)



# login_required, só permite executar a função se o usuário estiver logado
@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
# o usuário pode ta vendo o próprio perfil
        formfoto=FormFoto()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
# tratando os nomes das imagens coletadas para não causar erro no código
            nome_seguro = secure_filename(arquivo.filename)
# salvar o arquivo dentro da pasta de fotos post
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                    app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
# salvar o caminho do arquivo dentro do banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=formfoto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)