function abrirFormularioContato() {
  const form = document.getElementById('formulario-contato');
  form.classList.remove('hidden');
  form.classList.add('animate-fade-in');
}

function contatar(metodo) {
  const form = document.getElementById('formulario-contato');
  form.classList.add('hidden');
  form.classList.remove('animate-fade-in');

  if (metodo === 'email') {
    window.location.href = 'mailto:victorszmaia@gmail.com?subject=Contato%20do%20site';
  } else if (metodo === 'whatsapp') {
    window.open('https://wa.me/5541991437615?text=Olá,%20vi%20seu%20portfólio%20e%20gostaria%20de%20conversar.', '_blank');
  }
}