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
        choices=[("comprador", "Quero contratar serviços"), ("vendedor", "Quero oferecer serviços (Vendedor)")],
        validators=[DataRequired()]
    )
    especialidade = StringField(
        "Especialidade (ex: League of Legends, Valorant)",
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

class FormPedido(FlaskForm):
    jogo = StringField(
        "Jogo",
        validators=[DataRequired(message="Informe o jogo."),
                    Length(max=100)]
    )
    servico = StringField(
        "Serviço desejado",
        validators=[DataRequired(message="Informe o serviço."),
                    Length(max=100)]
    )
    rank_atual = StringField(
        "Rank atual",
        validators=[Optional(), Length(max=50)]
    )
    rank_desejado = StringField(
        "Rank desejado",
        validators=[Optional(), Length(max=50)]
    )
    valor = DecimalField(
        "Valor (R$)",
        validators=[DataRequired(message="Informe o valor."),
                    NumberRange(min=0.01, message="Valor deve ser maior que zero.")],
        places=2
    )
    submit = SubmitField("Confirmar Pedido")

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
        choices=[("comprador", "Comprador"), ("vendedor", "Vendedor")],
        validators=[DataRequired()]
    )
    nova_senha = PasswordField(
        "Nova senha (deixe em branco para não alterar)",
        validators=[Optional(), Length(min=6, message="Senha deve ter no mínimo 6 caracteres.")]
    )
    submit = SubmitField("Salvar alterações")

class FormStatusPedido(FlaskForm):
    status = SelectField(
        "Status do Pedido",
        choices=[
            ("Pendente", "Pendente"),
            ("Aceito", "Aceito"),
            ("Em andamento", "Em andamento"),
            ("Concluido", "Concluído"),
            ("Cancelado", "Cancelado")
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Atualizar Status")

class FormMensagem(FlaskForm):
    mensagem = TextAreaField(
        "Mensagem",
        validators=[DataRequired(message="A mensagem não pode estar vazia.")]
    )
    submit = SubmitField("Enviar")

class FormAvaliacao(FlaskForm):
    nota = IntegerField(
        "Nota (1 a 5)",
        validators=[DataRequired(message="Informe a nota."),
                    NumberRange(min=1, max=5, message="Nota deve ser entre 1 e 5.")]
    )
    comentario = TextAreaField(
        "Comentário",
        validators=[Optional()]
    )
    submit = SubmitField("Avaliar")

class FormVendedor(FlaskForm):
    especialidade = StringField(
        "Especialidade",
        validators=[Optional(), Length(max=100)]
    )
    submit = SubmitField("Salvar")
