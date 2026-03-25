<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

$input = json_decode(file_get_contents("php://input"), true);

$id = $input["id"] ?? null;

if (!$id) {
    echo json_encode(["status" => "error", "message" => "ID não informado"]);
    exit;
}

$sql = "DELETE FROM eventos WHERE id = :id";
$stmt = $conn->prepare($sql);
$stmt->execute([":id" => $id]);

echo json_encode(["status" => "success", "message" => "Evento deletado"]);