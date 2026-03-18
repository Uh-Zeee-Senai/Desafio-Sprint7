CREATE DATABASE IF NOT EXISTS cadastro_eventos
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE cadastro_eventos;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_evento VARCHAR(255) NOT NULL,
    descricao TEXT,
    data_evento DATE NOT NULL,
    preco DECIMAL(10,2) NOT NULL
);

CREATE TABLE  IF NOT EXISTS ingressos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_evento INT NOT NULL,
    data_compra DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_evento) REFERENCES eventos(id) ON DELETE CASCADE
);

INSERT INTO usuarios (nome, email, senha)
VALUES (
    'Teste',
    'teste@teste.com',
    '$2y$10$wH8QzQ1QzQ1QzQ1QzQ1QzOe6ZkQm2J7rF0XyYlV9lYq9vV7u7Uu2G'
);

INSERT INTO eventos (nome_evento, descricao, data_evento, preco) VALUES
('Show de Rock', 'Evento musical ao vivo', '2026-05-10', 50.00),
('Palestra Tech', 'Tecnologia e inovação', '2026-06-15', 30.00),
('Festival Gamer', 'Jogos e competições', '2026-07-20', 70.00);