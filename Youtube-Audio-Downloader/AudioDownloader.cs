using System.Diagnostics;
using System.Globalization;
using System.IO;

namespace Youtube_Audio_Downloader {
    class AudioDownloader {
        private string url;
        public string Url { get => url; }

        private bool isValidVideo;
        public bool IsValidVideo { get => isValidVideo; }

        private string title;
        public string Title { get => title; }

        /// <summary>
        /// Gestiona la información y descarga de la musica de un video de Youtube
        /// </summary>
        /// <param name="url">Url del video de Youtube</param>
        public AudioDownloader(string url) {
            this.url = url;
            this.isValidVideo = true;
            this.title = Strings.video_default_name;

            GetInfo();
        }

        /// <summary>
        /// Si es una url valida, obtiene el nombre del video.
        /// Si no es una url valida, el video es marcada como invalido.
        /// </summary>
        private void GetInfo() {
            try {
                ProcessStartInfo processStartInfo = new ProcessStartInfo() {
                    FileName = Strings.ytdlp_path,
                    Arguments = Strings.videoinfo_ytdlp_args.Replace("%(url)s", this.url),
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                };

                Process? process = Process.Start(processStartInfo);

                if (process != null) {
                    Thread outputThread = new Thread(() => {                        
                        string data = process.StandardOutput.ReadToEnd();

                        if (data == string.Empty) {
                            this.isValidVideo = false;
                            return;
                        }

                        this.isValidVideo = true;
                        this.title = data;
                    });
                    
                    outputThread.Start();

                    process.WaitForExit();
                    
                    outputThread.Join();
                }
            } catch (Exception) { this.isValidVideo = false; }
        }

        /// <summary>
        /// Si el video es valido, intenta descargarlo en la carpeta especificada y con el nombre especificado.
        /// </summary>
        /// <param name="downloadFolder">Donde guardar la musica</param>
        /// <param name="fileName">Nombre del archivo ó NULL para usar el titulo del video</param>
        /// <param name="funcSendDownloadData">Función a la que enviar información sobre la descarga</param>
        /// <param name="error">Parametro de salida que devuelve los errores obtenidos durante la descarga</param>
        /// <returns>True si y solo si se ha podido descargar el video, si no de vuelve False</returns>
        public bool DownloadAudio(string downloadFolder, string? fileName, Action<double, string, string>? funcSendDownloadData, out string error) {
            if(!this.isValidVideo) {
                error = Strings.videoerror_invalid;
                return false;
            } else if(fileName == null || fileName == string.Empty) {
                fileName = this.title + ".mp3";
            }

            bool result = true;
            string internalError = "";

            try {
                ProcessStartInfo processStartInfo = new ProcessStartInfo() {
                    FileName = Strings.ytdlp_path,
                    Arguments = Strings.videodownload_ytdlp_args.Replace("%(downloadFolder)s", downloadFolder).Replace("%(fileName)s", fileName).Replace("%(url)s", this.url),
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                };

                Process? process = Process.Start(processStartInfo);

                if (process != null) {
                    Thread outputThread = new Thread(() => {
                        StreamReader reader = process.StandardOutput;
                        string? line;

                        while ((line = reader.ReadLine()) != null) {
                            if (line.StartsWith("[download]") && line.Contains("ETA")) {
                                line = line.Replace("[download]", "").Trim();

                                string percentageStr = line.Substring(0, line.IndexOf("% of"));
                                string ETA = line.Substring(line.LastIndexOf("ETA ") + 4);

                                funcSendDownloadData(double.Parse(percentageStr, CultureInfo.InvariantCulture), ETA, fileName);
                            }
                        }
                    });

                    Thread errorThread = new Thread(() => {
                        StreamReader errorReader = process.StandardError;
                        string? line;

                        while ((line = errorReader.ReadLine()) != null) {
                            if (!line.ToLower().Contains("warning")) {
                                internalError += line + "\n";

                                result = false;
                            }
                        }
                    });
                    
                    errorThread.Start();

                    if(funcSendDownloadData != null) {
                        outputThread.Start();
                        outputThread.Join();
                    }

                    errorThread.Join();

                    process.WaitForExit();
                    
                } else {
                    
                }
            } catch (Exception ex) {
                result = false;
                internalError += ex.Message;
            }

            if(funcSendDownloadData != null) {
                funcSendDownloadData(100, "00:00", fileName);
            }

            error = internalError;
            return result;
        }
    }
}