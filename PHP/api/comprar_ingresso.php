<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

// 🔥 LER JSON
$data = json_decode(file_get_contents("php://input"), true);

$user_id = $data["user_id"] ?? null;
$evento_id = $data["evento_id"] ?? null;
$pagamento = $data["pagamento"] ?? null;

if (!$user_id || !$evento_id || !$pagamento) {
    echo json_encode([
        "status" => "error",
        "message" => "Dados incompletos",
        "debug" => $data // 👈 ajuda a ver o que chegou
    ]);
    exit;
}

$sql = "SELECT 
            i.id,
            e.nome_evento AS titulo,
            e.data_evento,
            i.data_compra,
            i.codigo_compra,
            i.qr_code,
            i.pagamento,
            i.valor
        FROM ingressos i
        JOIN eventos e ON i.id_evento = e.id
        WHERE i.id_usuario = :user_id
        ORDER BY i.id DESC";

$stmt = $conn->prepare($sql);
$stmt->execute([
    ":user_id" => $user_id
]);

$ingressos = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo json_encode([
    "status" => "success",
    "dados" => $ingressos
]);