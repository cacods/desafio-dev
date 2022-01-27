from django import template

register = template.Library()


@register.simple_tag(name='get_operacao')
def get_operacao(tipo):
    if tipo == 1:
        return 'Débito (+)'
    elif tipo == 2:
        return 'Boleto (-)'
    elif tipo == 3:
        return 'Financiamento (-)'
    elif tipo == 4:
        return 'Crédito (+)'
    elif tipo == 5:
        return 'Recebimento Empréstimo (+)'
    elif tipo == 6:
        return 'Vendas (+)'
    elif tipo == 7:
        return 'Recebimento TED (+)'
    elif tipo == 8:
        return 'Recebimento DOC (+)'
    elif tipo == 9:
        return 'Aluguel (-)'
    else:
        return '?'
