# To generate binaries for this script, run "pyinstaller --onefile main.py"
# Generated binaries are made for the native system where the pyinstaller command is run.

import csv
import json
import math
import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from typing import Any

import pandas as pd


class HomeWindow(tk.Frame):
    def __init__(self, parent: tk.Tk, *args: Any, **kwargs: Any):
        """
        Initializes an instance of the class.

        Args:
            parent(tk.Tk): The parent widget or window where this frame will be placed.
            csv_path(str): CSV path and name.

        Returns:
            None
        """

        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create the buttons
        self.label = tk.Label(self, text="Sélectionnez une action à exécuter:")
        self.label.pack()

        self.data_path = tk.Button(self, text="dossier", width=30, command=self.data_folder)
        self.data_path.pack()

        self.button_add = tk.Button(self, text="Générer une liste de commande", width=30, command=self.launch_add)

        self.button_remove = tk.Button(self, text="Retirer une cuvée du stock", width=30, command=self.launch_remove)

        self.button_add_recipe = tk.Button(
            self, text="Entrer une nouvelle recette", width=30, command=self.launch_add_recipe
        )

        try:
            with open("user_data.json") as file:
                data = json.load(file)["data_path"]
                self.add_folder(data)

        except FileNotFoundError:
            self.label.config(text="Sélectionnez le dossier de stockage des données:")

    def data_folder(self) -> None:
        """
        Asks the user to choose the data folder where stock data will be stored.

        Args:
            None

        Returns:
            None
        """

        data_folder = filedialog.askdirectory()
        if data_folder:
            parts = data_folder.split("/")
            folder = parts[-1]
            self.data_path.config(text=f"dossier sélectionné: {folder}")
            self.label.config(text="Sélectionnez une action à exécuter:")
            data = {"data_path": data_folder}
            with open("user_data.json", "w") as file:
                json.dump(data, file)
            # Check if CSV files exist
            self.check_csv_files(data_folder)
            self.button_add.pack()
            self.button_remove.pack()
            self.button_add_recipe.pack()

    def add_folder(self, data: str) -> None:
        """
        If user has already selected a data folder, adds it automatically.

        Args:
            None

        Returns:
            None
        """
        parts = data.split("/")
        folder = parts[-1]
        self.data_path.config(text=f"dossier selectionné: {folder}")
        # Check if CSV files exist
        self.check_csv_files(data)
        self.button_add.pack()
        self.button_remove.pack()
        self.button_add_recipe.pack()

    def check_csv_files(self, data_folder: str) -> None:
        # List of specific CSV filenames to check
        csv_filenames = ["recettes.csv", "ingredients.csv"]

        # List all files in the folder
        files = os.listdir(data_folder)

        # Check if each specific CSV filename is present
        missing_files = [filename for filename in csv_filenames if filename not in files]

        if missing_files:
            self.create_missing_csv_files(data_folder, missing_files)

    def create_missing_csv_files(self, folder_path: str, missing_files: list) -> None:
        # Create missing CSV files
        for filename in missing_files:
            file_path = os.path.join(folder_path, filename)
            if filename == "recettes.csv":
                with open(file_path, "w", newline="") as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(["nom_biere", "nombre_en_stock"])
            elif filename == "ingredients.csv":
                with open(file_path, "w", newline="") as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(
                        [
                            "type_ingredient",
                            "ingredient",
                            "quantite_reservee",
                            "quantite_libre",
                            "quantite_totale",
                            "arrondi_commande",
                        ]
                    )

    def launch_add(self) -> None:
        """
        Returns to main script which option did the user choose.

        Args:
            None

        Returns:
            None
        """
        add = tk.Toplevel(root)
        add.title("Sélectionnez les bières à commander")
        # Show the window for a new batch
        addBeer(add, root)

    def launch_remove(self) -> None:
        """
        Returns to main script which option did the user choose.

        Args:
            None

        Returns:
            None
        """
        remove = tk.Toplevel(root)
        remove.title("Sélectionnez les bières à retirer du stock")
        # Show the window for a new batch
        removeBeer(remove, root)

    def launch_add_recipe(self) -> None:
        """
        Returns to main script which option did the user choose.

        Args:
            None

        Returns:
            None
        """
        add_recipe = tk.Toplevel(root)
        add_recipe.title("Ajouter une recette")
        add_recipe.minsize(600, 600)
        # Show the window for a new batch
        addRecipe(add_recipe, root)


