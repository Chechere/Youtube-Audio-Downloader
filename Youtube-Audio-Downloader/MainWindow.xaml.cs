using System.IO;
using System.Security.AccessControl;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using Microsoft.Win32;
using Path = System.IO.Path;
using ButtonBase = System.Windows.Controls.Primitives.ButtonBase;


namespace Youtube_Audio_Downloader;

/// <summary>
/// Interaction logic for MainWindow.xaml
/// </summary>
public partial class MainWindow : Window {
    string pathTempFolder;

    public MainWindow() {
        UpdateYtdlpWindow updater = new UpdateYtdlpWindow();
        updater.ShowDialog();

        this.InitializeComponent();
        
        this.pathTempFolder = CreateTempFolder();

        this.BTN_DOWNLOAD.Click += this.BTN_DOWNLOAD_Click;
        this.TB_URL.KeyDown += this.TB_URL_KeyDown;
    }

    /// <summary>
    /// Si se pulsa la tecla enter en TB_URL, ejecuta una pulsación en el boton BTN_DOWNLOAD
    /// </summary>    
    private void TB_URL_KeyDown(object sender, KeyEventArgs e) {
        if (e.Key == Key.Enter) {
            this.BTN_DOWNLOAD.RaiseEvent(new RoutedEventArgs(ButtonBase.ClickEvent));
        }
    }

    /// <summary>
    /// Inicia la descarga de un video ó una playlist, según la url insertada
    /// </summary>
    private void BTN_DOWNLOAD_Click(object sender, RoutedEventArgs e) {
        string url = TB_URL.Text;

        BTN_DOWNLOAD.IsEnabled = false;
        TB_URL.IsEnabled = false;
        Closing += Cancel_WindowClose;

        LB_INFO.Visibility = Visibility.Visible;

        if(url.Contains("/playlist?list=")) {
            LB_INFO.Content = Strings.mainwnd_searchingplaylist_text;
            _ = Task.Run(() => this.downloadPlayList(url)).ContinueWith((t) => this.FinishDownload());
        } else {
            LB_INFO.Content = Strings.mainwnd_searchingvideo_text;
            _ = Task.Run(() => this.downloadAudio(url)).ContinueWith((t) => this.FinishDownload());
        }
    }

