from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
import sqlite3
import os
import tempfile
from tkcalendar import *
from datetime import datetime
from time import strftime

class Reservation:
    def __init__(self, root):
        background = "cyan"
        self.root = root
        self.root.title("Reservation")
        self.root.geometry("1350x630+10+70")
        self.root.config(bg=background)


        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS reservation(ID INTEGER PRIMARY KEY AUTOINCREMENT,Mobile text,Date_Debut date, Date_Fin date,Type_Salle text, Nom_Salle text,Nombre_Place text,Type_Activite text,Prix_Salle text,Nombre_Jour text,Total_Payer text)")
        con.commit()
        con.close()


        self.ck_print = 0
        self.liste_facture = []
        self.liste_salle= []
        self.listesalle() 

        self.frame_reservation = LabelFrame(self.root, text="Réservation", bg=background ,bd=3, relief=RIDGE, font=("times new roman",15, "bold"), width=1340, height=625)
        self.frame_reservation.place(x=5, y=0)


        ########################### Saisir données
        self.var_id = IntVar()
        self.var_mobile = StringVar()
        self.var_type_salle = StringVar()
        self.var_nom_salle = StringVar()
        self.var_nombre_place = StringVar()
        self.var_type_activite = StringVar()
        self.var_prix_salle = StringVar()
        self.var_nombre_jour = StringVar()
        self.var_total_a_payer = StringVar()

        self.frame_saisi = Frame(self.frame_reservation, bd=3, relief=RAISED, bg=background, width=500,height=500)
        self.frame_saisi.place(x=0, y=0)

        lbl_mobile = Label(self.frame_saisi, text="Mobile", font=("times new roman",15,"bold"), bg=background).place(x=0, y=5)
        txt_mobile = ttk.Entry(self.frame_saisi,textvariable=self.var_mobile, font=("times new roman",12)).place(x=100, y=0, width=150, height=35)

        btn_verifier = Button(self.frame_saisi,command=self.verifier_identite ,text="Vérifier Identité", font=("times new roman",13, "bold"), bg="lightgreen", cursor="hand2").place(x=260, y=0)

        lbl_date_debut = Label(self.frame_saisi, text="Date Début", font=("times new roman",20,"bold"), bg=background).place(x=0, y=45)
        self.var_date_debut = DateEntry(self.frame_saisi, font=("times new roman",20), date_pattern="dd/mm/yy", justify=CENTER, state="r")
        self.var_date_debut.place(x=200, y=45,width=285)

        lbl_date_fin = Label(self.frame_saisi, text="Date Fin", font=("times new roman",20,"bold"), bg=background).place(x=0, y=90)
        self.var_date_fin = DateEntry(self.frame_saisi, font=("times new roman",20), date_pattern="dd/mm/yy", justify=CENTER, state="r")
        self.var_date_fin.place(x=200, y=90,width=285)

        lbl_type_Salle = Label(self.frame_saisi, text="Type Salle", font=("times new roman", 20,"bold"), bg=background).place(x=0, y=135)
        txt_type_Salle = ttk.Entry(self.frame_saisi,textvariable=self.var_type_salle,font=("times new roman",20)).place(x=200, y=135)

        lbl_nom_salle = Label(self.frame_saisi, text="Nom Salle", font=("times new roman", 20,"bold"), bg=background).place(x=0, y=180)
        txt_nom_salle = ttk.Combobox(self.frame_saisi,textvariable=self.var_nom_salle ,font=("times new roman",20),values=self.liste_salle, justify=CENTER, state='r')
        txt_nom_salle.current(0)
        txt_nom_salle.place(x=200, y=180, width=285, height=35)

        lbl_nombre_place = Label(self.frame_saisi, text="Nombre Place", font=("times new roman", 20,"bold"), bg=background).place(x=0, y=225)
        txt_nombre_place = ttk.Entry(self.frame_saisi,textvariable=self.var_nombre_place,font=("times new roman",20)).place(x=200, y=225)

        lbl_type_active = Label(self.frame_saisi, text="Type Activité", font=("times new roman", 20,"bold"), bg=background).place(x=0, y=270)
        txt_type_active = ttk.Entry(self.frame_saisi,textvariable=self.var_type_activite,font=("times new roman",20)).place(x=200, y=270)

        lbl_prix_salle = Label(self.frame_saisi, text="Prix de la Salle", font=("times new roman", 20,"bold"), bg=background).place(x=0, y=315)
        txt_prix_salle = ttk.Entry(self.frame_saisi,textvariable=self.var_prix_salle,font=("times new roman",20)).place(x=200, y=315)

        lbl_nombre_jour = Label(self.frame_saisi, text="Nombre Jour(s)", font=("times new roman", 20,"bold"), bg=background).place(x=0, y=360)
        self.txt_nombre_jour = Label(self.frame_saisi,text="",font=("times new roman",20), bg="lightgray")
        self.txt_nombre_jour.place(x=200, y=360, width=285, height=40)

        lbl_total_a_payer = Label(self.frame_saisi, text="Total à Payer", font=("times new roman", 20,"bold"), bg=background).place(x=0, y=405)
        txt_total_a_paye = ttk.Entry(self.frame_saisi,textvariable=self.var_total_a_payer,state="r",font=("times new roman",20)).place(x=200, y=405)

        bnt_facture = Button(self.frame_saisi, text="Facture",command=self.facture ,font=("times new roman",15, "bold"), bg="gold", cursor="hand2").place(x=20, y=450, width=110)

        
        ################# Bouton

        self.frame_btn = Frame(self.frame_reservation,bd=3, relief=RAISED, bg=background, width=500,height=80)
        self.frame_btn.place(x=0, y=510)

        self.btn_reservation = Button(self.frame_btn, text="Réservation",state=NORMAL ,command=self.reservation,font=("times new roman",15, "bold"), bg="green", cursor="hand2")
        self.btn_reservation.place(x=0, y=17, width=110)

        self.btn_modifier = Button(self.frame_btn, text="Modifier",command=self.modifier,state=DISABLED, font=("times new roman",15, "bold"), bg="yellow", cursor="hand2")
        self.btn_modifier.place(x=125, y=17, width=110)

        self.btn_annuler = Button(self.frame_btn, text="Annuler",command=self.supprimer,state=DISABLED, font=("times new roman",15, "bold"), bg="red", cursor="hand2")
        self.btn_annuler.place(x=250, y=17, width=110)

        self.btn_reini = Button(self.frame_btn, text="Réinitialiser",command=self.reini ,font=("times new roman",15, "bold"), bg="lightgray", cursor="hand2")
        self.btn_reini.place(x=375, y=17, width=110)


        ##########Affiche
        self.frame_affiche = Frame(self.frame_reservation, bd=3, relief=RAISED, bg=background, width=820,height=590)
        self.frame_affiche.place(x=510, y=0)

        

        ###########Vérifier l'identité

        self.frame_verifie_identite = Frame(self.frame_affiche,bd=3, relief=RAISED, bg=background, width=810,height=150)
        self.frame_verifie_identite.place(x=0, y=0)

        ####Recehcher
        self.var_type_recheche = StringVar()
        self.var_recheche = StringVar()
        self.frame_recheche = LabelFrame(self.frame_affiche, text="Rechercher", font=("times new roman", 20,"bold"), bd=3, relief=RAISED, bg=background, width=810, height=100)
        self.frame_recheche.place(x=0, y=160)

        type_rechecher = ttk.Combobox(self.frame_recheche,textvariable=self.var_type_recheche, values=["Facture", "Mobile","Date_Debut","Nom_Salle"], justify=CENTER, state="r", font=("times new roman",20, "bold"), width=12)
        type_rechecher.current(0)
        type_rechecher.place(x=0,y=15)

        recherche = ttk.Entry(self.frame_recheche,textvariable=self.var_recheche ,font=("times new roman",20, "bold"), width=17).place(x=205, y=15)

        btn_rechecher = Button(self.frame_recheche, text="Rechercher",command=self.recherche ,font=("times new roman",17, "bold"), bg="lightgreen", cursor="hand2").place(x=455, y=15, height=37)
        btn_tous = Button(self.frame_recheche, text="Tous",command=self.afficher ,font=("times new roman",17, "bold"), bg="lightgray", cursor="hand2").place(x=600, y=15, height=37)
        btn_imprimer = Button(self.frame_recheche, text="Imprimer",command=self.imprimer ,font=("times new roman",17, "bold"), bg="lightyellow", cursor="hand2").place(x=680, y=15, height=37)

        #######Facture
        FactureFrame = Frame(self.frame_affiche, bd=4, relief=GROOVE, bg="white")
        FactureFrame.place(x=400, y=270, width=400,height=310)
        
        ctitre = Label(FactureFrame, text="Zone de Facture Client", font=("goudy old style",20,"bold"),bg="#f44336", bd=3, relief=RIDGE).pack(side=TOP, fill=X)
        
        scrolly = Scrollbar(FactureFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx = Scrollbar(FactureFrame, orient=HORIZONTAL)
        scrollx.pack(side=BOTTOM, fill=X)

        self.txt_espace_facture = Text(FactureFrame, yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        self.txt_espace_facture.pack(fill=BOTH, expand=1)

        scrollx.config(command=self.txt_espace_facture.xview)
        scrolly.config(command=self.txt_espace_facture.yview)


        ##########Frame Tableau
        self.frame_tableau = Frame(self.frame_affiche, bd=4, relief=GROOVE, bg=background)
        self.frame_tableau.place(x=0, y=270, width=400,height=310)


        scroll_y = Scrollbar(self.frame_tableau, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(self.frame_tableau, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.reservationliste = ttk.Treeview(self.frame_tableau, columns=("ID","Mobile","Date_Debut", "Date_Fin","Type_Salle", "Nom_Salle","Nombre_Place","Type_Activite","Prix_Salle","Nombre_Jour","Total_Payer"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.reservationliste.xview)
        scroll_y.config(command=self.reservationliste.yview)

        self.reservationliste.heading("ID",text="ID", anchor=W)
        self.reservationliste.heading("Mobile",text="Mobile", anchor=W)
        self.reservationliste.heading("Date_Debut",text="Date Debut", anchor=W)
        self.reservationliste.heading("Date_Fin",text="Date Fin", anchor=W)
        self.reservationliste.heading("Type_Salle",text="Type Salle", anchor=W)
        self.reservationliste.heading("Nom_Salle",text="Nom Salle", anchor=W)
        self.reservationliste.heading("Nombre_Place",text="Nombre Place", anchor=W)
        self.reservationliste.heading("Type_Activite",text="Type Activite", anchor=W)
        self.reservationliste.heading("Prix_Salle",text="Prix Salle", anchor=W)
        self.reservationliste.heading("Nombre_Jour",text="Nombre Jour", anchor=W)
        self.reservationliste.heading("Total_Payer",text="Total Payer", anchor=W)

        self.reservationliste["show"] = "headings"
        self.reservationliste.pack(fill=BOTH, expand=1)
        self.reservationliste.bind("<ButtonRelease-1>", self.obtenir_information)



        self.afficher()


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

    def verifier_identite(self):
        if self.var_mobile.get()=="":
            messagebox.showerror("Erreur","Veillez saisir le numéro du client")
        else:
            con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
            cur = con.cursor()

            cur.execute("select Nom from client where Mobile=?",(self.var_mobile.get(),))
            self.var_nom = cur.fetchone()
            if self.var_nom == None:
                messagebox.showerror("Erreur","Le client n'est pas enrégistré")
            else:
                con.commit()
                con.close()
                lbl_nom = Label(self.frame_verifie_identite, text="Nom : ", font=("times new roman", 20, "bold"), bg="cyan").place(x=0, y=0)
                self.nom = Label(self.frame_verifie_identite, text=self.var_nom, font=("times new roman", 20), bg="cyan")
                self.nom.place(x=110, y=0, width=190)

            ########################## Prenom

                con = sqlite3.connect(database=r"C:\Users\uthma\OneDrive\TopSecret\Mes_Mini_Projet\Gestion_Reservation\gestionreservation.db")
                cur = con.cursor()

                cur.execute("select Prenom from client where Mobile=?",(self.var_mobile.get(),))
                self.var_prenom = cur.fetchone()
                con.commit()
                con.close()
                lbl_prenom = Label(self.frame_verifie_identite, text="Prénom : ", font=("times new roman", 20, "bold"), bg="cyan").place(x=0, y=50)
                self.prenom = Label(self.frame_verifie_identite, text=self.var_prenom, font=("times new roman", 20), bg="cyan")
                self.prenom.place(x=110, y=50, width=190)


            ########################## Pays

                con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
                cur = con.cursor()

                cur.execute("select Pays from client where Mobile=?",(self.var_mobile.get(),))
                self.var_pays = cur.fetchone()
                
                con.commit()
                con.close()
                lbl_pays = Label(self.frame_verifie_identite, text="Pays : ", font=("times new roman", 20, "bold"), bg="cyan").place(x=0, y=100)
                self.pays = Label(self.frame_verifie_identite, text=self.var_pays, font=("times new roman", 20), bg="cyan")
                self.pays.place(x=110, y=100, width=190)

            ########################## Type Identité

                con = sqlite3.connect(database=r"C:\Users\uthma\OneDrive\TopSecret\Mes_Mini_Projet\Gestion_Reservation\gestionreservation.db")
                cur = con.cursor()

                cur.execute("select Type_Identite from client where Mobile=?",(self.var_mobile.get(),))
                self.var_type_identite = cur.fetchone()
           
                con.commit()
                con.close()
                lbl_type_identite = Label(self.frame_verifie_identite, text="Type Identité : ", font=("times new roman", 15, "bold"), bg="cyan").place(x=300, y=0)
                self.type_identite = Label(self.frame_verifie_identite, text=self.var_type_identite, font=("times new roman", 15), bg="cyan")
                self.type_identite.place(x=510, y=0, width=190)

                ########################## Numéro Identité

                con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
                cur = con.cursor()

                cur.execute("select Numero_Identite from client where Mobile=?",(self.var_mobile.get(),))
                self.var_numero_identite = cur.fetchone()
                con.commit()
                con.close()
                lbl_n_identite = Label(self.frame_verifie_identite, text="Numéro Identité : ", font=("times new roman", 15, "bold"), bg="cyan").place(x=300, y=30)
                self.n_identite = Label(self.frame_verifie_identite, text=self.var_numero_identite, font=("times new roman", 15), bg="cyan")
                self.n_identite.place(x=510, y=30, width=190)

            ########################## Adresse

                con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
                cur = con.cursor()

                cur.execute("select Adresse from client where Mobile=?",(self.var_mobile.get(),))
                self.var_adresse = cur.fetchone()
           
                con.commit()
                con.close()
                lbl_adresse = Label(self.frame_verifie_identite, text="Adresse : ", font=("times new roman", 15, "bold"), bg="cyan").place(x=300, y=60)
                self.adresse = Label(self.frame_verifie_identite, text=self.var_adresse, font=("times new roman", 15), bg="cyan")
                self.adresse.place(x=510, y=60, width=190)

            ########################## DSG

                con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
                cur = con.cursor()

                cur.execute("select DSG from client where Mobile=?",(self.var_mobile.get(),))
                self.var_dsg = cur.fetchone()
            
                con.commit()
                con.close()
                lbl_gsg = Label(self.frame_verifie_identite, text="DS/G : ", font=("times new roman", 15, "bold"), bg="cyan").place(x=300, y=90)
                self.gsg = Label(self.frame_verifie_identite, text=self.var_dsg, font=("times new roman", 15), bg="cyan")
                self.gsg.place(x=510, y=90, width=190)

    def facture(self):
        date_debut = self.var_date_debut.get_date()
        date_fin = self.var_date_fin.get_date()
        if date_debut==date_fin:
            messagebox.showerror("Erreur","Date de début doit être différente à la date de fin")
        else:
            delta = date_fin - date_debut
            self.var_nombre_jour = delta.days
            nombre_jour = self.var_nombre_jour
            prix_place = int(self.var_prix_salle.get())

            total_a_pays = prix_place * nombre_jour

            tt = str(total_a_pays)

            self.txt_nombre_jour.config(text=f"{self.var_nombre_jour}")
            print(self.var_nombre_jour)
            self.var_total_a_payer.set(tt)
    def modifier(self):
        date_debut = self.var_date_debut.get_date()
        date_fin = self.var_date_fin.get_date()
        nombre_jour = str(self.var_nombre_jour)
        if self.var_mobile.get()=="":
            messagebox.showerror("Erreur","Veillez saisir le numéro mobile")
        elif self.var_nombre_jour<0:
            messagebox.showerror("Erreur","La date de début ne doit pas être inférieur à la date de fin")
        else: 
            try:
        #ID,Mobile text,Date_Debut date, Date_Fin date,Type_Salle text, Nom_Salle text,Nombre_Place text,Type_Activite text,Prix_Salle text,Nombre_Jour text,Total_Payer text)")

                con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
                cur = con.cursor()
                cur.execute("select count(*) FROM reservation WHERE Nom_Salle = ? AND ((Date_Debut <= ? AND Date_Fin >= ?) OR (Date_Debut <= ? AND Date_Fin >= ?))",
                (self.var_nom_salle.get(), date_fin, date_debut, date_debut, date_fin))
                count = cur.fetchone()[0]
    
                if count==0:
                    cur.execute("update reservation set Mobile=?, Date_Debut=?, Date_Fin=?, Type_Salle=?, Nom_Salle=?, Nombre_Place=?, Type_Activite=?, Prix_Salle=?, Nombre_Jour=?, Total_Payer=? WHERE ID=?",(
                        self.var_mobile.get(),
                        date_debut,
                        date_fin,
                        self.var_type_salle.get(),
                        self.var_nom_salle.get(),
                        self.var_nombre_place.get(),
                        self.var_type_activite.get(),
                        self.var_prix_salle.get(),
                        nombre_jour,
                        self.var_total_a_payer.get(),
                        self.var_id.get()
                    ))
                    con.commit()
                    con.close()
                    self.afficher()
                    self.genere_facture()
                    self.reini()
                    messagebox.showinfo("Succès","Réservation modifiée")
                else:
                    messagebox.showerror("Erreur", "La date est déjà réservé")

            except Exception as ex:
                messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")
    def reservation(self):
        date_debut = self.var_date_debut.get_date()
        date_fin = self.var_date_fin.get_date()
        nombre_jour = str(self.var_nombre_jour)
        if self.var_mobile.get()=="":
            messagebox.showerror("Erreur","Veillez saisir le numéro mobile")
        elif self.var_nombre_jour<0:
            messagebox.showerror("Erreur","La date de début ne doit pas être inférieur à la date de fin")
        elif date_debut==date_fin:
            messagebox.showerror("Erreur","Date de début doit être différente à la date de fin")
        else:
            try:

                con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
                cur = con.cursor()
                cur.execute("select count(*) FROM reservation WHERE Nom_Salle = ? AND ((Date_Debut <= ? AND Date_Fin >= ?) OR (Date_Debut <= ? AND Date_Fin >= ?))",
                (self.var_nom_salle.get(), date_fin, date_debut, date_debut, date_fin))
                count = cur.fetchone()[0]
    
                if count==0:
                    cur.execute("insert into reservation (Mobile, Date_Debut, Date_Fin, Type_Salle, Nom_Salle, Nombre_Place, Type_Activite, Prix_Salle, Nombre_Jour, Total_Payer) values(?,?,?,?,?,?,?,?,?,?)",(
                        self.var_mobile.get(),
                        date_debut,
                        date_fin,
                        self.var_type_salle.get(),
                        self.var_nom_salle.get(),
                        self.var_nombre_place.get(),
                        self.var_type_activite.get(),
                        self.var_prix_salle.get(),
                        nombre_jour,
                        self.var_total_a_payer.get()                          
                    ))
                    con.commit()
                    con.close()
                    self.afficher()
                    self.reini()
                    self.genere_facture()
                    messagebox.showinfo("Succes", "Réservation éffectuée")
                    
                else:
                    messagebox.showerror("Erreur", "La date est déjà réservé")

            except Exception as ex:
                messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")


    def afficher(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            cur.execute("select * from reservation")
            rows = cur.fetchall()
            self.reservationliste.delete(*self.reservationliste.get_children())
            for row in rows:
                self.reservationliste.insert("", END, values=row)


        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    def obtenir_information(self, ev):
        self.btn_reservation.config(state=DISABLED)
        self.btn_modifier.config(state=NORMAL)
        self.btn_annuler.config(state=NORMAL)

        r = self.reservationliste.focus()
        contenu = self.reservationliste.item(r)
        row = contenu["values"]

        self.var_id.set(row[0])
        self.var_mobile.set(row[1])

        date_str = row[2]
        date_obj = datetime.strptime(date_str,"%Y-%m-%d")
        date_inverse = datetime.strftime(date_obj, "%d/%m/%Y")
        self.var_date_debut.set_date(date_inverse)

        date_str1 = row[3]
        date_obj1 = datetime.strptime(date_str1,"%Y-%m-%d")
        date_inverse1 = datetime.strftime(date_obj1, "%d/%m/%Y")
        self.var_date_fin.set_date(date_inverse1)

        delta = date_obj1 - date_obj

        self.var_nombre_jour = delta.days

        self.var_type_salle.set(row[4])
        self.var_nom_salle.set(row[5])
        self.var_nombre_place.set(row[6])
        self.var_type_activite.set(row[7])
        self.var_prix_salle.set(row[8])
        self.txt_nombre_jour.config(text=f"{self.var_nombre_jour}")
        self.var_total_a_payer.set(row[10])


    def supprimer(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            op = messagebox.askyesno("Confirmer","Voulez-vous vraiment annuler la réservation?")
            if op==True:
                cur.execute("delete from reservation where ID=?",(self.var_id.get(),))
                con.commit()
                con.close()
                self.afficher()
                self.reini()
                messagebox.showinfo("Succes","Réservation annulée")   
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    def genere_facture(self):
        if self.var_id.get()=="":
            messagebox.showerror("Erreur","Choisir une réservation")
        else:
            self.entete_facture()
            self.footer_facture()
           

            fp = open(fr"C:\Users\uthma\OneDrive\TopSecret\Mes_Mini_Projet\Gestion_Reservation\facture\{str(self.facture)}.txt", "w")
            fp.write(self.txt_espace_facture.get("1.0",END))
            fp.close()
            messagebox.showinfo("Succes","La facture a été modifié")
            self.ck_print = 1
    

    def entete_facture(self):
        con = sqlite3.connect(database=r"C:\Users\uthma\OneDrive\TopSecret\Mes_Mini_Projet\Gestion_Reservation\gestionreservation.db")
        cur = con.cursor()

        cur.execute("select Nom from client where Mobile=?",(self.var_mobile.get(),))
        self.var_nom_client=cur.fetchone()[0]
        con.commit()
        con.close()

        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()

        cur.execute("select Prenom from client where Mobile=?",(self.var_mobile.get(),))
        self.var_prenom_client=cur.fetchone()[0]
        con.commit()
        con.close()

        self.facture = int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))

        facture_entete = f'''
        \t\t\tReservation Salle
{str("="*57)}
Nom du Client : {self.var_nom_client}
Prenom du Client : {self.var_prenom_client}
Tel du Client : {self.var_mobile.get()}
Numero Facture : {str(self.facture)}
Date : {str(time.strftime("%d/%m/%Y"))}
{str("="*57)}
    '''
        self.txt_espace_facture.delete("1.0",END)
        self.txt_espace_facture.insert("1.0", facture_entete)

    def footer_facture(self):
        facture_footer = f'''

{str("="*57)}
Date Debut : \t\t\t\t {self.var_date_debut.get()}
Date Fin : \t\t\t\t {self.var_date_fin.get()}
Nom Salle : \t\t\t\t {self.var_nom_salle.get()}
Somme Total: \t\t\t\t {self.var_total_a_payer.get()}

'''
        self.txt_espace_facture.insert(END, facture_footer)
        
    def imprimer(self):
        if self.ck_print==1:
            messagebox.showinfo("Imprimer","Veillez patienter pendant l'impression")
            fichier = tempfile.mktemp(".txt")
            open(fichier,"w").write(self.txt_espace_facture.get("1.0",END))
            os.startfile(fichier,"print")
        else:
            messagebox.showerror("Veillez générer la facture")

    def recherche(self):
        if self.var_type_recheche.get()=="Facture":
            for i in os.listdir(r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/facture"):
                if i.split(".")[-1]=="txt":
                    self.liste_facture.append(i.split(".")[0])
            if self.var_recheche.get() in self.liste_facture:
                fichier_ouvert = open(fr"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/facture/{self.var_recheche.get()}.txt", "r")
                self.txt_espace_facture.delete("1.0", END)
                for i in fichier_ouvert:
                    self.txt_espace_facture.insert(END, i)
                fichier_ouvert.close()
            else:
                messagebox.showerror("Erreur", "Numéro de la facture est invalide")
        else:
            con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
            cur = con.cursor()
            try:
                if self.var_recheche.get()=="":
                    messagebox.showerror("Erreur","Saisir le champs recherché")
                else:
                    cur.execute("select * from reservation where "+self.var_type_recheche.get()+" LIKE '%"+self.var_recheche.get()+"%'")
                    rows = cur.fetchall()

                    if len(rows)!=0:
                        self.reservationliste.delete(*self.reservationliste.get_children())
                        for row in rows:
                            self.reservationliste.insert("", END, values=row)

                    else:
                        messagebox.showinfo("resultat","Aucun résultat trouvé")


            except Exception as ex:
                messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")
    def reini(self):
        self.btn_reservation.config(state=NORMAL)
        self.btn_annuler.config(state=DISABLED)
        self.btn_modifier.config(state=DISABLED)

        self.var_mobile.set("")
        self.var_type_salle.set("")
        self.var_nom_salle.set("")
        self.var_nombre_place.set("")
        self.var_type_activite.set("")
        self.var_prix_salle.set("")
        self.txt_nombre_jour.config(text="")
        self.var_total_a_payer.set("")
if __name__=="__main__":
    root = Tk()
    obj = Reservation(root)
    root.mainloop()