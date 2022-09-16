from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.sqlite3'

db = SQLAlchemy(app)

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
