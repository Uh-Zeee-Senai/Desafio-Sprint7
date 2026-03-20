<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

$evento_id = $_GET["evento_id"];

$sql = "SELECT * FROM lotes WHERE id_evento = :id";
$stmt = $conn->prepare($sql);
$stmt->execute([":id" => $evento_id]);

echo json_encode([
    "status" => "success",
    "dados" => $stmt->fetchAll(PDO::FETCH_ASSOC)
]);