from flask import render_template, request, redirect, url_for, flash, session
from cliente import app, db
from models import Servico, Cliente

@app.route('/dashboard')
def dashboard():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))

    # Soma geral dos serviços
    receita_total = db.session.query(db.func.sum(Servico.valor)).scalar() or 0

    # Receita por cliente
    receita_por_cliente = (
        db.session.query(Cliente.nome_cliente, db.func.sum(Servico.valor))
        .join(Servico, Cliente.id_cliente == Servico.cliente_id)
        .group_by(Cliente.id_cliente)
        .all()
    )

    # Serviços por status
    servicos_por_status = (
        db.session.query(Servico.status, db.func.count(Servico.id_servico))
        .group_by(Servico.status)
        .all()
    )

    return render_template(
        'dashboard.html',
        receita_total=receita_total,
        receita_por_cliente=receita_por_cliente,
        servicos_por_status=servicos_por_status
    )
