import pandas as pd
from pathlib import Path


class DataManager:
    def __init__(self, csv_file="db.csv"):
        self.csv_file = csv_file
        if Path(self.csv_file).exists():
            self.df = pd.read_csv(self.csv_file)
        else:
            self.df = pd.DataFrame(
                columns=["id", "nom", "prenom", "email", "matiere", "note"]
            )
            self.df.to_csv(self.csv_file, index=False)

    def ajouter_etudiant(self, nom, prenom, email, matiere, note):
        new_id = 1 if self.df.empty else self.df["id"].max() + 1

        new_row = pd.DataFrame(
            {
                "id": [new_id],
                "nom": [nom],
                "prenom": [prenom],
                "email": [email],
                "matiere": [matiere],
                "note": [note],
            }
        )

        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.df.to_csv(self.csv_file, index=False)
        return new_id

    def supprimer_etudiant(self, id):
        if id in self.df["id"].values:
            self.df = self.df[self.df["id"] != id]
            self.df.to_csv(self.csv_file, index=False)
            return True
        return False

    def rechercher_etudiant(self, query):
        return self.df[
            self.df["nom"].str.contains(query, case=False, na=False)
            | self.df["prenom"].str.contains(query, case=False, na=False)
        ]

    def calculer_moyenne(self, matiere):
        notes_matiere = self.df[self.df["matiere"] == matiere]["note"]
        if notes_matiere.empty:
            return None
        return notes_matiere.mean()

    # I added this func so I would be able to access list of user from the web and the gui app
    def afficher_etudiants(self):
        return self.df
