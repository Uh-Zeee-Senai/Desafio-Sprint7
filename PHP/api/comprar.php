<?php
header("Content-Type: application/json");

require_once __DIR__ . "/../config/database.php";

$database = new Database();
$db = $database->getConnection();

$data = json_decode(file_get_contents("php://input"));

if (!empty($data->user_id) && !empty($data->evento_id)) {

    try {

        $db->beginTransaction();

        // Criar pedido
        $query = "INSERT INTO pedidos (id_user) VALUES (:user_id)";
        $stmt = $db->prepare($query);
        $stmt->bindParam(":user_id", $data->user_id);
        $stmt->execute();

        $pedido_id = $db->lastInsertId();

        // Gerar QR único
        $qr_code = uniqid("EVT_");

        // Criar ingresso
        $query = "INSERT INTO ingressos (id_pedido, id_evento, qr_code)
                  VALUES (:pedido_id, :evento_id, :qr_code)";
        $stmt = $db->prepare($query);
        $stmt->bindParam(":pedido_id", $pedido_id);
        $stmt->bindParam(":evento_id", $data->evento_id);
        $stmt->bindParam(":qr_code", $qr_code);
        $stmt->execute();

        $db->commit();

        echo json_encode([
            "status" => "success",
            "qr_code" => $qr_code
        ]);

    } catch (Exception $e) {
        $db->rollBack();
        echo json_encode(["status" => "error", "message" => "Erro na compra"]);
    }

} else {
    echo json_encode(["status" => "error", "message" => "Dados incompletos"]);
}