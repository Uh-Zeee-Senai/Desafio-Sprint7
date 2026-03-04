<?php
header("Content-Type: application/json");

require_once __DIR__ . "/../config/database.php";

$database = new Database();
$db = $database->getConnection();

$user_id = $_GET["user_id"] ?? null;

if ($user_id) {

    $query = "SELECT i.qr_code, e.titulo, e.data_evento
              FROM ingressos i
              JOIN pedidos p ON i.id_pedido = p.id_pedido
              JOIN eventos e ON i.id_evento = e.id_evento
              WHERE p.id_user = :user_id";

    $stmt = $db->prepare($query);
    $stmt->bindParam(":user_id", $user_id);
    $stmt->execute();

    $ingressos = $stmt->fetchAll(PDO::FETCH_ASSOC);

    echo json_encode([
        "status" => "success",
        "dados" => $ingressos
    ]);

} else {
    echo json_encode(["status" => "error"]);
}