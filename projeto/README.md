# BoostPro – Site de Boosting para Jogos

Aplicação web completa para venda de serviços de rank boosting e account leveling.
Desenvolvida com **Flask** (back-end) e **HTML5/CSS3/Bootstrap 5** (front-end).

---

## Estrutura do Projeto

```
projeto/
│
├── back-end/
│   ├── app.py              ← Ponto de entrada; cria a app Flask e registra blueprints
│   ├── config.py           ← Configurações (banco de dados, chave secreta)
│   ├── models.py           ← Modelos SQLAlchemy (Usuario, Servico)
│   ├── forms.py            ← Formulários WTForms com validação
│   ├── requirements.txt    ← Dependências Python
│   ├── database.sql        ← Script de criação do banco MySQL
│   ├── routes/
│   │   ├── __init__.py     ← Torna routes um pacote Python
│   │   ├── auth.py         ← Blueprint: cadastro, login, logout
│   │   ├── services.py     ← Blueprint: CRUD de serviços de boosting
│   │   └── users.py        ← Blueprint: dashboard e CRUD de usuários
│   ├── templates/
│   │   ├── base.html           ← Template base (navbar, flash, footer)
│   │   ├── servicos.html       ← Página pública de serviços
│   │   ├── login.html          ← Página de login
│   │   ├── cadastro.html       ← Página de cadastro
│   │   ├── dashboard.html      ← Dashboard do administrador
│   │   ├── admin_usuarios.html ← Listagem de usuários (admin)
│   │   ├── admin_servicos.html ← Listagem de serviços (admin)
│   │   ├── form_servico.html   ← Formulário criar/editar serviço
│   │   └── form_usuario.html   ← Formulário criar/editar usuário
│   └── static/
│       ├── css/style.css   ← Estilos principais (tema escuro)
│       └── js/script.js    ← JavaScript (navbar, modais, animações)
│
└── front-end/              ← Protótipo estático (HTML puro, sem servidor)
    ├── index.html
    ├── login.html
    ├── cadastro.html
    ├── servicos.html
    ├── dashboard.html
    ├── css/style.css
    └── js/script.js
```

---

## Pré-requisitos

- Python 3.10 ou superior
- MySQL 8.x
- pip

---

## Passo a Passo de Instalação

### 1. Clonar / baixar o projeto

```bash
# Se estiver usando Git:
git clone <url-do-repositorio>
cd projeto
```

### 2. Criar o banco de dados MySQL

Acesse o MySQL e execute o script:

```bash
mysql -u root -p < back-end/database.sql
```

Ou cole o conteúdo de `back-end/database.sql` diretamente no MySQL Workbench / DBeaver.

### 3. Configurar a conexão com o banco

Edite `back-end/config.py` e ajuste a linha:

```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://SEU_USUARIO:SUA_SENHA@localhost/boosting_db"
```

Substitua `SEU_USUARIO` e `SUA_SENHA` pelas suas credenciais MySQL.

Alternativamente, defina a variável de ambiente:

```bash
# Windows (PowerShell)
$env:DATABASE_URL = "mysql+pymysql://root:sua_senha@localhost/boosting_db"
$env:SECRET_KEY    = "uma-chave-secreta-segura"
```

### 4. Criar o ambiente virtual e instalar dependências

```bash
cd back-end

# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 5. Executar a aplicação

```bash
python app.py
```

A aplicação estará disponível em: **http://localhost:5000**

> **Administrador padrão criado automaticamente:**
> - E-mail: `admin@boosting.com`
> - Senha: `admin123`
> - **Altere a senha após o primeiro acesso!**

---

## Rotas Disponíveis

| Rota | Método | Acesso | Descrição |
|------|--------|--------|-----------|
| `/` | GET | Público | Redireciona para /servicos |
| `/servicos` | GET | Público | Lista serviços de boosting |
| `/cadastro` | GET/POST | Público | Cadastro de novo usuário |
| `/login` | GET/POST | Público | Autenticação |
| `/logout` | GET | Logado | Encerra sessão |
| `/admin/dashboard` | GET | Admin | Painel de controle |
| `/admin/usuarios` | GET | Admin | Lista usuários |
| `/admin/usuarios/novo` | GET/POST | Admin | Cadastra usuário |
| `/admin/usuarios/editar/<id>` | GET/POST | Admin | Edita usuário |
| `/admin/usuarios/excluir/<id>` | POST | Admin | Exclui usuário |
| `/admin/servicos` | GET | Admin | Lista serviços (admin) |
| `/admin/servicos/novo` | GET/POST | Admin | Cadastra serviço |
| `/admin/servicos/editar/<id>` | GET/POST | Admin | Edita serviço |
| `/admin/servicos/excluir/<id>` | POST | Admin | Exclui serviço |

---

## Funcionalidades Implementadas

### Autenticação
- [x] Cadastro com senha hasheada (Werkzeug)
- [x] Login com sessão (Flask-Login)
- [x] Logout
- [x] Páginas protegidas por `@login_required`
- [x] Restrição de rotas admin com decorador `@admin_required`

### CRUD – Usuários (Admin)
- [x] Cadastrar usuários
- [x] Listar todos os usuários
- [x] Editar dados e tipo de usuário
- [x] Excluir usuários (com proteção contra auto-exclusão)

### CRUD – Serviços (Admin)
- [x] Cadastrar serviços de boosting
- [x] Listar todos os serviços
- [x] Editar serviço existente
- [x] Excluir serviço

### Interface
- [x] Tema escuro
- [x] Design responsivo (Bootstrap 5)
- [x] Navbar com dropdown admin
- [x] Flash messages com auto-dismiss
- [x] Modal de confirmação de exclusão
- [x] Animações com IntersectionObserver
- [x] Toggle de visibilidade da senha

---

## Tecnologias Utilizadas

| Camada | Tecnologia |
|--------|-----------|
| Back-end | Python 3, Flask 3, SQLAlchemy, Flask-Login, Flask-WTF |
| Banco de dados | MySQL 8 via PyMySQL |
| Front-end (templates) | HTML5, CSS3, Bootstrap 5, JavaScript puro |
| Fontes | Google Fonts (Inter, Rajdhani) |
| Ícones | Bootstrap Icons |

---

## Solução de Problemas

**Erro de conexão com MySQL:**
Verifique se o MySQL está rodando e se as credenciais em `config.py` estão corretas.

**`ModuleNotFoundError`:**
Certifique-se de que o ambiente virtual está ativado e que `pip install -r requirements.txt` foi executado.

**Tabelas não criadas:**
O `app.py` chama `db.create_all()` automaticamente ao iniciar. Verifique se o banco `boosting_db` existe no MySQL.

**Porta 5000 em uso:**
Altere a porta no final de `app.py`: `app.run(debug=True, port=5001)`
