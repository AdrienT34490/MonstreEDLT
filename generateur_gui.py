from parametre import dict_caractéristiques, dict_etage, dict_type

import json
import os
import tkinter as tk

from tkinter import ttk, filedialog
from datetime import datetime

from fonctions import generer_monstre

def quit_program(root: tk.Tk) -> None:
    """
    This function closes the GUI and exits the program
    Parameters
    ----------
    root
        The root window for the GUI
    -------

    """
    root.destroy()

def remove_widgets(frame: tk.Frame) -> None:
    """
    This function closes all the widgets in a frame
    Parameters
    ----------
    frame
        the frame that needs to be purged
    -------

    """
    for widget in frame.winfo_children():
        widget.destroy()

def browse_file(widget: tk.Entry, string_var: tk.StringVar) -> None:
    """
    This function fills an Entry widget with the absolute path of a selected
    file
    Parameters
    ----------
    widget
        The entry widget that is to be filled
    string_var
        The tkinter textvariable of that widget
    -------

    """
    filename = filedialog.askopenfilename(initialdir="./",
                                          title="Choisit un fichier bg",
                                          filetypes=(
                                              ("TxT Files", "*.txt"),
                                              ("all files", "*.*")))

    string_var.set(filename)
    widget.configure(textvariable=string_var)


def save(monstre):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    chemin_base = "./Monstres/monstre"
    chemin_fichier = f"{chemin_base}_{timestamp}.json"

    dossier = os.path.dirname(chemin_fichier)
    if not os.path.exists(dossier):
        os.makedirs(dossier)

    with open(chemin_fichier, "w") as fichier:
        json.dump(monstre, fichier, indent=4)




