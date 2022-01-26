from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from uploads.models import Parser


def home_page(request):
    if request.method == 'POST' and request.FILES['cnab_file']:
        file = request.FILES['cnab_file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        # TODO: parse file and save in the database
        valid_file = Parser(filename)
        if not valid_file:
            message = 'Formato do arquivo inválido.'
            return render(request, 'uploads/home.html', {'message': message})

        # TODO: remove file after saving in the database
        # os.remove(settings.MEDIA_ROOT + '/' + filename)

    return render(request, 'uploads/home.html')
