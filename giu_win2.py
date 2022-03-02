import re 
from functools import partial
import csv
from complaintListing import ComplaintListing
from configdb import ConnectionDatabase

from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *

conn = ConnectionDatabase()


def en_access(user,passwor,code):
        code=code.get()
        user=user.get()
        passwor=passwor.get()
        if(passnauth_checker(passwor,code)==1):
            with open("pass.txt","a") as file1:
                file1.write(user+","+passwor+"\n")
                file1.close()
                show_frame(op_frame)

def chk_access(user,passwor):        
        with open("pass.txt","r") as file:
            rows=[]
            for row in csv.reader(file):
                rows.append(row)
            
            for row in rows:
                #print(row)
                if row[0] == user.get() and row[1] == passwor.get() :
                    print("username found", lo_username)
                    i= 1
                    break        
                else:
                    i=0
        
        return i       
                    
       
def passnauth_checker(Pass,code):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{7,}$"
    pat = re.compile(reg)
    mat = re.search(pat, Pass)
    if(code=="9918"):     ### auth code
        if mat:
            print("Password is valid.")
            return 1    
        else:
            print("Password invalid !!")
            return 0
    else:
        print("Invalid auth code")
        return 0
    


def validateLogin(username, password):
    print("username entered :", username.get())
    print("password entered :", password.get())
 
    if (chk_access(username,password) == 1):
        show_frame(op_frame)

    return

def show_frame(frame):
    frame.tkraise()
    
window = Tk()


window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

ls_frame = Frame(window)
si_frame = Frame(window)
op_frame = Frame(window)
dm_frame=Frame(window)
db_frame=Frame(window)

for frame in (ls_frame, si_frame, op_frame,dm_frame,db_frame):
    frame.grid(row=0,column=0,sticky='nsew')
    
#==================login sign-up code========================================================================================================#
lola_username=  Label(ls_frame, text='User Name', font='times 15').pack()
lo_username = StringVar()
lo_usernameEntry = Entry(ls_frame, textvariable=lo_username).pack()

lola_password = Label(ls_frame,text="Password").pack()
lo_password = StringVar()
lo_passwordEntry = Entry(ls_frame, textvariable=lo_password, show='*').pack()  

validateLogin = partial(validateLogin, lo_username, lo_password)

lo_btn = Button(ls_frame, text='Login',command=validateLogin).pack()
si_btn = Button(ls_frame, text='Sign-up',command=lambda:show_frame(si_frame)).pack()



#==================sign-up code=========================================================================================================#

sila_username=  Label(si_frame, text='Enter your user name', font='times 15').pack()
si_username = StringVar()
si_usernameEntry = Entry(si_frame, textvariable=si_username).pack()

sila_password = Label(si_frame,text="Enter a valid password \n The password should be longer than 7 characters \n Password should have atleast one upper and lower case\nPassword should contain atleast one special character and number").pack()
si_password = StringVar()
si_passwordEntry =Entry(si_frame, textvariable=si_password, show='*').pack()  

auth_title=  Label(si_frame, text='Enter the auth code', font='times 15').pack()
auth_code = StringVar()
authcodeEntry = Entry(si_frame, textvariable=auth_code, show='*').pack()

en_access= partial(en_access, si_username, si_password,auth_code)

sign_in_btn = Button(si_frame, text='Enter',command=en_access).pack()
si_b_btn = Button(si_frame, text='back',command=lambda:show_frame(ls_frame)).pack()

#==================option code==========================================================================================================#
frame3_title=  Label(op_frame, text='What does the user want to do:', font='times 15').pack()

frame2_r_btn = Button(op_frame, text='File a crime',command=lambda:show_frame(db_frame)).pack()
frame2_b_btn = Button(op_frame, text='Back to login',command=lambda:show_frame(ls_frame)).pack()


#=======================================================db frame============================================================================#





firstname_la=Label(db_frame, text="First Name").pack()
firstname = Entry(db_frame, width=40, font=('Arial', 14))
firstname.pack()
lastname_la=Label(db_frame, text="Last Name").pack()
lastname = Entry(db_frame,  width=40, font=('Arial', 14))
lastname.pack()


GenderGroup = StringVar()
Radiobutton(db_frame, text='Male', value='male', variable=GenderGroup).pack()
Radiobutton(db_frame, text='Female', value='female', variable=GenderGroup).pack()
Label(db_frame, text="Address").pack()
address = Entry(db_frame,  width=40, font=('Arial', 14))
address.pack()
comment_la=Label(db_frame, text="CHARGE").pack()
charge = Text(db_frame, width=40, height=5, font=('Arial', 14))
charge.pack()



def SaveData():
    message = conn.Add(firstname.get(), lastname.get(), address.get(), GenderGroup.get(), charge.get(1.0, 'end'))
    firstname.delete(0,'end')
    lastname.delete(0, 'end')
    address.delete(0, 'end')
    charge.delete(1.0, 'end')
    showinfo(title='Add Information', message=message)

def ShowComplainList():
    listrequest = ComplaintListing()


ButtonList = Button(db_frame, text='View Complain',command=ShowComplainList).pack()
ButtonSubmit = Button(db_frame, text='Submit Now',command=SaveData).pack()
framel_b_btn = Button(db_frame, text='Back ',command=lambda:show_frame(op_frame)).pack()
show_frame(ls_frame)

window.mainloop()