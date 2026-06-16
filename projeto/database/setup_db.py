import mysql.connector
from mysql.connector import Error

def setup():
    try:
        conexao = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="963968"
        )

        cursor = conexao.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS loja_boosting")
        cursor.execute("USE loja_boosting")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                senha VARCHAR(255) NOT NULL,
                tipo_usuario ENUM('comprador', 'vendedor') NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendedores (
                id_vendedor INT AUTO_INCREMENT PRIMARY KEY,
                id_usuario INT NOT NULL UNIQUE,
                especialidade VARCHAR(100),
                nota_media DECIMAL(3,2) DEFAULT 0.00,

                FOREIGN KEY (id_usuario)
                REFERENCES usuarios(id_usuario)
                ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id_pedido INT AUTO_INCREMENT PRIMARY KEY,

                id_comprador INT NOT NULL,
                id_vendedor INT NOT NULL,

                jogo VARCHAR(100) NOT NULL,
                servico VARCHAR(100) NOT NULL,

                rank_atual VARCHAR(50),
                rank_desejado VARCHAR(50),

                valor DECIMAL(10,2) NOT NULL,

                status ENUM(
                    'Pendente',
                    'Aceito',
                    'Em andamento',
                    'Concluido',
                    'Cancelado'
                ) DEFAULT 'Pendente',

                FOREIGN KEY (id_comprador)
                REFERENCES usuarios(id_usuario),

                FOREIGN KEY (id_vendedor)
                REFERENCES vendedores(id_vendedor)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensagens (
                id_mensagem INT AUTO_INCREMENT PRIMARY KEY,

                id_pedido INT NOT NULL,

                remetente INT NOT NULL,
                destinatario INT NOT NULL,

                mensagem TEXT NOT NULL,

                data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (id_pedido)
                REFERENCES pedidos(id_pedido)
                ON DELETE CASCADE,

                FOREIGN KEY (remetente)
                REFERENCES usuarios(id_usuario),

                FOREIGN KEY (destinatario)
                REFERENCES usuarios(id_usuario)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS avaliacoes (
                id_avaliacao INT AUTO_INCREMENT PRIMARY KEY,

                id_comprador INT NOT NULL,
                id_vendedor INT NOT NULL,

                nota INT NOT NULL CHECK (nota BETWEEN 1 AND 5),

                comentario TEXT,

                FOREIGN KEY (id_comprador)
                REFERENCES usuarios(id_usuario),

                FOREIGN KEY (id_vendedor)
                REFERENCES vendedores(id_vendedor)
            )
        """)

        conexao.commit()

        print("Banco de dados configurado com sucesso!")

        cursor.close()
        conexao.close()

    except Error as e:
        print(f"Erro ao configurar banco de dados: {e}")


if __name__ == "__main__":
    setup()