    /// <summary>
    /// Descarga el audio de un video de Youtube
    /// </summary>
    /// <param name="url">URL del video de Youtube</param>
    private void downloadAudio(string url) {
        AudioDownloader ad = new AudioDownloader(url);

        if (!ad.IsValidVideo) {
            MessageBox.Show(Strings.videoerror_invalid, Strings.videoerror_getvideo_title,
                            MessageBoxButton.OK, MessageBoxImage.Error);
            return;
        }

        SaveFileDialog saveFileDialog = new SaveFileDialog() { 
            Title = Strings.video_wheresave_title,
            Filter = Strings.video_wheresave_filter,
            FileName = ad.Title
        };        

        if (saveFileDialog.ShowDialog() != true) {
            return;
        }

        string finalDir = saveFileDialog.FileName;
        string fileName = saveFileDialog.SafeFileName;

        this.Dispatcher.Invoke(() => {
            this.PB_DOWNLOAD.Visibility = Visibility.Visible;
            this.LB_PB_PERCENTAGE.Visibility = Visibility.Visible;
            this.LB_INFO.Content = Strings.preparingdownload_text;
        });

        string error;
        bool result = ad.DownloadAudio(this.pathTempFolder, fileName, showDownloadProgress, out error);

        _ = this.Dispatcher.Invoke(() => this.LB_INFO.Content = Strings.savingdownload_text);

        if (result) {
            string orig = Path.Combine(this.pathTempFolder, fileName);

            result = moveFile(orig, finalDir);

            if (result) {
                MessageBox.Show(Strings.video_succesfuldownload_text, Strings.video_succesfuldownload_title,
                                MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            error = Strings.videoerror_cannotsave.Replace("%(folder)s", finalDir);
            File.Delete(orig);
        }

        MessageBox.Show(Strings.error_download_text + error, Strings.error_download_title,
                        MessageBoxButton.OK, MessageBoxImage.Error);
    }

    /// <summary>
    /// Descarga el audio de todos los videos dentro de una playlist de Youtube
    /// </summary>
    /// <param name="url">URL de la playlist de Youtube</param>
    private void downloadPlayList(string url) {
        PlaylistDownloader pd = new PlaylistDownloader(url);

        if (!pd.IsValidPlayList) {
            MessageBox.Show(Strings.playlisterror_invalid, Strings.playlisterror_getplaylist_title,
                            MessageBoxButton.OK, MessageBoxImage.Error);
            return;
        }

        OpenFolderDialog ofd = new OpenFolderDialog() { Title = Strings.playlist_wheresave_title };

        if (ofd.ShowDialog() != true) {
            return;
        }

        this.Dispatcher.Invoke(() => {
            this.PB_DOWNLOAD.Visibility = Visibility.Visible;
            this.LB_PB_PERCENTAGE.Visibility = Visibility.Visible;
            this.LB_INFO.Content = Strings.preparingdownload_text;
        });

        string destFolder = Path.Combine(ofd.FolderName, pd.PlayListName);
        string playlistTempFolder = Path.Combine(this.pathTempFolder, pd.PlayListName);

        if (Directory.Exists(destFolder)) {
            MessageBoxResult mbres = MessageBox.Show(Strings.playlistwarning_folderalreadyexist_text.Replace("%(folder)s", destFolder), 
                                                        Strings.playlistwarning_folderalreadyexist_title,
                                                        MessageBoxButton.YesNo, MessageBoxImage.Warning);

            if (mbres != MessageBoxResult.Yes) {
                return;
            }

            try {
                DirectoryInfo di = new DirectoryInfo(destFolder);   // Comprobar que puede borrar la vieja carpeta
                DirectorySecurity ds = di.GetAccessControl();       // y mover la nueva.
            } catch(Exception) {
                MessageBox.Show(Strings.playlisterror_cannotdeletefolder_text,
                                Strings.playlisterror_cannotdeletefolder_title, 
                                MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }
        }

        string error;
        bool result = pd.DownloadPlayList(playlistTempFolder, showDownloadProgress, out error);

        _ = this.Dispatcher.Invoke(() => this.LB_INFO.Content = Strings.savingdownload_text);

        if (result) {
            result = moveDir(playlistTempFolder, destFolder);

            if (result) {
                MessageBox.Show(Strings.playlist_succesfuldownload_text, Strings.playlist_succesfuldownload_title,
                                MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            error = Strings.playlisterror_cannotsave.Replace("%(folder)s", destFolder);
        }

        MessageBox.Show(Strings.error_download_text + error, Strings.error_download_title,
                       MessageBoxButton.OK, MessageBoxImage.Error);
    }

    /// <summary>
    /// Si esta visible, muestra el progreso de la descarga del audio actual
    /// </summary>
    /// <param name="percentage">Porcentage de descarga realizado</param>
    /// <param name="ETA">Tiempo restante de descarga</param>
    /// <param name="fileName">Nombre del archivo al que se descarga el audio</param>
    private void showDownloadProgress(double percentage, string ETA, string fileName) {
        this.Dispatcher.Invoke(() => {
            this.PB_DOWNLOAD.Value = percentage;
            this.LB_PB_PERCENTAGE.Content = percentage + "%";

            if (fileName.Length > 20) {
                fileName = fileName.Substring(0, 20) + "... .mp3";
            }

            this.LB_INFO.Content = Strings.mainwnd_downloadprogress_text.Replace("%(file)s", fileName).Replace("%(time)s", ETA);
        });
    }

    /// <summary>
    /// Oculta todos los elementos de información de descarga, 
    /// libera el TB_URL y el BTN_DOWNLOAD y vuelve a permitir 
    /// al usuario poder cerrar la ventana.
    /// </summary>
    /// <remarks> Usar solo cuando la descarga este completamente finalizada </remarks>
    private void FinishDownload() {
        this.Dispatcher.Invoke(() => {
            this.BTN_DOWNLOAD.IsEnabled = true;
            this.TB_URL.IsEnabled = true;
            this.Closing -= this.Cancel_WindowClose;

            this.LB_INFO.Visibility = Visibility.Hidden;
            this.LB_PB_PERCENTAGE.Visibility = Visibility.Hidden;
            this.PB_DOWNLOAD.Visibility = Visibility.Hidden;
        });
    }

    /// <summary>
    /// Evita que la ventana pueda ser cerrada de manera normal.
    /// </summary>    
    private void Cancel_WindowClose(object? sender, System.ComponentModel.CancelEventArgs e) {
        e.Cancel = true;
    }

    /// <summary>
    /// Si no existe, crea la carpeta temporal del programa
    /// </summary>
    /// <returns>La ruta a la carpeta temporal</returns>
    private string CreateTempFolder() {
        string path = Path.Combine(Path.GetTempPath(), Strings.prog_tempfolder_name);

        if (!Directory.Exists(path)) {
            Directory.CreateDirectory(path);
        }

        return path;
    }

    /// <summary>
    /// Mueve un archivo de un lugar a otro.
    /// </summary>
    /// <remarks>Si en el destino ya existe un archivo que se llama igual, es sobreescrito</remarks>
    /// <param name="orig">Ruta al archivo de origen</param>
    /// <param name="dest">Ruta al lugar de destino</param>
    /// <returns>True si y solo si ha podido realizar el movimiento, sino False</returns>
    private bool moveFile(string orig, string dest) {
        try {
            File.Move(orig, dest, true);
        } catch (IOException) {
            return false;
        }

        return true;
    }

    /// <summary>
    /// Mueve una carpeta de un lugar a otro
    /// </summary>
    /// <remarks>Si en el destino ya existe una carpeta que se llama igual, es sobreescrita</remarks>
    /// <param name="orig">Ruta a la carpeta de origen</param>
    /// <param name="dest">Ruta a la carpeta de destino</param>
    /// <returns>True si y solo si ha podido realizar el movimiento, sino False</returns>
    private bool moveDir(string orig, string dest) {
        try {
            if (Directory.Exists(dest)) {
                Directory.Delete(dest);
            }

            Directory.Move(orig, dest);
        } catch (IOException) {
            return false;
        }

        return true;
    }
}