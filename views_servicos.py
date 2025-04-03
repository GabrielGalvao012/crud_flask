from flask import render_template, request, redirect, url_for, flash, session
from cliente import app, db
from models import Servico, Cliente

@app.route('/servicos')
def listar_servicos():
    # Verifica se o usuário está logado, se necessário
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    
    servicos = Servico.query.order_by(Servico.id_servico).all()
    return render_template('servicos.html',  servicos=servicos)

@app.route('/servicos/novo', methods=['GET', 'POST'])
def criar_servico():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nome = request.form['nome_servico']
        descricao = request.form.get('descricao')
        cliente_id = request.form['cliente_id']
        
        novo_servico = Servico(nome_servico=nome, descricao=descricao, cliente_id=cliente_id)
        db.session.add(novo_servico)
        db.session.commit()
        flash("Serviço criado com sucesso!")
        return redirect(url_for('listar_servicos'))
    
    # Para exibir o formulário, precisamos listar os clientes cadastrados para seleção
    clientes = Cliente.query.order_by(Cliente.nome_cliente).all()
    return render_template('novo_servico.html', titulo="Criar Serviço", clientes=clientes)

@app.route('/servicos/editar/<int:id>', methods=['GET', 'POST'])
def editar_servico(id):
    # Busca o serviço pelo id, ou retorna 404 se não existir
    servico = Servico.query.get_or_404(id)

    if request.method == 'POST':
        # Atualiza os dados do serviço a partir do formulário
        servico.nome_servico = request.form['nome_servico']
        servico.descricao = request.form.get('descricao')
        servico.cliente_id = request.form['cliente_id']
        db.session.commit()
        flash('Serviço atualizado com sucesso!')
        return redirect(url_for('listar_servicos'))

    # Busca os clientes para o <select> do formulário de edição
    clientes = Cliente.query.order_by(Cliente.nome_cliente).all()
    return render_template('editar_servico.html', servico=servico, clientes=clientes, titulo='Editar Serviço')

@app.route('/servicos/excluir/<int:id>', methods=['POST'])
def excluir_servico(id):
    servico = Servico.query.get_or_404(id)
    db.session.delete(servico)
    db.session.commit()
    flash("Serviço excluído com sucesso!")
    return redirect(url_for('listar_servicos'))

# Outras rotas para editar/excluir serviço podem ser criadas de forma semelhante.
