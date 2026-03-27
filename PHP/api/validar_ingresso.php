<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

$input = json_decode(file_get_contents("php://input"), true);
$qr_code = $input["qr_code"] ?? null;

if (!$qr_code) {
    echo json_encode([
        "status" => "error",
        "message" => "QR Code não informado"
    ]);
    exit;
}

$sql = "SELECT * FROM ingressos WHERE qr_code = :qr";
$stmt = $conn->prepare($sql);
$stmt->execute([":qr" => $qr_code]);

$ingresso = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$ingresso) {
    echo json_encode([
        "status" => "error",
        "message" => "Ingresso inválido"
    ]);
    exit;
}

if ($ingresso["usado"] == 1) {
    echo json_encode([
        "status" => "error",
        "message" => "Ingresso já utilizado"
    ]);
    exit;
}

$sql = "UPDATE ingressos 
        SET usado = 1, data_validacao = NOW()
        WHERE id = :id";

$stmt = $conn->prepare($sql);
$stmt->execute([":id" => $ingresso["id"]]);

echo json_encode([
    "status" => "success",
    "message" => "Entrada liberada ✅"
]);