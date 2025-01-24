import os
from cliente import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField

class FormularioCliente(FlaskForm):
    nome = StringField('Nome do cliente', [validators.DataRequired(),
                                           validators.length(min=2, max=50)])
    
    email = StringField('Digite o email', [validators.DataRequired(),
                                           validators.length(min=2, max=50)])
    
    telefone = StringField('Digite o telefone', [validators.DataRequired(),
                                                 validators.length(min=2, max=15)])
    
    cadastrar = SubmitField('Cadastrar Cliente')
    
class FormularioUsuario(FlaskForm):
    
    usuario = StringField('Usuário', [validators.DataRequired(),
                                  validators.length(min=2, max=20)])
    
    senha = PasswordField('Senha',[validators.DataRequired(),
                                  validators.length(min=3, max=15)] )
    
    logar = SubmitField('Entrar')
    
    
class FormularioCadastroUsuario(FlaskForm):
    
    nome = StringField('Nome ', [validators.DataRequired(),
                       validators.length(min=2, max=50)])
    
    usuario = StringField('Usuario', [validators.DataRequired(),
                       validators.length(min=2, max=20)])
    
    senha = PasswordField('Senha', [validators.DataRequired(),
                       validators.length(min=6, max=255)])
    
    cadastrar = SubmitField('Cadastrar usuário')
    

def recupera_imagem(id):
    for nome_imagem in os.listdir(app.config['UPLOAD_PASTA']):
        
        nome = str(nome_imagem)
        
        nome = nome.split('.')
        
        if f'album{id}_' in nome[0]:
            return nome_imagem
        
    return 'default.png'

def deletar_imagem(id):
    imagem = recupera_imagem(id)
    
    if imagem != 'default.png':
        os.remove(os.path.join(app.config['UPLOAD_PASTA'], imagem))