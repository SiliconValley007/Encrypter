from cryptography.fernet import Fernet
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from tkinter.filedialog import askdirectory
import os


def ask_quit(): #function to ask if the user really wants to quit
    if messagebox.askokcancel("Quit", "Are You Sure you want to quit?"):
        gui.destroy()

#============================================================================================================================================================================================
def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
#===========================================================================================================================================================================================
def generate_and_load_key():
    try:
        return open("key.key", "rb").read()
    except FileNotFoundError:
        messagebox.showerror('Error!!', "Key not found.")
#===========================================================================================================================================================================================
def load_key(key):
    try:
        return open(key, "rb").read()
    except FileNotFoundError:
        messagebox.showerror('Error!!', "Key not found.")
#===========================================================================================================================================================================================
def already_have_key():
    gui2a = Tk()
    gui2a.configure(background = "yellow")
    gui2a.title("Using previous key")
    gui2a.geometry("650x120+200+270")
    gui2a.resizable(False, False)
    entry_label = Label(gui2a, text="Select to file to encrypt", bg = "yellow")
    file_name = Entry(gui2a, width = 40)
    entry_key = Label(gui2a, text="Select key.key file to be used.", bg = "yellow")
    key_file = Entry(gui2a, width = 40)
    def open_key(): #browse function for key.key files
        key = askopenfile(filetypes = [('Key Files', '*.key')])
        if key is not None:
                key_file.insert(0, key.name)
    def open_file(): #browse function for files to encrypt
        file = askopenfile()
        if file is not None:
            file_name.insert(0, file.name)
    def clear_old_file(): #clear function to clear input fields
        file_name.delete(0, END)
        key_file.delete(0, END)
    btn = Button(gui2a, text='Browse File', command = open_file)
    key_btn = Button(gui2a, text='Browse Key File', command = open_key)
    entry_label.grid(row = 0, column = 0)
    file_name.grid(row = 0, column = 2)
    entry_key.grid(row = 1, column = 0)
    key_file.grid(row = 1, column = 2)
    btn.grid(row = 0, column = 1)
    key_btn.grid(row = 1, column = 1)
    def old_key():
        try:
            filename = file_name.get()
            key_file_path = key_file.get()
            if filename == '':
                messagebox.showwarning('Warning!!','File path not entered')
            elif key_file_path == '':
                messagebox.showwarning('Warning!!','key.key file path not entered')
            else:
                #the key.key file with which to encrypt will be loaded and the selected file will be encrypted
                key = load_key(key_file_path)
                f = Fernet(key)
                with open(filename, "rb") as file:
                    # read all file data
                    file_data = file.read()
                # encrypt data
                encrypted_data = f.encrypt(file_data)
                # write the encrypted file
                with open(filename, "wb") as file:
                    file.write(encrypted_data)
                messagebox.showinfo('Sucess', "File Encrypted")
        except TypeError:
            messagebox.showwarning('Warning!!','Some files not found')
        except FileNotFoundError:
            messagebox.showerror('Error!!', 'File to encrypt not found')
        except ValueError:
            messagebox.showwarning('Error!!', 'The key.key file provided may be corrupt')
    encrypt_button = Button(gui2a, text="Encrypt File", fg = "White", bg="Black", width = 20, command = old_key)
    clear_button = Button(gui2a, text="Clear", command = clear_old_file)
    clear_button.grid(row = 2, column = 0)
    encrypt_button.grid(row = 2, column = 1)
    #to make the window resizable, although for this to work comment out the reziable(False, False) line.
    totalRows = 2
    totalCols = 2
    for row in range(totalRows + 1):
            gui2a.grid_rowconfigure(row, weight=1)
    for col in range(totalCols + 1):
            gui2a.grid_columnconfigure(col, weight=1)
    gui2a.mainloop()
