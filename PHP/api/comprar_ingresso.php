<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

// 🔥 RECEBE JSON
$data = json_decode(file_get_contents("php://input"), true);

$user_id = $data["user_id"] ?? null;
$evento_id = $data["evento_id"] ?? null;
$pagamento = $data["pagamento"] ?? null;

if (!$user_id || !$evento_id || !$pagamento) {
    echo json_encode([
        "status" => "error",
        "message" => "Dados incompletos",
        "debug" => $data
    ]);
    exit;
}

try {

    // 🔹 GERAR CODIGO
    $codigo = uniqid("ING_");

    // 🔹 QR (TEXTO)
    $qr_code = $codigo . "|" . $evento_id;

    // 🔹 PEGAR PREÇO
    $sql_evento = "SELECT preco FROM eventos WHERE id = :id";
    $stmt = $conn->prepare($sql_evento);
    $stmt->execute([":id" => $evento_id]);
    $evento = $stmt->fetch(PDO::FETCH_ASSOC);

    $valor = $evento["preco"] ?? 0;

    // 🔹 INSERT
    $sql = "INSERT INTO ingressos 
    (id_usuario, id_evento, qr_code, codigo_compra, pagamento, valor)
    VALUES (:user, :evento, :qr, :codigo, :pagamento, :valor)";

    $stmt = $conn->prepare($sql);

    $stmt->execute([
        ":user" => $user_id,
        ":evento" => $evento_id,
        ":qr" => $qr_code,
        ":codigo" => $codigo,
        ":pagamento" => $pagamento,
        ":valor" => $valor
    ]);

    echo json_encode([
        "status" => "success",
        "message" => "Compra realizada com sucesso",
        "codigo" => $codigo
    ]);

} catch (Exception $e) {

    echo json_encode([
        "status" => "error",
        "message" => "Erro ao salvar",
        "erro_real" => $e->getMessage()
    ]);
}