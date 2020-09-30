using System;
using System.Threading.Tasks;

namespace WpfNeverDied.Packages
{
    class VisualStudioEnterprise : Package
    {
        public override PackageType Type => PackageType.Development;
        public override string Name => "Visual Studio Enterprise";
        public override string Info => "...";
        public override string Root => Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86);

        public override Task Install()
        {
            throw new NotImplementedException();
        }

        protected override Task<string> Download()
        {
            throw new NotImplementedException();
        }

        protected override async Task<string> GetAvailableVersion()
        {
            await Task.Delay(new Random().Next(500, 5000));
            return "1.0.0.0";
        }

        protected override async Task<string> GetInstalledVersion()
        {
            await Task.Delay(new Random().Next(500, 5000));
            return "1.0.0.0";
        }
    }
}
