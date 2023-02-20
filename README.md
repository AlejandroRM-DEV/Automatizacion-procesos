# Automatización procesos

## video-sec.py
Este script es una herramienta para extraer imágenes de video. Se ejecuta desde la línea de comandos y procesa todos los archivos de video en un directorio especificado por el usuario. La frecuencia de las imágenes extraídas se especifica también por el usuario.

El script utiliza la biblioteca OpenCV para abrir archivos de video y extraer imágenes, y la biblioteca glob para buscar archivos de video en un directorio.

Para procesar los archivos de video en paralelo, se utiliza la biblioteca concurrent.futures y el código está diseñado para mostrar una barra de progreso utilizando la biblioteca tqdm.

La secuencia de imágenes resultante se guarda en un directorio con el mismo nombre que el archivo de video, y cada imagen se nombra como "frame_X.jpg", donde X es el número de imagen.

## hashes.py
Este script genera hashes SHA256 para los archivos encontrados en un directorio y su subdirectorio y los guarda en un archivo HTML. El script utiliza la biblioteca hashlib para calcular los hashes SHA256 de los archivos, os para buscar archivos en el directorio y subdirectorios, argparse para analizar argumentos de línea de comando y tqdm para mostrar una barra de progreso mientras se generan los hashes.

## images-in-doc.py
Utiliza varios módulos de Python para buscar imágenes en un directorio, insertarlas en un documento de Word y guardar el documento en una carpeta de destino. Además, utiliza argumentos de línea de comandos para permitir que el usuario especifique el directorio de búsqueda y el número de columnas del documento.