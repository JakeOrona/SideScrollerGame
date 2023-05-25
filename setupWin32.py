import cx_Freeze
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"


# Create the setup script
cx_Freeze.setup(
    name="Jump Nerd! Jump!",
    version="0.1",
    options={
        "build_exe": {
            "packages": ["pygame", "json", "random"],
            'include_files': [("gameLogic/saveScore.py", "gameLogic/saveScore.py"), "sprites", "resources", "gameData", "gameLogic"],}
            },
    executables = [cx_Freeze.Executable("myGameMain.py", base=base)]
)
