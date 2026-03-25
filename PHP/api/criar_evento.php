<?php
header("Content-Type: application/json");
require_once "../config/database.php";

$conn = Database::getConnection();

// 🔥 LER JSON
$input = json_decode(file_get_contents("php://input"), true);

// 🔥 DADOS
$user_id = $input["user_id"] ?? null;
$nome = $input["nome_evento"] ?? null;
$descricao = $input["descricao"] ?? null;
$data = $input["data_evento"] ?? null;
$preco = $input["preco"] ?? null;
$imagem_base64 = $input["imagem"] ?? "";

// 🔍 VALIDAÇÃO
if (!$user_id || !$nome || !$descricao || !$data || !$preco) {
    echo json_encode([
        "status" => "error",
        "message" => "Dados incompletos"
    ]);
    exit;
}

// 🔥 VERIFICAR ADMIN
$sql = "SELECT is_admin FROM usuarios WHERE id_usuario = :id";
$stmt = $conn->prepare($sql);
$stmt->execute([":id" => $user_id]);

$user = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$user || $user["is_admin"] != 1) {
    echo json_encode([
        "status" => "error",
        "message" => "Apenas admins podem criar eventos"
    ]);
    exit;
}

// 🔥 SALVAR IMAGEM (SE EXISTIR)
$url_imagem = null;

if (!empty($imagem_base64)) {

    // cria pasta uploads se não existir
    $pasta = "../uploads/";
    if (!file_exists($pasta)) {
        mkdir($pasta, 0777, true);
    }

    $nome_arquivo = uniqid() . ".jpg";
    $caminho = $pasta . $nome_arquivo;

    file_put_contents($caminho, base64_decode($imagem_base64));

    // ⚠️ MUDA ISSO QUANDO FOR PUBLICAR
    $url_imagem = "http://localhost/Desafio_Sprint/php/uploads/" . $nome_arquivo;
}

// 🔥 INSERIR EVENTO
try {
    $sql = "INSERT INTO eventos (nome_evento, descricao, data_evento, preco, imagem)
            VALUES (:nome, :descricao, :data, :preco, :imagem)";

    $stmt = $conn->prepare($sql);

    $stmt->execute([
        ":nome" => $nome,
        ":descricao" => $descricao,
        ":data" => $data,
        ":preco" => $preco,
        ":imagem" => $url_imagem
    ]);

    echo json_encode([
        "status" => "success",
        "message" => "Evento criado com sucesso"
    ]);

} catch (Exception $e) {
    echo json_encode([
        "status" => "error",
        "message" => "Erro ao criar evento",
        "erro_real" => $e->getMessage()
    ]);
}