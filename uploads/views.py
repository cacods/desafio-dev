from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from uploads.models import Parser, Transacao


def home_page(request):
    if request.method == 'POST' and request.FILES['cnab_file']:
        file = request.FILES['cnab_file']

        parser = Parser(text=file.read().decode('utf-8'))
        file.close()
        valid_content = parser.validate_content()
        if not valid_content:
            message = 'Formato do arquivo inválido.'
            return render(request, 'uploads/home.html', {'message': message})
        else:
            parser.save_data()
            transacoes = Transacao.objects.all()
            return render(request, 'uploads/home.html',
                          {'transacoes': transacoes})

    transacoes = Transacao.objects.all()
    return render(request, 'uploads/home.html', {'transacoes': transacoes})
