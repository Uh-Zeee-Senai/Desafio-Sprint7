<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

$nome = $_POST["nome_evento"] ?? null;
$descricao = $_POST["descricao"] ?? null;
$data = $_POST["data_evento"] ?? null;
$preco = $_POST["preco"] ?? null;

if (!$nome || !$data || !$preco) {
    echo json_encode([
        "status" => "error",
        "message" => "Preencha os campos obrigatórios"
    ]);
    exit;
}

$sql = "INSERT INTO eventos (nome_evento, descricao, data_evento, preco)
        VALUES (:nome, :descricao, :data, :preco)";

$stmt = $conn->prepare($sql);

$stmt->execute([
    ":nome" => $nome,
    ":descricao" => $descricao,
    ":data" => $data,
    ":preco" => $preco
]);

echo json_encode([
    "status" => "success",
    "message" => "Evento criado com sucesso"
]);