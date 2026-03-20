<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

$data = json_decode(file_get_contents("php://input"), true);
$qr = $data["qr_code"] ?? null;

if (!$qr) {
    echo json_encode([
        "status" => "error",
        "message" => "QR não informado"
    ]);
    exit;
}

// 🔎 BUSCAR INGRESSO
$sql = "SELECT * FROM ingressos WHERE qr_code = :qr";
$stmt = $conn->prepare($sql);
$stmt->execute([":qr" => $qr]);

$ingresso = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$ingresso) {
    echo json_encode([
        "status" => "error",
        "message" => "Ingresso inválido"
    ]);
    exit;
}

// 🔴 JÁ USADO
if ($ingresso["status"] == "usado") {
    echo json_encode([
        "status" => "error",
        "message" => "Ingresso já utilizado"
    ]);
    exit;
}

// ✅ MARCAR COMO USADO
$sql = "UPDATE ingressos SET status = 'usado' WHERE id = :id";
$stmt = $conn->prepare($sql);
$stmt->execute([":id" => $ingresso["id"]]);

echo json_encode([
    "status" => "success",
    "message" => "Entrada liberada"
]);