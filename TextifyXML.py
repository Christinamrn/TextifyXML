import tkinter as tk
from tkinter import filedialog, messagebox, Menu
import xml.etree.ElementTree as ET
import os
import sys

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
        "help_texte":   "+/- : Ajouter ou supprimer des fichiers XML.\n "
                        "Sélectionnez un fichier pour voir son aperçu.\n"
                        "⬆/⬇ : Déplacer un fichier dans la liste.\n"
                        "A→Z / Z→A : Trier les fichiers par ordre alphabétique.\n\n"
                        "'Clic droit' sur un fichier pour le convertir ou le supprimer.\n"
                        "'Sauvegarder' pour créer un fichier TXT qui combine tous les fichiers XML.",
        "about" : "À propos",
        "about_text" : "TextifyXML v1.0\n\nCréé par Christina M. (@christinamrn sur GitHub)"
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
                        "A→Z / Z→A : Sort files alphabetically.\n\n"
                        "'Right-click' on a file to convert or delete it.\n"
                        "'Save' to create a TXT file that combines all XML files.",
        "about" : "About",
        "about_text" : "TextifyXML v1.0\n\nCreated by Christina M. (@christinamrn on GitHub)"
    }
}

langue_activee = "en"

def trad(cle):
    return langues[langue_activee][cle]

def changer_langue(nouvelle_langue):
    global langue_activee
    langue_activee = nouvelle_langue
    langue_var.set(nouvelle_langue)
    rafraichir_interface()
    rafraichir_menus()
    rafraichir_menu_contextuel()

def rafraichir_interface():
    nom_nouveau_fichier.delete(0, tk.END)
    nom_nouveau_fichier.insert(0, trad("filename"))
    btn_sauvegarde.config(text=trad("save"))

def rafraichir_menus():
    menubar.delete(0, tk.END)

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label=trad("new"), command=tout_supprimer)
    filemenu.add_command(label=trad("add_xml_files"), command=ajouter_fichiers)
    filemenu.add_command(label=trad("save"), command=sauvegarder_fichier)
    filemenu.add_separator()
    filemenu.add_command(label=trad("quit"), command=fenetre.quit)
    menubar.add_cascade(label=trad("File"), menu=filemenu)

    languagemenu = Menu(menubar, tearoff=0)
    languagemenu.add_radiobutton(label=trad("fr"), variable=langue_var, value="fr", command=lambda: changer_langue("fr"))
    languagemenu.add_radiobutton(label=trad("en"), variable=langue_var, value="en", command=lambda: changer_langue("en"))
    menubar.add_cascade(label=trad("Language"), menu=languagemenu)

    affichage_menu = Menu(menubar, tearoff=0)
    affichage_menu.add_checkbutton(label=trad("preview"), variable=affichage_var, command=affichage_apercus)
    menubar.add_cascade(label=trad("View"), menu=affichage_menu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label=trad("help"), command=afficher_aide)
    helpmenu.add_command(label=trad("about"), command=afficher_a_propos)
    menubar.add_cascade(label=trad("Help"), menu=helpmenu)

    fenetre.config(menu=menubar)

def rafraichir_menu_contextuel():
    global menu_contextuel
    menu_contextuel = tk.Menu(liste, tearoff=0)
    menu_contextuel.add_command(label=trad("convert_file"), command=convertir_fichier)
    menu_contextuel.add_command(label=trad("delete"), command=supprimer_fichier)

fichiers_xml = []
drag_index = None

# --- fonctionnalités ---

def ajouter_fichiers():
    global fichiers_xml
    fichiers = filedialog.askopenfilenames(
        title=trad("add_xml_files"),
        filetypes=[(trad("file_type"), "*.xml")]
    )
    for fichier in fichiers:
        fichiers_xml.append(fichier)
    rafraichir_liste()

def supprimer_fichier(event=None):
    global fichiers_xml
    fichier_selectionne = liste.curselection()
    if not fichier_selectionne:
        messagebox.showwarning(trad("warning"), trad("select_file_to_delete"))
        return
    for index in reversed(fichier_selectionne):
        fichiers_xml.pop(index)
    rafraichir_liste()

def tout_supprimer(event=None):
    global fichiers_xml

    if not fichiers_xml:
        return

    confirmation = messagebox.askyesno(
        trad("warning"),
        trad("delete?")
    )

    if confirmation:
        fichiers_xml.clear()
        rafraichir_liste()
        mise_a_jour_etat_boutons()

def nouveau(event=None):
    tout_supprimer()
    nom_nouveau_fichier.delete(0, tk.END)
    nom_nouveau_fichier.insert(0, trad("filename"))

