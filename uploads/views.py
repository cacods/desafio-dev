from django.shortcuts import render

from uploads.models import Parser, Transacao


def home_page(request):
    if request.method == 'POST' and request.FILES['cnab_file']:
        file = request.FILES['cnab_file']

        try:
            parser = Parser(text=file.read().decode('utf-8'))
        except UnicodeError:
            message = 'Formato do arquivo inválido.'
            return render(request, 'uploads/home.html', {'message': message})

        file.close()
        valid_content = parser.validate_content()
        if not valid_content:
            message = 'Formato do arquivo inválido.'
            return render(request, 'uploads/home.html', {'message': message})
        else:
            parser.save_data()
            transacoes = Transacao.objects.all()
            balance = Transacao.get_balance()
            return render(request, 'uploads/home.html',
                          {'transacoes': transacoes, 'balance': balance})

    transacoes = Transacao.objects.all()
    balance = Transacao.get_balance()
    return render(request, 'uploads/home.html',
                  {'transacoes': transacoes, 'balance': balance})
