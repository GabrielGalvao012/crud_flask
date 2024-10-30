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