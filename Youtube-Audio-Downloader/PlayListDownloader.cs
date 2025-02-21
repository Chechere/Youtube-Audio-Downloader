using System.Diagnostics;
using System.Globalization;
using System.IO;

namespace Youtube_Audio_Downloader {
    class PlaylistDownloader {
        private bool isValidPlayList;
        public bool IsValidPlayList { get => isValidPlayList; }

        private string url;
        public string Url { get => url; }

        private string playListName;
        public string PlayListName { get => playListName; }

        private string[]? videoNames = null;

        public PlaylistDownloader(string url) {
            this.isValidPlayList = true;
            this.url = url;
            this.playListName = Strings.playlist_default_name;

            this.GetInfo();
        }

        /// <summary>
        /// Si es una url valida, obtiene el nombre de la playlist (O por defecto su id) y el nombre de los videos que contiene.
        /// Si no es una url valida, la playlist es marcada como invalida.
        /// </summary>
        private void GetInfo() {
            try {
                ProcessStartInfo processStartInfo = new ProcessStartInfo() {
                    FileName = Strings.ytdlp_path,
                    Arguments = Strings.playlistinfo_ytdlp_args.Replace("%(url)s", this.url),
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                };

                Process? process = Process.Start(processStartInfo);

                if (process != null) {
                    process.WaitForExit();

                    Thread outputThread = new Thread(() => {
                        string data = process.StandardOutput.ReadToEnd();                        

                        if (data is null || data == string.Empty) {
                            this.isValidPlayList = false;
                            return;
                        }

                        data = data.Substring(0, data.Length - 1);
                        string[] videos = data.Split('\n');


                        this.isValidPlayList = true;                        
                        this.playListName = videos[0].Split(" - ")[0];

                        videos = videos.Select(video => video.Split(" - ")[1]).ToArray();
                        this.videoNames = videos;
                    });

                    outputThread.Start();
                    outputThread.Join();
                }
            } catch (Exception) { this.isValidPlayList = false; }
        }

        /// <summary>
        /// Si la playlist es valida y contiene videos, intenta descargar la playlist en la carpeta especificada.
        /// </summary>
        /// <param name="downloadFolder">Donde crear una carpeta con el nombre de la playlist que contiene las musicas</param>
        /// <param name="funcSendProgress">Función a la que enviar información sobre la descarga</param>
        /// <param name="error">Parametro de salida que devuelve los errores obtenidos durante la descarga</param>
        /// <returns>True si y solo si se ha podido descargar la playlist, si no de vuelve False</returns>
        public bool DownloadPlayList(string downloadFolder, Action<double, string, string>? funcSendProgress, out string error) {
            if(!this.isValidPlayList) {
                error = Strings.playlisterror_invalid;
                return false;
            } else if(this.videoNames == null) {
                error = Strings.playlisterror_novideos;
                return false;
            }

            bool result = true;
            string innerError = "";

            try {
                ProcessStartInfo processStartInfo = new ProcessStartInfo() {
                    FileName = Strings.ytdlp_path,
                    Arguments = Strings.playlistdownload_ytdlp_args.Replace("%(folder)s", downloadFolder).Replace("%(url)s", this.url),
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

                        int videoIndex = 0;

                        while ((line = reader.ReadLine()) != null) {

                            if(line.StartsWith("[download] Destination: ") && videoIndex < videoNames.Length - 1) {
                                videoIndex++;
                            } else if (line.StartsWith("[download]") && line.Contains("ETA")) {
                                line = line.Replace("[download]", "").Trim();

                                string percentageStr = line.Substring(0, line.IndexOf("% of"));
                                string ETA = line.Substring(line.LastIndexOf("ETA ") + 4);

                                funcSendProgress(double.Parse(percentageStr, CultureInfo.InvariantCulture), 
                                                    ETA, this.videoNames[videoIndex - 1]);
                            }
                        }
                    });
                    
                    Thread errorThread = new Thread(() => {
                        StreamReader errorReader = process.StandardError;
                        string? line;

                        while ((line = errorReader.ReadLine()) != null) {
                            if (!line.ToLower().Contains("warning")) {
                                innerError += line + "\n";

                                result = false;
                            }
                        }
                    });

                    errorThread.Start();

                    if(funcSendProgress != null) {
                        outputThread.Start();
                        outputThread.Join();
                    }

                    errorThread.Join();

                    process.WaitForExit();
                } else {

                }
            } catch (Exception ex) {
                result = false;
                innerError += ex.Message;
            }

            if(funcSendProgress != null) {
                funcSendProgress(100.0, "00:00", this.videoNames.Last());
            }

            error = innerError;
            return result;
        }
    }
}