class addBeer:
    def __init__(self, add: tk.Toplevel, root: tk.Tk):
        """
        Initializes an instance of the class.

        Args:
            add(tk.Toplevel): The parent widget where this frame will be placed.
            root(tk.Tk): The root window to perform actions on it.

        Returns:
            None
        """
        self.add = add
        self.root = root

        # Make CsvWindow wait for AskBoxPrefixWindow result
        self.root.withdraw()

        self.add.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Retrieve path to data folder
        with open("user_data.json") as file:
            self.data = json.load(file)["data_path"]

        # Load recipe CSV ad dataframe
        path_recettes = self.data + "/recettes.csv"
        path_ingredients = self.data + "/ingredients.csv"
        self.df_recettes = pd.read_csv(path_recettes)
        self.df_ingredients = pd.read_csv(path_ingredients)

        # Create the GUI elements
        label = tk.Label(self.add, text="Sélectionnez ce que vous souhaitez ajouter au stock:", pady=10)
        label.pack()

        self.text_entries = {}  # Dictionary to store references to text entry widgets

        for _, (_, row) in enumerate(self.df_recettes.iterrows()):
            frame = tk.Frame(self.add)
            frame.pack(fill=tk.X, padx=5, pady=5)

            beer_name = row["nom_biere"]
            if math.isnan(row["nombre_en_stock"]):
                label_text = f"{beer_name} (aucune en stock):"
            else:
                number = int(row["nombre_en_stock"])
                label_text = f"{beer_name} ({number} en stock):"

            label = tk.Label(frame, text=label_text)
            label.pack(side=tk.LEFT)

            entry = tk.Entry(frame)
            entry.pack(side=tk.RIGHT)

            self.text_entries[beer_name] = entry  # Store entry widget with beer name as key

        self.submit_button = tk.Button(
            self.add,
            text="Ajouter au stock et générer la liste de commande",
            width=40,
            command=self.submit_command,
            pady=10,
        )
        self.submit_button.pack()

    def on_exit(self) -> None:
        """
        Defines behaviour when user quits this window (by x button or specified button).

        Args:
            None

        Returns:
            None
        """
        self.add.destroy()
        self.root.deiconify()

    def submit_command(self) -> None:
        """
        Asks the path to input CSV.

        Args:
            None

        Returns:
            None
        """
        # Initialize an empty DataFrame with the required columns
        df_command = pd.DataFrame(
            columns=["ingredient", "quantite_brute", "quantite_libre", "arrondi_commande", "quantite", "portions"]
        )

        # Replace annoying NaN by 0 to avoid calculation errors
        self.df_recettes.fillna(0, inplace=True)
        self.df_ingredients.fillna(0, inplace=True)

        for beer_name, entry in self.text_entries.items():
            # Retrieve the number chosen by the user
            stock_value = int(entry.get())

            # Update the corresponding row in recipes
            self.df_recettes.loc[self.df_recettes["nom_biere"] == beer_name, "nombre_en_stock"] += stock_value

            # Update the corresponding ingredients in ingredients
            for _, row in self.df_ingredients.iterrows():
                # Retrieve ingredient and arrondi
                ingredient = row["ingredient"]
                round_value = row["arrondi_commande"]
                free_quantity = row["quantite_libre"]

                # Retrieve quantity for the selected recipe
                quantity_series = self.df_recettes.loc[self.df_recettes["nom_biere"] == beer_name, ingredient]

                # Extract the scalar value from the Series and handle NaN values
                if not quantity_series.empty and not math.isnan(quantity_series.iloc[0]):
                    quantity = quantity_series.iloc[0]
                else:
                    quantity = 0

                # Update the quantite_reservee column in the ingredient dataframe
                self.df_ingredients.loc[self.df_ingredients["ingredient"] == ingredient, "quantite_reservee"] += (
                    stock_value * quantity
                )

                # Update the command DataFrame without duplicates
                if ingredient in df_command["ingredient"].values and quantity != 0:
                    df_command.loc[df_command["ingredient"] == ingredient, "quantite_brute"] += stock_value * quantity
                elif quantity != 0:
                    new_row = pd.DataFrame(
                        {
                            "ingredient": [ingredient],
                            "quantite_brute": [stock_value * quantity],
                            "quantite_libre": [free_quantity],
                            "arrondi_commande": [round_value],
                            "quantite": 0,
                            "portions": 0,
                        }
                    )
                    df_command = pd.concat([df_command, new_row], ignore_index=True)
        # Round quantite to match command quantity and make portions, then add the surplus quantity to quantite_libre
        for _, row in df_command.iterrows():
            ingredient = row["ingredient"]
            if row["quantite_brute"] > row["quantite_libre"]:
                quantite = (
                    math.ceil((row["quantite_brute"] - row["quantite_libre"]) / row["arrondi_commande"])
                    * row["arrondi_commande"]
                )
                portion = math.ceil((row["quantite_brute"] - row["quantite_libre"]) / row["arrondi_commande"])
                df_command.loc[df_command["ingredient"] == ingredient, "quantite"] = quantite
                df_command.loc[df_command["ingredient"] == ingredient, "portions"] = portion
                quantite_libre = quantite - (row["quantite_brute"] - row["quantite_libre"])
                print(
                    f"quantité: {quantite}, quantité brute: {row['quantite_brute']}, quantité libre: {row['quantite_libre']}"
                )
            else:
                quantite_libre = row["quantite_libre"] - row["quantite_brute"]
            self.df_ingredients.loc[self.df_ingredients["ingredient"] == ingredient, "quantite_libre"] = quantite_libre

        # Update quantite_totale
        for _, row in self.df_ingredients.iterrows():
            ingredient = row["ingredient"]
            self.df_ingredients.loc[self.df_ingredients["ingredient"] == ingredient, "quantite_totale"] = (
                row["quantite_reservee"] + row["quantite_libre"]
            )

        # Drop the arrondi_commande column and the empty rows (due to quantite_libre > quantite_brute)
        df_command = df_command.drop(columns=["arrondi_commande", "quantite_brute", "quantite_libre"])
        df_command = df_command[df_command["quantite"] != 0]

        # Write command file
        csv_command = self.data + f"/commande_{datetime.now().strftime('%Y%d%m%H%M')}.csv"
        df_command.to_csv(csv_command, index=False)

        # Write stock in recettes
        csv_recettes = self.data + "/recettes.csv"
        self.df_recettes.to_csv(csv_recettes, index=False)

        # Write stock in ingredients
        csv_ingredients = self.data + "/ingredients.csv"
        self.df_ingredients.to_csv(csv_ingredients, index=False)

        # Quit command window and show homepage
        self.add.destroy()
        self.root.deiconify()


