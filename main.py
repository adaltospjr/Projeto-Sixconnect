from flask import Flask, render_template, request, request
from flask_sqlalchemy import SQLAlchemy
from twitter import busca
from envio import novos_clientes, clientes_antigo

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.sqlite3'

db = SQLAlchemy(app)

class Funcionarios(db.Model):
    id_funcionario = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    senha = db.Column(db.String(10), nullable=False)

    def create_funcionario(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()
    
    def atualizar_funcionarios(id, nome, email):
        funcionario = Funcionarios.query.filter_by(id_funcionario=f'{id}').first()
        funcionario.email = email
        funcionario.name = nome
        db.session.commit()
        db.session.close()

    def delete_funcionario(id):
        Funcionarios.query.filter(Funcionarios.id_funcionario == f'{id}').delete()
        db.session.commit()
        db.session.close()

    def consultar_id_funcionario():
        lista_id = []
        id_funcionarios = db.session.query(Funcionarios.id_funcionario).all()
        for i in id_funcionarios:
            lista_id.append(i[0])
        return lista_id

class Clientes(db.Model):
    id_cliente = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(30), nullable=False)

    def create_cliente(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()

    def atualizar_clientes(id, nome, email):
        cliente = Clientes.query.filter_by(id_cliente=f'{id}').first()
        cliente.email = email
        cliente.name = nome
        db.session.commit()
        db.session.close()

    def delete_cliente(id):
        Clientes.query.filter(Clientes.id_cliente == f'{id}').delete()
        db.session.commit()
        db.session.close()

    def consultar_id_clientes():
        lista_id = []
        id_clientes = db.session.query(Clientes.id_cliente).all()
        for i in id_clientes:
            lista_id.append(i[0])
        return lista_id
    
    def email_cliente_deletado(id):
        email = Clientes.query.filter_by(id_cliente=id).first()
        return email.email

class Equipamentos(db.Model):
    id_equipamento = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    codigo = db.Column(db.Integer, nullable=False, unique=True)
    qtde = db.Column(db.Integer, nullable=False)

    def create_equipamento(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()

    def delete_equipamento(id):
        Equipamentos.query.filter(Equipamentos.id_equipamento == f'{id}').delete()
        db.session.commit()
        db.session.close()

    def atualizar_equipamentos(id, nome, codigo, qtde):
        equipamento = Equipamentos.query.filter_by(id_equipamento=f'{id}').first()
        equipamento.codigo = codigo
        equipamento.name = nome
        equipamento.qtde = qtde
        db.session.commit()
        db.session.close()

    def consultar_id_equipamentos():
        lista_id = []
        id_equipamentos = db.session.query(Equipamentos.id_equipamento).all()
        for i in id_equipamentos:
            lista_id.append(i[0])
        return lista_id

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
