import sys
import os
import xml.etree.ElementTree as ET

from PyQt6.QtWidgets import (
    QApplication, QWidget, QFileDialog, QMessageBox,
    QListWidget, QListWidgetItem, QTextEdit, QPushButton, QLineEdit,
    QHBoxLayout, QVBoxLayout, QMenu, QSplitter, QMenuBar, QDialog,
    QDialog, QLabel, QFrame 
)
from PyQt6.QtGui import QAction, QCursor, QActionGroup, QIcon, QImage, QPixmap
from PyQt6.QtCore import Qt

# --- traductions ---

langues = {
    "fr": {
        "new" : "Nouveau",
        "add_xml_files" : "Ajouter des fichiers XML",
        "file_type" : "Fichiers XML (*.xml)",
        "save" : "Sauvegarder",
        "error" : "Erreur",
        "select_file": "Sélectionnez un fichier",
        "convert_file" : "Convertir ce fichier",
        "warning" : "Attention",
        "select_file_to_delete" : "Sélectionnez un fichier à supprimer.",
        "no_file_selected" : "Aucun fichier sélectionné.",
        "delete" : "Supprimer",
        "delete?" : "Supprimer tous les fichiers de la liste ?",
        "add_filename" : "Veuillez entrer un nom de fichier.",
        "text_file" : "Fichier texte (*.txt)",
        "done" : "Terminé",
        "saved" : "Fichier créé : ",
        "filename" : "nom_du_fichier",
        "quit" : "Quitter",
        "File" : "Fichier",
        "Language" : "Langue",
        "fr" : "Français",
        "en" : "Anglais",
        "View" : "Affichage",
        "preview" : "Aperçu",
        "Help" : "Aide",
        "help" : "Aide",
        "help_text":   "+/- : Ajouter ou supprimer des fichiers XML.\n "
                        "Sélectionnez un fichier pour voir son aperçu.\n"
                        "⬆/⬇ : Déplacer un fichier dans la liste.\n"
                        "A→Z / Z→A : Trier les fichiers par ordre alphabétique.\n"
                        "'Clic droit' : Convertir ou supprimer un fichier.\n"
                        "'Sauvegarder' : Créer un fichier TXT qui combine tous les fichiers XML.",
        "about" : "À propos",
        "about_text" : "TextifyXML v1.1 (Version Qt6)\n18 février 2026\n\nCréé par Christina M. (@christinamrn sur GitHub)",
        "yes": "Oui",
        "no": "Non"
    },

    "en": {
        "new" : "New",
        "add_xml_files" : "Add XML files",
        "file_type" : "XML Files (*.xml)",
        "save": "Save",
        "error" : "Error",
        "select_file" : "Select a file",
        "convert_file" : "Convert this file",
        "warning" : "Warning",
        "select_file_to_delete" : "Select a file to delete.",
        "no_file_selected" : "No file selected.",
        "delete" : "Delete",
        "delete?" : "Delete all files?",
        "add_filename" : "Please add a filename.",
        "text_file" : "Text file (*.txt)",
        "done" : "Done",
        "saved" : "File created : ",
        "filename" : "name_of_file",
        "quit" : "Quit",
        "File" : "File",
        "Language" : "Language",
        "fr" : "French",
        "en" : "English",
        "View" : "View",
        "preview" : "Preview",
        "Help" : "Help",
        "help" : "Help",
        "help_text" :   "+/- : Add or remove XML files.\n"
                        "Select a file to see its preview.\n"
                        "⬆/⬇ : Move a file up or down in the list.\n"
                        "A→Z / Z→A : Sort files alphabetically.\n"
                        "'Right-click' : Convert or delete a file.\n"
                        "'Save' : Create a TXT file that combines all XML files.",
        "about" : "About",
        "about_text" : "TextifyXML v1.1 (Qt6 Version)\n18 February 2026\n\nCreated by Christina M. (@christinamrn on GitHub)",
        "yes": "Yes",
        "no": "No"
    }

}

langue_activee = "en"

def trad(cle):
    return langues[langue_activee][cle]


fichiers_xml = []

class FileListWidget(QListWidget):
    def dropEvent(self, event):
        super().dropEvent(event)
        rafraichir_liste_drag_drop()

def ajouter_fichiers():
    global fichiers_xml
    fichiers, _ = QFileDialog.getOpenFileNames(
        fenetre,
        trad("add_xml_files"),
        os.path.abspath('.'),
        "*.xml"
    )
    for fichier in fichiers:
        fichiers_xml.append(fichier)
    rafraichir_liste()

