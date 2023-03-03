from ast import Delete
from tkinter import *
from turtle import title
from PIL import ImageTk
from tkinter import messagebox,filedialog
import pandas as pd
import os
import email_function 
import time

class BULK_EMAIL:
    def __init__(self,root):
        self.root=root
        self.root.title("Email Portal")
        self.root.geometry("1000x550+200+50")
        self.root.resizable(False,False)
        self.root.config(bg="white") 

        #=============icons===========

        self.email_icon=ImageTk.PhotoImage(file="email.png")
        self.Settings_icon=ImageTk.PhotoImage(file="Setting.png")


        #======title==================

        title=Label(self.root,text="Email Portal",image=self.email_icon,padx=130,compound=LEFT,font=("Goudy Old Style",48,"bold"),bg="#222A35",fg="white",anchor="w").place(x=0,y=0,relwidth=1)
        desc=Label(self.root,text="USE EXCEL FILE TO SEND BULK EMAILS AT ONCE, WITH JUST A SINGLE CLICK, ENSURE THE EMAIL COLUMN NAME MUST BE EMAIL",font=("Calibri (Body)",10),bg="#FFD966",fg="#262626").place(x=0,y=80,relwidth=1)

        btn_setting=Button(self.root,image=self.Settings_icon,bd=0,activebackground="#222A35",bg="#222A35",cursor="hand2",command=self.setting_window).place(x=800,y=5)

        #---------------------------------------------------
        self.var_choice=StringVar()
        single=Radiobutton(self.root,text="Single",value="single",variable=self.var_choice,activebackground="white",font=("times new roman", 30, "bold"),bg="white",fg="#262626",command=self.check_single_or_bulk).place(x=50,y=120)
        Bulk=Radiobutton(self.root,text="Bulk",value="bulk",variable=self.var_choice,activebackground="white",font=("times new roman", 30, "bold"),bg="white",fg="#262626",command=self.check_single_or_bulk).place(x=250,y=120)
        self.var_choice.set("single")


        #----------------------------------------------------

        to=Label(self.root,text="TO (Email Address)",font=("times new roman",18),bg="white").place(x=50,y=220)
        sub=Label(self.root,text="Subject",font=("times new roman",18),bg="white").place(x=50,y=270)
        msg=Label(self.root,text="Message",font=("times new roman",18),bg="white").place(x=50,y=320)

        self.txt_to=Entry(self.root,font=("times new roman",14),bg="lightyellow")
        self.txt_to.place(x=300,y=220,width=350,height=30)

        self.btn_browse=Button(self.root,command=self.browse_file,text="Browse",font=("times new roman",18,"bold"),bg="#262626",fg="white",cursor="hand2",state=DISABLED)
        self.btn_browse.place(x=670,y=220,width=120,height=30)

        self.txt_sub=Entry(self.root,font=("times new roman",14),bg="lightyellow")
        self.txt_sub.place(x=300,y=270,width=450,height=30)

        self.txt_msg=Text(self.root,font=("times new roman",12),bg="lightyellow")
        self.txt_msg.place(x=300,y=320,width=650,height=140)

