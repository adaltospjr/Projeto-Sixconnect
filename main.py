from flask import render_template, request, request
from flask_sqlalchemy import SQLAlchemy
from twitter import busca
from envio import novos_clientes, clientes_antigo
from conexao import Clientes, Funcionarios, Equipamentos, db, app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, AnyOf

app.config['SECRET_KEY'] = 'Thisisasecret!'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdoUiMiAAAAAC2Tp_8caBVKI_PzUE45CELwRis3'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdoUiMiAAAAAMdyUEFyNno-3Xt0k1-bB-LRS4JV'
app.config['TESTING'] = True

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is required!'), Length(min=5, max=10, message='Must be between 5 and 10 characters.')])
    password = PasswordField('password', validators=[InputRequired('Password is required!'), AnyOf(values=['password', 'secret'])])
    recaptcha = RecaptchaField()

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>The username is {}. The password is {}.'.format(form.username.data, form.password.data)
    return render_template('form.html', form=form)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/cadastrarfuncionarios')
def get_funcionarios():
    return render_template('cadastrarfuncionarios.html')

@app.route('/cadastrarfuncionarios', methods=["POST"])
def cadastrar_funcionarios():
    name = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    validador = name.replace(" ", "")
    if not validador.isalpha():
        message = "Por favor, digite somente letras no campo nome"
        return render_template("cadastrarfuncionarios.html", message=message)
    else:
        # class instance 
        funcionario = Funcionarios(name=name, email=email, senha=senha)
        # crio o registro no banco
        funcionario.create_funcionario()
        # busco todos os registros
        funcionarios = funcionario.query.all()
        return render_template('consultafuncionarios.html', funcionarios=funcionarios)

@app.route('/cadastrarclientes')
def get_clientes():
    return render_template('cadastrarclientes.html')

@app.route('/cadastrarclientes', methods=["POST"])
def cadastrar_clientes():
    name = request.form.get("nome")
    email = str(request.form.get("email"))
    validador = name.replace(" ", "")
    if not validador.isalpha():
        message = "Por favor, digite somente letras no campo nome."
        return render_template("cadastrarclientes.html", message=message)
    else:
        cliente = Clientes(name=name, email=email)
        cliente.create_cliente()
        clientes = Clientes.query.all()
        novos_clientes(email)
        return render_template('consultaclientes.html', clientes=clientes)

@app.route('/cadastrarequipamentos')
def get_equipamentos():
    return render_template('cadastrarequipamentos.html')

@app.route('/cadastrarequipamentos', methods=["POST"])
def cadastrar_equipamentos():
    name = request.form.get("nome")
    codigo = int(request.form.get("codigo"))
    qtde = int(request.form.get("qtde"))
    if not codigo >= 0:
        message = "Por favor, digite um código com números positivos"
        return render_template("cadastrarequipamentos.html", message=message)
    elif not qtde >= 0:
        message = "Por favor, digite a QDTE positiva para cadastrar no estoque"
        return render_template("cadastrarequipamentos.html", message=message)
    else:
        equipamento = Equipamentos(name=name, codigo=codigo, qtde=qtde)
        equipamento.create_equipamento()
        equipamentos = equipamento.query.all()
        return render_template('consultaequipamentos.html', equipamentos=equipamentos)

@app.route('/consultaequipamentos')
def consulta_equipamentos():
    equipamentos = Equipamentos.query.all()
    return render_template('consultaequipamentos.html', equipamentos=equipamentos)

@app.route('/consultafuncionarios')
def consulta_funcionarios():
    funcionarios = Funcionarios.query.all()
    return render_template('consultafuncionarios.html', funcionarios=funcionarios)

@app.route('/consultaclientes')
def consulta_clientes():
    clientes = Clientes.query.all()
    return render_template('consultaclientes.html', clientes=clientes)

@app.route('/deleteclientes')
def get_deletar_clientes():
    return render_template('deleteclientes.html')

@app.route('/deleteclientes', methods=["POST"])
def deletar_clientes():
    id = int(request.form.get("id"))
    if  id <= 0:
        message = "Por favor, digite somente números positivos no campo id."
        return render_template("deleteclientes.html", message=message)
    elif id in Clientes.consultar_id_clientes():
        email = Clientes.email_cliente_deletado(id)
        clientes_antigo(email)
        Clientes.delete_cliente(id)
        clientes = Clientes.query.all()
        return render_template('consultaclientes.html', clientes=clientes)
    else:
        message = "Id não encontrado, digite um id válido."
        return render_template("deleteclientes.html", message=message)

@app.route('/deletefuncionarios')
def get_deletar_funcionarios():
    return render_template('deletefuncionarios.html')

