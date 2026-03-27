<?php
header("Content-Type: application/json");
include_once "../config/database.php";

$database = new Database();
$db = $database->getConnection();

$data = json_decode(file_get_contents("php://input"));

if (
    !empty($data->id) &&
    !empty($data->nome_evento) &&
    !empty($data->descricao) &&
    !empty($data->preco)
) {

    $id = $data->id;
    $nome = $data->nome_evento;
    $descricao = $data->descricao;
    $data_evento = $data->data_evento ?? "";
    $preco = $data->preco;
    $imagem = $data->imagem ?? null;

    try {
        if ($imagem) {
            // 🔥 atualiza com imagem
            $query = "UPDATE eventos 
                      SET nome_evento=?, descricao=?, data_evento=?, preco=?, imagem=? 
                      WHERE id=?";
            $stmt = $db->prepare($query);
            $stmt->execute([$nome, $descricao, $data_evento, $preco, $imagem, $id]);
        } else {
            // 🔥 mantém imagem antiga
            $query = "UPDATE eventos 
                      SET nome_evento=?, descricao=?, data_evento=?, preco=? 
                      WHERE id=?";
            $stmt = $db->prepare($query);
            $stmt->execute([$nome, $descricao, $data_evento, $preco, $id]);
        }

        echo json_encode([
            "status" => "success",
            "message" => "Evento atualizado com sucesso"
        ]);

    } catch (Exception $e) {
        echo json_encode([
            "status" => "error",
            "message" => "Erro ao atualizar evento"
        ]);
    }

} else {
    echo json_encode([
        "status" => "error",
        "message" => "Dados incompletos"
    ]);
}
?>