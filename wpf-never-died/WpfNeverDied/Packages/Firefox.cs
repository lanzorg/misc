using System;
using System.Threading.Tasks;

namespace WpfNeverDied.Packages
{
    public class Firefox : Package
    {
        public override PackageType Type => PackageType.Internet;
        public override string Name => "Firefox";
        public override string Info => "Open-source web browser made for developers from Mozilla";
        public override string Root => Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86);

        protected override async Task<string> GetInstalledVersion()
        {
            await Task.Delay(new Random().Next(500, 5000));
            return "0.1.0.0";
        }

        protected override async Task<string> GetAvailableVersion()
        {
            await Task.Delay(new Random().Next(500, 5000));
            return "1.0.0.0";
        }

        protected override Task<string> Download()
        {
            throw new NotImplementedException();
        }

        public override async Task Install()
        {
            await Task.Delay(new Random().Next(500, 5000));
        }
    }
}