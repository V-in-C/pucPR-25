/*
  Funções para manipulação de jogos
  Chama os arquivos de jogos em python e executa as funções no browser
no formato *.py
  */

function loadGame(gameName) {
    // Verifica se o jogo já está carregado
    if (document.getElementById('gameFrame')) {
        document.getElementById('gameFrame').remove();
    }

    // Cria um novo iframe para o jogo
    const gameFrame = document.createElement('iframe');
    gameFrame.id = 'gameFrame';
    gameFrame.src = `games/${gameName}.py`;
    gameFrame.style.width = '100%';
    gameFrame.style.height = '600px';
    gameFrame.style.border = 'none';

    // Adiciona o iframe ao corpo do documento
    document.body.appendChild(gameFrame);
}
function loadGameList() {
    const games = [
        { name: 'Jogo da Forca', file: 'forca' },
        { name: 'Jogo da Velha', file: 'velha' },
        { name: 'Adivinhação de Números', file: 'adivinhacao' },
        { name: 'Jogo da Memória', file: 'memoria' }
    ];

    const gameList = document.getElementById('gameList');
    gameList.innerHTML = '';

    games.forEach(game => {
        const listItem = document.createElement('li');
        listItem.textContent = game.name;
        listItem.onclick = () => loadGame(game.file);
        gameList.appendChild(listItem);
    });
}
document.addEventListener('DOMContentLoaded', () => {
    loadGameList();
    // Carrega o primeiro jogo por padrão
    if (document.getElementById('gameList').children.length > 0) {
        document.getElementById('gameList').children[0].click();
    }
});
// Adiciona um evento para recarregar a lista de jogos ao clicar no botão
document.getElementById('reloadButton').addEventListener('click', loadGameList);