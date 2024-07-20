from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
import sqlite3
import os

class Login:
    def __init__(self, root):
        background = "cyan"
        self.root = root
        self.root.title("Login")
        self.root.geometry("1350x630+10+70")
        self.root.config(bg=background)

        titre = Label(self.root, text="Page de Connexion", font=("algerian", 50, "bold"), bg=background).pack()

        self.var_nom_utilisateur = StringVar()
        self.var_mot_de_passe = StringVar()

        self.frame_login = Frame(self.root, bd=5, relief=GROOVE, bg="lightgreen")
        self.frame_login.place(x=490, y=120, height=400, width=400)

        lbl_nom_utilisateur = Label(self.frame_login, text="Nom Utilisateur", font=("times new roman", 20, "bold"), bg="lightgreen").place(x=100, y=50)
        txt_nom_utilisateur = ttk.Entry(self.frame_login,textvariable=self.var_nom_utilisateur ,font=("times new roman",20)).place(x=60, y=100)

        lbl_mot_de_passe = Label(self.frame_login, text="Mot de Passe", font=("times new roman", 20, "bold"), bg="lightgreen").place(x=130, y=150)
        txt_mot_de_passe = ttk.Entry(self.frame_login,show="*",textvariable=self.var_mot_de_passe ,font=("times new roman",20)).place(x=60, y=200)

        btn_connexion = Button(self.frame_login, text="Connexion",command=self.connexion ,font=("times new roman", 20, "bold"), cursor="hand2", bg="lightblue").place(x=120, y=290, height=50)

    def connexion(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()

        try:
            if self.var_mot_de_passe.get()=="" or self.var_nom_utilisateur.get()=="":
                messagebox.showerror("Erreur","Veillez saisir le nom d'utilisateur et le mot de passe")
            else:
                cur.execute("select Role from admin where Login=? and Password=?",(self.var_nom_utilisateur.get(), self.var_mot_de_passe.get()))
                user = cur.fetchone()
                if user==None:
                    messagebox.showerror("Erreur","Nom Utilisateur / Mot de passe incorrecte")
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/administration.py")

                    else:
                        self.root.destroy()
                        os.system("python C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/home.py")

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")


if __name__=="__main__":
    root = Tk()
    obj = Login(root)
    root.mainloop()