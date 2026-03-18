<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

$dados = json_decode(file_get_contents("php://input"), true);

$nome = trim($dados["nome"] ?? "");
$email = trim($dados["email"] ?? "");
$senha = trim($dados["senha"] ?? "");

if (!$nome || !$email || !$senha) {
    echo json_encode([
        "status" => "error",
        "message" => "Dados incompletos"
    ]);
    exit;
}

$senhaHash = password_hash($senha, PASSWORD_DEFAULT);

$sql = "INSERT INTO usuarios (nome, email, senha) VALUES (:nome, :email, :senha)";
$stmt = $conn->prepare($sql);

$stmt->bindParam(":nome", $nome);
$stmt->bindParam(":email", $email);
$stmt->bindParam(":senha", $senhaHash);

if ($stmt->execute()) {

    echo json_encode([
        "status" => "success",
        "message" => "Usuário cadastrado com sucesso"
    ]);

} else {

    echo json_encode([
        "status" => "error",
        "message" => "Erro ao cadastrar"
    ]);

}