def trier_az():
    global fichiers_xml
    fichiers_xml.sort(key=lambda x: os.path.basename(x).lower())
    rafraichir_liste()

def trier_za():
    global fichiers_xml
    fichiers_xml.sort(key=lambda x: os.path.basename(x).lower(), reverse=True)
    rafraichir_liste()

def rafraichir_liste():
    liste.delete(0, tk.END)
    largeur = len(str(len(fichiers_xml)))
    for index, fichier in enumerate(fichiers_xml, 1):
        nom_fichier = os.path.basename(fichier)
        liste.insert(tk.END, f"{index:>{largeur}}. {nom_fichier}")
    mise_a_jour_etat_boutons()

# Drag & Drop
def on_start_drag(event):
    global drag_index
    drag_index = liste.nearest(event.y)

def on_drag_motion(event):
    global drag_index
    new_index = liste.nearest(event.y)
    if new_index != drag_index:
        fichiers_xml.insert(new_index, fichiers_xml.pop(drag_index))
        rafraichir_liste()
        liste.selection_set(new_index)
        liste.activate(new_index)
        drag_index = new_index
        mise_a_jour_etat_boutons()

def clic_droit(event):

    index = liste.nearest(event.y)

    if index >= 0:
        liste.selection_clear(0, tk.END)
        liste.selection_set(index)
        liste.activate(index)

        menu_contextuel.tk_popup(event.x_root, event.y_root)
        menu_contextuel.grab_release()

# Navigation clavier de la liste
def selection_clavier(event):
    fichier_selectionne = liste.curselection()
    if fichier_selectionne:
        index = fichier_selectionne[0]
    else:
        index = 0

    if event.keysym == "Up":
        index = max(0, index-1)
    elif event.keysym == "Down":
        index = min(len(fichiers_xml)-1, index+1)

    liste.selection_clear(0, tk.END)
    liste.selection_set(index)
    liste.activate(index)
    mise_a_jour_etat_boutons()
    mise_a_jour_selection()
    return "break" 

def monter():
    fichier_selectionne = liste.curselection()
    if not fichier_selectionne:
        return
    index = fichier_selectionne[0]
    if index == 0:
        return
    fichiers_xml[index-1], fichiers_xml[index] = fichiers_xml[index], fichiers_xml[index-1]
    rafraichir_liste()
    liste.selection_clear(0, tk.END)
    liste.selection_set(index-1)
    liste.activate(index-1)
    mise_a_jour_etat_boutons()

def descendre():
    fichier_selectionne = liste.curselection()
    if not fichier_selectionne:
        return
    index = fichier_selectionne[0]
    if index == len(fichiers_xml)-1:
        return
    fichiers_xml[index+1], fichiers_xml[index] = fichiers_xml[index], fichiers_xml[index+1]
    rafraichir_liste()
    liste.selection_clear(0, tk.END)
    liste.selection_set(index+1)
    liste.activate(index+1)
    mise_a_jour_etat_boutons()

def mise_a_jour_etat_boutons(event=None):
    fichier_selectionne = liste.curselection()
    btn_tri_az.config(state="normal" if len(fichiers_xml) >= 2 else "disabled")
    btn_tri_za.config(state="normal" if len(fichiers_xml) >= 2 else "disabled")
    btn_sauvegarde.config(state="normal" if len(fichiers_xml) != 0 else "disabled")
    filemenu.entryconfig(2, state="normal" if len(fichiers_xml) != 0 else "disabled")

    if not fichier_selectionne or len(fichiers_xml) == 0:
        btn_moins.config(state="disabled")
        btn_haut.config(state="disabled")
        btn_bas.config(state="disabled")
        return
    
    index = fichier_selectionne[0]
    btn_moins.config(state="normal" if index >= 0 else "disabled")
    btn_haut.config(state="normal" if index > 0 else "disabled")
    btn_bas.config(state="normal" if index < len(fichiers_xml)-1 else "disabled")

def mise_a_jour_selection(event=None):
    mise_a_jour_etat_boutons()
    afficher_apercu()

def affichage_apercus(event=None):
    if frame_fenetre_droite.winfo_ismapped():
        frame_fenetre_droite.pack_forget()
        affichage_var.set(False)
    else:
        frame_fenetre_droite.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=15)
        affichage_var.set(True)

# Menu - Affichage
def afficher_texte(widget, contenu):
    widget.config(state="normal")
    widget.delete("1.0", tk.END)
    widget.insert("1.0", contenu)
    widget.config(state="disabled")

