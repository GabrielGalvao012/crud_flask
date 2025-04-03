from cliente import db

class Cliente(db.Model):
    id_cliente = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nome_cliente = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50),nullable = False)
    telefone = db.Column(db.String(15), nullable = False)
    
    def __repr__(self):
        return '<Name %r' %self.name
    
class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nome_usuario = db.Column(db.String(50), nullable = False)
    login_usuario = db.Column(db.String(20),nullable = False)
    senha_usuario = db.Column(db.String(15), nullable = False)
    
    def __repr__(self):
        return '<Name %r' %self.name

# Serviço novo se der erro tirar isso 
class Servico(db.Model):
    id_servico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_servico = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=False)
    # Relacionamento com o modelo Cliente:
    cliente = db.relationship('Cliente', backref='servicos')

    def __repr__(self):
        return f"<Servico {self.nome_servico}>"