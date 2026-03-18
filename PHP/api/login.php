<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

$data = json_decode(file_get_contents("php://input"), true);

$email = trim($data["email"] ?? "");
$senha = trim($data["senha"] ?? "");

$sql = "SELECT id_usuario, senha, is_admin FROM usuarios WHERE email = :email";
$stmt = $conn->prepare($sql);
$stmt->bindParam(":email", $email);
$stmt->execute();

$user = $stmt->fetch(PDO::FETCH_ASSOC);

if ($user) {

    if (password_verify($senha, $user["senha"])) {

        echo json_encode([
            "status" => "success",
            "user_id" => $user["id_usuario"],
            "is_admin" => $user["is_admin"]
        ]);

    } else {

        echo json_encode([
            "status" => "error",
            "message" => "Credenciais inválidas"
        ]);
    }

} else {

    echo json_encode([
        "status" => "error",
        "message" => "Usuário não encontrado"
    ]);
}