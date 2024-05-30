import subprocess
import sys

def get_version():
    """读取版本号"""
    with open('version.txt', 'r') as file:
        return file.read().strip()

def compile_translations():
    """编译翻译文件"""
    subprocess.run([sys.executable, 'setup.py', 'build'], check=True)

def package_with_pyinstaller(version):
    """使用 PyInstaller 打包"""
    icon_path = 'assets/icon.ico'
    main_script = 'src/main.py'
    output_name = f"WindowsFolderRestore_{version}"
    subprocess.run([
        'pyinstaller',
        '--onefile',
        '--name', output_name,
        '--icon', icon_path,
        main_script
    ], check=True)

def main():
    version = get_version()
    print(f"Current version: {version}")

    compile_translations()
    package_with_pyinstaller(version)

if __name__ == '__main__':
    main()
