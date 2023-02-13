import os
import cv2


def generate_image_sequence(video_path, image_interval):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
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


def list_files_by_extension(extension):
    video_files = []
    current_dir = os.getcwd()
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith(extension):
                video_files.append(os.path.join(root, file))

    return video_files


extension = input("Introduce la extensión de los archivos (ejemplo: '.mp4'): ")
video_files = list_files_by_extension(extension)

if len(video_files) == 0:
    print("No se encontraron archivos de video con esa extensión")
else:
    image_interval = float(input("Introduce cada cuántos segundos quieres una imagen: "))
    for video_file in video_files:
        print(f"Procesando video: {video_file}")
        generate_image_sequence(video_file, image_interval)
    
    print("Fin")

