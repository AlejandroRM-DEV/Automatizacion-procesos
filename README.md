# Automatización procesos

## video-sec.py
Este script es una herramienta para extraer imágenes de video. Se ejecuta desde la línea de comandos y procesa todos los archivos de video en un directorio especificado por el usuario. La frecuencia de las imágenes extraídas se especifica también por el usuario.

El script utiliza la biblioteca OpenCV para abrir archivos de video y extraer imágenes, y la biblioteca glob para buscar archivos de video en un directorio.

Para procesar los archivos de video en paralelo, se utiliza la biblioteca concurrent.futures y el código está diseñado para mostrar una barra de progreso utilizando la biblioteca tqdm.

La secuencia de imágenes resultante se guarda en un directorio con el mismo nombre que el archivo de video, y cada imagen se nombra como "frame_X.jpg", donde X es el número de imagen.
