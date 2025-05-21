import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import (
    db, Transportadora,
    Produtor, Produto,
    Consumidor,
    consumidor_produto
    )
from populate_db import popular_db
from prometheus_client import Counter, Gauge, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(base_dir, 'db')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
db_path = os.path.join(base_dir, 'db', 'db_supermercado.db')

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def db_vazia():
    return not any([
        Transportadora.query.first(),
        Produtor.query.first(),
        Produto.query.first()
        ])


with app.app_context():
    db.create_all()

    if db_vazia():
        popular_db()


HTTP_REQUESTS_TOTAL = Counter(
    'http_requests_total',
    'Total de requisições HTTP',
    ['method', 'endpoint', 'http_status']
)

REQUESTS_IN_PROGRESS = Gauge(
    'http_requests_in_progress',
    'Número de requisições sendo processadas',
    ['method', 'endpoint']
)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

@app.before_request
def before_request():
    REQUESTS_IN_PROGRESS.labels(
        method=request.method,
        endpoint=request.path
    ).inc()


@app.after_request
def after_request(response):
    # Atualiza métricas após cada request
    HTTP_REQUESTS_TOTAL.labels(
        method=request.method,
        endpoint=request.path,
        http_status=response.status_code
    ).inc()

    REQUESTS_IN_PROGRESS.labels(
        method=request.method,
        endpoint=request.path
    ).dec()

    return response


@app.route('/', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        consumidor = Consumidor(nome=nome)  # Criando consumidor
        db.session.add(consumidor)
        db.session.commit()  # Salvando no banco

        return redirect(url_for(
            'escolher_produtos',
            consumidor_id=consumidor.id
            ))  # Redireciona com o ID correto

    return render_template('cadastro.html')


@app.route('/escolher_produtos/<int:consumidor_id>', methods=['GET', 'POST'])
def escolher_produtos(consumidor_id):
    consumidor = Consumidor.query.get_or_404(consumidor_id)

    produtos = Produto.query.all()
    frutas = list(set(p.nome.split()[0] for p in produtos))
    produtos_por_fruta = {fruta: Produto.query.filter(
        Produto.nome.startswith(fruta)
        ).all() for fruta in frutas}

    produto_recomendado_por_fruta = {
        fruta: min(fornecedores, key=lambda p: p.custo_poluicao)
        for fruta, fornecedores in produtos_por_fruta.items()
    }

    if request.method == 'POST':
        # Remover produtos antigos do consumidor
        db.session.execute(consumidor_produto.delete().where(
            consumidor_produto.c.consumidor_id == consumidor.id
            ))

        for fruta, fornecedores in produtos_por_fruta.items():
            for produto in fornecedores:
                quantidade = int(
                    request.form.get(
                        f'quantidade_{produto.id}',
                        0
                        ))
                if quantidade > 0:
                    db.session.execute(consumidor_produto.insert().values(
                        consumidor_id=consumidor.id,
                        produto_id=produto.id,
                        quantidade=quantidade
                    ))

        db.session.commit()
        return redirect(url_for('resumo_compra', consumidor_id=consumidor.id))

    return render_template(
        'escolher_produtos.html',
        produtos_por_fruta=produtos_por_fruta,
        produto_recomendado_por_fruta=produto_recomendado_por_fruta,
        consumidor=consumidor
        )


@app.route('/resumo_compra/<int:consumidor_id>')
def resumo_compra(consumidor_id):
    consumidor = Consumidor.query.get_or_404(consumidor_id)

    total_poluicao = 0
    produtos_selecionados = []

    # Buscar produtos comprados e quantidades
    resultado = db.session.execute(
        consumidor_produto.select().where(
            consumidor_produto.c.consumidor_id == consumidor.id
            )
    ).fetchall()

    for row in resultado:
        produto = Produto.query.get(row.produto_id)
        quantidade = row.quantidade
        total_poluicao += produto.custo_poluicao * quantidade
        produtos_selecionados.append((produto, quantidade))

    return render_template(
        'resumo_compra.html',
        consumidor=consumidor,
        total_poluicao=total_poluicao,
        produtos_selecionados=produtos_selecionados
        )


# Listar consumidores
@app.route('/api/consumidores/', methods=['GET'])
def get_consumidores():
    consumidores = Consumidor.query.all()
    return jsonify([{'id': c.id, 'nome': c.nome} for c in consumidores])


# Criar consumidor
@app.route('/api/consumidores/', methods=['POST'])
def create_consumidor():
    data = request.get_json()
    consumidor = Consumidor(nome=data.get('nome'))
    db.session.add(consumidor)
    db.session.commit()
    return jsonify({'id': consumidor.id, 'nome': consumidor.nome}), 201


# Listar transportadoras
@app.route('/api/transportadoras/', methods=['GET'])
def get_transportadoras():
    transportadoras = Transportadora.query.all()
    return jsonify([{
        'id': t.id,
        'nome': t.nome,
        'co2_km': t.co2_km,
        'eletrica': t.eletrica
    } for t in transportadoras])


# Listar produtores
@app.route('/api/produtores/', methods=['GET'])
def get_produtores():
    produtores = Produtor.query.all()
    return jsonify([{
        'id': p.id,
        'nome': p.nome,
        'consumo_produto': p.consumo_produto,
        'consumo_diario': p.consumo_diario,
        'distancia_km': p.distancia_km,
        'dias_armazenado': p.dias_armazenado
    } for p in produtores])


# Listar produtos
@app.route('/api/produtos/', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    return jsonify([{
        'id': p.id,
        'nome': p.nome,
        'produtor_id': p.produtor_id,
        'transportadora_id': p.transportadora_id,
        'custo_poluicao': p.custo_poluicao
    } for p in produtos])


# Consumidor escolhe produtos
@app.route('/api/consumidores/<int:consumidor_id>/produtos/', methods=['POST'])
def escolher_produtos_api(consumidor_id):
    consumidor = Consumidor.query.get_or_404(consumidor_id)
    data = request.get_json()

    db.session.execute(consumidor_produto.delete().where(
        consumidor_produto.c.consumidor_id == consumidor.id
        ))

    for item in data.get('produtos', []):
        produto_id = item.get('produto_id')
        quantidade = item.get('quantidade', 0)
        if quantidade > 0:
            db.session.execute(consumidor_produto.insert().values(
                consumidor_id=consumidor.id,
                produto_id=produto_id,
                quantidade=quantidade
            ))

    db.session.commit()
    return jsonify({'message': 'Produtos escolhidos com sucesso'}), 201


# Resumo da compra
@app.route('/api/consumidores/<int:consumidor_id>/resumo/', methods=['GET'])
def resumo_compra_api(consumidor_id):
    consumidor = Consumidor.query.get_or_404(consumidor_id)
    total_poluicao = 0
    produtos_selecionados = []

    resultado = db.session.execute(
        consumidor_produto.select().where(
            consumidor_produto.c.consumidor_id == consumidor.id
            )
    ).fetchall()

    for row in resultado:
        produto = Produto.query.get(row.produto_id)
        quantidade = row.quantidade
        total_poluicao += produto.custo_poluicao * quantidade
        produtos_selecionados.append({
            'produto': {
                'id': produto.id,
                'nome': produto.nome,
                'produtor_id': produto.produtor_id,
                'transportadora_id': produto.transportadora_id,
                'custo_poluicao': produto.custo_poluicao
            },
            'quantidade': quantidade
        })

    return jsonify({
        'consumidor': {'id': consumidor.id, 'nome': consumidor.nome},
        'total_poluicao': total_poluicao,
        'produtos_selecionados': produtos_selecionados
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
