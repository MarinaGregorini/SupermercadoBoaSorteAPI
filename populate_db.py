from models import db, Transportadora, Produtor, Produto
from app import app

with app.app_context():
    db.create_all()

    # Criando Transportadoras
    t1 = Transportadora(nome="EcoTrans", co2_km=0, eletrica=True)
    t2 = Transportadora(nome="FastDelivery", co2_km=738)

    # Criando Produtores
    p1 = Produtor(nome="Fazenda Verde", consumo_produto=2.1, consumo_diario=0.2, distancia_km=100, dias_armazenado=3)
    p2 = Produtor(nome="AgroVida", consumo_produto=1.5, consumo_diario=0.2, distancia_km=70, dias_armazenado=4)
    p3 = Produtor(nome="EcoFrutas", consumo_produto=1.8, consumo_diario=0.1, distancia_km=150, dias_armazenado=2)

    db.session.add_all([t1, t2, p1, p2, p3])
    db.session.commit()

    # Criando Produtos
    produtos = [
        Produto(nome="Maçã A", produtor=p1, transportadora=t1),
        Produto(nome="Maçã B", produtor=p2, transportadora=t2),
        Produto(nome="Maçã C", produtor=p3, transportadora=t1),
        Produto(nome="Laranja A", produtor=p1, transportadora=t2),
        Produto(nome="Laranja B", produtor=p2, transportadora=t1),
        Produto(nome="Laranja C", produtor=p3, transportadora=t2),
        Produto(nome="Banana A", produtor=p1, transportadora=t1),
        Produto(nome="Banana B", produtor=p2, transportadora=t2),
        Produto(nome="Banana C", produtor=p3, transportadora=t1),
    ]

    db.session.add_all(produtos)
    db.session.commit()
