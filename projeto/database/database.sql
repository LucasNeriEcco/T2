CREATE DATABASE IF NOT EXISTS loja_boosting;
USE loja_boosting;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(256) NOT NULL,
    tipo_usuario ENUM('comprador', 'vendedor') NOT NULL,
    PRIMARY KEY (id_usuario),
    UNIQUE (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS vendedores (
    id_vendedor INT AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    especialidade VARCHAR(100),
    nota_media DECIMAL(3, 2) DEFAULT 0.00,
    PRIMARY KEY (id_vendedor),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido INT AUTO_INCREMENT,
    id_comprador INT NOT NULL,
    id_vendedor INT NOT NULL,
    jogo VARCHAR(100) NOT NULL,
    servico VARCHAR(100) NOT NULL,
    rank_atual VARCHAR(50),
    rank_desejado VARCHAR(50),
    valor DECIMAL(10, 2),
    status ENUM('Pendente', 'Aceito', 'Em andamento', 'Concluido', 'Cancelado') DEFAULT 'Pendente',
    PRIMARY KEY (id_pedido),
    FOREIGN KEY (id_comprador) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_vendedor) REFERENCES vendedores(id_vendedor) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS mensagens (
    id_mensagem INT AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    remetente INT NOT NULL,
    destinatario INT NOT NULL,
    mensagem TEXT NOT NULL,
    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_mensagem),
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (remetente) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (destinatario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS avaliacoes (
    id_avaliacao INT AUTO_INCREMENT,
    id_comprador INT NOT NULL,
    id_vendedor INT NOT NULL,
    nota INT NOT NULL,
    comentario TEXT,
    PRIMARY KEY (id_avaliacao),
    FOREIGN KEY (id_comprador) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_vendedor) REFERENCES vendedores(id_vendedor) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
