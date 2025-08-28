from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import csv
import os
import zipfile
from io import BytesIO

def upload_view(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        rows_per_file = int(request.POST.get("rows_per_file", 1000))

        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        uploaded_file_path = fs.path(filename)

        # In-memory ZIP file
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            with open(uploaded_file_path, 'r', newline='', encoding="utf-8") as infile:
                reader = csv.reader(infile)
                header = next(reader)

                file_num = 1
                current_rows = []

                for i, row in enumerate(reader):
                    current_rows.append(row)
                    if (i + 1) % rows_per_file == 0:
                        output_file = f"{os.path.splitext(filename)[0]}_{file_num}.csv"
                        zip_file.writestr(output_file, write_csv(header, current_rows))
                        current_rows = []
                        file_num += 1

                # Save remaining rows
                if current_rows:
                    output_file = f"{os.path.splitext(filename)[0]}_{file_num}.csv"
                    zip_file.writestr(output_file, write_csv(header, current_rows))

        zip_buffer.seek(0)

        # Return ZIP as download
        response = HttpResponse(zip_buffer, content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename="split_csv_files.zip"'
        return response

    return render(request, "splitte_csv/upload.html")


# Helper function to convert rows → CSV string
def write_csv(header, rows):
    from io import StringIO
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(header)
    writer.writerows(rows)
    return buffer.getvalue()