@app.route('/deletefuncionarios', methods=["POST"])
def deletar_funcionarios():
    id = int(request.form.get("id"))
    if  id <= 0:
        message = "Por favor, digite somente números positivos no campo id."
        return render_template("deletefuncionarios.html", message=message)
    elif id in Funcionarios.consultar_id_funcionario():
        Funcionarios.delete_funcionario(id)
        funcionarios = Funcionarios.query.all()
        return render_template('consultafuncionarios.html', funcionarios=funcionarios)
    else:
        message = "Id não encontrado, digite um id válido."
        return render_template("deletefuncionarios.html", message=message)

@app.route('/deleteequipamento')
def get_deletar_equipamentos():
    return render_template('deleteequipamentos.html')

@app.route('/deleteequipamento', methods=["POST"])
def deletar_equipamentos():
    id = int(request.form.get("id"))
    if  not id >= 0:
        message = "Por favor, digite somente números positivos no campo id."
        return render_template("deleteequipamentos.html", message=message)
    elif id in Equipamentos.consultar_id_equipamentos():
        Equipamentos.delete_equipamento(id)
        equipamentos = Equipamentos.query.all()
        return render_template('consultaequipamentos.html', equipamentos=equipamentos)
    else:
        message = "Id não encontrado, digite um id válido."
        return render_template("deleteequipamentos.html", message=message)

@app.route('/atualizarclientes')
def get_atualizar_cliente():
    return render_template('atualizarclientes.html')

@app.route('/atualizarclientes', methods=["POST"])
def atualizar_cliente():
    id = int(request.form.get("id"))
    nome = request.form.get("nome")
    email = request.form.get("email")
    validador = nome.replace(" ", "")
    if not validador.isalpha():
        message = "Por favor, digite somente letras no campo nome."
        return render_template("atualizarclientes.html", message=message)
    elif not id >= 0:
        message = "Por favor, digite somente números positivos no campo id."
        return render_template("atualizarclientes.html", message=message)
    elif id in Clientes.consultar_id_clientes():
        Clientes.atualizar_clientes(id, nome, email)
        clientes = Clientes.query.all()
        return render_template('consultaclientes.html', clientes=clientes)
    else:
        message = "Id não encontrado, digite um id válido."
        return render_template("atualizarclientes.html", message=message)

@app.route('/atualizarequipamentos')
def get_atualizar_equipamento():
    return render_template('atualizarequipamentos.html')

@app.route('/atualizarequipamentos', methods=["POST"])
def atualizar_equipamento():
    id = int(request.form.get("id"))
    nome = request.form.get("nome")
    codigo = request.form.get("codigo") 
    qtde = int(request.form.get("qtde"))
    if not id >= 0:
        message = "Por favor, digite somente números positivos no campo id."
        return render_template("atualizarequipamentos.html", message=message)
    elif not qtde >= 0:
        message = "Por favor, digite a QDTE positiva para cadastrar no estoque"
        return render_template("atualizarequipamentos.html", message=message)
    elif id in Equipamentos.consultar_id_equipamentos():
        Equipamentos.atualizar_equipamentos(id, nome, codigo, qtde)
        equipamentos = Equipamentos.query.all()
        return render_template('consultaequipamentos.html', equipamentos=equipamentos)
    else:
        return "Id não encontrado, digite um id válido"

@app.route('/atualizarfuncionarios')
def get_atualizar_funcionario():
    return render_template('atualizarfuncionarios.html')

@app.route('/atualizarfuncionarios', methods=["POST"])
def atualizar_funcionario():
    id = int(request.form.get("id"))
    nome = request.form.get("nome")
    email = request.form.get("email")
    validador = nome.replace(" ", "")
    if not validador.isalpha():
        message = "Por favor, digite somente letras no campo nome"
        return render_template("atualizarfuncionarios.html", message=message)
    elif not id >= 0:
        message = "Por favor, digite somente números positivos no campo id."
        return render_template("atualizarfuncionarios.html", message=message)
    elif nome.isalpha() == False:
        message = "Por favor, digite um id com número positivo."
        return render_template("atualizarfuncionarios.html", message=message)    
    elif id in Funcionarios.consultar_id_funcionario():
        Funcionarios.atualizar_funcionarios(id, nome, email)
        funcionarios = Funcionarios.query.all()
        return render_template('consultafuncionarios.html', funcionarios=funcionarios)
    else:
        message = "Id não encontrado, digite um id válido"
        return render_template("atualizarfuncionarios.html", message=message)

@app.route('/twitter')
def twitter():
    retorno_busca = busca()
    return render_template('twitter.html', retorno_busca=retorno_busca)

if __name__ =="__main__":
	db.create_all()
	app.run(debug=True)
