<?php
header("Content-Type: application/json");

// LER JSON DO PYTHON
$dados = json_decode(file_get_contents("php://input"), true);

$email = $dados["email"] ?? null;
$senha = $dados["senha"] ?? null;

if (!$email || !$senha) {
    echo json_encode([
        "status" => "error",
        "message" => "Email ou senha não enviados"
    ]);
    exit;
}

// SIMULA LOGIN (depois você conecta ao banco)
if ($email == "admin@email.com" && $senha == "123") {
    echo json_encode([
        "status" => "success",
        "user_id" => 1
    ]);
} else {
    echo json_encode([
        "status" => "error",
        "message" => "Credenciais inválidas"
    ]);
}