<?php
$id = $_GET["id"] ?? null;

if (!$id) {
    echo "ID inválido";
    exit;
}

// BUSCAR EVENTO
$api = "http://localhost/Desafio_Sprint/php/api/listar_eventos.php";
$dados = json_decode(file_get_contents($api), true);

$evento = null;
foreach ($dados["dados"] as $e) {
    if ($e["id"] == $id) {
        $evento = $e;
        break;
    }
}

if (!$evento) {
    echo "Evento não encontrado";
    exit;
}

// SALVAR
if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $dados = [
        "id" => $id,
        "nome_evento" => $_POST["nome_evento"],
        "descricao" => $_POST["descricao"],
        "data_evento" => $_POST["data_evento"],
        "preco" => $_POST["preco"],
        "imagem" => null
    ];

    $ch = curl_init("http://localhost/Desafio_Sprint/php/api/editar_evento.php");

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($dados));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);

    $response = curl_exec($ch);
    curl_close($ch);

    $res = json_decode($response, true);

    echo "<p>{$res["message"]}</p>";
}
?>

<h2>✏️ Editar Evento</h2>

<form method="POST">
    <input name="nome_evento" value="<?= $evento["nome_evento"] ?>"><br><br>
    <input name="descricao" value="<?= $evento["descricao"] ?>"><br><br>
    <input name="data_evento" value="<?= $evento["data_evento"] ?>"><br><br>
    <input name="preco" value="<?= $evento["preco"] ?>"><br><br>

    <button>Salvar</button>
</form>