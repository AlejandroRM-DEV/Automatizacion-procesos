import os
import cv2
import glob
import argparse
import subprocess
from tqdm import tqdm

VIDEO_EXTENSIONS = [
    ".3g2", ".3gp", ".asf", ".avi", ".dav", ".divx", ".f4v", ".flv", ".h264", ".m2t",
    ".m2ts", ".m2v", ".mkv", ".m4v", ".mov", ".mp4", ".mpg", ".mpg2", ".mpg4", ".mpeg",
    ".nut", ".ogm", ".ogv", ".rm", ".rmvb", ".tod", ".tp", ".trp", ".ts", ".vob", ".webm", ".wmv", ".xvid"
]


def generate_image_sequence(dest_directory, video_path, image_interval):
    video_file_name = os.path.splitext(os.path.basename(video_path))[0]
    image_directory = os.path.join(dest_directory, video_file_name)
    os.makedirs(image_directory, exist_ok=True)

    command = [
        "ffmpeg",
        "-hide_banner",
        "-i", video_path,
        "-r", str(1 / image_interval),
        "-f", "image2",
        "-vf", "fps=fps=1/{}".format(image_interval),
        "-loglevel", "panic",
        "{}/{}-%05d.png".format(image_directory, video_file_name),
    ]

    process = subprocess.Popen(command, universal_newlines=True, encoding='utf-8')
    process.wait()


def process_video(dest_img_directory, video_file, image_interval):
    generate_image_sequence(dest_img_directory, video_file, image_interval)


def search_video_files(current_dir):
    video_files = []
    for extension in VIDEO_EXTENSIONS:
        video_files.extend(
            glob.glob(f"{current_dir}/**/*{extension}", recursive=True))

    return video_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--dir", help="Directorio donde buscar los archivos de video", default=".")
    args = parser.parse_args()

    print(f"Buscando archivos de video en: {args.dir}")
    video_files = search_video_files(args.dir)

    if len(video_files) == 0:
        print("No se encontraron archivos de video")
    else:
        dest_img_directory = os.path.join(
            os.path.dirname(args.dir), "_IJCF_SEC_IMAGENES")
        os.makedirs(dest_img_directory, exist_ok=True)

        image_interval = float(
            input("Introduce cada cuántos segundos quieres una imagen: "))
        for video_file in tqdm(video_files, desc="Procesando videos"):
            process_video(dest_img_directory, video_file, image_interval)

    print("Presiona una tecla para terminar...")
    input()
