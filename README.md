# stock-manager

[![Release](https://img.shields.io/github/v/release/edouardbruelhart/stock-manager)](https://img.shields.io/github/v/release/edouardbruelhart/stock-manager)
[![Build status](https://img.shields.io/github/actions/workflow/status/edouardbruelhart/stock-manager/main.yml?branch=main)](https://github.com/edouardbruelhart/stock-manager/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/edouardbruelhart/stock-manager)](https://img.shields.io/github/commit-activity/m/edouardbruelhart/stock-manager)

- **Github repository**: <https://github.com/edouardbruelhart/stock-manager/>

## Version Française

Un petit logiciel de gestion de stock pour brasserie codé en python

### Fonctionnalités:

- Créer de nouvelles recettes avec différents ingrédients sous forme de cuvées
- Une fois les recettes créées, permet d'ajouter des cuvées et de générer une liste de commande automatique datée. Arrondit la commande à la plus petite unité disponible (à indiquer lors de l'ajout de l'ingrédient) et gère la quantité de surplus des commandes précédentes
- Lors du brassage, permet de retirer les cuvées brassées du stock facilement

Le logiciel génère des fichiers CSV dans le dossier sélectionné. Cela permet, par exemple, d'ajouter ou d'enlever du matériel dans la colonne "quantite_libre" si celui-ci a été acheté ou utilisé dans un autre cadre que celui prévu par l'application.

### Comment l'utiliser:

- **Windows:** simplement télécharger le fichier `stock_manager.exe` dans l'onglet `Releases` puis l'exécuter.
- **Linux:** Télécharger le fichier `stock_manager` dans l'onglet `Releases`, puis ajouter le droit d'exécution :

  ```bash
  sudo chmod +x stock_manager
  ```

Il sera ensuite exécutable. Si vous voulez l'exécuter par ligne de commande, vous pouvez simplement le déplacer dans un dossier du PATH (par exemple `/usr/local/bin`). Il vous suffira ensuite de taper :

```bash
stock_manager
```

dans bash.

- **MacOS:** Pas d'exécutable disponible pour l'instant. Se référer à la méthode générale. Une fois le projet mis en place, il est possible de générer un exécutable avec la commande `pyinstaller`.
- **Méthode générale:** clonez le projet, puis installez un environnement avec `poetry` :

  ```bash
  poetry install
  ```

  Activez ensuite l'environnement :

  ```bash
  poetry shell
  ```

  puis exécutez le script `main.py` :

  ```bash
  python main.py
  ```

  Si vous n'avez pas poetry, vous pouvez l'installer avec la commande :

  ```bash
  pipx install poetry
  ```

## English Version

A small stock management software for breweries coded in Python

### Features:

- Create new recipes with different ingredients in the form of batches
- Once the recipes are created, allows adding batches and generating an automatic dated order list. Rounds the order to the smallest available unit (to be specified when adding the ingredient) and manages the surplus quantity from previous orders
- During brewing, allows easy removal of brewed batches from stock

The software generates CSV files in the selected folder. This allows, for example, adding or removing equipment in the "quantite_libre" column if it has been purchased or used for purposes other than those intended by the application.

### How to use:

- **Windows:** Simply download the `stock_manager.exe` file from the "releases" tab and run it.
- **Linux:** Download the `stock_manager` file from the "releases" tab, then add execution rights:

  ```bash
  sudo chmod +x stock_manager
  ```

  It will then be executable. If you want to run it from the command line, you can simply move it to a folder in the PATH (e.g., `/usr/local/bin`). Then you just need to type:

  ```bash
  stock_manager
  ```

  in bash.

- **MacOS:** No executable available for now. Refer to the general method. Once the project is set up, it is possible to generate an executable with the `pyinstaller` command.
- **General method:** Clone the project, then set up an environment with `poetry`:

  ```bash
  poetry install
  ```

  Then activate the environment:

  ```bash
  poetry shell
  ```

  and run the `main.py` script:

  ```bash
  python main.py
  ```

  If you do not have poetry, you can install it with the command:

  ```bash
  pipx install poetry
  ```

```

```

```

```