def supprimer_fichier(event=None):
    global fichiers_xml
    index = liste.currentRow()
    if index < 0:
        QMessageBox.warning(fenetre, trad("warning"), trad("select_file_to_delete"))
        return
    fichiers_xml.pop(index)
    rafraichir_liste()

def tout_supprimer(event=None):
    global fichiers_xml

    if not fichiers_xml:
        return

    msg = QMessageBox(fenetre)
    msg.setWindowTitle(trad("warning"))
    msg.setText(trad("delete?"))
    yes_btn = msg.addButton(trad("yes"), QMessageBox.ButtonRole.YesRole)
    no_btn = msg.addButton(trad("no"), QMessageBox.ButtonRole.NoRole)
    msg.setDefaultButton(yes_btn)
    msg.exec()

    if msg.clickedButton() == yes_btn:
        fichiers_xml.clear()
        rafraichir_liste()
        mise_a_jour_etat_boutons()

def nouveau(event=None):
    global fichiers_xml
    if not fichiers_xml:
        ajouter_fichiers()
        return
    else :
        tout_supprimer()
    nom_nouveau_fichier.setText(trad("filename"))

def trier_az():
    global fichiers_xml
    fichiers_xml.sort(key=lambda x: os.path.basename(x).lower())
    rafraichir_liste()

def trier_za():
    global fichiers_xml
    fichiers_xml.sort(key=lambda x: os.path.basename(x).lower(), reverse=True)
    rafraichir_liste()

def rafraichir_liste():
    liste.clear()
    largeur = len(str(len(fichiers_xml))) if fichiers_xml else 1
    for index, fichier in enumerate(fichiers_xml, 1):
        nom_fichier = os.path.basename(fichier)
        item_text = f"{index:>{largeur}}. {nom_fichier}"
        item = QListWidgetItem(item_text)
        item.setData(Qt.ItemDataRole.UserRole, fichier)
        liste.addItem(item)
    mise_a_jour_etat_boutons()

def rafraichir_liste_drag_drop():
    global fichiers_xml

    item = liste.currentItem()
    fichier_dropped = item.data(Qt.ItemDataRole.UserRole) if item else None

    fichiers_xml = [liste.item(i).data(Qt.ItemDataRole.UserRole) for i in range(liste.count())]
    rafraichir_liste()

    if fichier_dropped:
        for i in range(liste.count()):
            if liste.item(i).data(Qt.ItemDataRole.UserRole) == fichier_dropped:
                liste.setCurrentRow(i)
                break

    mise_a_jour_etat_boutons()

def monter():
    index = liste.currentRow()
    if index <= 0:
        return
    fichiers_xml[index-1], fichiers_xml[index] = fichiers_xml[index], fichiers_xml[index-1]
    rafraichir_liste()
    liste.setCurrentRow(index-1)
    mise_a_jour_etat_boutons()

def descendre():
    index = liste.currentRow()
    if index < 0 or index >= len(fichiers_xml)-1:
        return
    fichiers_xml[index+1], fichiers_xml[index] = fichiers_xml[index], fichiers_xml[index+1]
    rafraichir_liste()
    liste.setCurrentRow(index+1)
    mise_a_jour_etat_boutons()

def mise_a_jour_etat_boutons(event=None):
    has_files = len(fichiers_xml) > 0
    btn_tri_az.setEnabled(len(fichiers_xml) >= 2)
    btn_tri_za.setEnabled(len(fichiers_xml) >= 2)
    btn_sauvegarde.setEnabled(has_files)

    index = liste.currentRow()
    btn_moins.setEnabled(index >= 0 and has_files)
    btn_haut.setEnabled(index > 0)
    btn_bas.setEnabled(index >= 0 and index < len(fichiers_xml)-1)

def mise_a_jour_selection(event=None):
    mise_a_jour_etat_boutons()
    afficher_apercu()

def affichage_apercus_xml_txt(event=None):
    visible = preview_xml.isVisible()
    preview_xml.setVisible(not visible)
    preview_txt.setVisible(not visible)

def afficher_texte(widget, contenu):
    widget.setReadOnly(False)
    widget.setPlainText(contenu)
    widget.setReadOnly(True)

def afficher_apercu(event=None):
    index = liste.currentRow()
    if index < 0:
        afficher_texte(preview_xml, "")
        afficher_texte(preview_txt, "")
        return

    chemin_xml = fichiers_xml[index]
    try:
        with open(chemin_xml, "r", encoding="utf-8") as f:
            contenu_xml = f.read()
        afficher_texte(preview_xml, contenu_xml)

        tree = ET.parse(chemin_xml)
        root = tree.getroot()
        texte = "\n".join(t.strip() for t in root.itertext() if t.strip())
        afficher_texte(preview_txt, texte)
    except Exception as e:
        afficher_texte(preview_xml, "")
        afficher_texte(preview_txt, str(e))

