from flask import render_template, request, redirect, url_for, flash, session
from cliente import app, db
from models import Servico, Cliente


def usuario_nao_autenticado():
    return 'usuario_logado' not in session or session['usuario_logado'] is None


@app.route('/servicos')
def listar_servicos():
    if usuario_nao_autenticado():
        return redirect(url_for('login'))

    servicos = Servico.query.order_by(Servico.id_servico).all()
    return render_template('servicos.html', servicos=servicos)


@app.route('/servicos/novo', methods=['GET', 'POST'])
def criar_servico():
    if usuario_nao_autenticado():
        return redirect(url_for('login'))

    if request.method == 'POST':
        novo_servico = Servico(
            nome_servico=request.form['nome_servico'],
            descricao=request.form.get('descricao'),
            valor=float(request.form.get('valor', 0)),
            status=request.form.get('status', ''),
            cliente_id=request.form['cliente_id']
        )
        db.session.add(novo_servico)
        db.session.commit()
        flash("Serviço criado com sucesso!")
        return redirect(url_for('listar_servicos'))

    clientes = Cliente.query.order_by(Cliente.nome_cliente).all()
    return render_template('novo_servico.html', titulo="Criar Serviço", clientes=clientes)

@app.route('/servicos/editar/<int:id>', methods=['GET', 'POST'])
def editar_servico(id):
    servico = Servico.query.get_or_404(id)

    if request.method == 'POST':
        servico.nome_servico = request.form['nome_servico']
        servico.descricao = request.form.get('descricao')
        servico.valor = float(request.form.get('valor', 0))
        servico.status = request.form.get('status', '')
        servico.cliente_id = request.form['cliente_id']

        db.session.commit()
        flash('Serviço atualizado com sucesso!')
        return redirect(url_for('listar_servicos'))

    clientes = Cliente.query.order_by(Cliente.nome_cliente).all()
    return render_template('editar_servico.html', servico=servico, clientes=clientes, titulo='Editar Serviço')



@app.route('/servicos/excluir/<int:id>', methods=['POST'])
def excluir_servico(id):
    servico = Servico.query.get_or_404(id)
    db.session.delete(servico)
    db.session.commit()
    flash("Serviço excluído com sucesso!")
    return redirect(url_for('listar_servicos'))