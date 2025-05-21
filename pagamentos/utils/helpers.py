"""
Funções auxiliares para o aplicativo de pagamentos.
"""
import datetime
import locale
from decimal import Decimal

# Configurar locale para formatação de moeda
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except:
        pass  # Fallback para o locale padrão

def format_currency(value):
    """
    Formata um valor como moeda brasileira (R$).
    """
    if value is None:
        return "R$ 0,00"
    try:
        return locale.currency(float(value), grouping=True)
    except:
        value = Decimal(str(value))
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def parse_date(date_str, formats=None):
    """
    Converte uma string de data para um objeto datetime.date.
    """
    if not date_str:
        return None
    if formats is None:
        formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']
    for fmt in formats:
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None

def calculate_late_days(due_date, reference_date=None):
    """
    Calcula quantos dias um pagamento está atrasado.
    """
    if reference_date is None:
        reference_date = datetime.date.today()
    if due_date >= reference_date:
        return 0
    return (reference_date - due_date).days