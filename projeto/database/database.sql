DROP DATABASE IF EXISTS loja_boosting;
CREATE DATABASE loja_boosting;
USE loja_boosting;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo_usuario ENUM('comprador', 'vendedor') NOT NULL
);

CREATE TABLE vendedores (
    id_vendedor INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE,
    especialidade VARCHAR(100),
    nota_media DECIMAL(3,2) DEFAULT 0.00,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_comprador INT NOT NULL,
    id_vendedor INT NOT NULL,
    jogo VARCHAR(100) NOT NULL,
    servico VARCHAR(100) NOT NULL,
    rank_atual VARCHAR(50),
    rank_desejado VARCHAR(50),
    valor DECIMAL(10,2) NOT NULL,
    status ENUM('Pendente', 'Aceito', 'Em andamento', 'Concluido', 'Cancelado') DEFAULT 'Pendente',
    FOREIGN KEY (id_comprador) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_vendedor) REFERENCES vendedores(id_vendedor)
);

CREATE TABLE mensagens (
    id_mensagem INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    remetente INT NOT NULL,
    destinatario INT NOT NULL,
    mensagem TEXT NOT NULL,
    data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (remetente) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (destinatario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE avaliacoes (
    id_avaliacao INT AUTO_INCREMENT PRIMARY KEY,
    id_comprador INT NOT NULL,
    id_vendedor INT NOT NULL,
    nota INT NOT NULL CHECK (nota BETWEEN 1 AND 5),
    comentario TEXT,
    FOREIGN KEY (id_comprador) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_vendedor) REFERENCES vendedores(id_vendedor)
);
