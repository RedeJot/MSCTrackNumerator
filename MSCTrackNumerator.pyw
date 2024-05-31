
import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Listbox, CENTER, END
from PIL import Image, ImageTk
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR

class App:
    def __init__(self):
        self.path_filename = "data\Path_dir.txt"
        self.songs = []
        self.root = tk.Tk()
        self.root.geometry('700x500')
        self.root.title('MSCTrackNumerator')
        self.root.iconbitmap('data\mscicon.ico')
        self.root.resizable(False, False)
        
        self.mainframe = tk.Frame(self.root, width=100, height=100)
        self.mainframe.pack(fill='none', expand=False)
        self.mainframe.place(relx=0.5, rely=0.5, anchor='center')

        self.setup_ui()

        self.root.mainloop()

    def setup_ui(self):
        original_logo = Image.open('data\mscicon.png')
        resized_logo = original_logo.resize((100, 100))
        self.logo = ImageTk.PhotoImage(resized_logo)
        
        logo_label = ttk.Label(self.mainframe, image=self.logo)
        logo_label.grid(row=0, column=0, columnspan=2)

        ttk.Label(self.mainframe, text='Numerate your tracks like pro!', font=("Brass Mono", 30)).grid(row=1, column=0, columnspan=2)

        ttk.Label(self.mainframe, text='Select source folder with songs', font=("Brass Mono", 12)).grid(row=2, column=0, columnspan=2)
        self.set_source_field = Listbox(self.mainframe)
        self.set_source_field.grid(row=3, column=0, pady=10, sticky='NWES')
        ttk.Button(self.mainframe, text='Browse', command=self.set_source_directory).grid(row=3, column=1, pady=10)

        ttk.Label(self.mainframe, text='Track starting number', font=("Brass Mono", 12)).grid(row=4, column=0, columnspan=2)
        self.number_field = ttk.Spinbox(self.mainframe, justify=CENTER, from_=1, to=1000)
        self.number_field.delete(0, END)
        self.number_field.insert(0, 1)
        self.number_field.grid(row=5, column=0, columnspan=2)

        ttk.Label(self.mainframe, text='Select path folder (Radio folder in MSC directory)', font=("Brass Mono", 12)).grid(row=6, column=0, columnspan=2)
        self.set_path_field = ttk.Entry(self.mainframe)
        self.set_path_field.delete(0, END)
        self.set_path_field.insert(0, self.open_path_dir())
        self.set_path_field.grid(row=7, column=0, pady=10, sticky='NWES')
        ttk.Button(self.mainframe, text='Browse', command=self.set_path_directory).grid(row=7, column=1, pady=10)

        ttk.Button(self.mainframe, text='Numerate', command=self.numerate_tracks).grid(row=8, column=0, columnspan=2, pady=10)

    def set_source_directory(self):
        folder_source_selected = filedialog.askopenfilenames(title="Select songs to numerate", filetypes=[("MP3 Files", "*.mp3")])
        self.songs = list(folder_source_selected)
        self.set_source_field.delete(0, END) 
        for i, file in enumerate(self.songs):
            self.set_source_field.insert(i, os.path.split(file)[1])

    def open_path_dir(self):
        if os.path.isfile(self.path_filename):
            with open(self.path_filename, "r") as open_path_dir:
                return open_path_dir.read().strip()
        else:
            return r"C:\Program Files (x86)\Steam\steamapps\common\My Summer Car\Radio"

    def save_path_dir(self):
        saved_path_dir = self.set_path_field.get()
        if os.path.exists(self.path_filename):
            os.chmod(self.path_filename, S_IWUSR)
            with open(self.path_filename, "w") as file_saved_dir:
                file_saved_dir.write(saved_path_dir)
            os.chmod(self.path_filename, S_IREAD | S_IRGRP | S_IROTH)
        else:
            with open(self.path_filename, "w") as file_saved_dir:
                file_saved_dir.write(saved_path_dir)
            os.chmod(self.path_filename, S_IREAD | S_IRGRP | S_IROTH)

    def set_path_directory(self):
        folder_path_selected = filedialog.askdirectory(initialdir=self.open_path_dir())
        if folder_path_selected:
            self.set_path_field.delete(0, END)
            self.set_path_field.insert(0, folder_path_selected)
            self.save_path_dir()

    def numerate_tracks(self):
        starting_index = int(self.number_field.get())
        songstocopy = self.songs
        pth_folder = self.set_path_field.get()
        count = starting_index

        if songstocopy and pth_folder and starting_index != "":
            files_already_present = any(os.path.isfile(os.path.join(pth_folder, f"track{count}.mp3")) for count in range(starting_index, starting_index + len(songstocopy)))

            if not files_already_present:
                for file in songstocopy:
                    dest_path = pth_folder
                    copied_file = os.path.split(file)[1]
                    shutil.copy(file, dest_path)
                    renamed = f"track{count}.mp3"
                    src = os.path.join(dest_path, copied_file)
                    dst = os.path.join(dest_path, renamed)
                    os.rename(src, dst)
                    count += 1
                self.root.bell()    
                messagebox.showinfo('Success', 'Songs have been renamed!')
            else:
                self.root.bell()
                messagebox.showwarning('Error', "Files are already present in path folder!")
        else:
            self.root.bell()
            messagebox.showwarning('Error', "You didn't specify path or starting number of track!")

if __name__ == '__main__':
    App()
