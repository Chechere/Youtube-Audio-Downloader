# Youtube Audio Downloader
> [!CAUTION]
> Esta aplicación no se hace responsable del uso ilicito de ella en cualquier aspecto. Esta aplicación no aboga a la pirateria, ni conductas similares.

## Resumen
Youtube Audio Downloader permite de manera sencilla poder descargar el audio de video de Youtube o el audio de listas creadas en Youtube.

![Imagen con la pantalla principal de la aplicación](https://github.com/user-attachments/assets/6c04eb95-5980-4cfe-90de-76c90ac8f138)

## Funcionamiento
1. Copiamos el link del video del que queremos descargar el audio ó la lista de youtube que contenga los videos cuyos audios queremos descargar.
2. Clickamos en "Descargar Video"
3. Si estamos descargando el audio de un vidoe, nos pedira especificar donde guardarlo y como nombrar al archivo
4. Si estamos descargando una lista, nos pedira especificar donde guardarla. Allí, se creara una carpeta con el nombre de la lista y dentro los audios de los videos de la lista.
5. Esperamos a que se descargue
6. !Ya tienes descargados tus audios¡

## Descargar
En la parte de [Releases](../../releases) esta disponible un archivo .zip con la version para Windows de la aplicación.

## Herramientas usadas
Estructura de la aplicación: C# - WPF ([Visual Studio](https://visualstudio.microsoft.com/es/))

Descarga de videos de YouTube: [YT_DLP](https://github.com/yt-dlp/yt-dlp)

Transformación de videos a mp3: [FFMPEG](https://www.ffmpeg.org)
