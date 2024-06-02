# Exemplo de script para gerar README.md automaticamente

def gerar_readme():
    nome_projeto = "Projeto Final - Estoque Supermercado "
    descricao = "Projeto tem o objetivo de demonstrar a escalabilidade e facilidades relacionadas ao MongoDB. Com esse projeto e possivel crar um base de dado tandomicos e visualizar no frontpage."

    conteudo = f"""
    # {nome_projeto}

    {descricao}

    ## Instalação

    Para instalar as dependências do projeto, execute o seguinte comando:

    ```
    pip install -r requirements.txt
    ```

    ## Configuração

    Certifique-se de configurar corretamente as variáveis de ambiente antes de executar o projeto.

    ## Uso
    Recomenda-se a utilizacao de VirtualEnvs.
    Apos as lib instaladas, executar o arquivo run.py
    Ativar MongoDB e conectar na porta 27017
    Iniciar o flask: python run.py
    Acessar o site http://localhost:5000/
    Para criar o banco de dados, collections e popula-los, basta rodar os seguintes scripts:
        entradas.py
        saidas_em_massa.py
        saida_entrada_em_massa.py

    
    ## Contribuições

    Contribuições são bem-vindas! Para contribuir:

    1. Faça um fork do projeto
    2. Crie uma branch com suas modificações (`git checkout -b feature/nova-feature`)
    3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
    4. Faça push para a branch (`git push origin feature/nova-feature`)
    5. Abra um Pull Request

    ## Licença

    Este projeto está licenciado sob a MIT Open Source. Veja o arquivo LICENSE.md para mais detalhes.
    """

    with open('README.md', 'w', encoding='utf-8') as arquivo:
        arquivo.write(conteudo)

if __name__ == "__main__":
    gerar_readme()