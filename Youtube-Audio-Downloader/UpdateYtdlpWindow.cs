using System.Diagnostics;
using System.Windows;

namespace Youtube_Audio_Downloader {
    /// <summary>
    /// Lógica de interacción para updateYtdlpWindow.xaml
    /// </summary>
    public partial class UpdateYtdlpWindow : Window {
        public UpdateYtdlpWindow() {
            InitializeComponent();

            Closing += UpdateYtdlpWindow_Closing;
            Loaded += UpdateYtdlpWindow_Loaded;
        }

        /// <summary>
        /// Ejecuta el comando para comprobar y descargar una actualización del programa.
        /// Tras esta se cierra la ventana
        /// </summary>        
        private void UpdateYtdlpWindow_Loaded(object sender, RoutedEventArgs e) {
            ProcessStartInfo processStartInfo = new ProcessStartInfo() {
                FileName = Strings.ytdlp_path,
                Arguments = Strings.update_ytdlp_args,
                CreateNoWindow = true,
                UseShellExecute = false,
            };

            Process? updater = Process.Start(processStartInfo);

            if(updater != null) {
                Task t = updater.WaitForExitAsync();
                t.ContinueWith((t) => {
                    Dispatcher.Invoke(() => {
                        Closing -= UpdateYtdlpWindow_Closing;
                        Close();
                    });
                });
            }
        }

        /// <summary>
        /// Evita que se pueda cerrar la ventana mientras se busca y descargan actualizaciones
        /// </summary>        
        private void UpdateYtdlpWindow_Closing(object? sender, System.ComponentModel.CancelEventArgs e) {
            e.Cancel = true;
        }
    }
}
