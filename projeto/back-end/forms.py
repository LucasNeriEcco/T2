from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SelectField,
    TextAreaField, DecimalField, IntegerField, SubmitField, BooleanField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length,
    NumberRange, Optional
)
class FormCadastro(FlaskForm):
    nome = StringField(
        "Nome completo",
        validators=[DataRequired(message="Nome é obrigatório."),
                    Length(min=3, max=100)]
    )
    email = StringField(
        "E-mail",
        validators=[DataRequired(message="E-mail é obrigatório."),
                    Email(message="Informe um e-mail válido.")]
    )
    senha = PasswordField(
        "Senha",
        validators=[DataRequired(message="Senha é obrigatória."),
                    Length(min=6, message="Senha deve ter no mínimo 6 caracteres.")]
    )
    confirmar_senha = PasswordField(
        "Confirmar senha",
        validators=[DataRequired(), EqualTo("senha", message="Senhas não coincidem.")]
    )
    tipo_usuario = SelectField(
        "Você deseja:",
        choices=[("cliente", "Quero contratar serviços"), ("booster", "Quero oferecer serviços (Booster)")],
        validators=[DataRequired()]
    )
    nickname = StringField(
        "Nome de exibição (Nickname)",
        validators=[Optional(), Length(max=100)]
    )
    jogos_atuacao = StringField(
        "Jogos em que atua (separados por vírgula)",
        validators=[Optional(), Length(max=255)]
    )
    descricao_profissional = TextAreaField(
        "Breve descrição profissional",
        validators=[Optional()]
    )
    discord = StringField(
        "Discord ou outro contato",
        validators=[Optional(), Length(max=100)]
    )
    termos = BooleanField(
        "Eu concordo com os Termos e Condições de Uso",
        validators=[DataRequired(message="Você deve aceitar os termos de uso para se cadastrar.")]
    )
    submit = SubmitField("Cadastrar")
class FormLogin(FlaskForm):
    email = StringField(
        "E-mail",
        validators=[DataRequired(message="E-mail é obrigatório."),
                    Email(message="Informe um e-mail válido.")]
    )
    senha = PasswordField(
        "Senha",
        validators=[DataRequired(message="Senha é obrigatória.")]
    )
    submit = SubmitField("Entrar")
class FormServico(FlaskForm):
    nome = StringField(
        "Nome do Serviço",
        validators=[DataRequired(message="Informe o nome."),
                    Length(max=150)]
    )
    jogo = StringField(
        "Jogo",
        validators=[DataRequired(message="Informe o jogo."),
                    Length(max=100)]
    )
    categoria = StringField(
        "Categoria",
        validators=[DataRequired(message="Informe a categoria do serviço."),
                    Length(max=100)]
    )
    descricao = TextAreaField(
        "Descrição",
        validators=[Optional(), Length(max=1000)]
    )
    preco = DecimalField(
        "Preço (R$)",
        validators=[DataRequired(message="Informe o preço."),
                    NumberRange(min=0.01, message="Preço deve ser maior que zero.")],
        places=2
    )
    prazo_dias = IntegerField(
        "Prazo estimado (em dias)",
        validators=[DataRequired(message="Informe o prazo estimado.")]
    )
    max_pedidos_simultaneos = IntegerField(
        "Máx. de pedidos simultâneos",
        validators=[DataRequired(message="Informe o limite.")],
        default=1
    )
    status = SelectField(
        "Status do Serviço",
        choices=[("Ativo", "Ativo"), ("Inativo", "Inativo")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Salvar")

class FormEditarUsuario(FlaskForm):
    nome = StringField(
        "Nome completo",
        validators=[DataRequired(message="Nome é obrigatório."),
                    Length(min=3, max=100)]
    )
    email = StringField(
        "E-mail",
        validators=[DataRequired(message="E-mail é obrigatório."),
                    Email(message="Informe um e-mail válido.")]
    )
    tipo_usuario = SelectField(
        "Tipo de usuário",
        choices=[("cliente", "Cliente"), ("administrador", "Administrador")],
        validators=[DataRequired()]
    )
    nova_senha = PasswordField(
        "Nova senha (deixe em branco para não alterar)",
        validators=[Optional(), Length(min=6, message="Senha deve ter no mínimo 6 caracteres.")]
    )
    submit = SubmitField("Salvar alterações")

class FormContratacao(FlaskForm):
    nick_jogador = StringField(
        "Nick do jogador",
        validators=[DataRequired(message="Informe o nick do jogador."),
                    Length(max=100)]
    )
    rank_atual = StringField(
        "Rank atual",
        validators=[Optional(), Length(max=50)]
    )
    rank_desejado = StringField(
        "Rank desejado (quando aplicável)",
        validators=[Optional(), Length(max=50)]
    )
    observacoes = TextAreaField(
        "Informações adicionais / Observações",
        validators=[Optional()]
    )
    submit = SubmitField("Confirmar Contratação")

class FormStatusPedido(FlaskForm):
    status = SelectField(
        "Status do Pedido",
        choices=[
            ("Pendente", "Pendente"),
            ("Em andamento", "Em andamento"),
            ("Concluído", "Concluído"),
            ("Cancelado", "Cancelado")
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Atualizar Status")
