from pathlib import Path
import argparse

import sys, platform, subprocess

def doesGitExist():
  system = platform.system()
  if system == "Linux":
    log = subprocess.run("command -v git >/dev/null 2>&1 || { echo 'error: git not found' >&2;}", shell=True)
    if log.stdout == b'error: git not found':
      return False
    return True
  elif system == "Windows":
    log = subprocess.run("where git >nul 2>&1 || ( echo error: git not found )", shell=True)
    if log.stdout == b'error: git not found':
      return False
    return True


def error_message(message: str) -> None:
  # \u001b[31m makes it red, \u001b[0m makes the color reset
  print("\u001b[31m" + message + "\u001b[0m")
  sys.exit(0)

def create_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(description="Install or uninstall auto-backup")
  parser.add_argument("--uninstall", action='store_true')

  return parser

args = create_parser().parse_args()

system = platform.system()

if system == "Linux":
  install_path = Path.home() / ".auto-backup"
  
  if not args.uninstall:
    if (install_path.exists() and (install_path / '.is-auto-backup').exists()):
      print("Already installed auto-backup")
    elif (install_path.exists() and not (install_path / '.is-auto-backup').exists() ):
      error_message("Could not create the ~/.auto-backup directory: directory already exists")
    else: # this else statement only runs if ~/.auto-backup doesn't exist
      install_path.mkdir(exist_ok=True)
      (install_path / ".is-auto-backup").touch()

      # add this git repository (and also leave out the .git directory and name it `backup`)
      if doesGitExist():
        if not (install_path / "backup").exists():
          print("Installing auto-backup...")

          subprocess.run("git clone --quiet --depth=1 --branch=main https://github.com/CrazyVideoGamer/auto-backup.git backup", cwd=install_path, shell=True)
          subprocess.run("rm -rf ./backup/.git", cwd=install_path, shell=True)

          print("Done!\n")
      else:
        error_message("Please install git using `sudo apt install git`")

      print(f"add `export PATH={str(install_path / 'auto-backup' / 'backup' / 'bin')}:$PATH` to ~/.bashrc to complete the installation")
  else:
    subprocess.run(f"rm -r {str(install_path)}", shell=True)

elif system == "Windows":
  install_path = Path.home() / "auto-backup"

  if not args.uninstall:

    if (install_path.exists() and (install_path / 'is-auto-backup').exists()):
      print("Already installed auto-backup")
    elif (install_path.exists() and not (install_path / 'is-auto-backup').exists() ):
      error_message(f"Could not create the {str(install_path)} directory: directory already exists")

    else:
      install_path.mkdir(exist_ok=True)
      (install_path / "is-auto-backup").touch() # note that it is "is-auto-backup", not ".is-auto-backup"

      # add this git repository (and also leave out the .git directory and name it `backup`)
      if doesGitExist():
        if not (install_path / "backup").exists():
          print("Installing auto-backup...")

          subprocess.run("git clone --quiet --depth=1 --branch=main https://github.com/CrazyVideoGamer/auto-backup.git backup", cwd=install_path, shell=True)
          subprocess.run("rm -rf ./backup/.git", cwd=install_path, shell=True)

          print("Done!\n")
      else:
        error_message("Please install git first (go to https://git-scm.com/) ")

      print(f"add {str(install_path / 'auto-backup' / 'backup' / 'bin')} to path to complete the installation")
  else:
    subprocess.run(f"rm -r {str(install_path)}", shell=True)
else:
  error_message("System {system} is not supported")