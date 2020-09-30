using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Windows;
using MahApps.Metro.Controls.Dialogs;
using WpfNeverDied.Packages;

namespace WpfNeverDied
{
    public partial class MainWindow
    {
        public MainWindow()
        {
            InitializeComponent();
            PackagesTable.ItemsSource = GetPackages();
        }

        private List<Package> GetPackages()
        {
            return Assembly.GetExecutingAssembly().GetTypes()
                .Where(t => t.BaseType == typeof(Package))
                .Select(Activator.CreateInstance).Cast<Package>().ToList();
        }

        private List<Package> GetSelected()
        {
            return (PackagesTable.ItemsSource as IEnumerable<Package>)?.Where(p => p.IsSelected).ToList();
        }

        private async void OnInstall(object sender, RoutedEventArgs e)
        {
            var selected = GetSelected();

            if (selected == null || !selected.Any())
            {
                await this.ShowMessageAsync(null, "You haven't selected anything!");
                return;
            }

            InstallButton.IsEnabled = false;
            PackagesTable.IsEnabled = false;

            var progress = 100 / selected.Count() / 5;
            ProgressGauge.Value = progress;

            for (var i = 0; i < selected.Count(); i++)
            {
                try
                {
                    await selected[i].Install();
                }
                catch
                {
                    // TODO: Add to failed installations.
                }
                progress = (i + 1) * 100 / selected.Count();
                ProgressGauge.Value = progress;
            }

            await this.ShowMessageAsync(null, "The installation has been successfully completed!");
            InstallButton.IsEnabled = true;
            PackagesTable.IsEnabled = true;
            PackagesTable.ItemsSource = GetPackages();
            ProgressGauge.Value = 0;
        }

        private void OnRefresh(object sender, RoutedEventArgs e)
        {
            PackagesTable.ItemsSource = GetPackages();
        }
    }
}