from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from uploads.models import Parser


def home_page(request):
    if request.method == 'POST' and request.FILES['cnab_file']:
        file = request.FILES['cnab_file']

        parser = Parser(text=str(file.read()))
        file.close()
        valid_content = parser.validate_content()
        if not valid_content:
            message = 'Formato do arquivo inválido.'
            return render(request, 'uploads/home.html', {'message': message})

    return render(request, 'uploads/home.html')
