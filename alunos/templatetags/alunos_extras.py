import re
from django import template
from datetime import date

register = template.Library()


@register.filter(name="anos_desde")
def anos_desde(start_date):
    """
    Calcula o número de anos completos desde uma data de início até hoje.
    """
    if not start_date:
        return "-"

    today = date.today()

    # Converte datetime para date, se necessário
    if hasattr(start_date, "date"):
        start_date = start_date.date()

    if not isinstance(start_date, date):
        return "-"

    try:
        delta = today - start_date
        # Retorna 0 se o resultado for negativo
        return max(0, delta.days // 365)
    except TypeError:
        # Retorna "-" se a subtração de datas falhar
        return "-"


@register.filter(name="mask_cpf")
def mask_cpf(cpf):
    """
    Mascara um CPF, exibindo apenas parte dele. Ex: ***.123.456-**.
    """
    if not cpf or not isinstance(cpf, str):
        return ""

    cpf_numerico = re.sub(r"\D", "", cpf)

    if len(cpf_numerico) != 11:
        return cpf  # Retorna o valor original se não for um CPF válido

    return f"***.{cpf_numerico[3:6]}.{cpf_numerico[6:9]}-**"
