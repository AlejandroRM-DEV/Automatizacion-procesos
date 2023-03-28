import os
import glob
import json
import argparse
import concurrent.futures
import subprocess
from tqdm import tqdm


def save_metadata(dest_directory, file):
    file_name = os.path.splitext(os.path.basename(file))[0]
    metadata_file = os.path.join(dest_directory, f"Metadata_{file_name}.txt")

    p = subprocess.Popen(
        ["exiftool", "-j", file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf-8',
    )

    json_output, err = p.communicate()
    metadata = json.loads(json_output)[0]
    metadata.pop("SourceFile", None)
    metadata.pop("Directory", None)
    with open(metadata_file, "w", encoding='utf-8') as f:
        f.write(json.dumps(metadata, indent=4))


def process(dest_meta_directory, file):
    save_metadata(dest_meta_directory, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="Directorio donde buscar los archivos", default=".")
    args = parser.parse_args()

    print(f"Buscando archivos en: {args.dir}")
    files = glob.glob(f"{args.dir}/**/*.*", recursive=True)

    if len(files) == 0:
        print("No se encontraron archivos")
    else:
        dest_meta_directory = os.path.join(os.path.dirname(args.dir), "_METADATA_")
        os.makedirs(dest_meta_directory, exist_ok=True)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(process, dest_meta_directory, file) for file in files]
            for _ in tqdm(concurrent.futures.as_completed(results), total=len(results), desc="Obteniendo metadatos"):
                pass

    print("Presiona una tecla para terminar...")
    input()
