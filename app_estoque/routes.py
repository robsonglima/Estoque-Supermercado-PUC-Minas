from flask import request, jsonify, render_template
from app_estoque import app, mongo
from bson.objectid import ObjectId
from bson import json_util  # Importe o json_util para converter documentos BSON para JSON

# Conexão com o banco de dados MongoDB
db = mongo.estoque_db
produtos = db['produtos']
movimentos_estoque = db['movimentos_estoque']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/produto', methods=['POST'])
def adicionar_produto():
    dados = request.json
    produto_id = produtos.insert_one(dados).inserted_id
    return jsonify(str(produto_id)), 201

@app.route('/produto/<produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    dados = request.json
    produtos.update_one({'_id': ObjectId(produto_id)}, {'$set': dados})
    return jsonify({'msg': 'Produto atualizado com sucesso'}), 200

@app.route('/api/produtos')
def listar_produtos():
    # Consulta todos os documentos na coleção 'produtos'
    lista_produtos = list(produtos.find())  # Exclui o campo '_id' do resultado
    # Converte os documentos BSON para JSON serializável
    produtos_json = json_util.dumps(lista_produtos)
    return produtos_json

@app.route('/produtos')
def mostrar_estoque():
    return render_template('visualizar_estoque.html'), 200

# Função para obter os movimentos de estoque de acordo com a página e a quantidade de itens por página
def get_movimentos_estoque(page, per_page):
    # Calcula o índice inicial e final dos documentos a serem retornados
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    # Consulta no banco de dados para obter os movimentos de estoque na página atual
    movimentos_estoque = list(movimentos_estoque.find().sort('_id', -1).skip(start_idx).limit(per_page))
    return movimentos_estoque

@app.route('/api/movimentacao')
def listar_movimentacao():
   
    # Consulta todos os documentos na coleção 'movimentacao'
    lista_movimentacao = list(movimentos_estoque.find().sort('_id', -1).limit(20))  # Exclui o campo '_id' do resultado
    # Converte os documentos BSON para JSON serializável
    movimentacao_json = json_util.dumps(lista_movimentacao)
    return movimentacao_json

@app.route('/movimentacao')
def mostrar_movimentacao():
    return render_template('movimentacao.html'), 200

@app.route('/produto/<produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    produtos.delete_one({'_id': ObjectId(produto_id)})
    return jsonify({'msg': 'Produto deletado com sucesso'}), 200

@app.route('/produto/nome/<nome>', methods=['GET'])
def buscar_produto_por_nome(nome):
    produtos_encontrados = list(produtos.find({'nome': {'$regex': nome, '$options': 'i'}}))
    for produto in produtos_encontrados:
        produto['_id'] = str(produto['_id'])
    return jsonify(produtos_encontrados), 200

# @app.route('/visualizar_estoque/<nome>', methods=['GET'])
# def visualizar_estoque_por_produto(nome):
#     movimentos = list(movimentos_estoque.find({'produto': nome}))

#     entradas = sum(mov['quantidade'] for mov in movimentos if mov['tipo'] == 'entrada')
#     saidas = sum(mov['quantidade'] for mov in movimentos if mov['tipo'] == 'saida')

#     estoque_atual = entradas - saidas
   
#     return render_template('visualizar_estoque.html', 
#                            produto={'nome': nome, 'entradas': entradas, 'saidas': saidas, 'estoque_atual': estoque_atual},
#                            movimentos=movimentos)

@app.route('/visualizar_estoque/<nome>', methods=['GET'])
def visualizar_estoque_por_produto(nome,filial):
    pipeline = [
        # Fase de match para filtrar os documentos
        {
        "$match": {
            "filial": filial,
            "produto": nome  
        }
    },
    {
        "$group": {
            "_id": "$produto",
            "estoque_atual": { "$sum": "$quantidade" } 
        }
    }

    ]

    resultado_agregacao = list(movimentos_estoque.aggregate(pipeline))
    estoque_atual = resultado_agregacao[0]['estoque_atual'] if resultado_agregacao else 0

    print("Nome do Produto:", nome)
    print("Estoque Atual:", estoque_atual)

    return render_template('visualizar_estoque.html', 
                           produto={'nome': nome, 'estoque_atual': estoque_atual})


@app.route('/movimento_estoque', methods=['POST'])
def adicionar_movimento_estoque():
    dados = request.json
    movimento_id = movimentos_estoque.insert_one(dados).inserted_id
    return jsonify(str(movimento_id)), 201
