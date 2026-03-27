<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$data = json_decode(file_get_contents("php://input"), true);

$id = $data["id"] ?? null;
$nome = $data["nome_evento"] ?? "";
$descricao = $data["descricao"] ?? "";
$data_evento = $data["data_evento"] ?? "";
$preco = $data["preco"] ?? "";
$imagem_base64 = $data["imagem"] ?? null;

if (!$id) {
    echo json_encode(["status" => "error", "message" => "ID não informado"]);
    exit;
}

try {
    $database = new Database();
    $db = $database->getConnection();

    // 🔥 Se veio imagem nova
    if ($imagem_base64) {

        $nomeArquivo = "img_" . time() . ".png";
        $caminho = "../uploads/" . $nomeArquivo;

        file_put_contents($caminho, base64_decode($imagem_base64));

        $sql = "UPDATE eventos SET 
                nome_evento = ?, 
                descricao = ?, 
                data_evento = ?, 
                preco = ?, 
                imagem = ?
                WHERE id = ?";

        $stmt = $db->prepare($sql);
        $stmt->execute([$nome, $descricao, $data_evento, $preco, $nomeArquivo, $id]);

    } else {
        // 🔥 Sem imagem (não altera imagem atual)
        $sql = "UPDATE eventos SET 
                nome_evento = ?, 
                descricao = ?, 
                data_evento = ?, 
                preco = ?
                WHERE id = ?";

        $stmt = $db->prepare($sql);
        $stmt->execute([$nome, $descricao, $data_evento, $preco, $id]);
    }

    echo json_encode(["status" => "success", "message" => "Evento atualizado"]);

} catch (Exception $e) {
    echo json_encode(["status" => "error", "message" => $e->getMessage()]);
}