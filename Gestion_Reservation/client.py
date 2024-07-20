from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
import sqlite3
import os
import random

class Client:
    def __init__(self, root):
        background = "cyan"
        self.root = root
        self.root.title("Client")
        self.root.geometry("1350x630+10+70")
        self.root.config(bg=background)

        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS client(Matricule INTEGER PRIMARY KEY,DSG text,Nom text,Prenom text,Pays text,Adresse text,Postal text,Type_Identite text,Numero_Identite text,Email text,Mobile text)")
        con.commit()
        con.close()

        self.frameclient = LabelFrame(self.root, text="Détails du client", font=("times new roman",15, "bold"),bd=4, bg=background, relief=GROOVE, width=1340, height=625)
        self.frameclient.place(x=5,y=0)
        #####Zone de saisie
        self.frame_saisi = Frame(self.frameclient,bg=background, bd=2, relief=RAISED, width=500, height=520)
        self.frame_saisi.place(x=10, y=0)

        self.var_matricule = StringVar()
        x = random.randint(1000000, 9999999)
        self.var_matricule.set(str(x))

        self.var_dsg = StringVar()
        self.var_nom = StringVar()
        self.var_prenom = StringVar()
        self.var_pays = StringVar()
        self.var_adresse = StringVar()
        self.var_code_postal = StringVar()
        self.var_type_identite = StringVar()
        self.var_numero_identite = StringVar()
        self.var_email = StringVar()
        self.var_mobile = StringVar()

        lbl_matricule = Label(self.frame_saisi, text="Matricule",font=("times new roman",20, "bold"), bg=background).place(x=10, y=10)
        txt_matricule = Entry(self.frame_saisi, font=("times new roman",20),textvariable=self.var_matricule, state=DISABLED).place(x=180, y=10, width=300)

        lbl_dsg = Label(self.frame_saisi, text="DS/G", font=("times new roman",20, "bold"), bg=background).place(x=10, y=55)
        txt_dsg = Entry(self.frame_saisi,textvariable=self.var_dsg, font=("times new roman",20)).place(x=180, y=55, width=300)

        lbl_nom = Label(self.frame_saisi, text="Nom", font=("times new roman",20, "bold"), bg=background).place(x=10, y=100)
        txt_nom = Entry(self.frame_saisi, textvariable=self.var_nom,font=("times new roman",20)).place(x=180, y=100, width=300)

        lbl_prenom = Label(self.frame_saisi, text="Prénom", font=("times new roman",20, "bold"), bg=background).place(x=10, y=145)
        txt_prenom = Entry(self.frame_saisi, textvariable=self.var_prenom,font=("times new roman",20)).place(x=180, y=145, width=300)

        lbl_pays = Label(self.frame_saisi, text="Pays", font=("times new roman",20, "bold"), bg=background).place(x=10, y=190)
        txt_pays = Entry(self.frame_saisi,textvariable=self.var_pays ,font=("times new roman",20)).place(x=180, y=190, width=300)

        lbl_adresse = Label(self.frame_saisi, text="Adresse", font=("times new roman",20, "bold"), bg=background).place(x=10, y=235)
        txt_adresse = Entry(self.frame_saisi,textvariable=self.var_adresse ,font=("times new roman",20)).place(x=180, y=235, width=300)

        lbl_code_postal = Label(self.frame_saisi, text="Code Postal", font=("times new roman",20, "bold"), bg=background).place(x=10, y=280)
        txt_code_postal = Entry(self.frame_saisi, textvariable=self.var_code_postal,font=("times new roman",20)).place(x=180, y=280, width=300)

        lbl_type_identite = Label(self.frame_saisi, text="Type Identité", font=("times new roman",20, "bold"), bg=background).place(x=10, y=325)
        txt_type_identite = ttk.Combobox(self.frame_saisi, textvariable=self.var_type_identite,values=["CNI", "Passport"], state="r", justify=CENTER, font=("times new roman",20))
        txt_type_identite.current(0)
        txt_type_identite.place(x=180, y=325,width=300, height=40)

        lbl_numero_identite = Label(self.frame_saisi, text="N° Identité", font=("times new roman",20, "bold"), bg=background).place(x=10, y=370)
        txt_numero_identite = Entry(self.frame_saisi,textvariable=self.var_numero_identite ,font=("times new roman",20)).place(x=180, y=370, width=300)

        lbl_email = Label(self.frame_saisi, text="Email", font=("times new roman",20, "bold"), bg=background).place(x=10, y=415)
        txt_email = Entry(self.frame_saisi, textvariable=self.var_email,font=("times new roman",20)).place(x=180, y=415, width=300)

        lbl_mobile = Label(self.frame_saisi, text="Mobile", font=("times new roman",20, "bold"), bg=background).place(x=10, y=460)
        txt_mobile = Entry(self.frame_saisi,textvariable=self.var_mobile ,font=("times new roman",20)).place(x=180, y=460, width=300)



        ####Zone Bouton
        self.frame_bouton = Frame(self.frameclient, bd=2, bg=background, relief=RAISED,width=500, height=50)
        self.frame_bouton.place(x=10, y=540)
        
        self.bnt_ajouter = Button(self.frame_bouton,text="Ajouter" ,state=NORMAL,command=self.ajouter,font=("times new roman", 15,"bold"), bg="green", cursor="hand2")
        self.bnt_ajouter.place(x=0, y=5, width=120)

        self.bnt_modifier = Button(self.frame_bouton,text="Modifier" ,command=self.modifier,state=DISABLED, font=("times new roman", 15,"bold"), bg="yellow", cursor="hand2")
        self.bnt_modifier.place(x=125, y=5, width=120)

        self.bnt_supprimer = Button(self.frame_bouton,text="Supprimer",command=self.supprimer ,state=DISABLED,font=("times new roman", 15,"bold"), bg="red", cursor="hand2")
        self.bnt_supprimer.place(x=250, y=5, width=120)

        self.bnt_reini = Button(self.frame_bouton,text="Réinitialiser" ,command=self.reini,font=("times new roman", 15,"bold"), bg="lightgray", cursor="hand2")
        self.bnt_reini.place(x=375, y=5, width=120)


        ###Zone Affichage
        self.frame_table = Frame(self.frameclient, bd=2,bg=background,relief=RAISED,width=810, height=590)
        self.frame_table.place(x=520, y=0)

        self.frame_recherche = LabelFrame(self.frame_table, text="Recherche par", font=("times new roman", 20,"bold"), bg=background, width=790,height=100)
        self.frame_recherche.place(x=10, y=10)

        self.var_type_recherche = StringVar()
        self.var_recherche = StringVar()

        txt_type_recherche = ttk.Combobox(self.frame_recherche, textvariable=self.var_type_recherche,values=["Nom", "Prenom","Mobile"], state="r", justify=CENTER, font=("times new roman",20))
        txt_type_recherche.current(0)
        txt_type_recherche.place(x=0, y=10,width=250)

        txt_recherche = Entry(self.frame_recherche,textvariable=self.var_recherche ,font=("times new roman",20)).place(x=260, y=10, width=300)

        self.bnt_recherche = Button(self.frame_recherche,command=self.recherche,text="Rechercher" ,font=("times new roman", 15,"bold"), bg="lightgray", cursor="hand2").place(x=580, y=10, height=37)
        self.bnt_tous = Button(self.frame_recherche,text="Tous", command=self.afficher,font=("times new roman", 15,"bold"), bg="lightgray", cursor="hand2").place(x=710, y=10, height=37)

        ###Liste

        self.frame_tree = Frame(self.frame_table, bd=3, relief=RIDGE, bg=background)
        self.frame_tree.place(x=10, y=120 ,height=460, width=790)

        scrol_y = Scrollbar(self.frame_tree, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = Scrollbar(self.frame_tree, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.clientliste = ttk.Treeview(self.frame_tree, columns=("Matricule","DSG","Nom","Prenom","Pays","Adresse","Postal","Type_Identite","Numero_Identite","Email","Mobile"),yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)

        scrol_x.config(command=self.clientliste.xview)
        scrol_y.config(command=self.clientliste.yview)

        self.clientliste.heading("Matricule", text="Matricule",anchor=W)
        self.clientliste.heading("DSG", text="DSG",anchor=W)
        self.clientliste.heading("Nom", text="Nom",anchor=W)
        self.clientliste.heading("Prenom", text="Prenom",anchor=W)
        self.clientliste.heading("Adresse", text="Adresse",anchor=W)
        self.clientliste.heading("Postal", text="Code Postal",anchor=W)
        self.clientliste.heading("Type_Identite", text="Type Identite",anchor=W)
        self.clientliste.heading("Numero_Identite", text="Numero Identite",anchor=W)
        self.clientliste.heading("Email", text="Email",anchor=W)
        self.clientliste.heading("Mobile", text="Mobile",anchor=W)

        self.clientliste["show"] = "headings"
        self.clientliste.pack(fill=BOTH, expand=1)
        self.clientliste.bind("<ButtonRelease-1>",self.obtenir_information)

        self.afficher()
    

    def ajouter(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            if self.var_nom.get()=="" or self.var_prenom.get()=="" or self.var_mobile.get()=="" or self.var_type_identite.get()=="" or self.var_numero_identite.get()=="":
                messagebox.showerror("Erreur","Veillez remplir les champs obligatoire")
            else:
                cur.execute("select * from client where Matricule=?",(self.var_matricule.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Erreur","Le Matricule existe déjà")
                else:
                    cur.execute("insert into client (Matricule,DSG,Nom,Prenom,Pays,Adresse,Postal,Type_Identite,Numero_Identite,Email,Mobile) values(?,?,?,?,?,?,?,?,?,?,?)",(
                        self.var_matricule.get(),
                        self.var_dsg.get(),
                        self.var_nom.get(),
                        self.var_prenom.get(),
                        self.var_pays.get(),
                        self.var_adresse.get(),
                        self.var_code_postal.get(),
                        self.var_type_identite.get(),
                        self.var_numero_identite.get(),
                        self.var_email.get(),
                        self.var_mobile.get()
                    ))

                    con.commit()
                    con.close()
                    self.afficher()
                    self.reini()
                    messagebox.showinfo("Succes","Client ajouté")

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    def afficher(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            cur.execute("select * from client")
            rows = cur.fetchall()
            self.clientliste.delete(*self.clientliste.get_children())
            for row in rows:
                self.clientliste.insert("", END, values=row)


        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    def obtenir_information(self, ev):
        self.bnt_ajouter.config(state=DISABLED)
        self.bnt_modifier.config(state=NORMAL)
        self.bnt_supprimer.config(state=NORMAL)
        r=self.clientliste.focus()
        contenu = self.clientliste.item(r)
        row = contenu['values']
        self.var_matricule.set(row[0])
        self.var_dsg.set(row[1])
        self.var_nom.set(row[2])
        self.var_prenom.set(row[3])
        self.var_pays.set(row[4])
        self.var_adresse.set(row[5])
        self.var_code_postal.set(row[6])
        self.var_type_identite.set(row[7])
        self.var_numero_identite.set(row[8])
        self.var_email.set(row[9])
        self.var_mobile.set(row[10])

    def reini(self):
        self.bnt_ajouter.config(state=NORMAL)
        self.bnt_modifier.config(state=DISABLED)
        self.bnt_supprimer.config(state=DISABLED)
        x = random.randint(1000000, 9999999)
        self.var_matricule.set(str(x))
        self.var_dsg.set("")
        self.var_nom.set("")
        self.var_prenom.set("")
        self.var_pays.set("")
        self.var_adresse.set("")
        self.var_code_postal.set("")
        self.var_type_identite.set("CNI")
        self.var_numero_identite.set("")
        self.var_email.set("")
        self.var_mobile.set("")
    
    def modifier(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            cur.execute("update client set DSG=?,Nom=?,Prenom=?,Pays=?,Adresse=?,Postal=?,Type_Identite=?,Numero_Identite=?,Email=?,Mobile=? where Matricule=?",(
                
                        self.var_dsg.get(),
                        self.var_nom.get(),
                        self.var_prenom.get(),
                        self.var_pays.get(),
                        self.var_adresse.get(),
                        self.var_code_postal.get(),
                        self.var_type_identite.get(),
                        self.var_numero_identite.get(),
                        self.var_email.get(),
                        self.var_mobile.get(),
                        self.var_matricule.get()
            ))     
            con.commit()
            con.close()
            self.afficher()
            self.reini()
            messagebox.showinfo("Succes","Client modifié")   

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    def supprimer(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            op = messagebox.askyesno("Confirmer","Voulez-vous vraiment supprimer le client?")
            if op==True:
                cur.execute("delete from client where Matricule=?",(self.var_matricule.get(),))
                con.commit()
                con.close()
                self.afficher()
                self.reini()
                messagebox.showinfo("Succes","Client modifié")   
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    def recherche(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            if self.var_recherche.get()=="":
                messagebox.showerror("Erreur","Saisir le champs recherche")
            else:
                cur.execute("select * from client where "+self.var_type_recherche.get()+" Like '%"+self.var_recherche.get()+"%'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.clientliste.delete(*self.clientliste.get_children())
                    for row in rows:
                        self.clientliste.insert("", END, values=row)
                else:
                    messagebox.showerror("Erreur","Aucun résultat trouvé")
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")
if __name__=="__main__":
    root = Tk()
    obj = Client(root)
    root.mainloop()