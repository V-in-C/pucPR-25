// script.js

// Espera o DOM carregar
document.addEventListener('DOMContentLoaded', () => {
    // Seleciona elementos do index.html
    const main = document.querySelector('main') || document.body;

    // Aplica um fundo moderno usando CSS
    document.body.style.minHeight = '100vh';

    // Adiciona uma foto pessoal centralizada
    const foto = document.createElement('img');
    foto.src = '/Maia/gitpersonal/pucPR-25/imagens/foto.jpg'; // Ajuste o caminho conforme a estrutura do seu projeto
    foto.alt = 'Foto pessoal';
    foto.style.width = '160px';
    foto.style.height = '160px';

    // Cria uma div para a foto no canto superior esquerdo
    const fotoDiv = document.createElement('div');
    fotoDiv.style.position = 'fixed';
    fotoDiv.style.top = '24px';
    fotoDiv.style.left = '24px';
    fotoDiv.style.zIndex = '1000';
    fotoDiv.appendChild(foto);

    document.body.appendChild(fotoDiv);
    foto.style.objectFit = 'cover';
    foto.style.borderRadius = '50%';
    foto.style.marginBottom = '24px';
    main.appendChild(foto);

    // Centraliza todos os parágrafos
    const style = document.createElement('style');
    style.textContent = `
        p {
            text-align: center;
        }
    `;
    document.head.appendChild(style);
    document.body.style.margin = '0';
    document.body.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    document.body.style.fontFamily = 'Segoe UI, Arial, sans-serif';

    // Cria um título
    const titulo = document.createElement('h1');
    titulo.textContent = 'Bem-vindo à Minha Página Web!';
    titulo.style.color = '#fff';
    titulo.style.textShadow = '0 2px 8px rgba(0,0,0,0.2)';

    // Cria um parágrafo
    const paragrafo = document.createElement('p');
    paragrafo.textContent = 'Esta página foi criada dinamicamente usando JavaScript.';
    paragrafo.style.color = '#f3f3f3';

    // Cria um botão
    const botao = document.createElement('button');
    botao.textContent = 'Clique aqui';
    botao.style.padding = '10px 24px';
    botao.style.border = 'none';
    botao.style.borderRadius = '6px';
    botao.style.background = '#fff';
    botao.style.color = '#764ba2';
    botao.style.fontWeight = 'bold';
    botao.style.cursor = 'pointer';
    botao.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
    botao.addEventListener('click', () => {
        alert('Você clicou no botão!');
    });

    // Centraliza o conteúdo
    main.style.display = 'flex';
    main.style.flexDirection = 'column';
    main.style.justifyContent = 'center';
    main.style.alignItems = 'center';
    main.style.minHeight = '100vh';

    // Adiciona os elementos à página
    main.appendChild(titulo);
    main.appendChild(paragrafo);
    main.appendChild(botao);
});