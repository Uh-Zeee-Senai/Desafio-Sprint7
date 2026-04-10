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
    curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);

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
<title>Painel AccessPass</title>

<style>
body {
    margin: 0;
    font-family: 'Segoe UI';
    background: #0f172a;
    color: white;
}

/* NAVBAR */
.navbar {
    background: #1e293b;
    padding: 15px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.navbar h1 {
    margin: 0;
    font-size: 20px;
}

.navbar a {
    color: #3b82f6;
    margin-left: 15px;
    text-decoration: none;
}

/* CONTAINER */
.container {
    padding: 30px;
}

/* CARD */
.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
    max-width: 400px;
    margin: auto;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
}

/* INPUT */
input {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    border-radius: 8px;
    border: none;
    background: #0f172a;
    color: white;
}

/* BUTTON */
button {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    border-radius: 8px;
    border: none;
    background: #2563eb;
    color: white;
    cursor: pointer;
}

button:hover {
    background: #1d4ed8;
}

/* GRID */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

/* EVENT CARD */
.event-card {
    background: #1e293b;
    border-radius: 15px;
    overflow: hidden;
}

.event-card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
}

.event-body {
    padding: 15px;
}

.event-body p {
    color: #cbd5f5;
}

/* BUTTONS INLINE */
.actions a {
    margin-right: 10px;
    color: #3b82f6;
    text-decoration: none;
}
</style>

</head>
<body>

<div class="navbar">
    <h1>🎟 AccessPass</h1>

    <?php if(isset($_SESSION["user_id"])): ?>
        <div>
            <a href="?page=eventos">Eventos</a>
            <?php if($_SESSION["is_admin"] == 1): ?>
                <a href="?page=criar">Criar</a>
            <?php endif; ?>
            <a href="?logout=1">Sair</a>
        </div>
    <?php endif; ?>
</div>

<div class="container">

<?php if (!isset($_SESSION["user_id"])): ?>

    <div class="card">
        <h2>Login</h2>

        <form method="POST">
            <input name="email" placeholder="Email" required>
            <input type="password" name="senha" placeholder="Senha" required>
            <button name="login">Entrar</button>
        </form>

        <?php if (isset($erro_login)) echo "<p>$erro_login</p>"; ?>
    </div>

<?php else: ?>

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
    }
    ?>

<?php endif; ?>

</div>

</body>
</html>