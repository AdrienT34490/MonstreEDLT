from tkinter import *
from tkinter import ttk
from classCoquille import *

resultat = None


def generer():
    global resultat
    Etage = varEtage.get()
    Categorie = varPuissance.get()
    PointFort = varPointFort.get()
    if PointFort == "AUCUN":
        PointFort = None

    if Categorie == "Faible":
        resultat = CreatureFaible(Etage, PointFort)
    elif Categorie == "Moyen":
        resultat = CreatureMoyenne(Etage, PointFort)
    elif Categorie == "Fort":
        resultat = CreatureForte(Etage, PointFort)

    # ----------{Cadre de résultat}---------- #

    cadreResultat = ttk.Frame(fenetre, padding="3 3 12 12")
    cadreResultat.grid(column=1, row=0)

    # ----------{Caractéristiques}
    listeC = []
    for clef, valeur in resultat.caracteristiques.items():
        listeC = listeC + [f"{clef} : {valeur}"]
    texteCarac = StringVar(value=listeC)

    listeCarac = Listbox(cadreResultat, listvariable=texteCarac, height=10)
    listeCarac.grid(column=0, row=0, columnspan=2)

    # ----------{Autres}
    labelPO = Label(cadreResultat, text="PO")
    labelPO.grid(column=0, row=1)

    labelQtePO = Label(cadreResultat, text=resultat.PO)
    labelQtePO.grid(column=1, row=1)

    labelEXP = Label(cadreResultat, text="EXP")
    labelEXP.grid(column=0, row=2)

    labelQteEXP = Label(cadreResultat, text=resultat.experience)
    labelQteEXP.grid(column=1, row=2)

    labelFaiblesse = Label(cadreResultat, text="Faiblesse")
    labelFaiblesse.grid(column=0, row=3)

    labelQteFaiblesse = Label(cadreResultat, text=resultat.FaibResi["faiblesse"])
    labelQteFaiblesse.grid(column=1, row=3)

    labelResistance = Label(cadreResultat, text="Résistance")
    labelResistance.grid(column=0, row=4)

    labelQteResistance = Label(cadreResultat, text=resultat.FaibResi["resistance"])
    labelQteResistance.grid(column=1, row=4)

    # ----------{Cadre d'action}---------- #
    cadreAction = ttk.Frame(fenetre, padding="3 3 12 12")
    cadreAction.grid(column=0, row=1, columnspan=2)

    descAction = StringVar(value="Description")
    descriptionAction = Label(cadreAction, textvariable=descAction)
    descriptionAction.grid(column=1, row=0)

    listeAct = []
    for clef, valeur in resultat.actions.items():
        listeAct = listeAct + [f"{clef}"]
    texteActions = StringVar(value=listeAct)

    selectionAction = Listbox(cadreAction, listvariable=texteActions, height=5)
    selectionAction.grid(column=0, row=0)

    def affichageAction(*args):
        selection = selectionAction.curselection()

        if len(selectionAction.curselection()) >= 1:
            listeClef = list(resultat.actions.keys())

            clefAction = listeClef[int(selection[0])]
            descAction.set(value=resultat.actions[clefAction].toString())

    selectionAction.bind("<<ListboxSelect>>", affichageAction)


fenetre = Tk()
fenetre.title("Outil bestiaire")

# ----------{Cadre de génération}---------- #

cadreGeneration = ttk.Frame(fenetre, padding="3 3 12 12")
cadreGeneration.grid(column=0, row=0)

# ----------{étage}
varEtage = IntVar()
labelEtage = ttk.Label(cadreGeneration, text="étage")
labelEtage.grid(column=0, row=0)

etage = ttk.Combobox(cadreGeneration, textvariable=varEtage)
etage["values"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
etage.state(["readonly"])
etage.grid(column=2, row=0)

# ----------{puissance}
varPuissance = StringVar()
labelPuissance = ttk.Label(cadreGeneration, text="Catégorie")
labelPuissance.grid(column=0, row=1)

puissanceFaible = ttk.Radiobutton(cadreGeneration, text="Faible", variable=varPuissance, value="Faible")
puissanceFaible.grid(column=1, row=1)
puissanceMoyen = ttk.Radiobutton(cadreGeneration, text="Moyen", variable=varPuissance, value="Moyen")
puissanceMoyen.grid(column=2, row=1)
puissanceFort = ttk.Radiobutton(cadreGeneration, text="Fort", variable=varPuissance, value="Fort")
puissanceFort.grid(column=3, row=1)

# ----------{point fort}
labelPointFort = ttk.Label(cadreGeneration, text="Point fort")
labelPointFort.grid(column=0, row=2)

varPointFort = StringVar()
pointFort = ttk.Combobox(cadreGeneration, textvariable=varPointFort)
pointFort["values"] = ("FOR", "ADR", "CON", "INT", "PER", "CHA", "AUCUN")
pointFort.state(["readonly"])
pointFort.grid(column=2, row=2)

# ----------{bouton génération}
boutonGenerateur = ttk.Button(cadreGeneration, text="Générer!", command=generer)
boutonGenerateur.grid(column=2, row=3)

fenetre.mainloop()
