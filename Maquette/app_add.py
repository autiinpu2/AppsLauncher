import sys
import json
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

def dragEnterEvent(event):
    if event.mimeData().hasImage():
        event.accept()
    else:
        event.ignore()

def dropEvent(event, label):
    if event.mimeData().hasImage():
        image_path = event.mimeData().urls()[0].toLocalFile()
        updateImageLabel(label, image_path)

def browseImage(label):
    file_dialog = QFileDialog(None, "Sélectionner une image")
    file_dialog.setNameFilter("Images (*.png *.xpm *.jpg)")
    file_dialog.setViewMode(QFileDialog.List)
    if file_dialog.exec_():
        image_path = file_dialog.selectedFiles()[0]
        updateImageLabel(label, image_path)

def updateImageLabel(label, image_path):
    label.setPixmap(QtGui.QPixmap(image_path).scaled(label.size(), QtCore.Qt.KeepAspectRatio))
    global image_path_var
    image_path_var = image_path

def browsePath():
    file_dialog = QFileDialog(None, "Sélectionner un fichier")
    file_dialog.setNameFilter("Fichiers exécutables (*.exe)")
    file_dialog.setViewMode(QFileDialog.List)
    if file_dialog.exec_():
        file_path = file_dialog.selectedFiles()[0]
        if file_path.lower().endswith('.exe'):
            path_display_label.setText(f"Chemin du fichier : {file_path}")
            global exe_path_var
            exe_path_var = file_path
        else:
            QMessageBox.warning(None, "Type de fichier invalide", "Veuillez sélectionner un fichier .exe uniquement.")

def saveToJSON():
    data = {
        'image_path': image_path_var,
        'app_name': text_edit.text(),
        'exe_path': exe_path_var
    }
    with open('app_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    QMessageBox.information(None, "Enregistrement", "Les données ont été sauvegardées avec succès.")

def onLabelClicked(label):
    browseImage(label)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Ajouter une application")
window.setWindowIcon(QtGui.QIcon("AppsLauncher/ressources/icon.png"))
window.setStyleSheet("background-color: grey")

# Layout principal
main_layout = QVBoxLayout()

# QLabel pour le drag & drop des images
image_label = QLabel("Faites glisser et déposez une image ici ou cliquez pour sélectionner une image", window)
image_label.setAlignment(QtCore.Qt.AlignCenter)
image_label.setStyleSheet("border: 2px dashed black; padding: 10px; background-color: rgb(59,59,59);")
image_label.setAcceptDrops(True)
image_label.dragEnterEvent = lambda event: dragEnterEvent(event)
image_label.dropEvent = lambda event: dropEvent(event, image_label)
image_label.mousePressEvent = lambda event: onLabelClicked(image_label)
image_label.setFixedSize(400, 300)  # Ajuste la taille du QLabel

# QLineEdit pour le texte
text_edit = QLineEdit(window)
text_edit.setPlaceholderText("Nom de l'application")
text_edit.setFixedWidth(400)  # Ajuste la largeur du QLineEdit

# QLabel pour le texte au-dessus du bouton
path_label = QLabel("Chemin de l'application", window)
path_label.setAlignment(QtCore.Qt.AlignCenter)
path_label.setStyleSheet("color: white;")  # Ajuste la couleur du texte si nécessaire

# QLabel pour afficher le chemin du fichier .exe
path_display_label = QLabel("", window)
path_display_label.setAlignment(QtCore.Qt.AlignCenter)
path_display_label.setStyleSheet("color: white; padding-top: 10px;")

# QPushButton pour parcourir le chemin
browse_path_button = QPushButton("Parcourir", window)
browse_path_button.setFixedWidth(400)  # Ajuste la largeur du QPushButton
browse_path_button.clicked.connect(browsePath)

# QPushButton pour enregistrer les données
save_button = QPushButton("Enregistrer", window)
save_button.setFixedWidth(400)  # Ajuste la largeur du QPushButton
save_button.clicked.connect(saveToJSON)

# Layout pour chaque ligne
image_layout = QHBoxLayout()
image_layout.addWidget(image_label)
image_layout.setAlignment(QtCore.Qt.AlignCenter)

text_layout = QHBoxLayout()
text_layout.addWidget(text_edit)
text_layout.setAlignment(QtCore.Qt.AlignCenter)

path_layout = QHBoxLayout()
path_layout.addWidget(path_label)
path_layout.setAlignment(QtCore.Qt.AlignCenter)

button_layout = QVBoxLayout()
button_layout.addLayout(path_layout)
button_layout.addWidget(browse_path_button)
button_layout.addWidget(path_display_label)
button_layout.addWidget(save_button)
button_layout.setAlignment(QtCore.Qt.AlignCenter)

# Ajout des layouts au layout principal
main_layout.addLayout(image_layout)
main_layout.addLayout(text_layout)
main_layout.addLayout(button_layout)

window.setLayout(main_layout)

# Variables globales pour les chemins
image_path_var = ''
exe_path_var = ''

# Affichage en mode maximisé
window.showMaximized()

sys.exit(app.exec_())
