<?php
require_once __DIR__ . "/../../config/database.php";
require_once __DIR__ . "/../models/Evento.php";

class EventoController {

    public function index() {
        $database = new Database();
        $db = $database->getConnection();

        $evento = new Evento($db);
        $stmt = $evento->listar();

        $eventos = $stmt->fetchAll(PDO::FETCH_ASSOC);

        require_once __DIR__ . "/../views/eventos/index.php";
    }
}