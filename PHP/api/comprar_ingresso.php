<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

$user_id = $_POST["user_id"] ?? null;
$evento_id = $_POST["evento_id"] ?? null;

if (!$user_id || !$evento_id) {
    echo json_encode([
        "status" => "error",
        "message" => "Dados incompletos"
    ]);
    exit;
}

$sql = "INSERT INTO ingressos (id_usuario, id_evento)
        VALUES (:user_id, :evento_id)";

$stmt = $conn->prepare($sql);

$stmt->execute([
    ":user_id" => $user_id,
    ":evento_id" => $evento_id
]);

echo json_encode([
    "status" => "success",
    "message" => "Ingresso comprado com sucesso"
]);