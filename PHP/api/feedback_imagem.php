<?php
header("Content-Type: application/json");

$arquivo_temp = "../Uploads/ultima_imagem.txt";

if ($_SERVER["REQUEST_METHOD"] === "POST") {

    if (isset($_FILES["imagem"])) {

        $pasta = "../Uploads/";

        if (!is_dir($pasta)) {
            mkdir($pasta, 0777, true);
        }

        $nome = time() . "_" . basename($_FILES["imagem"]["name"]);
        $caminho = $pasta . $nome;

        if (move_uploaded_file($_FILES["imagem"]["tmp_name"], $caminho)) {

            $url = "http://localhost/Desafio_Sprint/PHP/Uploads/" . $nome;

            // 🔥 SALVA A URL
            file_put_contents($arquivo_temp, $url);

            echo json_encode([
                "status" => "success",
                "url" => $url
            ]);
        } else {
            echo json_encode(["status" => "error", "message" => "Erro ao salvar"]);
        }

    } else {
        echo json_encode(["status" => "error", "message" => "Nenhuma imagem"]);
    }

} else {
    // 🔥 GET → retorna última imagem salva
    if (file_exists($arquivo_temp)) {
        $url = file_get_contents($arquivo_temp);

        echo json_encode([
            "status" => "success",
            "url" => $url
        ]);
    } else {
        echo json_encode([
            "status" => "error",
            "message" => "Nenhuma imagem enviada ainda"
        ]);
    }
}