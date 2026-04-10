<?php

if ($_SESSION["is_admin"] != 1) {
    echo "<p>Apenas admin</p>";
    exit;
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $dados = [
        "user_id" => $_SESSION["user_id"],
        "nome_evento" => $_POST["nome_evento"],
        "descricao" => $_POST["descricao"],
        "data_evento" => $_POST["data_evento"],
        "preco" => $_POST["preco"],
        "imagem" => $_POST["imagem"]
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

<div class="card">
<h2>➕ Criar Evento</h2>

<form method="POST">

<input name="nome_evento" placeholder="Nome" required>
<input name="descricao" placeholder="Descrição" required>
<input name="data_evento" placeholder="YYYY-MM-DD" required>
<input name="preco" placeholder="Preço" required>

<input type="hidden" name="imagem" id="imagem">

<button type="button" onclick="abrirUpload()">📷 Upload</button>
<button type="button" onclick="confirmarImagem()">✔ Confirmar</button>

<p id="status"></p>

<button type="submit">Criar Evento</button>

</form>

<?php if (isset($resultado)) echo "<p>{$resultado["message"]}</p>"; ?>
</div>

<script>
function abrirUpload(){
    window.open("http://localhost/Desafio_Sprint/php/assets/upload.html");
}

function confirmarImagem(){
    fetch("http://localhost/Desafio_Sprint/php/api/feedback_imagem.php")
    .then(res => res.json())
    .then(data => {
        if(data.status === "success"){
            document.getElementById("imagem").value = data.url;
            document.getElementById("status").innerText = "Imagem OK";
        }
    });
}
</script>