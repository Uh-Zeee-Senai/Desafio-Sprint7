<h2>Lista de Eventos</h2>

<?php foreach($eventos as $e): ?>
    <p>
        <?= $e['titulo'] ?> -
        R$ <?= $e['preco'] ?> -
        <?= $e['data_evento'] ?>
    </p>
<?php endforeach; ?>