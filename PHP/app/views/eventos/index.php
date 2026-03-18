<h1>🎟️ Painel de Eventos</h1>

<a href="criar.php" style="padding:10px; background:green; color:white;">
    + Novo Evento
</a>

<hr>

<?php foreach($eventos as $e): ?>
    <div style="border:1px solid #ccc; padding:10px; margin:10px;">
        <h3><?= $e['nome_evento'] ?></h3>
        <p><?= $e['descricao'] ?></p>
        <p>📅 <?= $e['data_evento'] ?></p>
        <p>💰 R$ <?= $e['preco'] ?></p>
    </div>
<?php endforeach; ?>