<?php
$api = "http://localhost/Desafio_Sprint/php/api/listar_eventos.php";
$response = file_get_contents($api);
$dados = json_decode($response, true);
?>

<h2>📅 Eventos</h2>

<div class="grid">

<?php foreach ($dados["dados"] as $e): ?>

<div class="event-card">

    <img src="<?= $e["imagem"] ?>">

    <div class="event-body">
        <h3><?= $e["nome_evento"] ?></h3>
        <p><?= $e["descricao"] ?></p>
        <b>R$ <?= $e["preco"] ?></b>

        <?php if($_SESSION["is_admin"] == 1): ?>
        <div class="actions">
            <a href="?page=editar&id=<?= $e["id"] ?>">✏️ Editar</a>
            <a href="?page=deletar&id=<?= $e["id"] ?>">🗑 Deletar</a>
        </div>
        <?php endif; ?>
    </div>

</div>

<?php endforeach; ?>

</div>