#===========================================================================================================================================================================================
def generate_new_key():
    gui2b = Tk()
    gui2b.configure(background = "yellow")
    gui2b.title("Generating new key")
    gui2b.geometry("650x70+0+600")
    gui2b.resizable(False, False)
    entry_label = Label(gui2b, text="Select or Enter the path of the file to be encrypted", bg = "yellow")
    file_name = Entry(gui2b, width = 40)
    def open_file():
        file = askopenfile()
        if file is not None:
                file_name.insert(0, file.name)
    def clear_new_file():
        file_name.delete(0, END)
    btn = Button(gui2b, text='Browse File', command = open_file)
    entry_label.grid(row = 0, column = 0)
    file_name.grid(row = 0, column = 2)
    btn.grid(row = 0, column = 1)
    def New_key():
        try:
            filename = file_name.get()
            if filename == '':
                    messagebox.showwarning('Warning!!','File path not entered')
            else:
                # a new key will be generated and then the file will be encrypted using the new generated key
                write_key()
                key = generate_and_load_key()
                f = Fernet(key)
                with open(filename, "rb") as file:
                    # read all file data
                    file_data = file.read()
                # encrypt data
                encrypted_data = f.encrypt(file_data)
                # write the encrypted file
                with open(filename, "wb") as file:
                    file.write(encrypted_data)
                messagebox.showinfo('Sucess', "File Encrypted. Key file stored in current directory")
        except FileNotFoundError:
            messagebox.showwarning('Warning!!',f'{filename} not found')
        except ValueError:
                messagebox.showwarning('Error!!', 'The key.key file provided may be corrupt')
    encrypt_button = Button(gui2b, text="Encrypt File", fg="white", bg="Black", width = 20, command = New_key)
    clear_button = Button(gui2b, text="Clear", command = clear_new_file)
    clear_button.grid(row = 2, column = 0)
    encrypt_button.grid(row = 2, column = 1)
    totalRows = 2
    totalCols = 2
    for row in range(totalRows + 1):
            gui2b.grid_rowconfigure(row, weight=1)
    for col in range(totalCols + 1):
            gui2b.grid_columnconfigure(col, weight=1)
    gui2b.mainloop()
#============================================================================================================================================================================================
def encrypt_now():
    gui2 = Tk()
    gui2.configure(background = "yellow")
    gui2.title("Encrypter")
    gui2.geometry("500x150+500+70")
    gui2.resizable(False, False)
    choice = Label(gui2, text="If you have previously run the program and would like to use a previous key.Press here.", fg = "Black", bg = "yellow")
    prev_key = Button(gui2, text="Use previous key", command = already_have_key)

    choice2 = Label(gui2, text="To create a new key and then encrypt file.Click here", fg = "Black", bg = "yellow")
    new_key = Button(gui2, text="Generate New Key", command = generate_new_key)

    choice.grid(row = 0, column = 0)
    prev_key.grid(row = 1, column = 0)
    choice2.grid(row = 2, column = 0)
    new_key.grid(row = 3, column = 0)
    totalRows = 3
    totalCols = 0
    for row in range(totalRows + 1):
            gui2.grid_rowconfigure(row, weight=1)
    for col in range(totalCols + 1):
            gui2.grid_columnconfigure(col, weight=1)
    gui2.mainloop()
#===================================================================================================================================================================================================
def decrypt_now():
    gui3 = Tk()
    gui3.configure(background = "light blue")
    gui3.title("Decrypter")
    gui3.geometry("650x120+750+600")
    gui3.resizable(False, False)
    entry_label = Label(gui3, text="Select or Enter file to be decrypted.", bg = "light blue")
    file_name = Entry(gui3, width = "40")
    entry_key = Label(gui3, text=" Enter key.key file that was used to encrypt the file", bg = "light blue")
    key_file = Entry(gui3, width = "40")
    def open_file():
        file = askopenfile()
        if file is not None:
                file_name.insert(0, file.name)
    def open_key():
        key = askopenfile(filetypes = [('Key Files', '*.key')])
        if key is not None:
                key_file.insert(0, key.name)
    def clear_decrypt():
        file_name.delete(0, END)
        key_file.delete(0, END)
    btn = Button(gui3, text='Browse File', command = open_file)
    key_btn = Button(gui3, text='Browse Key File', command = open_key)
    entry_label.grid(row = 0, column = 0)
    file_name.grid(row = 0, column = 2)
    entry_key.grid(row = 1, column = 0)
    key_file.grid(row = 1, column = 2)
    btn.grid(row = 0, column = 1)
    key_btn.grid(row = 1, column = 1)
    def de():
        try:
            filename = file_name.get()
            keyfile = key_file.get()
            if filename == '':
                messagebox.showwarning('Warning!!','File path not entered')
            elif keyfile == '':
                messagebox.showwarning('Warning!!','key.key file path not entered')
            else:
                key = load_key(keyfile)
                f = Fernet(key)
                with open(filename, "rb") as file:
                    # read the encrypted data
                    encrypted_data = file.read()
                # decrypt data
                decrypted_data = f.decrypt(encrypted_data)
                # write the original file
                with open(filename, "wb") as file:
                    file.write(decrypted_data)
                messagebox.showinfo('Success', "File Decrypted")
        except TypeError:
            messagebox.showwarning('Warning!!','Required Files not found')
        except FileNotFoundError:
            messagebox.showwarning('Warning!!', f'{filename} not found')
        except ValueError:
                messagebox.showwarning('Error!!', 'The key.key file provided may be corrupt')
        except: #this block will be executed when the file provided is already decrypted, or the key provided was not the one with which the file was encrypted
            messagebox.showerror('Error!', 'File provided is not Encrypted or the key provided was not used to encrypt this file.')

    decrypt_button = Button(gui3, text="Decrypt File", fg = "White", bg = "Black", width = 20, command = de)
    clear_button = Button(gui3, text="Clear", command = clear_decrypt)
    clear_button.grid(row = 2, column = 0)
    decrypt_button.grid(row = 2, column = 1)
    totalRows = 2
    totalCols = 2
    for row in range(totalRows + 1):
            gui3.grid_rowconfigure(row, weight=1)
    for col in range(totalCols + 1):
            gui3.grid_columnconfigure(col, weight=1)

    gui3.mainloop()
