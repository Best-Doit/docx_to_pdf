import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from docx2pdf import convert
from django.conf import settings

def convertir_word_pdf(request):
    message = None
    archivo_pdf = None
    
    if request.method == 'POST' and request.FILES.get('word_file'):
        word_file = request.FILES['word_file']
        
        # Definir el almacenamiento en la carpeta MEDIA_ROOT/pdf_files
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_files')
        os.makedirs(upload_dir, exist_ok=True)  # Asegurar que la carpeta existe
        fs = FileSystemStorage(location=upload_dir)

        # Guardar el archivo en la carpeta definida
        filename = fs.save(word_file.name, word_file)
        filepath = os.path.join(upload_dir, filename)

        # Definir la ruta del archivo PDF
        pdf_filename = os.path.splitext(filename)[0] + '.pdf'
        pdf_path = os.path.join(upload_dir, pdf_filename)

        try:
            # Realizar la conversión
            convert(filepath, pdf_path)
            
            # Eliminar el archivo Word después de la conversión
            os.remove(filepath)

            archivo_pdf = pdf_filename
            message = f"¡Se ha convertido {word_file.name} a {archivo_pdf} exitosamente!"
        except Exception as e:
            message = f"Ocurrió un error al convertir el archivo: {str(e)}"

    return render(request, 'index.html', {'message': message, 'archivo_pdf': archivo_pdf})

def descargar_pdf(request, filename):
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdf_files', filename)

    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponseNotFound('El archivo PDF no se encontró')
