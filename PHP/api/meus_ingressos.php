<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

$user_id = $_GET["user_id"] ?? null;

if (!$user_id) {
    echo json_encode([
        "status" => "error",
        "message" => "Usuário não informado"
    ]);
    exit;
}

$sql = "SELECT 
            i.id,
            e.nome_evento AS titulo,
            e.data_evento,
            i.data_compra
        FROM ingressos i
        JOIN eventos e ON i.id_evento = e.id
        WHERE i.id_usuario = :user_id";

$stmt = $conn->prepare($sql);

$stmt->execute([
    ":user_id" => $user_id
]);

$ingressos = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo json_encode([
    "status" => "success",
    "dados" => $ingressos
]);