import ctypes
import os
import sys
import winreg

class Registry:
    @staticmethod
    def add(app_name: str, app_path: str) -> None:
        """Add an entry to the list of installed programs."""
        key_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
        subkey = winreg.CreateKey(key, app_name)
        winreg.SetValueEx(subkey, 'DisplayName', 0, winreg.REG_SZ, app_name)
        winreg.SetValueEx(subkey, 'UninstallString', 0, winreg.REG_SZ, f'{app_path} /uninstall')
        winreg.CloseKey(subkey)
        winreg.CloseKey(key)

    @staticmethod
    def remove(app_name: str) -> None:
        """Remove an entry from the list of installed programs."""
        key_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
        winreg.DeleteKey(key, app_name)
        winreg.CloseKey(key)

    @staticmethod
    def is_installed(app_name: str) -> bool:
        """Check if the specified program is installed."""
        key_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)

        subkey_path = app_name
        try:
            winreg.OpenKey(key, subkey_path, 0, winreg.KEY_READ)
            return True  # Application is installed
        except FileNotFoundError:
            return False  # Application is not installed
        finally:
            winreg.CloseKey(key)

    @staticmethod
    def get_uninstall_string(app_name: str) -> str:
        """Get the UninstallString for the specified program."""
        key_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)

        subkey_path = app_name
        try:
            subkey = winreg.OpenKey(key, subkey_path, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(subkey, 'UninstallString')
            return value
        except FileNotFoundError:
            return None
        finally:
            winreg.CloseKey(key)

def isAdmin() -> bool:
    return ctypes.windll.shell32.IsUserAnAdmin()

def runAsAdmin() -> bool:
    # Re-launch the script with admin privileges
    params = f'\'{sys.executable}\' \'{__file__}\''
    result = ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, params, None, 1)
    return result > 32

if __name__ == '__main__':
    add = True
    remove = True

    if not isAdmin():
        runAsAdmin()
    
    if add:
        Registry.add('MyApp', r'C:\Program Files\MyApp\MyApp.exe')
        print('Installed:', Registry.isInstalled('MyApp'))
        print('Uninstall String:', Registry.getUninstallString('MyApp'))

    if remove:
        Registry.remove('MyApp')
        print('Installed:', Registry.isInstalled('MyApp'))
        print('Uninstall String:', Registry.getUninstallString('MyApp'))

    # Installed: True
    # Uninstall String: C:\Program Files\MyApp\MyApp.exe /uninstall
    # Installed: False
    # Uninstall String: None