<?php
header("Content-Type: application/json");

require_once __DIR__ . "/../config/database.php";
require_once __DIR__ . "/../app/models/Evento.php";

$database = new Database();
$db = $database->getConnection();

$evento = new Evento($db);
$stmt = $evento->listar();

$eventos = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo json_encode([
    "status" => "success",
    "dados" => $eventos
]);