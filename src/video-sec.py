import os
import cv2
import glob
import concurrent.futures
from tqdm import tqdm


def generate_image_sequence(video_path, image_interval):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    image_counter = 0
    success, frame = cap.read()

    video_file_name = os.path.splitext(os.path.basename(video_path))[0]
    image_directory = os.path.join(os.path.dirname(video_path), video_file_name)
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)

    while success:
        if image_counter % (fps * image_interval) == 0:
            image_name = f"{image_directory}/frame_{image_counter}.jpg"
            cv2.imwrite(image_name, frame)
        success, frame = cap.read()
        image_counter += 1

    cap.release()


def process_video(video_file, image_interval):
    generate_image_sequence(video_file, image_interval)


def list_files():
    video_files = []
    current_dir = "."
    for extension in [".mp4", ".avi", ".mov", ".dav"]:
        video_files.extend(glob.glob(f"{current_dir}/**/*{extension}", recursive=True))

    return video_files


video_files = list_files()

if len(video_files) == 0:
    print("No se encontraron archivos de video")
else:
    image_interval = float(input("Introduce cada cuántos segundos quieres una imagen: "))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(process_video, video_file, image_interval) for video_file in video_files]
        for _ in tqdm(concurrent.futures.as_completed(results), total=len(results), desc="Procesando videos"):
            pass
    
    print("Fin")
