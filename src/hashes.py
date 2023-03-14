import os
import hashlib
import argparse
from tqdm import tqdm
import pyperclip


def search_files(current_dir):
    files_array = []

    for root, dirs, files in os.walk(current_dir):
        for file in files:
            files_array.append(os.path.join(root, file))

    return files_array


def calculate_hash(file):
    sha256_hash = hashlib.sha256()
    block_size = 4096

    with open(file, "rb") as f:
        block = f.read(block_size)
        while block:
            sha256_hash.update(block)
            block = f.read(block_size)

    return sha256_hash.hexdigest().upper()


def save_to_html(results, dest_directory):
    results.sort()

    with open(os.path.join(dest_directory, 'Hashes.html'), 'w', encoding='utf-8') as f:
        f.write('<html>\n')
        f.write('<head>\n')
        f.write('<title>Resultados de hash SHA256</title>\n')
        f.write('<style>\n')
        f.write('table {\n')
        f.write('  border-collapse: collapse;\n')
        f.write('  width: 100%;\n')
        f.write('  border: 2px solid black;\n')
        f.write('}\n')
        f.write('th, td {\n')
        f.write('  text-align: left;\n')
        f.write('  padding: 8px;\n')
        f.write('  border: 1px solid black;\n')
        f.write('}\n')
        f.write('tr:nth-child(even) {\n')
        f.write('  background-color: #f2f2f2;\n')
        f.write('}\n')
        f.write('h1 {\n')
        f.write('  text-align: center;\n')
        f.write('}\n')
        f.write('</style>\n')
        f.write('</head>\n')
        f.write('<body>\n')
        f.write('<h1>Resultados de hash SHA256</h1>\n')
        f.write('<table>\n')
        f.write('<tr><th>Nombre de archivo</th><th>Valor hash SHA256</th></tr>\n')

        for result in results:
            f.write(
                '<tr><td>{}</td><td>{}</td></tr>\n'.format(result[0], result[1]))

        f.write('</table>\n')
        f.write('</body>\n')
        f.write('</html>\n')

    hash_report = calculate_hash(os.path.join(dest_directory, 'Hashes.html'))
    print(f"Valor hash del reporte: {hash_report}")
    pyperclip.copy(hash_report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="Directorio donde buscar los archivos", default=".")
    args = parser.parse_args()

    print(f"Generando hashes de: {args.dir}")
    files = search_files(args.dir)

    if len(files) == 0:
        print("No se encontraron archivos")
    else:
        dest_directory = os.path.join(os.path.dirname(args.dir), "_HASHES_")
        os.makedirs(dest_directory, exist_ok=True)

        results = []
        for file in tqdm(files):
            results.append((os.path.basename(file), calculate_hash(file)))

        save_to_html(results, dest_directory)

    print("Presiona una tecla para terminar...")
    input()
