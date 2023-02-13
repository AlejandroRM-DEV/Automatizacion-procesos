# Automatización procesos

## Ejemplo de menú contextual
Entonces el archivo .reg sería algo así:
```
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\*\shell\Automatización\command]
@="python.exe \"ruta_a_tu_script.py\" \"%1\""

[HKEY_CLASSES_ROOT\*\shell\Automatización\Secuencia de imágenes\command]
@="python.exe \"ruta_a_tu_script.py\" \"%1\"
```
Asegúrate de reemplazar ruta_a_tu_script.py con la ruta absoluta a tu script de Python. Luego, haz doble clic en el archivo .reg para agregar la entrada al registro de Windows, y reinicia el Explorador de Windows para que los cambios tengan efecto. Después de estos pasos, deberías poder ver "Automatización" en el menú contextual al hacer clic derecho en un archivo cualquiera, y "Secuencia de imágenes" como una opción en el submenú al seleccionar "Automatización". Al hacer clic en "Secuencia de imágenes", se ejecutará tu script de Python con el archivo seleccionado como argumento.