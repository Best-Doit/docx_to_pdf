from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from docx2pdf import convert
import os

def convertir_word_pdf(request):
    message = None
    archivo_pdf = None
    if request.method == 'POST' and request.FILES.get('word_file'):
        word_file = request.FILES['word_file']
        fs = FileSystemStorage()
        filename = fs.save(word_file.name, word_file)
        filepath = fs.path(filename)
        pdf_path = os.path.splitext(filepath)[0] + '.pdf'

        # Realizar la conversión
        convert(filepath, pdf_path)

        # Eliminar el archivo de Word después de la conversión
        os.remove(filepath)

        archivo_pdf = os.path.basename(pdf_path)
        message = f"¡Se ha convertido {word_file.name} a {archivo_pdf} exitosamente!"

    return render(request, 'index.html', {'message': message, 'archivo_pdf': archivo_pdf})

def descargar_pdf(request, filename):
    fs = FileSystemStorage()
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponseNotFound('El archivo PDF no se encontró')