def afficher_apercu(event=None):
    selection = liste.curselection()
    if not selection:
        afficher_texte(texte_avant, "")
        afficher_texte(texte_apres, "")
        return

    index = selection[0]
    chemin_xml = fichiers_xml[index]

    liste.selection_set(index)
    liste.activate(index)

    try:
        # afficher XML brut
        with open(chemin_xml, "r", encoding="utf-8") as f:
            contenu_xml = f.read()
        afficher_texte(texte_avant, contenu_xml)

        # afficher TXT converti
        tree = ET.parse(chemin_xml)
        root = tree.getroot()
        texte = "\n".join(t.strip() for t in root.itertext() if t.strip())
        afficher_texte(texte_apres, texte)

    except Exception as e:
        afficher_texte(texte_avant, "")
        afficher_texte(texte_apres, str(e))

# Menu - Aide
def afficher_aide():
    messagebox.showinfo(
        trad("help"),
        trad("help_text")
    )

def afficher_a_propos():
    messagebox.showinfo(
        trad("about"),
        trad("about_text")
    )

# Sauvegarde
def sauvegarder_fichier():
    if not fichiers_xml:
        messagebox.showwarning(trad("warning"), trad("no_file_selected"))
        return

    nom_fichier = nom_nouveau_fichier.get().strip()
    if not nom_fichier:
        messagebox.showwarning(trad("warning"), trad("add_filename"))
        return

    chemin_final = filedialog.asksaveasfilename(
        title=trad("save"),
        defaultextension=".txt",
        initialfile=nom_fichier,
        filetypes=[(trad("text_file"), "*.txt")]
    )

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

        messagebox.showinfo(trad("done"), trad("saved")+chemin_final)

    except Exception as e:
        messagebox.showerror(trad("error"), str(e))

def convertir_fichier():
    fichier_selectionne = liste.curselection()  
    if not fichier_selectionne:
        return
    
    index = fichier_selectionne[0]
    chemin_xml = fichiers_xml[index]
    chemin_final = os.path.splitext(chemin_xml)[0] + ".txt"

    if not chemin_final:
        return

    try:
        tree = ET.parse(chemin_xml)
        root = tree.getroot()
        texte = "\n".join(t.strip() for t in root.itertext() if t.strip())

        with open(chemin_final, "w", encoding="utf-8") as f:
            f.write(texte)

        messagebox.showinfo(trad("done"), trad("saved")+chemin_final)

    except Exception as e:
        messagebox.showerror(trad("error"), str(e))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# === Interface Tk ===

fenetre = tk.Tk()
fenetre.title("TextifyXML")
fenetre.geometry("550x550")
fenetre.minsize(750,750)

frame_fenetre = tk.Frame(fenetre)
frame_fenetre.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

frame_fenetre_gauche = tk.Frame(frame_fenetre)
frame_fenetre_gauche.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=15)

frame_fenetre_droite = tk.Frame(frame_fenetre)
frame_fenetre_droite.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=15)

# Aperçu 
frame_apercu_avant = tk.Frame(frame_fenetre_droite, bg="white", relief="sunken", bd=1, border=1)
frame_apercu_avant.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
frame_apercu_avant.pack_propagate(False)

scroll_xml = tk.Scrollbar(frame_apercu_avant)
scroll_xml.pack(side=tk.RIGHT, fill=tk.Y)

texte_avant = tk.Text(frame_apercu_avant, wrap="word")
texte_avant.pack(fill=tk.BOTH, expand=True)
texte_avant.config(state="disabled", cursor="arrow")
texte_avant.bind("<Key>", lambda e: "break")

texte_avant.config(yscrollcommand=scroll_xml.set)
scroll_xml.config(command=texte_avant.yview)

frame_apercu_apres = tk.Frame(frame_fenetre_droite, bg="white", relief="sunken", bd=1, border=1)
frame_apercu_apres.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
frame_apercu_apres.pack_propagate(False)

scroll_txt = tk.Scrollbar(frame_apercu_apres)
scroll_txt.pack(side=tk.RIGHT, fill=tk.Y)

texte_apres = tk.Text(frame_apercu_apres, wrap="word")
texte_apres.pack(fill=tk.BOTH, expand=True)
texte_apres.config(state="disabled", cursor="arrow")
texte_apres.bind("<Key>", lambda e: "break")

texte_apres.config(yscrollcommand=scroll_txt.set)
scroll_txt.config(command=texte_apres.yview)

# Liste des fichiers
frame_liste = tk.Frame(frame_fenetre_gauche)
frame_liste.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

scrollbar = tk.Scrollbar(frame_liste)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

