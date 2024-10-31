from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from cliente import db, app
from models import Cliente, Usuario
from definicoes import recupera_imagem

@app.route('/')
def listarClientes():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    
    lista = Cliente.query.order_by(Cliente.id_cliente)
    
    return render_template('lista_clientes.html', 
                           titulo='Clientes Cadastrados',
                           clientes=lista)

@app.route('/cadastrar')
def cadastrarClientes():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    
    return render_template('cadastro_cliente.html',
                           titulo="Cadastrar cliente")

@app.route('/adicionar', methods=['POST',])
def adicionar_cliente():
    nome = request.form['txtNome']
    email = request.form['txtEmail']
    telefone = request.form['txtTelefone']

    cliente = Cliente.query.filter_by(nome_cliente=nome).first()
    
    if cliente: 
        flash("Cliente já está cadastrado!")
        return redirect(url_for('listarClientes'))
    
    novo_cliente = Cliente(nome_cliente=nome, email=email, telefone=telefone)
    
    db.session.add(novo_cliente)
    db.session.commit()
    
    arquivo = request.files['arquivo']
    
    pasta_arquivos = app.config['UPLOAD_PASTA']
    
    nome_arquivo = arquivo.filename
    
    nome_arquivo = nome_arquivo.split('.')
    
    extensao = nome_arquivo[len(nome_arquivo)-1]
    
    nome_completo = f'album{novo_cliente.id_cliente}.{extensao}'
    
    arquivo.save(f'{pasta_arquivos}/{nome_completo}')

    return redirect(url_for('listarClientes'))

@app.route('/editar/<int:id>')
def editar(id):
    
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    
    clienteBuscado = Cliente.query.filter_by(id_cliente=id).first()
    
    album = recupera_imagem(id)
    
    return render_template('editar_cliente.html', 
                           titulo = 'Editar cliente',
                           cliente = clienteBuscado,
                           album_cliente = album)
    

@app.route('/atualizar', methods=['POST',])
def atualizar():
    
    cliente = Cliente.query.filter_by(id_cliente=request.form['txtId']).first()
    
    cliente.nome_cliente = request.form['txtNome']
    cliente.email = request.form['txtEmail']
    cliente.telefone = request.form['txtTelefone']
    
    db.session.add(cliente)
    db.session.commit()
    
    return redirect(url_for('listarClientes'))

@app.route('/excluir/<int:id>')
def excluir(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    
    Cliente.query.filter_by(id_cliente=id).delete()
    
    db.session.commit()
    
    flash("Cliente excluida com sucesso")
    
    return redirect(url_for('listarClientes'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuario.query.filter_by(login_usuario=request.form['txtLogin']).first()
    
    if usuario:
        if request.form['txtSenha'] == usuario.senha_usuario:
            session['usuario_logado'] = request.form['txtLogin']
            flash(f"Usuário {usuario.login_usuario} logado com sucesso")
            return redirect(url_for('listarClientes'))
        else:
            flash("Senha inválida")
            return redirect(url_for('login'))
    else:
        flash("Usuário ou senha inválidos")
    
    return redirect(url_for('login'))

@app.route('/sair')
def sair():
    session['usuario_logado'] = None
    return redirect(url_for('login'))

@app.route('/uploads/<nome_imagem>')
def imagem(nome_imagem):
    return send_from_directory('uploads', nome_imagem)
