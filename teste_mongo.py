from pymongo import MongoClient

# Configuração da conexão com o MongoDB
MONGO_URI = "mongodb://root:senha123@localhost:27017/"
client = MongoClient(MONGO_URI)

# Testar a conexão
try:
    client.server_info()  # Isso verifica se a conexão está funcionando
    print("Conexão bem-sucedida ao MongoDB!")
except Exception as e:
    print(f"Falha na conexão ao MongoDB: {e}")

   
#mongodb://root:senha123@localhost:27017/