#=====================================================================================================================================================================================================

def decrypt_folder(): #function to decrypt entire folders 
    gui4 = Tk()
    gui4.configure(background = "red")
    gui4.title("Folder Decrypter")
    gui4.geometry("650x120")
    gui4.resizable(False, False)
    entry_label = Label(gui4, text="Select Folder to be decrypted", bg = "red")
    fold_path = Entry(gui4, width = "40")
    entry_key = Label(gui4, text=" Enter key.key file that was used to encrypt the folder", bg = "red")
    key_file = Entry(gui4, width = "40")
    def open_file():
        file = askdirectory()
        if file is not None:
                fold_path.insert(0, file)
    def open_key():
        key = askopenfile(filetypes = [('Key Files', '*.key')])
        if key is not None:
                key_file.insert(0, key.name)
    def clear_decrypt():
        fold_path.delete(0, END)
        key_file.delete(0, END)
    btn = Button(gui4, text='Browse File', command = open_file)
    key_btn = Button(gui4, text='Browse Key File', command = open_key)
    entry_label.grid(row = 0, column = 0)
    fold_path.grid(row = 0, column = 2)
    entry_key.grid(row = 1, column = 0)
    key_file.grid(row = 1, column = 2)
    btn.grid(row = 0, column = 1)
    key_btn.grid(row = 1, column = 1)
    def folder():
        try:
            folder_path = fold_path.get()
            key_path = key_file.get()
            if folder_path == '':
                messagebox.showwarning('Empty!!', 'Folder path not specified')
            elif key_path == '':
                messagebox.showwarning('Empty!!', 'key file not provided')
            else:
                key = load_key(key_path)
                for subdir, dirs, files in os.walk(folder_path):
                    for filename in files:
                        filepath = subdir + os.sep + filename
                        f = Fernet(key)
                        with open(filepath, "rb") as file:
                            # read the encrypted data
                            encrypted_data = file.read()
                        # decrypt data
                        decrypted_data = f.decrypt(encrypted_data)
                        # write the original file
                        with open(filepath, "wb") as file:
                            file.write(decrypted_data)
                messagebox.showinfo('Success', "Folder Decrypted")
        except TypeError:
            messagebox.showwarning('Warning!!','Required Files not found')
        except FileNotFoundError:
            messagebox.showwarning('Warning!!', f'{filename} not found')
        except ValueError:
            messagebox.showwarning('Error!!', 'The key.key file provided may be corrupt')
        except:
            messagebox.showerror('Error!!', 'Folder provided is not Encrypted or the key provided was not used to encrypt this folder.')
    decrypt_folder_button = Button(gui4, text="Decrypt Folder", fg = "White", bg = "Black", width = 20, command = folder)
    clear_button = Button(gui4, text="Clear", command = clear_decrypt)
    clear_button.grid(row = 2, column = 0)
    decrypt_folder_button.grid(row = 2, column = 1)
    totalRows = 2
    totalCols = 2
    for row in range(totalRows + 1):
            gui4.grid_rowconfigure(row, weight=1)
    for col in range(totalCols + 1):
            gui4.grid_columnconfigure(col, weight=1)

    gui4.mainloop()

