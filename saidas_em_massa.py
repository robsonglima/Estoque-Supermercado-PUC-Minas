import random
import time
from app_estoque import  mongo
import threading

# Conexão com o banco de dados MongoDB
db = mongo.estoque_db
movimentos_estoque = db.movimentos_estoque
produtos = db.produtos  # Tabela de produtos

# # Listas de valores possíveis
nomes =nomes = [
    "Arroz", "Feijão", "Açúcar", "Sal", "Café", "Macarrão", "Farinha", "Óleo", "Leite", "Manteiga", 
    "Pão", "Carne", "Frango", "Peixe", "Ovos", "Queijo", "Presunto", "Iogurte", "Sorvete", "Biscoito",
    "Chocolate", "Chá", "Refrigerante", "Suco", "Água", "Cerveja", "Vinho", "Vodka", "Whisky", "Gin",
    "Detergente", "Sabão em Pó", "Amaciante", "Água Sanitária", "Desinfetante", "Sabonete", "Shampoo", "Condicionador", "Creme Dental", "Escova de Dentes",
    "Papel Higiênico", "Guardanapo", "Esponja", "Papel Toalha", "Lâmina de Barbear", "Desodorante", "Perfume", "Hidratante", "Protetor Solar", "Repelente",
    "Arroz Integral", "Feijão Preto", "Açúcar Mascavo", "Sal Marinho", "Café Orgânico", "Macarrão Integral", "Farinha de Trigo Integral", "Óleo de Coco", "Leite Desnatado", "Manteiga Ghee",
    "Pão Integral", "Carne Moída", "Filé de Frango", "Salmão", "Ovos Orgânicos", "Queijo Cottage", "Peito de Peru", "Iogurte Grego", "Açaí", "Biscoito Integral",
    "Chocolate Amargo", "Chá Verde", "Refrigerante Diet", "Suco Natural", "Água de Coco", "Cerveja Artesanal", "Vinho Tinto", "Vodka Importada", "Whisky 12 Anos", "Gin Importado",
    "Detergente Neutro", "Sabão Líquido", "Amaciante Concentrado", "Água Sanitária Perfumada", "Desinfetante Herbal", "Sabonete Líquido", "Shampoo Anticaspa", "Condicionador Hidratante", "Creme Dental Clareador", "Escova de Dentes Elétrica",
    "Papel Higiênico Folha Dupla", "Guardanapo de Tecido", "Esponja Antiaderente", "Papel Toalha Absorvente", "Lâmina de Barbear Descartável", "Desodorante Roll-on", "Perfume Importado", "Hidratante Corporal", "Protetor Solar Facial", "Repelente Natural"
]

filiais = [
    "Filial A", "Filial B", "Filial C", "Filial D", "Filial E"
]

tipos = ["saida", ]


def verificar_estoque(filial, produto):
    # Consulta o banco de dados para obter o estoque atual do produto na filial
    resultado = produtos.find_one({'filial': filial, 'produto': produto})
    if resultado:
        return resultado['estoque']
    else:
        return 0 
def atualizar_estoque(filial, produto, tipo, estoque):
    # Atualiza o estoque do produto na filial
    estoque_atual = verificar_estoque(filial, produto)
    if tipo == 'saída':
        estoque_atual -= estoque
    elif tipo == 'entrada':
        estoque_atual += estoque

    # Atualiza a tabela de produtos
    produtos.update_one({'filial': filial, 'produto': produto}, {'$set': {'estoque': estoque_atual}}, upsert=True)

def simular_caixa_entradas(caixa_id):
    while True:
        produto = random.choice(nomes)
        filial = random.choice(filiais)
        tipo = random.choice(tipos)
        quantidade = random.randint(1, 10)
        preco = round(random.uniform(10, 15), 2)

        # Verifica se há estoque disponível para a saída
        if tipo == 'saída':
            estoque_atual = verificar_estoque(filial, produto)
            if estoque_atual < quantidade:
                print(f"Não há estoque suficiente de {produto} na {filial}. Saída não realizada no caixa {caixa_id}.")
                continue

        # Insere o movimento na tabela movimentos_estoque
        movimento = {
            'produto': produto,
            'filial': filial,
            'tipo': tipo,
            'quantidade': quantidade,
            'preco': preco  # Adicionando o preço ao movimento de estoque
        }
        movimentos_estoque.insert_one(movimento)

        atualizar_estoque(filial, produto, tipo, quantidade)

        print(f"Registro inserido no caixa {caixa_id}: {movimento}")

        time.sleep(0.00000006)

if __name__ == "__main__":
    num_caixas = 5
    threads = []

    for i in range(num_caixas):
        thread = threading.Thread(target=simular_caixa_entradas, args=(i + 1,))
        threads.append(thread)
        thread.start()

    # Aguarda todas as threads terminarem
    for thread in threads:
        thread.join()
        simular_caixa_entradas()