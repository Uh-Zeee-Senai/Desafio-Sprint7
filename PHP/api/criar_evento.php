<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

$user_id = $_POST["user_id"] ?? null;
$nome = $_POST["nome_evento"] ?? null;
$descricao = $_POST["descricao"] ?? null;
$data = $_POST["data_evento"] ?? null;
$preco = $_POST["preco"] ?? null;

// 🔒 VERIFICA ADMIN
$sql = "SELECT is_admin FROM usuarios WHERE id_usuario = :id";
$stmt = $conn->prepare($sql);
$stmt->execute([":id" => $user_id]);
$user = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$user || $user["is_admin"] != 1) {
    echo json_encode([
        "status" => "error",
        "message" => "Apenas admins podem criar eventos"
    ]);
    exit;
}

// VALIDAÇÃO
if (!$nome || !$data || !$preco) {
    echo json_encode([
        "status" => "error",
        "message" => "Preencha os campos obrigatórios"
    ]);
    exit;
}

// INSERT
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