def raccourci_display(raccourci_nom, raccourci_fonction, parent=None):
    frame = QFrame(parent)
    frame.setAutoFillBackground(True)
    frame.setStyleSheet("QFrame { background-color: palette(base); border-radius: 5px; padding: 2px; }")
    layout = QHBoxLayout()
    frame.setLayout(layout)
    nom_label = QLabel(raccourci_nom)
    nom_label.setStyleSheet("QLabel { font-weight: bold; }")
    fonction_label = QLabel(raccourci_fonction)
    layout.addWidget(nom_label)
    layout.addWidget(fonction_label)
    return frame

def raccourci_liste_aide(key_dict_text, parent=None):
    raccourci_vlayout = QVBoxLayout()
    for line in key_dict_text.splitlines():
        if ":" in line:
            raccourci_nom, raccourci_fonction = line.split(":", 1)
            raccourci_frame = raccourci_display(raccourci_nom.strip(), raccourci_fonction.strip(), parent)
            raccourci_vlayout.addWidget(raccourci_frame)
    return raccourci_vlayout

def afficher_aide():
    aide_dialog = QDialog(fenetre)
    aide_dialog.setWindowTitle(trad("help"))
    aide_layout = QVBoxLayout(aide_dialog)
    raccourcis_layout = raccourci_liste_aide(trad("help_text"), aide_dialog)
    aide_layout.addLayout(raccourcis_layout)
    aide_dialog.exec()

def afficher_a_propos():
    a_propos_dialog = QDialog(fenetre)
    a_propos_dialog.setWindowTitle(trad("about"))
    a_propos_layout = QVBoxLayout(a_propos_dialog)
    logo_app = QImage(resource_path('logo/TextifyXML_png.png'))
    logo_app = logo_app.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    logo_label = QLabel()
    logo_label.setPixmap(QPixmap.fromImage(logo_app))
    logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    a_propos_layout.addWidget(logo_label)
    a_propos_label = QLabel(trad("about_text"))
    a_propos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    a_propos_layout.addWidget(a_propos_label)
    a_propos_dialog.exec()

def sauvegarder_fichier():
    if not fichiers_xml:
        QMessageBox.warning(fenetre, trad("warning"), trad("no_file_selected"))
        return

    nom_fichier = nom_nouveau_fichier.text().strip()
    if not nom_fichier:
        QMessageBox.warning(fenetre, trad("warning"), trad("add_filename"))
        return

    chemin_final, _ = QFileDialog.getSaveFileName(fenetre, trad("save"), nom_fichier, "*.txt")
    if not chemin_final:
        return

    try:
        contenu_total = []
        for fichier in fichiers_xml:
            tree = ET.parse(fichier)
            root = tree.getroot()
            texte = "\n".join(t.strip() for t in root.itertext() if t.strip())
            contenu_total.append(texte)

        resultat = "\n\n\n".join(contenu_total)

        with open(chemin_final, "w", encoding="utf-8") as f:
            f.write(resultat)

        QMessageBox.information(fenetre, trad("done"), trad("saved") + chemin_final)

    except Exception as e:
        QMessageBox.critical(fenetre, trad("error"), str(e))

def convertir_fichier():
    index = liste.currentRow()
    if index < 0:
        return
    chemin_xml = fichiers_xml[index]
    chemin_final = os.path.splitext(chemin_xml)[0] + ".txt"
    try:
        tree = ET.parse(chemin_xml)
        root = tree.getroot()
        texte = "\n".join(t.strip() for t in root.itertext() if t.strip())

        with open(chemin_final, "w", encoding="utf-8") as f:
            f.write(texte)

        QMessageBox.information(fenetre, trad("done"), trad("saved") + chemin_final)

    except Exception as e:
        QMessageBox.critical(fenetre, trad("error"), str(e))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


# === Interface PyQt6 ===

app = QApplication(sys.argv)

fenetre = QWidget()
fenetre.setWindowTitle("TextifyXML")
fenetre.resize(750, 750)

main_layout = QVBoxLayout(fenetre)

# Menu bar
menu_bar = QMenuBar()
main_layout.setMenuBar(menu_bar)

