from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from cliente import db, app
from models import Cliente
from definicoes import recupera_imagem, deletar_imagem, FormularioCliente
import time
from views_servicos import *

@app.route('/')
def listarClientes():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    
    lista = Cliente.query.order_by(Cliente.id_cliente)
    
    return render_template('lista_clientes.html', clientes=lista)

@app.route('/cadastrar')
def cadastrarClientes():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    
    form = FormularioCliente()
    
    return render_template('cadastro_cliente.html',
                           titulo="Cadastrar cliente", form=form)

@app.route('/adicionar', methods=['POST',])
def adicionar_cliente():
    
    formRecebido = FormularioCliente(request.form)
    
    if not formRecebido.validate_on_submit():
        return redirect(url_for('cadastrarClientes'))
    
    nome = formRecebido.nome.data
    email = formRecebido.email.data
    telefone = formRecebido.telefone.data

    cliente = Cliente.query.filter_by(nome_cliente=nome).first()
    
    if cliente: 
        flash("Cliente já está cadastrado!")
        return redirect(url_for('listarClientes'))
    
    novo_cliente = Cliente(nome_cliente=nome, email=email, telefone=telefone)
    
    db.session.add(novo_cliente)
    db.session.commit()
    
    arquivo = request.files['arquivo']
    
    if arquivo:
    
        pasta_arquivos = app.config['UPLOAD_PASTA']
    
        nome_arquivo = arquivo.filename
    
        nome_arquivo = nome_arquivo.split('.')
    
        extensao = nome_arquivo[len(nome_arquivo)-1]
    
        momento = time.time()
    
        nome_completo = f'album{novo_cliente.id_cliente}_{momento}.{extensao}'
    
        arquivo.save(f'{pasta_arquivos}/{nome_completo}')

    return redirect(url_for('listarClientes'))

@app.route('/editar/<int:id>')
def editar(id):
    
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    
    clienteBuscado = Cliente.query.filter_by(id_cliente=id).first()
    
    form = FormularioCliente()
    
    form.nome.data = clienteBuscado.nome_cliente
    form.email.data = clienteBuscado.email
    form.telefone.data = clienteBuscado.telefone
    
    
    album = recupera_imagem(id)
    
    return render_template('editar_cliente.html', 
                           titulo = 'Editar cliente',
                           cliente = form, album_cliente = album, id=id)
    

@app.route('/atualizar', methods=['POST',])
def atualizar():
    
    formRecebido = FormularioCliente(request.form)
    
    if formRecebido.validate_on_submit():
    
        cliente = Cliente.query.filter_by(id_cliente=request.form['txtId']).first()
        
        cliente.nome_cliente = formRecebido.nome.data
        cliente.email = formRecebido.email.data
        cliente.telefone = formRecebido.telefone.data
        
        db.session.add(cliente)
        db.session.commit()
        
        arquivo = request.files['arquivo']
        
        if arquivo:
        
            pasta_upload = app.config['UPLOAD_PASTA']
            
            nome_arquivo = arquivo.filename
            
            nome_arquivo = nome_arquivo.split('.')
            
            extensao = nome_arquivo[len(nome_arquivo)-1]
            
            momento = time.time()
            
            nome_completo = f'album{cliente.id_cliente}_{momento}.{extensao}'
            
            deletar_imagem(cliente.id_cliente)
            
            arquivo.save(f'{pasta_upload}/{nome_completo}')
            
        flash("Cliente editado com Sucesso!")
    
    return redirect(url_for('listarClientes'))

@app.route('/excluir/<int:id>')
def excluir(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    
    # 1. Verifique se o cliente tem serviços associados
    from sqlalchemy import func
    servicos_associados = db.session.query(func.count(Servico.id_servico)).filter_by(cliente_id=id).scalar()
    
    # 2. Se houver serviços, retorne um aviso
    if servicos_associados > 0:
        flash("Não é possível excluir este cliente, pois ele possui serviços associados.", "error")
        return redirect(url_for('listarClientes'))
        
    # 3. Se não houver serviços, prossiga com a exclusão
    try:
        Cliente.query.filter_by(id_cliente=id).delete()
        deletar_imagem(id)
        db.session.commit()
        flash("Cliente excluído com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        print(f"Ocorreu um erro ao tentar excluir: {e}")
        flash("Ocorreu um erro ao tentar excluir o cliente.", "error")
    
    return redirect(url_for('listarClientes'))