class VerticalScrolledFrame(ttk.Frame):
    """
    This class creates a scrollable frame

    This class comes from this webpage :
    https://coderslegacy.com/python/make-scrollable-frame-in-tkinter/
    """

    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                                width=200, height=300,
                                yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = ttk.Frame(self.canvas)
        self.interior.columnconfigure(1, weight=1)
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior,
                                                     anchor=tk.NW)

    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id,
                                      width=self.canvas.winfo_width())
            
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Générateur de mob")
        self.geometry("550x800")

        label_title1 = tk.Label(self, text="Options de génération", justify="center")
        label_title1.pack(padx=8, pady=0, fill="x")
        self.frame1 = tk.Frame(self)
        self.frame1.pack(padx=8, pady=8, fill="x")
        self.frame1.columnconfigure(1, weight=1)
        self._create_widget_frame1()
        
        label_title2 = tk.Label(self, text="Caractéristiques générée", justify="center")
        label_title2.pack(padx=8, pady=0, fill="x")
        self.frame2 = tk.Frame(self)
        self.frame2.pack(padx=8, pady=8, fill="x")
        self.frame2.columnconfigure(1, weight=1)

        label_title3 = tk.Label(self, text="Statistiques générales", justify="center")
        label_title3.pack(padx=8, pady=0, fill="x")
        self.frame3 = tk.Frame(self)
        self.frame3.pack(padx=8, pady=8, fill="x")
        self.frame3.columnconfigure(1, weight=1)

        self.frame4 = tk.Frame(self)
        self.frame4.pack(padx=8, pady=8, fill="x")
        self.frame4.columnconfigure(1, weight=1)
        self._create_widget_frame4()


    def _create_widget_frame1(self):
        liste_etages = list(dict_etage.keys())
        var_etage = tk.StringVar()
        label_etage = tk.Label(self.frame1, text="Étage")
        label_etage.grid(column=0, row=0, padx=8, pady=0, sticky="e")
        combobox_etage = ttk.Combobox(self.frame1, justify="center", values=liste_etages, 
                                      textvariable=var_etage, state="readonly")
        combobox_etage.grid(column=1, row=0, padx=8, pady=0, sticky="we")


        liste_types = list(dict_type.keys())
        var_type = tk.StringVar()
        label_type = tk.Label(self.frame1, text="type")
        label_type.grid(column=0, row=1, padx=8, pady=0, sticky="e")
        combobox_type = ttk.Combobox(self.frame1, justify="center", values=liste_types, 
                                     textvariable=var_type, state="readonly")
        combobox_type.grid(column=1, row=1, padx=8, pady=0, sticky="we")


        liste_caracs = list(dict_caractéristiques.keys())
        var_carac = tk.StringVar()
        label_carac = tk.Label(self.frame1, text="Caractéristique principale")
        label_carac.grid(column=0, row=2, padx=8, pady=0, sticky="e")
        combobox_carac = ttk.Combobox(self.frame1, justify="center", values=liste_caracs, 
                                      textvariable=var_carac, state="readonly")
        combobox_carac.grid(column=1, row=2, padx=8, pady=0, sticky="we")

        boutton_generer = tk.Button(self.frame1, text="Generer", justify="center", 
                                    command=lambda :self.get_var_monstre(var_etage, var_type, var_carac))
        boutton_generer.grid(column=1, row=4, padx=8, pady=8, sticky="we")


    def _create_widget_frame2(self, monstre):
        ligne = 1
        liste_points_carac = [int(x) for x in list(monstre["Caractéristiques"].values())]

        def update_monstre(key, var_points_carac):
            monstre["Caractéristiques"][key] = int(var_points_carac.get())

        for key, value in monstre["Caractéristiques"].items():
            label_carac = tk.Label(self.frame2, text=key)
            label_carac.grid(column=0, row=ligne, padx=8, pady=8, sticky="e")

            var_points_carac = tk.StringVar(value=str(value))
            combobox_points_carac = ttk.Combobox(
                self.frame2,
                values=liste_points_carac,
                textvariable=var_points_carac,
                state="readonly"
            )
            combobox_points_carac.grid(column=1, row=ligne, padx=8, pady=0, sticky="we")

            # Attacher un événement pour mettre à jour le dictionnaire
            combobox_points_carac.bind(
                "<<ComboboxSelected>>",
                lambda e, k=key, var=var_points_carac: update_monstre(k, var)
            )

            ligne += 1



    def _create_widget_frame3(self, monstre):
        ligne = 0

        label_degat = tk.Label(self.frame3, text="Dégâts", justify="center")
        label_degat.grid(column=1, row=ligne, padx=8, pady=8, sticky="we")

        label_degat_moy = tk.Label(self.frame3, text=f"Dégâts moyens : {monstre["Dégâts moyens"]}")
        label_degat_moy.grid(column=2, row=ligne, padx=8, pady=8, sticky="w")

        label_degat_max = tk.Label(self.frame3, text=f"Dégâts maximum : {monstre["Dégâts max"]}")
        label_degat_max.grid(column=3, row=ligne, padx=8, pady=8, sticky="w")

        ligne = ligne + 1

        label_complexite = tk.Label(self.frame3, text="Complexités", justify="center")
        label_complexite.grid(column=1, row=ligne, padx=8, pady=8, sticky="we")

        label_cmplx_moy = tk.Label(self.frame3, text=f"Complexité moyenne : {monstre["Complexité moyenne"]}")
        label_cmplx_moy.grid(column=2, row=ligne, padx=8, pady=8, sticky="w")

        label_cmplx_max = tk.Label(self.frame3, text=f"Complexité maximum : {monstre["Complexité max"]}")
        label_cmplx_max.grid(column=3, row=ligne, padx=8, pady=8, sticky="w")

        ligne = ligne + 1

        label_autre = tk.Label(self.frame3, text="Autre", justify="center")
        label_autre.grid(column=1, row=ligne, padx=8, pady=8, sticky="we")

        label_PV = tk.Label(self.frame3, text=f"Points de vie: {monstre["PV"]}")
        label_PV.grid(column=2, row=ligne, padx=8, pady=8, sticky="w")

        label_XP = tk.Label(self.frame3, text=f"Expérience : {monstre["XP"]}")
        label_XP.grid(column=3, row=ligne, padx=8, pady=8, sticky="w")

        ligne = ligne + 1

        label_Rencontre = tk.Label(self.frame3, text=f"Dé de rencontre : {monstre["Dé de rencontre"]}")
        label_Rencontre.grid(column=2, row=ligne, padx=8, pady=8, sticky="w")

        label_Danger = tk.Label(self.frame3, text=f"Danger : {monstre["Danger"]}")
        label_Danger.grid(column=3, row=ligne, padx=8, pady=8, sticky="w")

        ligne = ligne + 1

        label_CA = tk.Label(self.frame3, text=f"Classe d'Armure : {monstre["CA"]}")
        label_CA.grid(column=2, row=ligne, padx=8, pady=8, sticky="w")

        label_CE = tk.Label(self.frame3, text=f"Classe d'Esprit : {monstre["CE"]}")
        label_CE.grid(column=3, row=ligne, padx=8, pady=8, sticky="w")

        ligne = ligne + 1

        label_SD = tk.Label(self.frame3, text=f"Score de Déplacement : {monstre["SD"]}")
        label_SD.grid(column=2, row=ligne, padx=8, pady=8, sticky="w")

        label_PO = tk.Label(self.frame3, text=f"PO : {monstre["PO"]}")
        label_PO.grid(column=3, row=ligne, padx=8, pady=8, sticky="w")

        ligne = ligne + 1

    def get_var_monstre(self, var_E, var_T, var_C):
        etage = dict_etage[str(var_E.get())]
        base = dict_type[str(var_T.get())]
        pref = str(var_C.get())
        self.monstre = generer_monstre(etage, base, pref)
        remove_widgets(self.frame2)
        self._create_widget_frame2(self.monstre)
        remove_widgets(self.frame3)
        self._create_widget_frame3(self.monstre)

    def _create_widget_frame4(self):
        bouton_fermer = tk.Button(self.frame4, text="Fermer", justify="center", 
                                  command=lambda: quit_program(self))
        bouton_fermer.grid(column=1, row=0, sticky="w")

        bouton_enregistrer = tk.Button(self.frame4, text="Enregistrer", justify="center", 
                                       command=lambda: save(self.monstre))
        bouton_enregistrer.grid(column=2, row=0, sticky="e")
        
        

if __name__ == "__main__":
    app = GUI()
    app.mainloop()