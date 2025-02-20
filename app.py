from flask import Flask, render_template, request, redirect, url_for
from manager import DataManager

app = Flask(__name__)
dm = DataManager()


@app.route("/")
def index():
    etudiants = dm.afficher_etudiants()
    return render_template("index.html", etudiants=etudiants)


@app.route("/ajouter", methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        matiere = request.form["matiere"]
        note = float(request.form["note"])

        dm.ajouter_etudiant(nom, prenom, email, matiere, note)
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/supprimer/<int:id>")
def supprimer(id):
    dm.supprimer_etudiant(id)
    return redirect(url_for("index"))


@app.route("/stats")
def stats():
    matieres = dm.df["matiere"].unique()
    moyennes = {matiere: dm.calculer_moyenne(matiere) for matiere in matieres}
    return render_template("stats.html", moyennes=moyennes)


if __name__ == "__main__":
    app.run(port=3001, debug=True)
