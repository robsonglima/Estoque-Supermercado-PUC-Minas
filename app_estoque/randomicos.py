import pandas as pd
import numpy as np
import random

# Lists of possible values for each column
nomes = [
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
filiais = ["Filial A", "Filial B", "Filial C", "Filial D", "Filial E"]
tipos = ["entrada", "saida"]

# Generate random data
random.seed(0)
data = {
    "nome": np.random.choice(nomes, 1000),
    "preco": np.round(np.random.uniform(1, 100, 1000), 2),
    "quantidade": np.random.randint(1, 50, 1000),
    "filial": np.random.choice(filiais, 1000),
    "tipo": np.random.choice(tipos, 1000)
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV


# Save to CSV
df.to_csv('./DataSets/Estados_Brasileiros.csv', index=False)
df