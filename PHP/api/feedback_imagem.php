<?php
header("Content-Type: application/json");

session_start();

if(isset($_SESSION["ultima_imagem"])){
    echo json_encode([
        "status" => "success",
        "url" => $_SESSION["ultima_imagem"]
    ]);
} else {
    echo json_encode([
        "status" => "error",
        "message" => "Nenhuma imagem enviada"
    ]);
}