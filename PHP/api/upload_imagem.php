<?php
header("Content-Type: application/json");
session_start();

if(isset($_FILES["imagem"])){

    $pasta = "../Uploads/";

    if(!is_dir($pasta)){
        mkdir($pasta, 0777, true);
    }

    $nome = time() . "_" . basename($_FILES["imagem"]["name"]);
    $caminho = $pasta . $nome;

    if(move_uploaded_file($_FILES["imagem"]["tmp_name"], $caminho)){

        $url = "http://localhost/Desafio_Sprint/Uploads/" . $nome;

        $_SESSION["ultima_imagem"] = $url;

        echo json_encode([
            "status" => "success",
            "url" => $url
        ]);

    } else {
        echo json_encode([
            "status" => "error",
            "message" => "Erro ao salvar"
        ]);
    }

} else {
    echo json_encode([
        "status" => "error",
        "message" => "Nenhuma imagem"
    ]);
}