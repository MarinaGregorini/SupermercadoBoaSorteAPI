from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

consumidor_produto = db.Table('consumidor_produto',
    db.Column('consumidor_id', db.Integer, db.ForeignKey('consumidor.id'), primary_key=True),
    db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'), primary_key=True),
    db.Column('quantidade', db.Integer, nullable=False, default=0)  # Guarda a quantidade escolhida
)

class Transportadora(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    co2_km = db.Column(db.Float, nullable=False)
    eletrica = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Transportadora(nome={self.nome}, co2_km={self.co2_km}, eletrica={self.eletrica})"


class Produtor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    consumo_produto = db.Column(db.Float, nullable=False)
    consumo_diario = db.Column(db.Float, nullable=False)
    distancia_km = db.Column(db.Float, nullable=False)
    dias_armazenado = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Produtor(nome={self.nome}, consumo_produto={self.consumo_produto}, distancia_km={self.distancia_km})"


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    produtor_id = db.Column(db.Integer, db.ForeignKey('produtor.id'), nullable=False)
    transportadora_id = db.Column(db.Integer, db.ForeignKey('transportadora.id'), nullable=False)

    produtor = db.relationship('Produtor', backref=db.backref('produtos', lazy=True))
    transportadora = db.relationship('Transportadora', backref=db.backref('produtos', lazy=True))

    def calcular_poluicao_producao(self):
        poluicao_producao = self.produtor.consumo_produto + (self.produtor.dias_armazenado * self.produtor.consumo_diario)
        return 1 if poluicao_producao <= 2 else 2

    def calcular_poluicao_transporte(self):
        poluicao_transporte = self.produtor.distancia_km * self.transportadora.co2_km
        if self.transportadora.eletrica:
            return 0
        elif poluicao_transporte < 52000:
            return 1
        elif poluicao_transporte < 74000:
            return 2
        return 3

    @property
    def custo_poluicao(self):
        return self.calcular_poluicao_producao() + self.calcular_poluicao_transporte()

    def __repr__(self):
        return f"Produto(nome={self.nome}, produtor={self.produtor.nome}, transportadora={self.transportadora.nome}, custo_poluicao={self.custo_poluicao})"


class Consumidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"Consumidor(nome={self.nome}, id={self.id})"
