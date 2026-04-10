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
        "imagem" => $_POST["imagem"] ?? null
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
    <input type="hidden" name="imagem" id="imagem">

    <button type="button" onclick="abrirUpload()">📷 Trocar Imagem</button>
    <button type="button" onclick="confirmarImagem()">✔ Confirmar Upload</button>

    <p id="status"></p>

    <button>Salvar</button>
</form>

<script>
function abrirUpload(){
    window.open("http://localhost/Desafio_Sprint/php/assets/upload.html", "_blank");
}

function confirmarImagem(){
    fetch("http://localhost/Desafio_Sprint/php/api/feedback_imagem.php")
    .then(res => res.json())
    .then(data => {
        if(data.status === "success"){
            document.getElementById("imagem").value = data.url;
            document.getElementById("status").innerText = "Imagem atualizada!";
        } else {
            document.getElementById("status").innerText = data.message;
        }
    });
}
</script>