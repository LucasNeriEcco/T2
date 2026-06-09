"""
forms.py – Formulários WTForms para validação de dados no back-end.
Valida campos de cadastro, login, criação/edição de serviços e usuários.
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SelectField,
    TextAreaField, DecimalField, SubmitField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length,
    NumberRange, Optional
)


class FormCadastro(FlaskForm):
    """Formulário de cadastro de novo usuário."""
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
    submit = SubmitField("Cadastrar")


class FormLogin(FlaskForm):
    """Formulário de login."""
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
    """Formulário de cadastro/edição de serviço de boosting."""
    jogo = StringField(
        "Jogo",
        validators=[DataRequired(message="Informe o jogo."),
                    Length(max=100)]
    )
    tipo_servico = StringField(
        "Tipo de serviço",
        validators=[DataRequired(message="Informe o tipo de serviço."),
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
    prazo_estimado = StringField(
        "Prazo estimado",
        validators=[DataRequired(message="Informe o prazo."),
                    Length(max=50)]
    )
    submit = SubmitField("Salvar")


class FormEditarUsuario(FlaskForm):
    """Formulário de edição de usuário pelo administrador."""
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
