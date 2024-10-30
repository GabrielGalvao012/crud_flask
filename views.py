from flask import render_template, request, redirect, session, flash, url_for
from models import Cliente, Usuario
from cliente import db, app

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
