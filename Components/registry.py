import winreg

class Registry:

    @staticmethod
    def add(app_name, app_path):
        """Add an entry to the list of installed programs"""
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_WRITE)
        subkey = winreg.CreateKey(key, app_name)
        winreg.SetValueEx(subkey, "DisplayName", 0, winreg.REG_SZ, app_name)
        winreg.SetValueEx(subkey, "UninstallString", 0, winreg.REG_SZ, f"{app_path} /uninstall")
        winreg.CloseKey(subkey)
        winreg.CloseKey(key)
    
    @staticmethod
    def remove(app_name):
        """Remove an entry from the list of installed programs"""
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_WRITE)
        winreg.DeleteKey(key, app_name)
        winreg.CloseKey(key)
    
    @staticmethod
    def is_installed(app_name):
        """Check if the specified program is installed"""
        # Open the Uninstall key for reading
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
        
        # Check if the application subkey exists under the Uninstall key
        subkey_path = app_name
        try:
            winreg.OpenKey(key, subkey_path, 0, winreg.KEY_READ)
            return True  # Application is installed
        except FileNotFoundError:
            return False  # Application is not installed
        finally:
            winreg.CloseKey(key)
    
    @staticmethod
    def get_uninstall_string(app_name):
        """Get the UninstallString for the specified program"""
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
        
        subkey_path = app_name
        try:
            subkey = winreg.OpenKey(key, subkey_path, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(subkey, "UninstallString")
            return value
        except FileNotFoundError:
            return None
        finally:
            winreg.CloseKey(key)
            