<?php

// BLOQUEIO DE ACESSO
if (!isset($_SESSION["user_id"])) {
    echo "Faça login primeiro";
    exit;
}

if ($_SESSION["is_admin"] != 1) {
    echo "Apenas admin pode criar eventos";
    exit;
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $dados = [
        "user_id" => $_SESSION["user_id"],
        "nome_evento" => $_POST["nome_evento"] ?? "",
        "descricao" => $_POST["descricao"] ?? "",
        "data_evento" => $_POST["data_evento"] ?? "",
        "preco" => $_POST["preco"] ?? "",
        "imagem" => ""
    ];

    $ch = curl_init("http://localhost/Desafio_Sprint/php/api/criar_evento.php");

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($dados));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Content-Type: application/json"
    ]);

    $response = curl_exec($ch);

    if ($response === false) {
        echo "Erro cURL: " . curl_error($ch);
    }

    curl_close($ch);

    $resultado = json_decode($response, true);
}
?>

<h1>➕ Criar Evento</h1>

<form method="POST">
    <input type="text" name="nome_evento" placeholder="Nome" required><br><br>
    <input type="text" name="descricao" placeholder="Descrição" required><br><br>
    <input type="text" name="data_evento" placeholder="Data" required><br><br>
    <input type="text" name="preco" placeholder="Preço" required><br><br>

    <button type="submit">Criar</button>
</form>

<?php
if (isset($resultado)) {
    echo "<pre>";
    print_r($resultado);
    echo "</pre>";
}   
?>