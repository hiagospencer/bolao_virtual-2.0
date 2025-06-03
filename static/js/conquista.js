function exibirConquista(conquista) {
  document.getElementById('conquista-nome').innerText = conquista.nome;
  document.getElementById('conquista-descricao').innerText =
    conquista.descricao;
  document.getElementById('conquista-xp').innerText = `⭐ XP: +${conquista.xp}`;
  document.getElementById(
    'conquista-moedas',
  ).innerText = `🪙 Moedas: +${conquista.moedas}`;

  document.getElementById('conquista-unlocked').classList.remove('hidden');
}

function fecharConquista() {
  document.getElementById('conquista-unlocked').classList.add('hidden');
}
