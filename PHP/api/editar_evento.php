<?php
header("Content-Type: application/json");
include_once "../config/database.php";

$data = json_decode(file_get_contents("php://input"), true);

$id = $data["id"] ?? null;
$nome = $data["nome_evento"] ?? "";
$descricao = $data["descricao"] ?? "";
$data_evento = $data["data_evento"] ?? "";
$preco = $data["preco"] ?? 0;
$imagem = $data["imagem"] ?? null;

if (!$id) {
    echo json_encode(["status" => "error", "message" => "ID obrigatório"]);
    exit;
}

$database = new Database();
$conn = $database->getConnection();

try {

    // 🔥 Se NÃO enviou imagem → NÃO altera imagem
    if (!empty($data->imagem)) {
        $sql = "UPDATE eventos 
                SET nome_evento=?, descricao=?, data_evento=?, preco=?, imagem=? 
                WHERE id=?";
        $stmt = $conn->prepare($sql);
        $stmt->execute([$nome, $descricao, $data_evento, $preco, $imagem, $id]);
    } else {
        $sql = "UPDATE eventos 
                SET nome_evento=?, descricao=?, data_evento=?, preco=? 
                WHERE id=?";
        $stmt = $conn->prepare($sql);
        $stmt->execute([$nome, $descricao, $data_evento, $preco, $id]);
    }

    echo json_encode([
        "status" => "success",
        "message" => "Evento atualizado com sucesso"
    ]);

} catch (Exception $e) {
    echo json_encode([
        "status" => "error",
        "message" => $e->getMessage()
    ]);
}   