#-----------------------------STATUS---------------------------
        self.lbl_total=Label(self.root,font=("times new roman",18),bg="white")
        self.lbl_total.place(x=50,y=490)

        self.lbl_sent=Label(self.root,font=("times new roman",18),bg="white", fg="green")
        self.lbl_sent.place(x=300,y=490)

        self.lbl_left=Label(self.root,font=("times new roman",18),bg="white", fg="orange")
        self.lbl_left.place(x=420,y=490)

        self.lbl_failed=Label(self.root,font=("times new roman",18),bg="white", fg="red")
        self.lbl_failed.place(x=550,y=490)



        btn_send=Button(self.root,command=self.send_email,text="SEND",font=("times new roman",18,"bold"),bg="#00B0F0",fg="white",cursor="hand2").place(x=700,y=490,width=120,height=30)
        btn_clear=Button(self.root,command=self.clear1,text="CLEAR",font=("times new roman",18,"bold"),bg="#262626",fg="white",cursor="hand2").place(x=830,y=490,width=120,height=30)

        self.check_file_exist()

    def browse_file(self):
        op=filedialog.askopenfile(initialdir='/',title="Select Excel File For Emails",filetypes=(("All files","*.*"),("Excel Files",".xlsx")))
        if op!=None:
            data=pd.read_excel(op.name)
            if 'Email' in data.columns:
                self.emails=list(data['Email'])
                c=[]
                for i in self.emails :   
                    if pd.isnull(i)==False:
                    
                        c.append(i)
                self.emails=c
                if len(self.emails)>0:
                    self.txt_to.config(state=NORMAL)
                    self.txt_to.delete(0,END)
                    self.txt_to.insert(0,str(op.name.split("/")[-1]))
                    self.txt_to.config(state='readonly')
                    self.lbl_total.config(text="Total:"+str(len(self.emails)))
                    self.lbl_sent.config(text="Sent:")
                    self.lbl_left.config(text="Left:")
                    self.lbl_failed.config(text="Failed:")
                else:
                    messagebox.showerror("Error", "This file does not have any emails", parent=self.root)
            else:
                messagebox.showerror("Error","Please Select File Which have Email Columns", parent=self.root)
 

    


    def send_email(self):
        x=len(self.txt_msg.get('1.0',END))
        if self.txt_to.get()==""or self.txt_sub.get()=="" or x==1:
            messagebox.showerror("Error", "All fields are required",parent=self.root)
        else:
            if self.var_choice.get()=="single":
                status=email_function.email_send_funct(self.txt_to.get(),self.txt_sub.get(),self.txt_msg.get('1.0',END),self.from_,self.passw)
                if status=="s":
                    messagebox.showinfo("Success", "Email has been sent",parent=self.root)
                if status=="f":
                    messagebox.showerror("Failed", "Email not sent, Try Again",parent=self.root)
            if self.var_choice.get()=="bulk":
                self.failed=[]
                self.s_count=0
                self.f_count=0
                for x in self.emails:
                    status=email_function.email_send_funct(x,self.txt_sub.get(),self.txt_msg.get('1.0',END),self.from_,self.passw)
                    if status=="s":
                        self.s_count+=1
                    if status=="f":
                        self.f_count+=1
                    self.status_bar()                   
                messagebox.showinfo("Success", "Email has been sent, Please check status",parent=self.root)
    def status_bar(self):
        self.lbl_total.config(text="STATUS:"+str(len(self.emails))+"=>>")
        self.lbl_sent.config(text="Sent:"+str(self.s_count))
        self.lbl_left.config(text="Left:"+str(len(self.emails)-(self.s_count+self.f_count)))
        self.lbl_failed.config(text="Failed:"+str(self.f_count))  
        self.lbl_total.update()
        self.lbl_sent.update() 
        self.lbl_left.update() 
        self.lbl_failed.update()           

    def check_single_or_bulk(self):
        if self.var_choice.get()=="single":
             self.btn_browse.config(state=DISABLED)
             self.txt_to.config(state=NORMAL)
             self.txt_to.delete(0,END)
             self.clear1()
        if self.var_choice.get()=="bulk":
             self.btn_browse.config(state=NORMAL)
             self.txt_to.delete(0,END)
             self.txt_to.config(state='readonly')
             

    def clear1(self):
        self.txt_to.config(state=NORMAL)
        self.txt_to.delete(0,END)
        self.txt_sub.delete(0,END)
        self.txt_msg.delete('1.0',END)
        self.var_choice.set("single")
        self.btn_browse.config(state=DISABLED)
        self.lbl_total.config(text="")
        self.lbl_sent.config(text="")
        self.lbl_left.config(text="")
        self.lbl_failed.config(text="")


    def setting_window(self):
        self.check_file_exist()
        self.root2=Toplevel()
        self.root2.title("Settings")
        self.root2.geometry("700x310+350+90")
        self.root2.focus_force()
        self.root2.grab_set()
        self.root2.config(bg="white")
        title2=Label(self.root2,text="Settings Portal",image=self.Settings_icon,padx=70,compound=LEFT,font=("Goudy Old Style",48,"bold"),bg="#222A35",fg="white",anchor="w").place(x=0,y=0,relwidth=1)
        desc2=Label(self.root2,text="Enter the email and password from which to send the all emails",font=("Calibri (Body)",10),bg="#FFD966",fg="#262626").place(x=0,y=80,relwidth=1)

        from_=Label(self.root2,text="Email Address",font=("times new roman",18),bg="white").place(x=50,y=130)
        Passw=Label(self.root2,text="Password",font=("times new roman",18),bg="white").place(x=50,y=180)

        self.txt_from=Entry(self.root2,font=("times new roman",14),bg="lightyellow")
        self.txt_from.place(x=250,y=130,width=410,height=30)
        self.txt_pass=Entry(self.root2,font=("times new roman",14),bg="lightyellow",show="*")
        self.txt_pass.place(x=250,y=180,width=410,height=30)

        btn_save=Button(self.root2,command=self.save_setting,text="SAVE",font=("times new roman",18,"bold"),bg="#00B0F0",fg="white",cursor="hand2").place(x=330,y=220,width=120,height=30)
        btn_clear2=Button(self.root2,command=self.clear2,text="CLEAR",font=("times new roman",18,"bold"),bg="#262626",fg="white",cursor="hand2").place(x=470,y=220,width=120,height=30)
        self.txt_from.insert(0,self.from_)
        self.txt_pass.insert(0,self.passw)

    def clear2(self):
        self.txt_from.delete(0,END)
        self.txt_pass.delete(0,END)

    def check_file_exist(self):
        if os.path.exists("important.txt")==False:
            f=open('important.txt','w')
            f.write(",")
            f.close()
        f2=open('important.txt','r')   
        self.credentials=[]
        for i in f2:
           
           self.credentials.append( [i.split(",")[0],i.split(",")[1]])
        
        self.from_=self.credentials[0][0]
        self.passw=self.credentials[0][1]
        

    def save_setting(self):
        if self.txt_from.get()=="" or self.txt_pass.get()=="":
            messagebox.showerror("Error", "All fields are required",parent=self.root2)
        else:
            f=open('important.txt','w')
            f.write(self.txt_from.get()+","+self.txt_pass.get())
            f.close()
            messagebox.showinfo("Success", "Saved Succesfully",parent=self.root2)
            self.check_file_exist()


root=Tk()
ojb=BULK_EMAIL(root)
root.mainloop()