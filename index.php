<?php
session_start();

$page = $_GET['page'] ?? 'eventos';

// LOGIN VIA API
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["login"])) {

    $dados = [
        "email" => $_POST["email"],
        "senha" => $_POST["senha"]
    ];

    $ch = curl_init("http://localhost/Desafio_Sprint/php/api/login.php");

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($dados));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Content-Type: application/json"
    ]);

    $response = curl_exec($ch);
    curl_close($ch);

    $res = json_decode($response, true);

    if ($res["status"] == "success") {
        $_SESSION["user_id"] = $res["user_id"];
        $_SESSION["is_admin"] = $res["is_admin"];
    } else {
        $erro_login = $res["message"];
    }
}

// LOGOUT
if (isset($_GET["logout"])) {
    session_destroy();
    header("Location: index.php");
    exit;
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Painel de Eventos</title>

    <style>
        img {
            height: 150px;
            object-fit: cover;
        }

        .card:hover {
            transform: scale(1.02);
            transition: 0.2s;
        }
        body {
            background: #0f172a;
            color: white;
            font-family: Arial;
            text-align: center;
        }

        .card {
            background: #1e293b;
            padding: 20px;
            border-radius: 15px;
            width: 350px;
            margin: 20px auto;
        }

        input {
            width: 90%;
            padding: 10px;
            margin: 5px;
            border-radius: 8px;
            border: none;
        }

        button {
            background: #2563eb;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            width: 95%;
        }

        a {
            color: #3b82f6;
            margin: 10px;
            text-decoration: none;
        }

        .erro {
            color: red;
        }
    </style>
</head>

<body>

<h1>🎟 Painel Admin</h1>

<?php if (!isset($_SESSION["user_id"])): ?>

    <!-- LOGIN -->
    <div class="card">
        <h2>Login</h2>

        <form method="POST">
            <input type="text" name="email" placeholder="Email" required>
            <input type="password" name="senha" placeholder="Senha" required>
            <button name="login">Entrar</button>
        </form>

        <?php if (isset($erro_login)) echo "<p class='erro'>$erro_login</p>"; ?>
    </div>

<?php else: ?>

    <p>Logado como ID: <?= $_SESSION["user_id"] ?></p>

    <a href="?page=eventos">Eventos</a> |
    <a href="?page=criar">Criar Evento</a> |
    <a href="?logout=1">Sair</a>

    <hr>

    <?php
    switch ($page) {

        case 'eventos':
            require __DIR__ . '/PHP/app/views/eventos.php';
            break;

        case 'criar':
            require __DIR__ . '/PHP/app/views/criar.php';
            break;

        case 'editar':
            require __DIR__ . '/PHP/app/views/editar.php';
            break;

        case 'deletar':
            $id = $_GET["id"] ?? null;

            if ($id) {
                $ch = curl_init("http://localhost/Desafio_Sprint/php/api/deletar_evento.php");

                curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch, CURLOPT_POST, true);
                curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(["id" => $id]));
                curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);

                curl_exec($ch);
                curl_close($ch);
            }

            header("Location: index.php?page=eventos");
            break;

        default:
            echo "Página não encontrada";
    }
    ?>

<?php endif; ?>

</body>
</html>