#===========================================================================================================================================================================================
def generate_new_key_folder(): #function used to encrypt entire folders at a time.
    gui5b = Tk()
    gui5b.configure(background = "#856ff8")
    gui5b.title("Folder encryption using new key")
    gui5b.geometry("650x70+100+700")
    gui5b.resizable(False, False)
    entry_label = Label(gui5b, text="Enter the path to the folder to be encrypted", bg = "#856ff8")
    file_name = Entry(gui5b, width = 40)
    def open_folder():
        file = askdirectory()
        if file is not None:
                file_name.insert(0, file)
    def clear_new():
        file_name.delete(0, END)
    btn = Button(gui5b, text='Browse Folder', command = open_folder)
    entry_label.grid(row = 0, column = 0)
    file_name.grid(row = 0, column = 2)
    btn.grid(row = 0, column = 1)
    def New_key():
        try:
            filename = file_name.get()
            if filename == '':
                    messagebox.showwarning('Warning!!','Folder path not entered')
            else:
                folder_path = file_name.get()
                write_key()
                for subdir, dirs, files in os.walk(folder_path):
                    for filename in files:
                        filepath = subdir + os.sep + filename
                        key = generate_and_load_key()
                        f = Fernet(key)
                        with open(filepath, "rb") as file:
                            # read all file data
                            file_data = file.read()
                        # encrypt data
                        encrypted_data = f.encrypt(file_data)
                        # write the encrypted file
                        with open(filepath, "wb") as file:
                            file.write(encrypted_data)
                messagebox.showinfo('Sucess', "Folder Encrypted. Key file stored in current directory.")
        except FileNotFoundError:
            messagebox.showwarning('Warning!!',f'{filename} not found')
    encrypt_button = Button(gui5b, text="Encrypt Folder", fg="white", bg="Black", width = 20, command = New_key)
    clear_button = Button(gui5b, text="Clear", command = clear_new)
    clear_button.grid(row = 2, column = 0)
    encrypt_button.grid(row = 2, column = 1)
    totalRows = 2
    totalCols = 2
    for row in range(totalRows + 1):
            gui5b.grid_rowconfigure(row, weight=1)
    for col in range(totalCols + 1):
            gui5b.grid_columnconfigure(col, weight=1)
    gui5b.mainloop()


#===========================================================================================================================================================================================

def encrypt_folder_old(): #function to encrypt entire folders using previously generated keys
    try:
        gui5a = Tk()
        gui5a.configure(background = "#856ff8")
        gui5a.title("Folder encryption using previous key.")
        gui5a.geometry("650x120+200+370")
        gui5a.resizable(False, False)
        entry_label = Label(gui5a, text="Select to Folder to encrypt", bg = "#856ff8")
        file_name = Entry(gui5a, width = 40)
        entry_key = Label(gui5a, text="Select key.key file to be used.", bg = "#856ff8")
        key_file = Entry(gui5a, width = 40)
        def open_key():
            key = askopenfile(filetypes = [('Key Files', '*.key')])
            if key is not None:
                    key_file.insert(0, key.name)
        def open_folder():
            file = askdirectory()
            if file is not None:
                file_name.insert(0, file)
        def clear_old():
            file_name.delete(0, END)
            key_file.delete(0, END)
        btn = Button(gui5a, text='Browse Folder', command = open_folder)
        key_btn = Button(gui5a, text='Browse Key File', command = open_key)
        entry_label.grid(row = 0, column = 0)
        file_name.grid(row = 0, column = 2)
        entry_key.grid(row = 1, column = 0)
        key_file.grid(row = 1, column = 2)
        btn.grid(row = 0, column = 1)
        key_btn.grid(row = 1, column = 1)
        def old_key():
            try:
                foldername = file_name.get()
                key_file_path = key_file.get()
                if foldername == '':
                    messagebox.showwarning('Warning!!','Folder path not entered')
                elif key_file_path == '':
                    messagebox.showwarning('Warning!!','key.key file path not entered')
                else:
                    key = load_key(key_file_path)
                    for subdir, dirs, files in os.walk(foldername):
                        for filename in files:
                            filepath = subdir + os.sep + filename
                            f = Fernet(key)
                            with open(filepath, "rb") as file:
                                # read all file data
                                file_data = file.read()
                            # encrypt data
                            encrypted_data = f.encrypt(file_data)
                            # write the encrypted file
                            with open(filepath, "wb") as file:
                                file.write(encrypted_data)
                    messagebox.showinfo('Sucess', "Folder Encrypted")
            except TypeError:
                messagebox.showwarning('Warning!!','Some files not found')
            except FileNotFoundError:
                messagebox.showerror('Error!!', 'Folder to encrypt not found')
            except ValueError:
                messagebox.showwarning('Error!!', 'The key.key file provided may be corrupt')
        encrypt_button = Button(gui5a, text="Encrypt Folder", fg = "White", bg="Black", width = 20, command = old_key)
        clear_button = Button(gui5a, text="Clear", command = clear_old)
        clear_button.grid(row = 2, column = 0)
        encrypt_button.grid(row = 2, column = 1)
        totalRows = 2
        totalCols = 2
        for row in range(totalRows + 1):
                gui5a.grid_rowconfigure(row, weight=1)
        for col in range(totalCols + 1):
                gui5a.grid_columnconfigure(col, weight=1)
        gui5a.mainloop()
    except FileNotFoundError:
        messagebox.showerror('Error!!', "Required files not found")
