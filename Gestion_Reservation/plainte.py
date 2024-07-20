from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
import sqlite3
import os

class Plainte:
    def __init__(self, root):
        background = "cyan"
        self.root = root
        self.root.title("Plainte")
        self.root.geometry("1350x630+10+70")
        self.root.config(bg=background)

        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS plainte (ID INTEGER PRIMARY KEY AUTOINCREMENT,Nom text,Prenom text, Type_Salle text ,Nom_Salle text, Probleme text,Budget text)")
        con.commit()
        con.close()

        self.liste_salle= []
        self.listesalle() 

        self.var_id = IntVar()
        self.var_nom_client = StringVar()
        self.var_prenom_client = StringVar()
        self.var_type_salle = StringVar()
        self.var_nom_salle = StringVar()
        self.var_probleme = StringVar()
        self.var_budget = StringVar()

        self.var_type_recherche = StringVar()
        self.var_recherche = StringVar()

        self.frame_plainte = LabelFrame(self.root, text="Plainte", bg=background, bd=3, relief=RIDGE, font=("times new roman",15,"bold"), width=1340, height=625)
        self.frame_plainte.place(x=5,y=0)

        ###########################

        self.frame_saisi = Frame(self.frame_plainte, bg=background,relief=GROOVE, bd=3)
        self.frame_saisi.place(x=0,y=0, width=900, height=200)
        
        lbl_nom_client = Label(self.frame_saisi, text="Nom Client", font=("times new roman", 20,"bold"), bg=background).place(x=70, y=0)
        txt_nom_client = ttk.Entry(self.frame_saisi, textvariable=self.var_nom_client,font=("times new roman",20)).place(x=0, y=50)

        lbl_prenom_client = Label(self.frame_saisi, text="Prénom Client", font=("times new roman", 20,"bold"), bg=background).place(x=70, y=100)
        txt_prenom_client = ttk.Entry(self.frame_saisi,textvariable=self.var_prenom_client ,font=("times new roman",20)).place(x=0, y=150)


        lbl_type_Salle = Label(self.frame_saisi, text="Type Salle", font=("times new roman", 20,"bold"), bg=background).place(x=390, y=0)
        txt_type_Salle = ttk.Entry(self.frame_saisi, textvariable=self.var_type_salle,font=("times new roman",20)).place(x=300, y=50)

        lbl_nom_salle = Label(self.frame_saisi, text="Nom Salle", font=("times new roman", 20,"bold"), bg=background).place(x=390, y=100)
        txt_nom_salle = ttk.Combobox(self.frame_saisi,textvariable=self.var_nom_salle ,font=("times new roman",20),values=self.liste_salle, justify=CENTER, state='r')
        txt_nom_salle.current(0)
        txt_nom_salle.place(x=300, y=150, width=285, height=35)

        lbl_probleme = Label(self.frame_saisi, text="Problème", font=("times new roman", 20,"bold"), bg=background).place(x=690, y=0)
        txt_probleme = ttk.Entry(self.frame_saisi,textvariable=self.var_probleme ,font=("times new roman",20)).place(x=600, y=50)

        lbl_budget = Label(self.frame_saisi, text="Budget", font=("times new roman", 20,"bold"), bg=background).place(x=690, y=100)
        txt_budget = ttk.Entry(self.frame_saisi,textvariable=self.var_budget ,font=("times new roman",20)).place(x=600, y=150)
        



        ###########################
        self.frame_btn = Frame(self.frame_plainte, bg=background,relief=GROOVE, bd=3)
        self.frame_btn.place(x=910,y=0, width=420, height=200)

        self.bnt_ajouter = Button(self.frame_btn,state=NORMAL ,text="Ajouter", command=self.ajouter,font=("times new roman", 20,"bold"), bg="green", cursor="hand2")
        self.bnt_ajouter.place(x=0, y=0, height=40, width=150)

        self.bnt_modifier = Button(self.frame_btn,state=DISABLED,command=self.modifier ,text="Modifier", font=("times new roman", 20,"bold"), bg="yellow", cursor="hand2")
        self.bnt_modifier.place(x=0, y=50, height=40, width=150)

        self.bnt_supprimer = Button(self.frame_btn, state=DISABLED,text="Supprimer",command=self.supprimer ,font=("times new roman", 20,"bold"), bg="red", cursor="hand2")
        self.bnt_supprimer.place(x=0, y=100, height=40, width=150)

        self.bnt_reini = Button(self.frame_btn, text="Réinitialiser",command=self.rein ,font=("times new roman", 20,"bold"), bg="lightgray", cursor="hand2")
        self.bnt_reini.place(x=0, y=150, height=40, width=150)


        type_recherche = ttk.Combobox(self.frame_btn,textvariable=self.var_type_recherche,font=("times new roman",20),values=["Type_Salle", "Nom_Salle", "Probleme"], justify=CENTER, state='r')
        type_recherche.current(0)
        type_recherche.place(x=160, y=0,width=250)

        recherche = ttk.Entry(self.frame_btn, textvariable=self.var_recherche,font=("times new roman",20)).place(x=160, y=50, width=250)

        self.bnt_recherche = Button(self.frame_btn,command=self.recherche,text="Rechercher",font=("times new roman",20,"bold"), cursor="hand2", bg="lightgreen")
        self.bnt_recherche.place(x=160, y=100, height=40, width=250)

        self.bnt_tous = Button(self.frame_btn, text="Tous",command=self.afficher,font=("times new roman",20,"bold"), cursor="hand2", bg="lightyellow")
        self.bnt_tous.place(x=160, y=150, height=40, width=250)


        ##################

        self.frame_tableau = Frame(self.frame_plainte, bg=background,relief=GROOVE, bd=3)
        self.frame_tableau.place(x=0,y=210, relwidth=1, height=385)

        scroll_y = Scrollbar(self.frame_tableau, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(self.frame_tableau, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.plainteliste = ttk.Treeview(self.frame_tableau, columns=("ID","Nom","Prenom", "Type_Salle","Nom_Salle", "Probleme","Budget"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.plainteliste.xview)
        scroll_y.config(command=self.plainteliste.yview)

        self.plainteliste.heading("ID",text="ID", anchor=W)
        self.plainteliste.heading("Nom",text="Nom", anchor=W)
        self.plainteliste.heading("Prenom",text="Prenom", anchor=W)
        self.plainteliste.heading("Type_Salle",text="Type Salle", anchor=W)
        self.plainteliste.heading("Nom_Salle",text="Nom Salle", anchor=W)
        self.plainteliste.heading("Probleme",text="Probleme", anchor=W)
        self.plainteliste.heading("Budget",text="Budget", anchor=W)

        self.plainteliste["show"] = "headings"
        self.plainteliste.pack(fill=BOTH, expand=1)

        self.plainteliste.bind("<ButtonRelease-1>", self.obtenir_information)


        self.afficher()

    def ajouter(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            cur.execute("Insert into plainte (Nom ,Prenom, Type_Salle ,Nom_Salle , Probleme ,Budget ) values(?,?,?,?,?,?)",(
                self.var_nom_client.get(),
                self.var_prenom_client.get(),
                self.var_type_salle.get(),
                self.var_nom_salle.get(),
                self.var_probleme.get(),
                self.var_budget.get()
            ))
            con.commit()
            con.close()
            self.afficher()
            self.rein()
            messagebox.showinfo("Succes","Plainte ajoutée")

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    def afficher(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            cur.execute("select * from plainte")
            rows = cur.fetchall()
            self.plainteliste.delete(*self.plainteliste.get_children())
            for row in rows:
                self.plainteliste.insert("", END, values=row)


        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    def obtenir_information(self, ev):
        self.bnt_ajouter.config(state=DISABLED)
        self.bnt_modifier.config(state=NORMAL)
        self.bnt_supprimer.config(state=NORMAL)
        r = self.plainteliste.focus()
        contenu = self.plainteliste.item(r)
        row = contenu['values']

        self.var_id.set(row[0])
        self.var_nom_client.set(row[1])
        self.var_prenom_client.set(row[2])
        self.var_type_salle.set(row[3])
        self.var_nom_salle.set(row[4])
        self.var_probleme.set(row[5])
        self.var_budget.set(row[6])


    def rein(self):
        self.bnt_ajouter.config(state=NORMAL)
        self.bnt_modifier.config(state=DISABLED)
        self.bnt_supprimer.config(state=DISABLED)
        self.var_nom_client.set("")
        self.var_prenom_client.set("")
        self.var_type_salle.set("")
        self.var_probleme.set("")
        self.var_budget.set("")
    

    def supprimer(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            op = messagebox.askyesno("Confirmer", "Voulez-vous supprimer?")
            if op:
                cur.execute("delete from plainte where ID=?",(self.var_id.get(),))
                con.commit()
                self.afficher()
                self.rein()
                con.close()
                messagebox.showinfo("Succes","Plainte supprimée")  

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    def modifier(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            cur.execute("UPDATE plainte set Nom=? ,Prenom=?, Type_Salle=? ,Nom_Salle=? , Probleme=? ,Budget=? where ID=?",(
               self.var_nom_client.get(),
                self.var_prenom_client.get(),
                self.var_type_salle.get(),
                self.var_nom_salle.get(),
                self.var_probleme.get(),
                self.var_budget.get(),
                self.var_id.get()
            ))
            con.commit()
            con.close()
            self.afficher()
            self.rein()
            messagebox.showinfo("Succès", "Plainte modifiée")

        
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")



    def recherche(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            if self.var_recherche.get()=="":
                messagebox.showerror("Erreur","Saisir le champs recherché")
            else:
                cur.execute("select * from plainte where "+self.var_type_recherche.get()+" LIKE '%"+self.var_recherche.get()+"%'")
                rows = cur.fetchall()

                if len(rows)!=0:
                    self.plainteliste.delete(*self.plainteliste.get_children())
                    for row in rows:
                        self.plainteliste.insert("", END, values=row)

                else:
                    messagebox.showinfo("resultat","Aucun résultat trouvé")


        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")


    def listesalle(self):
        self.liste_salle.append("Vide")
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            cur.execute("select Nom from salle")
            salle = cur.fetchall()
            if len(salle)>0:
                del self.liste_salle[:]
                for i in salle:
                    self.liste_salle.append(i[0])

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")




if __name__=="__main__":
    root = Tk()
    obj = Plainte(root)
    root.mainloop()