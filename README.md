# DynamicDynamiteCitySim

## Környezet beállítása:

1. **Python letöltése** (3.9-es vagy újabb verzió):\
    Győződj meg róla, hogy a telepítőben bejelölöd az "Add to PATH" (Hozzáadás a PATH-hoz) lehetőséget.

2. **Pipx letöltése:**\
    A következő parancsot írd be a Windows parancssorba:
    ```cmd
    python -m pip install --user pipx
    ```

    Valószínű, hogy a folyamat egy figyelmeztetéssel fog végződni, ami hasonlóan néz ki, mint ez:
    ```cmd
    `> WARNING: The script pipx.exe is installed in <USER folder>\AppData\Roaming\Python\Python3x\Scripts which is not on PATH`
    ```

    Ha ez történik, navigálj az említett mappába, hogy közvetlenül futtatni tudd a pipx végrehajtható fájlt. Írd be a következő parancsot (akkor is, ha nem kaptál figyelmeztetést):
    ```cmd
    .\pipx.exe ensurepath
    ```

3. **Poetry telepítése:**\
    Nyiss meg egy új terminált és futtasd a következő parancsot:
    ```cmd
    pipx install poetry
    ```

4. **Összes függőség telepítése:**\
    Navigálj a projekt könyvtárába, és telepítsd az összes függőséget a következő parancs futtatásával:
    ```cmd
    poetry install
    ```
    Amennyiben ez nem működik manuálisan töltsd le a szükséges függőségeket.

## A program futtatása:

Indítsd el a programot a ***"build"*** mappában található ***"start.bat"*** fájllal vagy a ***"src"*** mappában lévő ***"main.py"*** python fájl futtatásával.

## A program működése
1. **Adatok importálsa**
A programba ha meglévő várost szeretnél importálni akkor válaszd ki az adatok importálása gombot. Majd add meg a szükséges fájlokat
2. **A program irányítása**
A program irányításához használd a **'W','A','S','D'** gombokat a billentyűzeten körültekintéshez pedig az egeret használd.
A programon belül található gombok eléréséhez először a **'esc'** gombal érd el az egeret majd kattints a megfelelő gombra.
3. **A program kimenetele**
A program kimeneetelét minden hónapváltás után a projekt out mappájáan találod.
