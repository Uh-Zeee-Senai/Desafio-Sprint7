<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

$qr = $_POST["qr_code"] ?? null;

if (!$qr) {
    echo json_encode(["status" => "error"]);
    exit;
}

// VERIFICA
$sql = "SELECT * FROM ingressos WHERE qr_code = :qr";
$stmt = $conn->prepare($sql);
$stmt->execute([":qr" => $qr]);

$ingresso = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$ingresso) {
    echo json_encode(["status" => "error", "message" => "Inválido"]);
    exit;
}

if ($ingresso["status"] == "usado") {
    echo json_encode(["status" => "error", "message" => "Já utilizado"]);
    exit;
}

// MARCAR COMO USADO
$conn->prepare("UPDATE ingressos SET status='usado' WHERE id = :id")
     ->execute([":id" => $ingresso["id"]]);

echo json_encode([
    "status" => "success",
    "message" => "Entrada liberada"
]);