class removeBeer(tk.Frame):
    def __init__(self, remove: tk.Toplevel, root: tk.Tk):
        """
        Initializes an instance of the class.

        Args:
            add(tk.Toplevel): The parent widget where this frame will be placed.
            root(tk.Tk): The root window to perform actions on it.

        Returns:
            None
        """
        self.remove = remove
        self.root = root

        # Make CsvWindow wait for AskBoxPrefixWindow result
        self.root.withdraw()

        self.remove.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Retrieve path to data folder
        with open("user_data.json") as file:
            self.data = json.load(file)["data_path"]

        # Load recipe CSV ad dataframe
        path_recettes = self.data + "/recettes.csv"
        path_ingredients = self.data + "/ingredients.csv"
        self.df_recettes = pd.read_csv(path_recettes)
        self.df_ingredients = pd.read_csv(path_ingredients)

        # Create the GUI elements
        label = tk.Label(self.remove, text="Sélectionnez ce que vous souhaitez retirer du stock:", pady=10)
        label.pack()

        self.text_entries = {}  # Dictionary to store references to text entry widgets

        for _, (_, row) in enumerate(self.df_recettes.iterrows()):
            frame = tk.Frame(self.remove)
            frame.pack(fill=tk.X, padx=5, pady=5)

            beer_name = row["nom_biere"]
            if math.isnan(row["nombre_en_stock"]):
                label_text = f"{beer_name} (aucune en stock):"
            else:
                number = int(row["nombre_en_stock"])
                label_text = f"{beer_name} ({number} en stock):"

            label = tk.Label(frame, text=label_text)
            label.pack(side=tk.LEFT)

            entry = tk.Entry(frame)
            entry.pack(side=tk.RIGHT)

            self.text_entries[beer_name] = entry  # Store entry widget with beer name as key

        self.submit_button = tk.Button(
            self.remove, text="Enlever la sélection du stock", width=40, command=self.remove_selected, pady=10
        )
        self.submit_button.pack()

        self.error_label = tk.Label(self.remove, text="")
        self.error_label.pack()

    def on_exit(self) -> None:
        """
        Defines behaviour when user quits this window (by x button or specified button).

        Args:
            None

        Returns:
            None
        """
        self.remove.destroy()
        self.root.deiconify()

    def remove_selected(self) -> None:
        """
        Asks the path to input CSV.

        Args:
            None

        Returns:
            None
        """

        # Replace annoying NaN by 0 to avoid calculation errors
        self.df_recettes.fillna(0, inplace=True)
        self.df_ingredients.fillna(0, inplace=True)

        for beer_name, entry in self.text_entries.items():
            # Retrieve the number chosen by the user
            stock_value = int(entry.get())

            # Update the corresponding row in recipes
            self.df_recettes.loc[self.df_recettes["nom_biere"] == beer_name, "nombre_en_stock"] -= stock_value

            # Update the corresponding ingredients in ingredients
            for _, row in self.df_ingredients.iterrows():
                # Retrieve ingredient and arrondi
                ingredient = row["ingredient"]

                # Retrieve quantity for the selected recipe
                quantity_series = self.df_recettes.loc[self.df_recettes["nom_biere"] == beer_name, ingredient]

                # Extract the scalar value from the Series and handle NaN values
                if not quantity_series.empty and not math.isnan(quantity_series.iloc[0]):
                    quantity = quantity_series.iloc[0]
                else:
                    quantity = 0

                # Update the quantite_reservee column in the ingredient dataframe
                self.df_ingredients.loc[self.df_ingredients["ingredient"] == ingredient, "quantite_reservee"] -= (
                    stock_value * quantity
                )

        # Update quantite_totale
        for _, row in self.df_ingredients.iterrows():
            ingredient = row["ingredient"]
            self.df_ingredients.loc[self.df_ingredients["ingredient"] == ingredient, "quantite_totale"] = (
                row["quantite_reservee"] + row["quantite_libre"]
            )

        # Write stock in recettes
        csv_recettes = self.data + "/recettes.csv"
        self.df_recettes.to_csv(csv_recettes, index=False)

        # Write stock in ingredients
        csv_ingredients = self.data + "/ingredients.csv"
        self.df_ingredients.to_csv(csv_ingredients, index=False)

        # Check if there is no negative values in quantite_reservee column
        value = 0
        ingredient = ""
        for _, row in self.df_ingredients.iterrows():
            if row["quantite_reservee"] < 0:
                value += 1
                ingredient += f"{row['ingredient']}, "

        if value == 0:
            # Quit command window and show homepage
            self.remove.destroy()
            self.root.deiconify()
        else:
            self.error_label.config(
                text=f"Attention, les opérations effectuées ont créé {value} valeurs négatives dans le stock ({ingredient[:-2]})"
            )


