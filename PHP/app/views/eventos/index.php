<?php
?>

<!DOCTYPE html>
<html>
<head>
    <title>Painel de Eventos</title>
</head>
<body>

<h1>🎟 Sistema de Eventos</h1>

<h2>Criar Evento</h2>

<form action="php/api/criar_evento.php" method="POST">
    <input type="text" name="nome_evento" placeholder="Nome"><br><br>
    <input type="text" name="descricao" placeholder="Descrição"><br><br>
    <input type="text" name="data_evento" placeholder="Data"><br><br>
    <input type="text" name="preco" placeholder="Preço"><br><br>

    <button type="submit">Criar</button>
</form>

<hr>

<h2>Eventos</h2>

<?php
$dados = file_get_contents("php/api/listar_eventos.php");
$eventos = json_decode($dados, true);

foreach($eventos["dados"] as $e){
    echo "<p>";
    echo "<b>".$e["nome_evento"]."</b><br>";
    echo $e["descricao"]."<br>";
    echo "R$ ".$e["preco"]."<br>";
    echo "</p><hr>";
}
?>

</body>
</html>