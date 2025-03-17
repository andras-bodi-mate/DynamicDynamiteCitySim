# DynamicDynamiteCitySim

## Környezet beállítása:

1. **Python letöltése** (3.9-es vagy újabb verzió):\
    Győződj meg róla, hogy a telepítőben bejelölöd az "Add to PATH" (Hozzáadás a PATH-hoz) lehetőséget.

2. **Pipx letöltése:**\
    A következő parancsot írd be a Windows parancssorba:
    ```cmd
    py -m pip install --user pipx
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
    Futtasd a következő parancsot:
    ```cmd
    pipx install poetry
    ```

4. **Összes függőség telepítése:**\
    Navigálj a projekt könyvtárába, és telepítsd az összes függőséget a következő parancs futtatásával:
    ```cmd
    poetry install
    ```

## A program futtatása:

Indítsd el a programot a ***"start.bat"*** batch fájl futtatásával.
