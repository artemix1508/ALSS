# Artemix-Linux-Setup-Script [WIP]
This easily customizable setup script is designed to help you install the essentials for your hardware and distribution.

# Dependencies:
`ubuntu-drivers-common` - only needed on Linux Mint/Ubuntu, used for recommended NVIDIA driver detection

`python` - of course, unless you compile it

To install it:
`sudo apt install ubuntu-drivers-common`

# Running the script:
Download `alss.py` and `config.json` (they need to be in the same folder), open a terminal in that directory, then run:

python alss.py

That's it!

## Dry run
Want to see what would be installed without actually installing anything? Run:

python alss.py --dry-run


## Customizing what gets installed
Edit `config.json` to change which packages, GPU drivers, or package manager commands the script uses. No need to touch the Python code.

# Compiling
If you want to, you can compile it using [PyInstaller](https://pyinstaller.org/en/stable/) or something different.
