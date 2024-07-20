from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
import sqlite3
import os
import random

class Employe:
    def __init__(self, root):
        background = "cyan"
        self.root = root
        self.root.title("Employe")
        self.root.geometry("1350x630+10+70")
        self.root.config(bg=background)

        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS admin(Id INTEGER PRIMARY KEY, Nom text, Prenom text, Login text,Role text, Password text)")
        con.commit()
        con.close()

        self.var_matricule = StringVar()
        x = random.randint(1000000, 9999999)
        self.var_matricule.set(str(x))

        self.var_nom = StringVar()
        self.var_prenom = StringVar()
        self.var_login = StringVar()
        self.var_password = StringVar()
        self.var_role = StringVar()
        self.var_type_recherche = StringVar()
        self.var_recheche = StringVar()

        self.var_matricule.set(str(x))
        self.framadminitration = LabelFrame(self.root,text="Administration" ,font=("times new roman",15,"bold"),bg=background, bd=4, relief=GROOVE, width=1340, height=625)
        self.framadminitration.place(x=5, y=0)

        ####Frame details information employé

        self.frame_saisi = Frame(self.framadminitration, bg=background, relief=GROOVE, bd=3)
        self.frame_saisi.place(x=0, y=0, width=900, height=200)

        lbl_matricule = Label(self.frame_saisi, text="Matricule",font=("times new roman",20,"bold"), bg=background).place(x=70, y=0)
        txt_matricule = ttk.Entry(self.frame_saisi,state=DISABLED,textvariable=self.var_matricule ,font=("times new roman",20)).place(x=0, y=50)

        lbl_nom = Label(self.frame_saisi, text="Nom",font=("times new roman",20,"bold"), bg=background).place(x=120, y=100)
        txt_nom = ttk.Entry(self.frame_saisi,textvariable=self.var_nom ,font=("times new roman",20)).place(x=0, y=150)


        lbl_prenom = Label(self.frame_saisi, text="Prénom",font=("times new roman",20,"bold"), bg=background).place(x=390, y=0)
        txt_prenom = ttk.Entry(self.frame_saisi,textvariable=self.var_prenom ,font=("times new roman",20)).place(x=300, y=50)

        lbl_login = Label(self.frame_saisi, text="Login",font=("times new roman",20,"bold"), bg=background).place(x=350, y=100)
        txt_login = ttk.Entry(self.frame_saisi,textvariable=self.var_login ,font=("times new roman",20)).place(x=300, y=150)


        lbl_mot_de_passe = Label(self.frame_saisi, text="Mot de passe",font=("times new roman",20,"bold"), bg=background).place(x=660, y=0)
        txt_mot_de_passe = ttk.Entry(self.frame_saisi,show="*",textvariable=self.var_password ,font=("times new roman",20)).place(x=600, y=50)


        lbl_role = Label(self.frame_saisi,text="Role",font=("times new roman",20,"bold"), bg=background).place(x=700, y=100)
        txt_role = ttk.Combobox(self.frame_saisi,textvariable=self.var_role ,font=("times new roman",20),values=["Admin", "Personnel"], justify=CENTER, state='r')
        txt_role.current(0)
        txt_role.place(x=600, y=150,width=285)


        #####Frame bouton

        self.frame_btn = Frame(self.framadminitration, bd=3, relief=RAISED,bg=background)
        self.frame_btn.place(x=910, y=0, height=200, width=420)

        self.bnt_ajouter = Button(self.frame_btn, text="Ajouter",state=NORMAL,command=self.ajouter,font=("times new roman",20,"bold"), cursor="hand2", bg="green")
        self.bnt_ajouter.place(x=0, y=0, height=40, width=150)

        self.bnt_modifier = Button(self.frame_btn, text="Modifier",command=self.modifier,state=DISABLED,font=("times new roman",20,"bold"), cursor="hand2", bg="yellow")
        self.bnt_modifier.place(x=0, y=50, height=40, width=150)

        self.bnt_supprimer = Button(self.frame_btn, text="Supprimer",command=self.supprimer,state=DISABLED,font=("times new roman",20,"bold"), cursor="hand2", bg="red")
        self.bnt_supprimer.place(x=0, y=100, height=40, width=150)

        self.bnt_reini = Button(self.frame_btn, text="Réinitialiser",command=self.reini,font=("times new roman",20,"bold"), cursor="hand2", bg="lightgray")
        self.bnt_reini.place(x=0, y=150, height=40, width=150)

        type_recherche = ttk.Combobox(self.frame_btn,textvariable=self.var_type_recherche,font=("times new roman",20),values=["Nom", "Prenom", "Role", "Login"], justify=CENTER, state='r')
        type_recherche.current(0)
        type_recherche.place(x=160, y=0,width=250)

        recherche = ttk.Entry(self.frame_btn,textvariable=self.var_recheche ,font=("times new roman",20)).place(x=160, y=50, width=250)

        self.bnt_recherche = Button(self.frame_btn,command=self.recherche ,text="Rechercher",font=("times new roman",20,"bold"), cursor="hand2", bg="lightgreen")
        self.bnt_recherche.place(x=160, y=100, height=40, width=250)

        self.bnt_tous = Button(self.frame_btn, text="Tous",command=self.afficher,font=("times new roman",20,"bold"), cursor="hand2", bg="lightyellow")
        self.bnt_tous.place(x=160, y=150, height=40, width=250)




        #####Frame Tableau

        self.frame_tableau = Frame(self.framadminitration, bd=3, relief=RIDGE,bg=background)
        self.frame_tableau.place(x=0, y=210, height=365, relwidth=1)

        scroll_y = Scrollbar(self.frame_tableau, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(self.frame_tableau, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.adminliste = ttk.Treeview(self.frame_tableau, columns=("Id","Nom","Prenom", "Login","Role"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.adminliste.xview)
        scroll_y.config(command=self.adminliste.yview)

        self.adminliste.heading("Id",text="Matricule", anchor=W)
        self.adminliste.heading("Nom",text="Nom", anchor=W)
        self.adminliste.heading("Prenom",text="Prenom", anchor=W)
        self.adminliste.heading("Login",text="Login", anchor=W)
        self.adminliste.heading("Role",text="Role", anchor=W)

        self.adminliste["show"] = "headings"
        self.adminliste.pack(fill=BOTH, expand=1)

        self.adminliste.bind("<ButtonRelease-1>", self.obtenir_information)


        self.afficher()

    
    def ajouter(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()

        try:
            cur.execute("select * from admin where Login=?",(self.var_login.get(),))
            ro = cur.fetchone()
            if ro != None:
                messagebox.showerror("Erreur","Le nom d'utilisateur existe déjà")
            else:
                cur.execute("insert into admin (Id, Nom , Prenom , Login,Role, Password) values(?,?,?,?,?,?)",(
                    self.var_matricule.get(),
                    self.var_nom.get(),
                    self.var_prenom.get(),
                    self.var_login.get(),
                    self.var_role.get(),
                    self.var_password.get()
                ))
                con.commit()
                self.afficher()
                self.reini()
                con.close()
                messagebox.showinfo("Succes","Employé ajouté")
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    
    def afficher(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            cur.execute("select * from admin")
            rows = cur.fetchall()
            self.adminliste.delete(*self.adminliste.get_children())
            for row in rows:
                self.adminliste.insert("", END, values=row)


        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    
    def obtenir_information(self, ev):
        self.bnt_ajouter.config(state=DISABLED)
        self.bnt_modifier.config(state=NORMAL)
        self.bnt_supprimer.config(state=NORMAL)
        r=self.adminliste.focus()
        contenu = self.adminliste.item(r)
        row = contenu['values']

        self.var_matricule.set(row[0])
        self.var_nom.set(row[1])
        self.var_prenom.set(row[2])
        self.var_login.set(row[3])
        self.var_role.set(row[4])
        self.var_password.set(row[5])

    def modifier(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            cur.execute("update admin set Nom=? , Prenom=? , Login=?,Role=?, Password=? where Id=?",(
                self.var_nom.get(),
                self.var_prenom.get(),
                self.var_login.get(),
                self.var_role.get(),
                self.var_password.get(),
                self.var_matricule.get()
            ))

            con.commit()
            self.afficher()
            self.reini()
            con.close()
            messagebox.showinfo("Succes","Employé modifié")
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")
    
    def supprimer(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            op = messagebox.askyesno("Confirmer", "Voulez-vous supprimer?")
            if op:
                cur.execute("delete from admin where Id=?",(self.var_matricule.get(),))
                con.commit()
                self.afficher()
                self.reini()
                con.close()
                messagebox.showinfo("Succes","Employé supprimé")  

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    def reini(self):
        self.bnt_ajouter.config(state=NORMAL)
        self.bnt_modifier.config(state=DISABLED)
        self.bnt_supprimer.config(state=DISABLED)
        x = random.randint(1000000, 9999999)
        self.var_matricule.set(str(x))

        self.var_nom.set("")
        self.var_prenom.set("")
        self.var_login.set("")
        self.var_role.set("Admin")
        self.var_password.set("")

    def recherche(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            if self.var_recheche.get()=="":
                messagebox.showerror("Erreur","Saisir le champs recherché")
            else:
                cur.execute("select * from admin where "+self.var_type_recherche.get()+" LIKE '%"+self.var_recheche.get()+"%'")
                rows = cur.fetchall()

                if len(rows)!=0:
                    self.adminliste.delete(*self.adminliste.get_children())
                    for row in rows:
                        self.adminliste.insert("", END, values=row)

                else:
                    messagebox.showinfo("resultat","Aucun résultat trouvé")


        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")


if __name__=="__main__":
    root = Tk()
    obj = Employe(root)
    root.mainloop()