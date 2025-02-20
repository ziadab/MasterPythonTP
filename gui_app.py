from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLineEdit,
    QDialog,
    QFormLayout,
    QMessageBox,
    QDoubleSpinBox,
)
from manager import DataManager
import sys


class StatsDialog(QDialog):
    def __init__(self, parent=None, moyennes=None):
        super().__init__(parent)
        self.setWindowTitle("Statistiques")
        self.setModal(True)

        layout = QVBoxLayout()
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Matière", "Moyenne"])

        table.setRowCount(len(moyennes))
        for i, (matiere, moyenne) in enumerate(moyennes.items()):
            table.setItem(i, 0, QTableWidgetItem(matiere))
            table.setItem(i, 1, QTableWidgetItem(f"{moyenne:.2f}"))

        layout.addWidget(table)
        self.setLayout(layout)


class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un étudiant")
        self.setModal(True)

        layout = QFormLayout()

        self.nom = QLineEdit()
        self.prenom = QLineEdit()
        self.email = QLineEdit()
        self.matiere = QLineEdit()
        self.note = QDoubleSpinBox()
        self.note.setRange(0, 20)
        self.note.setDecimals(1)

        layout.addRow("Nom:", self.nom)
        layout.addRow("Prénom:", self.prenom)
        layout.addRow("Email:", self.email)
        layout.addRow("Matière:", self.matiere)
        layout.addRow("Note:", self.note)

        buttons = QHBoxLayout()
        self.accept_button = QPushButton("OK")
        self.cancel_button = QPushButton("Annuler")
        buttons.addWidget(self.accept_button)
        buttons.addWidget(self.cancel_button)

        layout.addRow(buttons)
        self.setLayout(layout)

        self.accept_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Étudiants")
        self.setMinimumSize(800, 600)

        self.dm = DataManager()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher par nom...")
        search_button = QPushButton("Rechercher")
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nom", "Prénom", "Email", "Matière", "Note"]
        )
        layout.addWidget(self.table)

        buttons_layout = QHBoxLayout()
        add_button = QPushButton("Ajouter")
        delete_button = QPushButton("Supprimer")
        stats_button = QPushButton("Statistiques")

        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addWidget(stats_button)
        layout.addLayout(buttons_layout)

        add_button.clicked.connect(self.add_student)
        delete_button.clicked.connect(self.delete_student)
        stats_button.clicked.connect(self.show_stats)
        search_button.clicked.connect(self.search_students)

        self.refresh_table()

    def refresh_table(self, data=None):
        if data is None:
            data = self.dm.afficher_etudiants()

        self.table.setRowCount(len(data))
        for i, row in data.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(str(row["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(row["nom"]))
            self.table.setItem(i, 2, QTableWidgetItem(row["prenom"]))
            self.table.setItem(i, 3, QTableWidgetItem(row["email"]))
            self.table.setItem(i, 4, QTableWidgetItem(row["matiere"]))
            self.table.setItem(i, 5, QTableWidgetItem(str(row["note"])))

    def add_student(self):
        dialog = AddStudentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.dm.ajouter_etudiant(
                dialog.nom.text(),
                dialog.prenom.text(),
                dialog.email.text(),
                dialog.matiere.text(),
                dialog.note.value(),
            )
            self.refresh_table()

    def delete_student(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un étudiant")
            return

        student_id = int(self.table.item(current_row, 0).text())
        if (
            QMessageBox.question(
                self,
                "Confirmation",
                "Voulez-vous vraiment supprimer cet étudiant ?",
                QMessageBox.Yes | QMessageBox.No,
            )
            == QMessageBox.Yes
        ):
            self.dm.supprimer_etudiant(student_id)
            self.refresh_table()

    def search_students(self):
        search_text = self.search_input.text()
        if search_text:
            results = self.dm.rechercher_etudiant(search_text)
            self.refresh_table(results)
        else:
            self.refresh_table()

    def show_stats(self):
        matieres = self.dm.df["matiere"].unique()
        moyennes = {matiere: self.dm.calculer_moyenne(matiere) for matiere in matieres}
        dialog = StatsDialog(self, moyennes)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
