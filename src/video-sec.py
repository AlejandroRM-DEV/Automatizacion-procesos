import os
import cv2
import glob
import argparse
import concurrent.futures
from tqdm import tqdm

EXTENSIONS = [".3g2", ".3gp", ".asf", ".avi", ".dav", ".divx", ".f4v", ".flv", ".h264", ".m2t", ".m2ts", ".m2v", ".mkv", ".m4v", ".mov", ".mp4",
              ".mpg", ".mpg2", ".mpg4", ".mpeg", ".nut", ".ogm", ".ogv", ".rm", ".rmvb", ".tod", ".tp", ".trp", ".ts", ".vob", ".webm", ".wmv", ".xvid"]


def generate_image_sequence(dest_directory, video_path, image_interval):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    image_counter = 0
    success, frame = cap.read()

    video_file_name = os.path.splitext(os.path.basename(video_path))[0]
    image_directory = os.path.join(dest_directory, video_file_name)
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)

    if image_interval >= 1:
        time_per_image = image_interval
    elif image_interval > 0:
        images_per_second = 1 / image_interval
        time_per_image = 1 / images_per_second
    else:
        raise ValueError("Sólo números mayores a 0")

    time_elapsed = 0
    while success:
        if time_elapsed >= time_per_image:
            image_name = f"{image_directory}/frame_{image_counter:010}.jpg"
            cv2.imwrite(image_name, frame)
            time_elapsed = 0
        success, frame = cap.read()
        image_counter += 1
        time_elapsed += 1 / fps

    cap.release()


def process_video(dest_directory, video_file, image_interval):
    generate_image_sequence(dest_directory, video_file, image_interval)


def search_files(current_dir):
    video_files = []
    for extension in EXTENSIONS:
        video_files.extend(glob.glob(f"{current_dir}/**/*{extension}", recursive=True))

    return video_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="Directorio donde buscar los archivos", default=".")
    args = parser.parse_args()

    print(f"Buscando archivos de video en: {args.dir}")
    video_files = search_files(args.dir)

    if len(video_files) == 0:
        print("No se encontraron archivos de video")
    else:
        dest_directory = os.path.join(os.path.dirname(args.dir), "_AUTO-IMG-SEC_")
        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory)

        image_interval = float(
            input("Introduce cada cuántos segundos quieres una imagen: "))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(process_video, dest_directory, video_file, image_interval) for video_file in video_files]
            for _ in tqdm(concurrent.futures.as_completed(results), total=len(results), desc="Procesando videos"):
                pass

    print("Presiona una tecla para terminar...")
    input()
