// Variável global para armazenar os dados dos jogos carregados do JSON
let dadosBanco = [];

// 1. Carrega o JSON assim que o ficheiro é lido pelo navegador
fetch('../Search_Bib.py/Bib_jogos_data.json')
    .then(response => response.json())
    .then(data => {
        dadosBanco = data.jogos;
    })
    .catch(error => console.error('Erro ao carregar o ficheiro JSON:', error));

// 2. Função de Autocompletar (chamada sempre que o utilizador digita uma letra)
function filtrarJogos() {
    const input = document.getElementById("input-pesquisa").value.toLowerCase();
    const listaSugestoes = document.getElementById("lista-sugestoes");
    
    // Limpa a lista anterior
    listaSugestoes.innerHTML = ''; 
    
    // Se o campo de pesquisa estiver vazio, oculta a lista e para a execução
    if (input === '') {
        listaSugestoes.classList.add('oculto');
        return;
    }

    // Filtra os jogos que contêm o que foi digitado no nome
    const resultados = dadosBanco.filter(jogo => jogo.nome.toLowerCase().includes(input));

    // Se houver resultados, mostra a lista e cria os itens (<li>)
    if (resultados.length > 0) {
        listaSugestoes.classList.remove('oculto');
        
        resultados.forEach(jogo => {
            const li = document.createElement('li');
            li.textContent = jogo.nome;
            
            // Quando o utilizador clica numa das sugestões da lista:
            li.onclick = function() {
                document.getElementById("input-pesquisa").value = jogo.nome; // Preenche a barra
                listaSugestoes.classList.add('oculto'); // Esconde a lista
                carregarJogo(); // Carrega os dados do jogo automaticamente
            };
            
            listaSugestoes.appendChild(li);
        });
    } else {
        // Se não encontrar nada, oculta a lista
        listaSugestoes.classList.add('oculto');
    }
}

// 3. Função para injetar os dados no HTML e mostrar a página do jogo
function carregarJogo() {
    const nomeBuscado = document.getElementById("input-pesquisa").value.toLowerCase();
    
    // Procura o jogo exato no banco de dados
    const jogoEncontrado = dadosBanco.find(jogo => jogo.nome.toLowerCase() === nomeBuscado);

    if (jogoEncontrado) {
        // Preenche os dados visuais (textos e imagem)
        document.getElementById("titulo-jogo").innerText = jogoEncontrado.nome;
        document.getElementById("img-capa").src = jogoEncontrado.capa;
        document.getElementById("tags-jogo").innerHTML = jogoEncontrado.tags;
        document.getElementById("texto-sinopse").innerText = jogoEncontrado.sinopse;
        
        // Preenche os preços
        document.getElementById("preco-xbox").innerText = jogoEncontrado.precos.xbox;
        document.getElementById("preco-playstation").innerText = jogoEncontrado.precos.playstation;
        document.getElementById("preco-steam").innerText = jogoEncontrado.precos.steam;

        // Mostra o conteúdo da página e garante que a lista de sugestões está escondida
        document.getElementById("conteudo-jogo").classList.remove('oculto');
        document.getElementById("lista-sugestoes").classList.add('oculto');
    } else {
        alert("Jogo não encontrado no banco de dados. Verifique se o nome está correto.");
    }
}