def creer_menus():
    menu_bar.clear()
    filemenu = menu_bar.addMenu(trad("File"))
    filemenu.addAction(trad("new"), lambda: nouveau())
    filemenu.addAction(trad("add_xml_files"), lambda: ajouter_fichiers())
    filemenu.addAction(trad("save"), lambda: sauvegarder_fichier())
    filemenu.addSeparator()
    filemenu.addAction(trad("quit"), lambda: QApplication.instance().quit())

    langmenu = menu_bar.addMenu(trad("Language"))
    groupe = QActionGroup(fenetre)
    act_fr = QAction(trad("fr"), fenetre)
    act_fr.setCheckable(True)
    act_en = QAction(trad("en"), fenetre)
    act_en.setCheckable(True)
    groupe.addAction(act_fr)
    groupe.addAction(act_en)
    langmenu.addAction(act_fr)
    langmenu.addAction(act_en)
    if langue_activee == 'fr':
        act_fr.setChecked(True)
    else:
        act_en.setChecked(True)
    act_fr.triggered.connect(lambda: changer_langue('fr'))
    act_en.triggered.connect(lambda: changer_langue('en'))

    viewmenu = menu_bar.addMenu(trad("View"))
    preview_action = QAction(trad("preview"), fenetre)
    preview_action.setCheckable(True)
    preview_action.setChecked(True)
    preview_action.triggered.connect(lambda: affichage_apercus_xml_txt())
    viewmenu.addAction(preview_action)

    helpmenu = menu_bar.addMenu(trad("Help"))
    helpmenu.addAction(trad("help"), lambda: afficher_aide())
    helpmenu.addAction(trad("about"), lambda: afficher_a_propos())

splitter = QSplitter()
splitter.setOrientation(Qt.Orientation.Horizontal)
main_layout.addWidget(splitter)

left_widget = QWidget()
left_layout = QVBoxLayout(left_widget)

liste = FileListWidget()
liste.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
liste.setDragDropMode(QListWidget.DragDropMode.InternalMove)
liste.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
liste.customContextMenuRequested.connect(lambda pos: menu_contextuel())
liste.currentRowChanged.connect(lambda _: mise_a_jour_selection())
left_layout.addWidget(liste)

btn_layout = QHBoxLayout()
btn_tri_az = QPushButton('A→Z')
btn_tri_za = QPushButton('Z→A')
btn_plus = QPushButton('+')
btn_moins = QPushButton('-')
btn_haut = QPushButton('⬆')
btn_bas = QPushButton('⬇')

btn_layout.addWidget(btn_tri_az)
btn_layout.addWidget(btn_tri_za)
btn_layout.addWidget(btn_plus)
btn_layout.addWidget(btn_moins)
btn_layout.addWidget(btn_haut)
btn_layout.addWidget(btn_bas)

left_layout.addLayout(btn_layout)

splitter.addWidget(left_widget)

right_widget = QWidget()
right_layout = QVBoxLayout(right_widget)

preview_xml = QTextEdit()
preview_txt = QTextEdit()
preview_xml.setReadOnly(True)
preview_txt.setReadOnly(True)
right_layout.addWidget(preview_xml)
right_layout.addWidget(preview_txt)

splitter.addWidget(right_widget)

bottom_layout = QHBoxLayout()
nom_nouveau_fichier = QLineEdit(trad("filename"))
btn_sauvegarde = QPushButton(trad("save"))
bottom_layout.addWidget(nom_nouveau_fichier)
bottom_layout.addWidget(btn_sauvegarde)
main_layout.addLayout(bottom_layout)

btn_plus.clicked.connect(ajouter_fichiers)
btn_moins.clicked.connect(supprimer_fichier)
btn_haut.clicked.connect(monter)
btn_bas.clicked.connect(descendre)
btn_tri_az.clicked.connect(trier_az)
btn_tri_za.clicked.connect(trier_za)
btn_sauvegarde.clicked.connect(sauvegarder_fichier)

def menu_contextuel():
    i = liste.currentRow()
    if i < 0:
        return
    menu = QMenu()
    menu.addAction(trad("convert_file"), lambda: convertir_fichier())
    menu.addAction(trad("delete"), lambda: supprimer_fichier())
    menu.exec(QCursor.pos())

def changer_langue(nouvelle_langue):
    global langue_activee
    langue_activee = nouvelle_langue
    nom_nouveau_fichier.setText(trad("filename"))
    btn_sauvegarde.setText(trad("save"))
    creer_menus()

creer_menus()

# Ajout logo
logo_path = resource_path('logo/TextifyXML_png.png')
try:
    fenetre.setWindowIcon(QIcon(logo_path))
except Exception:
    pass

rafraichir_liste()
mise_a_jour_etat_boutons()

fenetre.show()

sys.exit(app.exec())
