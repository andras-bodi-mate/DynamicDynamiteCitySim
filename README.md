# DynamicDynamiteCitySim

## How to set up environment:

1. **Download python** (version 3.9+):\
    Make sure to check "Add to PATH" in the installer

2. **Download pipx:**\
    Enter the following command in windows command prompt:
        `py -m pip install --user pipx`

    It is possible (even most likely) the above finishes with a WARNING looking similar to this:\
        `> WARNING: The script pipx.exe is installed in <USER folder>\AppData\Roaming\Python\Python3x\Scripts which is not on PATH`

    If so, navigate to the mentioned folder, allowing you to run the pipx executable directly. Enter the following line (even if you did not get the warning):\
        `.\pipx.exe ensurepath`
    
3. **Install poetry:**\
    Run the following command:
        `pipx install poetry`

4. I**nstall all dependencies:**\
    Navigate to the project directory and install all dependencies by running:
        `poetry install`

## How to run the program:

Start the program by running the ***"start.bat"*** batch file.