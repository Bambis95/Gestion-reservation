from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
import sqlite3
import os

class Home:
    def __init__(self, root):
        background = "cyan"
        self.root = root
        self.root.title("Home")
        self.root.geometry("1366x700+0+0")
        self.root.config(bg=background)

        Employe = Button(self.root, text="Employe",command=self.page_employe ,font=("times new roman", 15,"bold"), bd=0, activebackground=background, bg=background, cursor="hand2").place(x=10, y=10)
        Salle = Button(self.root, text="Salle",command=self.page_salle ,font=("times new roman", 15,"bold"), bd=0, activebackground=background, bg=background, cursor="hand2").place(x=100, y=10)
        
        
        deconnecter = Button(self.root,command=self.deconnecte ,text="Deconnecter", font=("times new roman", 15,"bold"), bd=0, activebackground=background, bg="red", cursor="hand2").place(x=1240, y=15)

        self.frame_main = Frame(self.root, bd=4, relief=RAISED, width=1350, height=650)
        self.frame_main.place(x=10, y=45)

        self.lbl_heure = Label(self.frame_main, text="Bienvenu Chez khadim Devsec Réservation\t\t Date : DD-MM-YYYY\t\t Heure : HH:MM:SS", font=("times new roman",15), bg="black", fg="white")
        self.lbl_heure.place(x=0, y=0, relwidth=1, height=40)

        self.corp2 = Frame(self.frame_main, bg="#009aa5")
        self.corp2.place(x=10, y=200, width=310, height=220)

        self.totalclientImage = Image.open(r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/image/left-icon.png")
        photo = ImageTk.PhotoImage(self.totalclientImage)
        self.totalclient= Label(self.corp2, image=photo,bg="#009aa5")
        self.totalclient.image = photo
        self.totalclient.place(x=220, y=0)

        self.ntotalcllient_text = Label(self.corp2, text="0", bg="#009aa5", font=("times new roman", 25,"bold"))
        self.ntotalcllient_text.place(x=120, y=100)

        self.totalcllient_text = Label(self.corp2, text="Total Client", bg="#009aa5", font=("times new roman", 25,"bold"))
        self.totalcllient_text.place(x=5, y=5)

        #######

        self.corp3 = Frame(self.frame_main, bg="#e21f26")
        self.corp3.place(x=500, y=200, width=310, height=220)

        self.totalemplyeImage = Image.open(r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/image/left-icon.png")
        photo = ImageTk.PhotoImage(self.totalemplyeImage)
        self.totalemplye= Label(self.corp3, image=photo,bg="#e21f26")
        self.totalemplye.image = photo
        self.totalemplye.place(x=220, y=0)

        self.ntotalemploye_text = Label(self.corp3, text="0", bg="#e21f26", font=("times new roman", 25,"bold"))
        self.ntotalemploye_text.place(x=120, y=100)

        self.totalemploye_text = Label(self.corp3, text="Total Employé", bg="#e21f26", font=("times new roman", 25,"bold"))
        self.totalemploye_text.place(x=5, y=5)


        ##############

        self.corp4 = Frame(self.frame_main, bg="#ffcb1f")
        self.corp4.place(x=1000, y=200, width=310, height=220)

        self.totalventeImage = Image.open(r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/image/earn3.png")
        photo = ImageTk.PhotoImage(self.totalventeImage)
        self.totalvente= Label(self.corp4, image=photo,bg="#ffcb1f")
        self.totalvente.image = photo
        self.totalvente.place(x=220, y=0)

        self.ntotalvente_text = Label(self.corp4, text="0", bg="#ffcb1f", font=("times new roman", 25,"bold"))
        self.ntotalvente_text.place(x=120, y=100)

        self.totalvente_text = Label(self.corp4, text="Total Vente", bg="#ffcb1f", font=("times new roman", 25,"bold"))
        self.totalvente_text.place(x=5, y=5)

        self.modifier_contenu()

    def page_employe(self):
        os.system("python C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/employe.py")


    def page_salle(self):
        os.system("python C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/salle.py")

        
    def deconnecte(self):
        self.root.destroy()
        os.system("python C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/login.py")

    
    def modifier_contenu(self):
        con = sqlite3.connect(database=r"C:/Users/windows 10/OneDrive/Bureau/Gestion_Reservation/gestionreservation.db")
        cur = con.cursor()
        try:
            cur.execute("select * from client")
            client = cur.fetchall()
            self.ntotalcllient_text.config(text=f"{str(len(client))}")

            cur.execute("select * from admin")
            admin = cur.fetchall()
            self.ntotalemploye_text.config(text=f"{str(len(admin))}")

            cur.execute("select sum(Total_Payer) from reservation")
            total = cur.fetchall()
            self.ntotalvente_text.config(text=total)

            heure_ = (time.strftime("%H:%M:%S"))
            date_ = (time.strftime("%d-%m-%Y"))
            self.lbl_heure.config(text=f"Bienvenu Chez khadim Devsec Réservation\t\t Date : {str(date_)}\t\t Heure : {str(heure_)}")
            self.lbl_heure.after(200,self.modifier_contenu)

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}") 


if __name__=="__main__":
    root = Tk()
    obj = Home(root)
    root.mainloop()