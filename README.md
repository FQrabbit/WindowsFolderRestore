# WindowsFolderRestore
Solving problems with certain folder permissions after Windows reinstallation  
解决重新安装 Windows 后某些文件夹权限的问题

## 手动编译注意事项（适用于 Windows）

#### 依赖项

在运行 `build.py` 之前，请确保你的环境中已经安装了以下依赖项：

1. [**Python**](https://www.python.org/downloads/)：确保安装了 Python 3.6 或更高版本。
2. **PyInstaller**：用于打包 Python 脚本为可执行文件。
   - 安装命令：在cmd或 PowerShell 中运行：
     ```bash
     pip install pyinstaller
     ```
3. **msgfmt**：~~(如果你不需要翻译文件的话可以不安装)~~

   ##### 方法一：使用 MSYS2
   
   MSYS2 是一个轻量级的 POSIX 仿真环境，可以安装许多 Unix 工具，包括 gettext。
   
   1. **下载并安装 MSYS2**：
      - 从 [MSYS2 官网](https://www.msys2.org/) 下载并安装 MSYS2。
   
   2. **安装 gettext**：
      - 打开 MSYS2 MSYS 命令行窗口，运行以下命令：
        ```bash
        pacman -S mingw-w64-x86_64-gettext
        ```
   
   3. **将 MSYS2 路径添加到系统 PATH**：
      - 将 MSYS2 的 `mingw64/bin` 目录添加到系统环境变量 PATH 中，以便在命令提示符中   使用 `msgfmt`。
   
   ##### 方法二：使用 GnuWin32
   
   GnuWin32 提供了许多 GNU 工具的 Windows 端口，包括 gettext。
   
   1. **下载并安装 GnuWin32 的 gettext**：
      - 从 [GnuWin32 gettext 下载页面](http://gnuwin32.sourceforge.net/packages/gettext.htm) 下载并安装 gettext 的二   进制和开发包。
   
   2. **将 GnuWin32 路径添加到系统 PATH**：
      - 将 GnuWin32 的 `bin` 目录添加到系统环境变量 PATH 中，以便在命令提示符中(cmd)使用`msgfmt`。
 
#### 项目结构

确保项目目录结构如下：

```
WindowsFolderRestore/
├── assets/
│   └── icon.ico
├── src/
│   └── main.py
├── version.txt
└── build.py
```

#### 编译步骤

1. **确保依赖项已安装**：按照上面的依赖项列表安装所需的软件包。
2. **检查项目结构**：确认项目目录结构与上述结构一致。
3. **运行编译脚本**：在项目根目录下运行以下命令：

   ```bash
   python build.py
   ```


---
编译后可执行文件图标来源于[WindowsIcons](https://github.com/HaydenReeve/WindowsIcons)  
The compiled executable file icon is derived from the
[WindowsIcons](https://github.com/HaydenReeve/WindowsIcons)