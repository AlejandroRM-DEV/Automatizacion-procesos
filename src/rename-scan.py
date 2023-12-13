import os
import argparse
from tqdm import tqdm
import pytesseract
from pdf2image import convert_from_path
import re


def search_files(current_dir):
    pdf_files = []
    pattern = r'^\d.*\.pdf$'
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if re.match(pattern, file, re.IGNORECASE):
                pdf_files.append(os.path.join(root, file))

    return pdf_files


def sanitize(str):
    str = str.replace('/', '-')
    str = str.replace(' ', '')

    parts = str.split("-")
    parts[1] = parts[1].replace('1', 'I')
    parts[4] = "IJCF"
    parts[7] = "IF"

    return "-".join(parts)


def process(file):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    print(file)

    rotations = [0, 90, 180, 270]
    images = convert_from_path(file,poppler_path=r'C:\Program Files\poppler-23.08.0\Library\bin')
    pattern = r'D-[\w]{1,3}\s*/\s*\d{1,6}\s*/\s*\d{4}\s*/\s*[\w]{4,}\s*/\s*0*\d{6}\s*/\s*\d{4}\s*/\s*[\w]{2}\s*/\s*0*\d{2}'
    found_match = None
    for degrees in rotations:
        for image in images:
            text = pytesseract.image_to_string(image.rotate(degrees), lang='spa')
            match = re.search(pattern, text)
            
            if match:
                found_match = match.group()
                break
        
        if found_match:
            pdf_directory = os.path.dirname(file)
            new_filename = os.path.join(pdf_directory, sanitize(found_match) + '.pdf')
            try:
                os.rename(file, new_filename)
            except FileExistsError as e:
                print(e)
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="Directorio donde buscar los archivos", default=".")
    args = parser.parse_args()

    print(f"Buscando archivos: {args.dir}")
    files = search_files(args.dir)

    if len(files) == 0:
        print("No se encontraron archivos")
    else:
        file = files.reverse()
        for file in tqdm(files):
            process(file)

    print("Presiona una tecla para terminar...")
    input()
