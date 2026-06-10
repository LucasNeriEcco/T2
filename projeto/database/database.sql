
CREATE DATABASE IF NOT EXISTS boosting_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE boosting_db;
CREATE TABLE IF NOT EXISTS usuarios (
  id            INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  nome          VARCHAR(100)    NOT NULL,
  email         VARCHAR(150)    NOT NULL,
  senha         VARCHAR(256)    NOT NULL COMMENT 'Hash bcrypt da senha',
  tipo_usuario  ENUM('cliente','administrador') NOT NULL DEFAULT 'cliente',
  data_criacao  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE IF NOT EXISTS servicos (
  id              INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  jogo            VARCHAR(100)    NOT NULL COMMENT 'Nome do jogo (ex: League of Legends)',
  tipo_servico    VARCHAR(100)    NOT NULL COMMENT 'Tipo do serviço (ex: Rank Boost, Leveling)',
  descricao       TEXT                    COMMENT 'Descrição detalhada do serviço',
  preco           DECIMAL(10, 2)  NOT NULL COMMENT 'Preço em reais',
  prazo_estimado  VARCHAR(50)     NOT NULL COMMENT 'Prazo de entrega (ex: 24h, 3 dias)',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO servicos (jogo, tipo_servico, descricao, preco, prazo_estimado) VALUES
('League of Legends', 'Rank Boosting',    'Boost de qualquer divisão. Jogaremos na sua conta com segurança e rapidez.', 49.90, '24h – 48h'),
('League of Legends', 'Account Leveling', 'Nivelamento da conta do nível 1 ao 30 com alta win-rate.',                   29.90, '3 dias'),
('Valorant',          'Rank Boosting',    'Subimos seu rank de Ferro até Imortal. Garantia de resultado.',              69.90, '24h – 72h'),
('Valorant',          'Placement Boost',  'Jogamos suas partidas de colocação para garantir o melhor rank inicial.',    39.90, '24h'),
('CS2',               'Rank Boosting',    'Boost de Silver a Global Elite realizado por jogadores profissionais.',      59.90, '48h'),
('Wild Rift',         'Account Leveling', 'Nivelamento rápido para liberar todas as funcionalidades do jogo.',          19.90, '2 dias');