liste = tk.Listbox(frame_liste, selectmode=tk.SINGLE, activestyle="none", yscrollcommand=scrollbar.set)
liste.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
liste.config(exportselection=False)

scrollbar.config(command=liste.yview)

# Boutons
frame_boutons = tk.Frame(frame_fenetre_gauche)
frame_boutons.pack(fill=tk.X, pady=5, padx=15)

# --- tri A→Z / Z→A ---
frame_gauche = tk.Frame(frame_boutons)
frame_gauche.pack(side=tk.LEFT, anchor="w")

btn_tri_az = tk.Button(frame_gauche, text="A→Z", width=5, command=trier_az)
btn_tri_az.pack(side=tk.LEFT, padx=2)

btn_tri_za = tk.Button(frame_gauche, text="Z→A", width=5, command=trier_za)
btn_tri_za.pack(side=tk.LEFT, padx=2)

# --- + / - ---
frame_centre = tk.Frame(frame_boutons)
frame_centre.pack(side=tk.LEFT, expand=True)

btn_plus = tk.Button(frame_centre, text="+", width=3, command=ajouter_fichiers)
btn_plus.pack(side=tk.LEFT, padx=2)

btn_moins = tk.Button(frame_centre, text="-", width=3, command=supprimer_fichier)
btn_moins.pack(side=tk.LEFT, padx=2)

# --- ↑ / ↓ ---
frame_droite = tk.Frame(frame_boutons)
frame_droite.pack(side=tk.RIGHT, anchor="e")

btn_haut = tk.Button(frame_droite, text="⬆", width=3, command=monter)
btn_haut.pack(side=tk.LEFT, padx=2)

btn_bas = tk.Button(frame_droite, text="⬇", width=3, command=descendre)
btn_bas.pack(side=tk.LEFT, padx=2)

# --- Nom fichier ---
frame_bas = tk.Frame(fenetre)
frame_bas.pack(fill=tk.X, pady=15, padx=15)

nom_nouveau_fichier = tk.Entry(frame_bas)
nom_nouveau_fichier.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
#nom_nouveau_fichier.insert(0, trad("filename"))

# --- sauvegarde ---
btn_sauvegarde = tk.Button(frame_bas, text=trad("save"), command=sauvegarder_fichier)
btn_sauvegarde.pack(side=tk.LEFT, padx=5)

# bindings de la liste
liste.bind("<<ListboxSelect>>", mise_a_jour_selection)

liste.bind("<Button-1>", on_start_drag)
liste.bind("<B1-Motion>", on_drag_motion)

liste.bind("<Button-3>", clic_droit)

liste.bind("<Up>", selection_clavier)
liste.bind("<Down>", selection_clavier)

liste.bind("<Delete>", supprimer_fichier)

# Barre de menu
menubar = Menu(fenetre)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label=trad("new"), command=nouveau)
filemenu.add_command(label=trad("add_xml_files"), command=ajouter_fichiers)
filemenu.add_command(label=trad("save"), command=sauvegarder_fichier)
filemenu.add_separator()
filemenu.add_command(label=trad("quit"), command=fenetre.quit)
menubar.add_cascade(label=trad("File"), menu=filemenu)

languagemenu = Menu(menubar, tearoff=0)
langue_var = tk.StringVar(value=langue_activee)
languagemenu.add_radiobutton(label=trad("fr"), variable=langue_var, value="fr", command=lambda: changer_langue("fr"))
languagemenu.add_radiobutton(label=trad("en"), variable=langue_var, value="en", command=lambda: changer_langue("en"))
menubar.add_cascade(label=trad("Language"), menu=languagemenu)

affichage_menu = Menu(menubar, tearoff=0)
affichage_var = tk.BooleanVar(value=not frame_fenetre_droite.winfo_ismapped())
affichage_menu.add_checkbutton(label=trad("preview"), variable=affichage_var, command=affichage_apercus)
menubar.add_cascade(label=trad("View"), menu=affichage_menu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label=trad("help"), command=afficher_aide)
helpmenu.add_command(label=trad("about"), command=afficher_a_propos)
menubar.add_cascade(label=trad("Help"), menu=helpmenu)

rafraichir_interface()
rafraichir_menu_contextuel()
mise_a_jour_etat_boutons()
fenetre.config(menu=menubar)

# Ajout logo
logo_path = resource_path("logo/TextifyXML_png.png")

try:
    logo = tk.PhotoImage(file=logo_path)
    fenetre.iconphoto(True, logo)
except Exception:
    pass


logo = tk.PhotoImage(file=logo_path)
fenetre.iconphoto(True, logo)

fenetre.mainloop()
