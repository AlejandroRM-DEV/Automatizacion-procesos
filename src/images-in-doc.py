import os
import argparse
import glob
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Cm

EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']


def make_document(dest_directory, files, columns):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    doc = DocxTemplate(os.path.abspath(f"{script_dir}/templates/imgs.docx"))

    datos = {"imgs": [], "columns": columns}
    for file in files:
        datos["imgs"].append(InlineImage(doc, image_descriptor=os.path.abspath(file), width=Cm(16/int(columns))))

    doc.render(datos)
    doc.save(os.path.abspath(f"{dest_directory}/imgs.docx"))
    os.startfile(os.path.abspath(f"{dest_directory}/imgs.docx"))


def search_files(dir):
    files = []
    for extension in EXTENSIONS:
        files.extend(glob.glob(f"{dir}/**/*{extension}", recursive=True))

    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--dir", help="Directorio donde buscar los archivos", default=".")
    args = parser.parse_args()

    print(f"Buscando archivos en: {args.dir}")
    files = search_files(args.dir)

    if len(files) == 0:
        print("No se encontraron archivos")
    else:
        dest_directory = os.path.join(os.path.dirname(args.dir), "_DOCS_")
        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory)

        columns = input("Introduce el número de columnas (1, 2, 3 o 4): ")
        make_document(dest_directory, files, columns)