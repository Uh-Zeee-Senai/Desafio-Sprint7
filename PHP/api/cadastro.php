<?php
header("Content-Type: application/json");

$dados = json_decode(file_get_contents("php://input"), true);

$nome = $dados["nome"] ?? null;
$email = $dados["email"] ?? null;
$senha = $dados["senha"] ?? null;

if (!$nome || !$email || !$senha) {
    echo json_encode([
        "status" => "error",
        "message" => "Dados incompletos"
    ]);
    exit;
}

echo json_encode([
    "status" => "success",
    "message" => "Usuário cadastrado com sucesso"
]);