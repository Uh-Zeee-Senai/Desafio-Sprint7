<?php

if (!isset($_SESSION["user_id"])) {
    echo "Faça login";
    exit;
}

if ($_SESSION["is_admin"] != 1) {
    echo "Apenas admin pode criar";
    exit;
}

$imagem = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $imagem = $_POST["imagem"] ?? "";

    $dados = [
        "user_id" => $_SESSION["user_id"],
        "nome_evento" => $_POST["nome_evento"],
        "descricao" => $_POST["descricao"],
        "data_evento" => $_POST["data_evento"],
        "preco" => $_POST["preco"],
        "imagem" => $imagem
    ];

    $ch = curl_init("http://localhost/Desafio_Sprint/php/api/criar_evento.php");

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($dados));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);

    $response = curl_exec($ch);
    curl_close($ch);

    $resultado = json_decode($response, true);
}
?>

<h1>➕ Criar Evento</h1>

<form method="POST">

    <input name="nome_evento" placeholder="Nome"><br><br>
    <input name="descricao" placeholder="Descrição"><br><br>
    <input name="data_evento" placeholder="Data (YYYY-MM-DD)"><br><br>
    <input name="preco" placeholder="Preço"><br><br>

    <input type="hidden" name="imagem" id="imagem">

    <button type="button" onclick="abrirUpload()">📷 Selecionar Imagem</button>
    <button type="button" onclick="confirmarImagem()">✔ Confirmar Upload</button>

    <p id="status"></p>

    <br>
    <button type="submit">Criar</button>
</form>

<?php
if (isset($resultado)) {
    echo "<p>{$resultado["message"]}</p>";
}
?>

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
            document.getElementById("status").innerText = "Imagem carregada!";
        } else {
            document.getElementById("status").innerText = data.message;
        }
    });
}
</script>