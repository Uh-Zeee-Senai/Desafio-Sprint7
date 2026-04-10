<?php
$api = "http://localhost/Desafio_Sprint/php/api/listar_eventos.php";
$response = file_get_contents($api);
$dados = json_decode($response, true);
?>

<h2>📅 Eventos</h2>

<div style="display:flex; flex-wrap:wrap; gap:20px; justify-content:center;">

<?php foreach ($dados["dados"] as $e): ?>

<div style="background:#1e293b; padding:15px; border-radius:10px; width:300px;">

    <img src="<?= $e["imagem"] ?>" style="width:100%; border-radius:10px;"><br><br>

    <b><?= $e["nome_evento"] ?></b><br>
    <?= $e["descricao"] ?><br>
    <b>R$ <?= $e["preco"] ?></b><br><br>

    <a href="?page=editar&id=<?= $e["id"] ?>">✏️ Editar</a> |
    <a href="?page=deletar&id=<?= $e["id"] ?>" onclick="return confirm('Excluir?')">🗑 Deletar</a>

</div>

<?php endforeach; ?>

</div>