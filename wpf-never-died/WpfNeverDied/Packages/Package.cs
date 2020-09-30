using System;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace WpfNeverDied.Packages
{
    public enum PackageType
    {
        Design,
        Development,
        Gaming,
        Internet,
        Miscellaneous,
        Multimedia,
        Office,
    }

    public abstract class Package
    {
        private bool? _isInstalled;
        private bool? _isUpdated;

        public string Icon => $"Assets/Packages/{GetType().Name}.ico";

        public bool IsInstalled
        {
            get
            {
                if (_isInstalled.HasValue)
                {
                    return _isInstalled.Value;
                }

                _isInstalled = Directory.Exists(Root) && Directory.EnumerateFileSystemEntries(Root).Any();

                return _isInstalled.Value;
            }
        }

        public bool IsUpdated
        {
            get
            {
                if (_isUpdated.HasValue)
                {
                    return _isUpdated.Value;
                }

                _isUpdated = IsInstalled && new Version(GetAvailableVersion().Result).CompareTo(new Version(GetInstalledVersion().Result)) <= 0;

                return _isUpdated.Value;
            }
        }

        public bool IsSelected { get; set; } = false;
        
        public abstract PackageType Type { get; }
        public abstract string Name { get; }
        public abstract string Info { get; }
        public abstract string Root { get; }

        public abstract Task Install();
        protected abstract Task<string> GetInstalledVersion();
        protected abstract Task<string> GetAvailableVersion();
        protected abstract Task<string> Download();
    }
}