class addRecipe:
    def __init__(self, add_recipe: tk.Toplevel, root: tk.Tk):
        """
        Initializes an instance of the class.

        Args:
            add_recipe(tk.Toplevel): The parent widget where this frame will be placed.
            root(tk.Tk): The root window to perform actions on it.

        Returns:
            None
        """
        self.add_recipe = add_recipe
        self.root = root

        # Create a dictionnary to store the recipe
        self.recipe: dict = {}

        # Make CsvWindow wait for AskBoxPrefixWindow result
        self.root.withdraw()

        self.add_recipe.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Retrieve path to data folder
        with open("user_data.json") as file:
            self.data = json.load(file)["data_path"]

        # Create variables to store user choices
        self.beer = tk.StringVar(None)
        self.malt = tk.StringVar(None)
        self.malt_weight = tk.IntVar(None)
        self.houblon = tk.StringVar(None)
        self.houblon_weight = tk.IntVar(None)
        self.levure = tk.StringVar(None)
        self.levure_weight = tk.IntVar(None)
        self.autre = tk.StringVar(None)
        self.autre_weight = tk.IntVar(None)

        self.ingredient_type = tk.StringVar(None)
        self.ingredient = tk.StringVar(None)
        self.round = tk.IntVar(None)

        # Create lists to store different ingredients
        self.malts = ["malt"]
        self.houblons = ["houblon"]
        self.levures = ["levure"]
        self.autres = ["autre"]

        # Update spinners
        if self.malts and self.houblons and self.levures and self.autres:
            self.update_spinners()

        label_add = tk.Label(
            self.add_recipe,
            text="Ajouter un nouvel ingrédient (type, ingrédient, arrondi lors de la commande (grammes)):",
        )
        label_add.pack()

        frame_add_ingredient = tk.Frame(self.add_recipe)
        frame_add_ingredient.pack(pady=(0, 0), padx=100)

        ingredients = ["malt", "houblon", "levure", "autre"]
        dropdown_ingredient = tk.OptionMenu(frame_add_ingredient, self.ingredient_type, *ingredients)
        dropdown_ingredient.pack(side="left")

        add_ingredient = tk.Entry(frame_add_ingredient, textvariable=self.ingredient)
        add_ingredient.pack(side="left")

        command_round = tk.Entry(frame_add_ingredient, textvariable=self.round)
        command_round.pack(side="left")

        self.add_ingredient_label = tk.Label(self.add_recipe, text="")
        self.add_ingredient_label.pack()

        submit_ingredient = tk.Button(
            self.add_recipe,
            text="Ajouter l'ingredient",
            width=17,
            command=lambda: self.add_ingredient(self.ingredient_type.get(), self.ingredient.get(), self.round.get()),
            pady=10,
        )
        submit_ingredient.pack()

        space_label = tk.Label(self.add_recipe, text="")
        space_label.pack()

        self.empty_label = tk.Label(self.add_recipe, text="")
        self.empty_label.pack()

        if self.malts and self.houblons and self.levures and self.autres:
            # Create the buttons
            self.empty_label.config(text="")

            recipe_label = tk.Label(self.add_recipe, text="Ajouter une recette")
            recipe_label.pack()

            label_beer_name = tk.Label(self.add_recipe, text="Nom de la bière:")
            label_beer_name.pack()

            entry_beer_name = tk.Entry(self.add_recipe, textvariable=self.beer)
            entry_beer_name.pack()

            submit_beer_name = tk.Button(
                self.add_recipe, text="Ajouter nom", width=17, command=lambda: self.update_description(1), pady=10
            )
            submit_beer_name.pack()

            self.label_malt = tk.Label(self.add_recipe, text="Ajouter du malt à le recette (grammes):")
            self.label_malt.pack()

            self.frame_add_malt = tk.Frame(self.add_recipe)
            self.frame_add_malt.pack(pady=(0, 5))

            self.dropdown_malt = tk.OptionMenu(self.frame_add_malt, self.malt, *self.malts)

            self.entry_malt = tk.Entry(self.frame_add_malt, textvariable=self.malt_weight)
            self.entry_malt.pack(side="right")

            self.submit_malt = tk.Button(
                self.add_recipe, text="Ajouter malt", width=17, command=lambda: self.update_description(2), pady=10
            )
            self.submit_malt.pack()

            label_houblon = tk.Label(self.add_recipe, text="Ajouter du houblon à le recette (grammes):")
            label_houblon.pack()

            frame_add_houblon = tk.Frame(self.add_recipe)
            frame_add_houblon.pack(pady=(0, 5))

            self.dropdown_houblon = tk.OptionMenu(frame_add_houblon, self.houblon, *self.houblons)

            entry_houblon = tk.Entry(frame_add_houblon, textvariable=self.houblon_weight)
            entry_houblon.pack(side="right")

            submit_houblon = tk.Button(
                self.add_recipe, text="Ajouter houblon", width=17, command=lambda: self.update_description(3), pady=10
            )
            submit_houblon.pack()

            label_levure = tk.Label(self.add_recipe, text="Ajouter une levure à le recette (sachets):")
            label_levure.pack()

            frame_add_levure = tk.Frame(self.add_recipe)
            frame_add_levure.pack(pady=(0, 5))

            self.dropdown_levure = tk.OptionMenu(frame_add_levure, self.levure, *self.levures)

            entry_levure = tk.Entry(frame_add_levure, textvariable=self.levure_weight)
            self.levure_weight.set(1)
            entry_levure.pack(side="right")

            submit_levure = tk.Button(
                self.add_recipe, text="Ajouter levure", width=17, command=lambda: self.update_description(4), pady=10
            )
            submit_levure.pack()

            label_autre = tk.Label(self.add_recipe, text="Ajouter un autre ingrédient à le recette (grammes):")
            label_autre.pack()

            frame_add_autre = tk.Frame(self.add_recipe)
            frame_add_autre.pack(pady=(0, 5))

            self.dropdown_autre = tk.OptionMenu(frame_add_autre, self.autre, *self.autres)

            entry_autre = tk.Entry(frame_add_autre, textvariable=self.autre_weight)
            entry_autre.pack(side="right")

            submit_autre = tk.Button(
                self.add_recipe, text="Ajouter autre", width=17, command=lambda: self.update_description(5), pady=10
            )
            submit_autre.pack()

            self.error_label = tk.Label(self.add_recipe, text="")
            self.error_label.pack()

            # Pack spinners
            self.dropdown_malt.pack(side="left")
            self.dropdown_houblon.pack(side="left")
            self.dropdown_levure.pack(side="left")
            self.dropdown_autre.pack(side="left")

            # Create the description variables
            self.beer_name_label = "Nom de la bière:\n"
            self.beer_name = ""
            self.malt_name = "\nMalt:\n"
            self.houblon_name = "\nHoublon:\n"
            self.levure_name = "\nLevure:\n"
            self.autre_name = "\nAutre:\n"

            # Create Text widget for description
            self.description_text = tk.Label(
                self.add_recipe,
                text=self.beer_name_label
                + self.beer_name
                + self.malt_name
                + self.houblon_name
                + self.levure_name
                + self.autre_name,
            )
            self.description_text.pack()

            save_recipe_button = tk.Button(
                self.add_recipe, text="Sauver la recette", width=17, command=self.save_recipe, pady=10
            )
            save_recipe_button.pack()

            self.status_write = tk.Label(self.add_recipe, text="")
            self.status_write.pack()
        else:
            self.empty_label.config(
                text="Entrez au moins un ingrédient par catégorie avant de pouvoir enregistrer un recette.",
                foreground="red",
            )
            refresh_button = tk.Button(
                self.add_recipe, text="Rafraîchir la page", width=17, command=self.refresh_page, pady=10
            )
            refresh_button.pack()

    def on_exit(self) -> None:
        """
        Defines behaviour when user quits this window (by x button or specified button).

        Args:
            None

        Returns:
            None
        """
        self.add_recipe.destroy()
        self.root.deiconify()

    def update_spinners(self) -> None:
        # Extract different ingredients to populate the spinners
        self.malts.clear()
        self.houblons.clear()
        self.levures.clear()
        self.autres.clear()

        path_ingredient = self.data + "/ingredients.csv"
        df = pd.read_csv(path_ingredient)
        for _, index in df.iterrows():
            if index["type_ingredient"] == "malt":
                self.malts.append(index["ingredient"])
            elif index["type_ingredient"] == "houblon":
                self.houblons.append(index["ingredient"])
            elif index["type_ingredient"] == "levure":
                self.levures.append(index["ingredient"])
            elif index["type_ingredient"] == "autre":
                self.autres.append(index["ingredient"])

    def pack_spinners(self) -> None:
        """
        Adds the beer name to the description.

        Args:
            None

        Returns:
            None
        """

        # Update the options of the spinners
        malt_menu = self.dropdown_malt["menu"]
        houblon_menu = self.dropdown_houblon["menu"]
        levure_menu = self.dropdown_levure["menu"]
        autre_menu = self.dropdown_autre["menu"]

        # Clear current options
        malt_menu.delete(0, "end")
        houblon_menu.delete(0, "end")
        levure_menu.delete(0, "end")
        autre_menu.delete(0, "end")

        # Add updated options
        for malt in self.malts:
            malt_menu.add_command(label=malt, command=lambda value=malt: self.malt.set(value))
        for houblon in self.houblons:
            houblon_menu.add_command(label=houblon, command=lambda value=houblon: self.houblon.set(value))
        for levure in self.levures:
            levure_menu.add_command(label=levure, command=lambda value=levure: self.levure.set(value))
        for autre in self.autres:
            autre_menu.add_command(label=autre, command=lambda value=autre: self.autre.set(value))

    def update_description(self, param: int) -> None:
        """
        Adds the beer name to the description.

        Args:
            None

        Returns:
            None
        """

        if param == 1 and self.beer.get():
            self.status_write.config(text="")
            self.error_label.config(text="Nom correctement enregistré!", foreground="green")
            self.beer_name = f"{self.beer.get()}\n"
            self.recipe["nom_biere"] = self.beer.get()
        elif param == 2 and self.malt.get() and self.malt_weight.get():
            if self.malt.get() in self.malt_name:
                self.error_label.config(text=f"{self.malt.get()} déjà ajouté!", foreground="red")
            else:
                self.error_label.config(text="Malt correctement enregistré!", foreground="green")
                self.malt_name += f"{self.malt.get()} ({self.malt_weight.get()}g), "
                self.recipe[self.malt.get()] = self.malt_weight.get()
                self.malt.set("")
                self.malt_weight.set(0)
        elif param == 3 and self.houblon.get() and self.houblon_weight.get():
            if self.houblon.get() in self.houblon_name:
                self.error_label.config(text=f"{self.houblon.get()} déjà ajouté!", foreground="red")
            else:
                self.error_label.config(text="Houblon correctement enregistré!", foreground="green")
                self.houblon_name += f"{self.houblon.get()} ({self.houblon_weight.get()}g), "
                self.recipe[self.houblon.get()] = self.houblon_weight.get()
                self.houblon.set("")
                self.houblon_weight.set(0)
        elif param == 4 and self.levure.get() and self.levure_weight.get():
            if self.levure.get() in self.levure_name:
                self.error_label.config(text=f"{self.levure.get()} déjà ajouté!", foreground="red")
            else:
                self.error_label.config(text="Levure correctement enregistrée!", foreground="green")
                self.levure_name += f"{self.levure.get()} ({self.levure_weight.get()}pcs), "
                self.recipe[self.levure.get()] = self.levure_weight.get()
                self.levure.set("")
                self.levure_weight.set(1)
        elif param == 5 and self.autre.get() and self.autre_weight.get():
            if self.autre.get() in self.autre_name:
                self.error_label.config(text=f"{self.autre.get()} déjà ajouté!", foreground="red")
            else:
                self.error_label.config(text="Autre ingrédient correctement enregistré!", foreground="green")
                self.autre_name += f"{self.autre.get()} ({self.autre_weight.get()}g), "
                self.recipe[self.autre.get()] = self.autre_weight.get()
                self.autre.set("")
                self.autre_weight.set(0)
        else:
            self.error_label.config(text="Certains champs sont vides!", foreground="red")

        self.description_text.config(
            text=self.beer_name_label
            + self.beer_name
            + self.malt_name
            + self.houblon_name
            + self.levure_name
            + self.autre_name
        )

    def save_recipe(self) -> None:
        path_recettes = self.data + "/recettes.csv"
        if self.recipe:
            self.error_label.config(text="")
            # Read existing headers from the CSV file
            with open(path_recettes) as f:
                reader = csv.DictReader(f)
                existing_headers = reader.fieldnames

            # Create a new dictionary with all keys, filling in empty values for non-matching keys
            existing_headers = existing_headers or []
            new_row = {key: self.recipe.get(key, "") for key in existing_headers}

            # Write the new row to the CSV file
            with open(path_recettes, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=existing_headers)
                writer.writerow(new_row)
            self.status_write.config(text="Recette ajoutée!", foreground="green")
            self.beer.set("")
            # Recreate a dictionnary to store the next recipe
            self.recipe = {}
            # Recreate the description variables
            self.beer_name_label = "Nom de la bière:\n"
            self.beer_name = ""
            self.malt_name = "\nMalt:\n"
            self.houblon_name = "\nHoublon:\n"
            self.levure_name = "\nLevure:\n"
            self.autre_name = "\nAutre:\n"
            self.description_text.config(
                text=self.beer_name_label
                + self.beer_name
                + self.malt_name
                + self.houblon_name
                + self.levure_name
                + self.autre_name
            )
        else:
            self.status_write.config(text="Aucune recette définie!", foreground="red")

    def add_ingredient(self, ingredient_type: str, ingredient: str, rounded: int) -> None:
        """
        Adds the beer name to the description.

        Args:
            None

        Returns:
            None
        """
        path_ingredient = self.data + "/ingredients.csv"
        path_recettes = self.data + "/recettes.csv"

        if ingredient_type and ingredient and rounded:  # Check if both ingredient type and ingredient are provided
            # Convert the input ingredient to lowercase for case insensitive comparison
            ingredient = ingredient.lower()
            self.ingredient.set("")

            # Check if the ingredient is already present
            with open(path_ingredient) as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    # Convert the ingredient read from the CSV to lowercase for comparison
                    if row[1].lower() == ingredient:
                        # If ingredient already exists, inform the user and return
                        self.add_ingredient_label.config(text=f"{ingredient} already exists!", foreground="red")
                        return

            # If the ingredient is not present, proceed with adding it
            with open(path_ingredient, "a") as csv_file:
                csv_writer = csv.writer(csv_file)
                # Write headers
                csv_writer.writerow([ingredient_type, ingredient, "", "", "", rounded])

            with open(path_recettes) as csv_file:
                csv_reader = csv.reader(csv_file)
                rows = list(csv_reader)
            for row in rows:
                row.append("")

            rows[0][-1] = ingredient

            with open(path_recettes, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(rows)

            # Update the spinners after adding the ingredient
            if self.malts and self.houblons and self.levures and self.autres:
                self.update_spinners()
                self.pack_spinners()

            # Inform the user that the ingredient has been added
            self.add_ingredient_label.config(text="Ingrédient correctement ajouté!", foreground="black")
        else:
            # If ingredient type or ingredient is empty, inform the user to enter correct values
            self.add_ingredient_label.config(
                text="Type d'ingrédient, ingrédient ou arrondi nul! Entrez des valeurs correctes", foreground="red"
            )

    def refresh_page(self) -> None:
        """
        Returns to main script which option did the user choose.

        Args:
            None

        Returns:
            None
        """
        self.add_recipe.destroy()
        add_recipe = tk.Toplevel(root)
        add_recipe.title("Ajouter une recette")
        add_recipe.minsize(600, 600)
        # Show the window for a new batch
        addRecipe(add_recipe, root)


# Create an instance of the main window
root = tk.Tk()
root.title("Stock Manager")
root.minsize(600, 200)

# Create an instance of the HomeWindow class
home = HomeWindow(root)

# Display the HomeWindow
home.pack()

# Start the tkinter event loop
root.mainloop()
