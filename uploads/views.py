from django.core.files.storage import FileSystemStorage
from django.shortcuts import render


def home_page(request):
    if request.method == 'POST' and request.FILES['cnab_file']:
        file = request.FILES['cnab_file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        # TODO: parse file and save in the database

        # TODO: remove file after saving in the database
        # os.remove(settings.MEDIA_ROOT + '/' + filename)

    return render(request, 'uploads/home.html')
