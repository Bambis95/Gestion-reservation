from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
import sqlite3
import os

class Salle:
    def __init__(self, root):
        background = "cyan"
        self.root = root
        self.root.title("Salle")
        self.root.geometry("620x300+10+70")
        self.root.config(bg=background)

        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS salle(id INTEGER PRIMARY KEY AUTOINCREMENT, Nom text)")
        con.commit()
        con.close()

        self.var_id = IntVar()
        self.var_salle = StringVar()

        lbl_salle = Label(self.root, text="Salle", font=("times new roman",20, "bold"), bg=background).place(x=100, y=0)
        txt_salle = ttk.Entry(self.root,textvariable=self.var_salle, font=("times new roman", 20)).place(x=10, y=50)

        self.btn_ajouter = Button(self.root, text="Ajouter",command=self.ajouter,font=("times new roman",20, "bold"), bg="green",cursor="hand2")
        self.btn_ajouter.place(x=300, y=50, height=40,width=150 )


        self.btn_supprimer = Button(self.root, text="Supprimer",command=self.supprimer,font=("times new roman",20, "bold"), bg="red",cursor="hand2")
        self.btn_supprimer.place(x=460, y=50, height=40,width=150 )

        self.frame_tableau = Frame(self.root, bg=background,relief=GROOVE, bd=3)
        self.frame_tableau.place(x=0,y=100, relwidth=1, height=200)

        scroll_y = Scrollbar(self.frame_tableau, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(self.frame_tableau, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.salleliste = ttk.Treeview(self.frame_tableau, columns=("ID","Nom"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.salleliste.xview)
        scroll_y.config(command=self.salleliste.yview)

        self.salleliste.heading("ID",text="ID", anchor=W)
        self.salleliste.heading("Nom",text="Nom Salle", anchor=W)

        self.salleliste["show"] = "headings"
        self.salleliste.pack(fill=BOTH, expand=1)

        self.salleliste.bind("<ButtonRelease-1>", self.obtenir_information)

        self.afficher()
    
    def ajouter(self):
        try:
            con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
            cur = con.cursor()
            cur.execute("insert into salle (Nom) values(?)",(self.var_salle.get(),))
            con.commit()
            self.afficher()
            con.close()
            self.var_salle.set("")
            messagebox.showinfo("Succes","Salle ajoutée")
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    
    def afficher(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            cur.execute("select * from salle")
            rows = cur.fetchall()
            self.salleliste.delete(*self.salleliste.get_children())
            for row in rows:
                self.salleliste.insert("", END, values=row)

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    def obtenir_information(self, ev):
        r = self.salleliste.focus()
        contenu = self.salleliste.item(r)
        row = contenu['values']
        self.var_id.set(row[0])
        self.var_salle.set(row[1])

    
    def supprimer(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            op = messagebox.askyesno("Confirmer", "Voulez-vous supprimer?")
            if op:
                cur.execute("delete from salle where id=?",(self.var_id.get(),))
                con.commit()
                self.afficher()
                con.close()
                messagebox.showinfo("Succes","Salle supprimée")  
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

if __name__=="__main__":
    root = Tk()
    obj = Salle(root)
    root.mainloop()