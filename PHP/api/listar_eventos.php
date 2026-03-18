<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

$sql = "SELECT * FROM eventos ORDER BY data_evento ASC";

$stmt = $conn->prepare($sql);
$stmt->execute();

$eventos = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo json_encode([
    "status" => "success",
    "dados" => $eventos
]);