<?php
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Painel de Eventos</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            margin: 0;
            text-align: center;
        }

        header {
            background: #2563eb;
            padding: 20px;
            font-size: 24px;
            font-weight: bold;
        }

        .container {
            width: 90%;
            max-width: 900px;
            margin: 30px auto;
        }

        .card {
            background: #1e293b;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.4);
        }

        input {
            width: 90%;
            padding: 10px;
            margin: 8px 0;
            border-radius: 8px;
            border: none;
        }

        button {
            padding: 10px 20px;
            background: #2563eb;
            border: none;
            border-radius: 10px;
            color: white;
            cursor: pointer;
            transition: 0.3s;
        }

        button:hover {
            background: #1d4ed8;
        }

        .evento {
            text-align: left;
            padding: 10px;
            border-bottom: 1px solid #334155;
        }

        .titulo {
            font-size: 18px;
            font-weight: bold;
        }

        .preco {
            color: #22c55e;
        }
    </style>
</head>

<body>

<header>
    🎟 Sistema de Eventos
</header>

<div class="container">

    <!-- CRIAR EVENTO -->
    <div class="card">
        <h2>➕ Criar Evento</h2>

        <form action="PHP/api/criar_evento.php" method="POST">
            <input type="text" name="nome_evento" placeholder="Nome do evento" required><br>
            <input type="text" name="descricao" placeholder="Descrição" required><br>
            <input type="text" name="data_evento" placeholder="Data" required><br>
            <input type="text" name="preco" placeholder="Preço" required><br>

            <button type="submit">Criar Evento</button>
        </form>
    </div>

    <!-- LISTA DE EVENTOS -->
    <div class="card">
        <h2>📅 Eventos</h2>

        <?php
        $dados = file_get_contents("PHP/api/listar_eventos.php");
        $eventos = json_decode($dados, true);

        if(isset($eventos["dados"])){
            foreach($eventos["dados"] as $e){
                echo "<div class='evento'>";
                echo "<div class='titulo'>".$e["nome_evento"]."</div>";
                echo "<div>".$e["descricao"]."</div>";
                echo "<div class='preco'>R$ ".$e["preco"]."</div>";
                echo "</div>";
            }
        } else {
            echo "<p>Erro ao carregar eventos</p>";
        }
        ?>
    </div>

</div>

</body>
</html>