#============================================================================================================================================================================================
def encrypt_folder():
    gui5 = Tk()
    gui5.configure(background = "#856ff8")
    gui5.title("Folder Encrypter")
    gui5.geometry("500x150+500+150")
    gui5.resizable(False, False)
    choice = Label(gui5, text="If you have previously run the program and would like to use a previous key.Press here.", fg = "Black", bg = "#856ff8")
    prev_key = Button(gui5, text="Use previous key", command = encrypt_folder_old)

    choice2 = Label(gui5, text="To create a new key and then encrypt folder.Click here", fg = "Black", bg = "#856ff8")
    new_key = Button(gui5, text="Generate New Key", command = generate_new_key_folder)

    choice.grid(row = 0, column = 0)
    prev_key.grid(row = 1, column = 0)
    choice2.grid(row = 2, column = 0)
    new_key.grid(row = 3, column = 0)
    totalRows = 3
    totalCols = 0
    for row in range(totalRows + 1):
            gui5.grid_rowconfigure(row, weight=1)
    for col in range(totalCols + 1):
            gui5.grid_columnconfigure(col, weight=1)
    gui5.mainloop()
#===============================================================================================================================================================================================
if __name__ == "__main__":
    gui = Tk()
    gui.configure(background = "Black")
    gui.title("Encrypter/Decrypter")
    gui.geometry("800x180+500+270")
    gui.resizable(False, False)
    intro_en = Label(gui, text="ENCRYPTER/", fg = "Green", bg = "Black" ,font=("Times", 50))
    intro_de = Label(gui, text="DECRYPTER", fg = "Green", bg = "Black" ,font=("Times", 50))
    encrypt = Button(gui, text = "Encrypt File", bg = "yellow", command = encrypt_now)
    decrypt = Button(gui, text = "Decrypt File", bg = "lightblue", command = decrypt_now)
    decrypt_folder = Button(gui, text = "Decrypt Folder", bg = "red", command = decrypt_folder)
    encrypt_folder = Button(gui, text = "Encrypt Folder", bg = "#856ff8", command = encrypt_folder)
    intro_en.grid(row = 0, column = 0)
    intro_de.grid(row = 0, column = 1)
    encrypt.grid(row = 1, column = 0)
    decrypt.grid(row = 1, column = 1)
    decrypt_folder.grid(row = 2, column = 1)
    encrypt_folder.grid(row = 2, column = 0)
    totalRows = 2
    totalCols = 1
    for row in range(totalRows + 1):
            gui.grid_rowconfigure(row, weight=1)
    for col in range(totalCols + 1):
            gui.grid_columnconfigure(col, weight=1)
    gui.protocol("WM_DELETE_WINDOW", ask_quit) #catch the exit command, when the user presses the close button.
    gui.mainloop()
