document.addEventListener('DOMContentLoaded', () => {
    const productForm = document.getElementById('productForm');
    const productList = document.getElementById('productList');
    const productIdField = document.getElementById('productId');
    const nomeField = document.getElementById('produto');
    const precoField = document.getElementById('preco');
    const quantidadeField = document.getElementById('estoque');
    const filialField = document.getElementById('filial');
    const tipoSelect = document.getElementById('tipo');

    // Função para carregar os produtos
    function loadProducts() {
        fetch('/movimentos_estoque')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar produtos');
                }
              
                return response.json();
            })
            .then(products => {
                if (!Array.isArray(products)) {
                    throw new Error('Dados inválidos recebidos do servidor');
                }
                productList.innerHTML = '';
                const latestProducts = products.slice(-2);
                latestProducts.forEach(product => {
                    const li = document.createElement('li');
                    const precoFloat = parseFloat(product.preco).toFixed(2);
                    li.innerHTML = `
                        <div>
                            <span><strong>Nome:</strong> ${sanitizeHTML(product.produto)}</span><br>
                            <span><strong>Preço:</strong> ${precoFloat}</span><br>
                            <span><strong>estoque:</strong> ${sanitizeHTML(product.estoque)}</span><br>
                            <span><strong>Filial:</strong> ${sanitizeHTML(product.filial)}</span>
                        </div>
                        <div>
                            <button onclick="editProduct('${sanitizeHTML(product._id)}', '${sanitizeHTML(product.produto)}', '${precoFloat}', '${sanitizeHTML(product.estoque)}', '${sanitizeHTML(product.filial)}')">Editar</button>
                            <button onclick="deleteProduct('${sanitizeHTML(product._id)}')" class="delete">Deletar</button>
                           
                        </div>
                    `;
                    productList.appendChild(li);
                });
            })
            .catch(error => console.error('Erro ao carregar produtos:', error));
    }
    
    // Função para sanitizar HTML (prevenir injeção de scripts)
    function sanitizeHTML(value) {
        const div = document.createElement('div');
        div.innerText = value;
        return div.innerHTML;
    }
    
    // function loadProducts() {
    //     fetch('/produtos')
    //         .then(response => {
    //             if (!response.ok) {
    //                 throw new Error('Erro ao carregar produtos');
    //             }
    //             return response.json();
    //         })
    //         .then(products => {
    //             productList.innerHTML = '';
    //             // Seleciona os últimos 5 produtos
    //             const latestProducts = products.slice(-2);
    //             latestProducts.forEach(product => {
    //                 const li = document.createElement('li');
    //                 // Converte o preço para float e garante duas casas decimais
    //                 const precoFloat = parseFloat(product.preco).toFixed(2);
    //                 li.innerHTML = `
    //                     <div>
    //                         <span><strong>Nome:</strong> ${product.nome}</span><br>
    //                         <span><strong>Preço:</strong> ${precoFloat}</span><br>
    //                         <span><strong>estoque:</strong> ${product.estoque}</span><br>
    //                         <span><strong>Filial:</strong> ${product.filial}</span>
    //                     </div>
    //                     <div>
    //                         <button onclick="editProduct('${product._id}', '${product.nome}', '${precoFloat}', '${product.estoque}', '${product.filial}')">Editar</button>
    //                         <button onclick="deleteProduct('${product._id}')" class="delete">Deletar</button>
    //                         <button onclick="viewStock('${product.nome}')">Visualizar Estoque</button>
    //                     </div>
    //                 `;
    //                 productList.appendChild(li);
    //             });
    //         })
    //         .catch(error => console.error('Erro ao carregar produtos:', error));
    // }
    
    
    // Função para enviar o formulário de produto
    function submitForm(event) {
        event.preventDefault();
        const productId = productIdField.value;
        const produto = nomeField.value;
        const preco = parseFloat(precoField.value).toFixed(2);
        const estoque = parseInt(quantidadeField.value); // Converter para inteiro
        const filial = filialField.value;
        const tipo = tipoSelect.value;
    
        const url = productId ? `/produto/${productId}` : '/produto';
        const method = productId ? 'PUT' : 'POST';
    
        fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ produto, preco, estoque, filial, tipo })
        }).then(response => {
            if (!response.ok) {
                throw new Error('Erro ao salvar produto');
            }
            return response.json();
        }).then(data => {
            console.log('Produto salvo:', data);
            // Após salvar o produto, salva o movimento de estoque
            if (tipo) {
                adicionarMovimentoEstoque(data._id, produto, estoque, tipo);
            }
            loadProducts();  // Recarrega a lista de produtos após salvar
        }).catch(error => {
            console.error('Erro ao salvar produto:', error);
        });
    
        // Limpa os campos do formulário após a submissão
        productIdField.value = '';
        nomeField.value = '';
        precoField.value = '';
        quantidadeField.value = '';
        filialField.value = '';
        tipoSelect.value = '';
    }
    

    // Função para adicionar um movimento de estoque
    function adicionarMovimentoEstoque(produtoId, produto, estoque, tipo) {
        fetch('/movimento_estoque', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ produto: produtoId, produto, estoque, tipo })
        }).then(response => {
            if (!response.ok) {
                throw new Error('Erro ao adicionar movimento de estoque');
            }
            console.log('Movimento de estoque adicionado com sucesso.');
        }).catch(error => {
            console.error('Erro ao adicionar movimento de estoque:', error);
        });
    }

    // Função para editar um produto
    window.editProduct = (id, produto, preco, estoque, filial) => {
        productIdField.value = id;
        nomeField.value = produto;
        precoField.value = preco;
        quantidadeField.value = estoque;
        filialField.value = filial;
    };

    // Função para deletar um produto
    // Função para deletar um produto pelo ID
    window.deleteProduct = (id) => {
        console.log('Deleting product with ID:', id);  // Linha de depuração
        fetch(`/produto/${id}`, { method: 'DELETE' })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao deletar produto');
                }
                loadProducts();  // Recarrega a lista de produtos após deletar
            })
            .catch(error => console.error('Erro ao deletar produto:', error));
    };
    


    // Função para visualizar o estoque por produto
    window.viewStock = (nomeProduto) => {
        window.location.href = `/visualizar_estoque/${nomeProduto}`;
    };

    // Carrega os produtos ao carregar a página inicial
    loadProducts();

    // Adiciona o listener de evento para o formulário de produto
    productForm.addEventListener('submit', submitForm);
});
