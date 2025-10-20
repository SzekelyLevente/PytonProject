import tkinter as tk
from tkinter import messagebox
import os
from model import PasswordModel
from Password_gen import generate_password

PASSWORD_FILE = "pwd.txt"


def create_password_window(root):
    win = tk.Toplevel(root)
    win.title("Jelszó beállítása")
    win.geometry("200x150")
    tk.Label(win, text="Állítsd be az alkalmazás jelszavát:").pack(pady=5)
    pw_entry = tk.Entry(win, show="*")
    pw_entry.pack(pady=5)

    def save_password():
        pw = pw_entry.get().strip()
        if not pw:
            messagebox.showerror("Hiba", "A jelszó nem lehet üres!")
            return
        with open(PASSWORD_FILE, "w", encoding="utf-8") as f:
            f.write(pw)
        messagebox.showinfo("OK", "Jelszó beállítva!")
        win.destroy()
        login_window(root)

    tk.Button(win, text="Mentés", command=save_password).pack(pady=5)
    win.protocol("WM_DELETE_WINDOW", root.destroy)


# --- bejelentkezés ablak ---
def login_window(root):
    win = tk.Toplevel(root)
    win.title("Bejelentkezés")
    win.geometry("150x150")

    tk.Label(win, text="Add meg a jelszót:").pack(pady=5)
    pw_entry = tk.Entry(win, show="*")
    pw_entry.pack(pady=5)

    def check_password():
        entered = pw_entry.get().strip()
        with open(PASSWORD_FILE, "r", encoding="utf-8") as f:
            real_pw = f.read().strip()
        if entered == real_pw:
            win.destroy()
            open_main_window(root)
        else:
            messagebox.showerror("Hiba", "Hibás jelszó!")

    tk.Button(win, text="Belépés", command=check_password).pack(pady=5)
    win.protocol("WM_DELETE_WINDOW", root.destroy)


def open_main_window(root):
    win = tk.Toplevel(root)
    win.title("Jelszókezelő")
    model = PasswordModel()

    tk.Label(win, text="Mentett bejegyzések:").pack(pady=5)
    listbox = tk.Listbox(win, width=40, height=10)
    listbox.pack(pady=5)

    def refresh():
        listbox.delete(0, tk.END)
        for name, _ in model.load():
            listbox.insert(tk.END, name)

    def add_entry():
        add_win = tk.Toplevel(win)
        add_win.title("Bejegyzés hozzáadása")
        add_win.geometry("150x200")
        tk.Label(add_win, text="Hozzáadás",font=("Arial", 18)).pack(pady=5)
        tk.Label(add_win, text="Név:").pack(pady=5)
        name_entry=tk.Entry(add_win)
        name_entry.pack(pady=5)
        tk.Label(add_win, text="Jelszó:").pack(pady=5)
        pw_entry=tk.Entry(add_win, show="*")
        pw_entry.pack(pady=5)

        def add():
            name = name_entry.get().strip()
            pw = pw_entry.get().strip()
            if name and pw:
                model.add(name, pw)
                name_entry.delete(0, tk.END)
                pw_entry.delete(0, tk.END)
                messagebox.showinfo("Létrehozás","Sikeres létrehozás!")
                refresh()
            else:
                messagebox.showerror("Hiba", "Egyik mező sem lehet üres!")

        add = tk.Button(add_win, text="Hozzáadás", command=add)
        add.pack(pady=5)
        add_win.mainloop()

    def update_entry():
        try:
            index = listbox.curselection()[0]
        except IndexError:
            messagebox.showwarning("Hiba", "Válassz ki egy bejegyzést!")
            return
        items=model.load()
        name, pw=items[index]
        update_win = tk.Toplevel(win)
        update_win.title("Bejegyzés módosítása")
        update_win.geometry("150x200")
        tk.Label(update_win, text="Módosítás", font=("Arial", 18)).pack(pady=5)
        tk.Label(update_win, text="Név:").pack(pady=5)
        name_entry = tk.Entry(update_win)
        name_entry.insert(0,name)
        name_entry.pack(pady=5)
        tk.Label(update_win, text="Jelszó:").pack(pady=5)
        pw_entry = tk.Entry(update_win, show="*")
        pw_entry.insert(0,pw)
        pw_entry.pack(pady=5)

        def update():
            new_name = name_entry.get().strip()
            new_pw = pw_entry.get().strip()
            if new_name and new_pw:
                model.update(index, new_name, new_pw)
                refresh()
                name_entry.delete(0, tk.END)
                pw_entry.delete(0, tk.END)
                messagebox.showinfo("Létrehozás", "Sikeres létrehozás!")
            else:
                messagebox.showerror("Hiba", "Egyik mező sem lehet üres!")

        update = tk.Button(update_win, text="Módosítás", command=update)
        update.pack(pady=5)
        update_win.mainloop()

    def delete_entry():
        try:
            index = listbox.curselection()[0]
        except IndexError:
            messagebox.showwarning("Hiba", "Válassz ki egy bejegyzést!")
            return
        if messagebox.askyesno("Törlés", "Biztosan törölni szeretnéd?"):
            model.delete(index)
            refresh()

    def show_password():
        try:
            index = listbox.curselection()[0]
        except IndexError:
            messagebox.showwarning("Hiba", "Válassz ki egy bejegyzést!")
            return
        data = model.load()
        name, pw = data[index]
        messagebox.showinfo("jelszó", f"{name} jelszava: {pw}")

    def generate_new():
        gen_win = tk.Toplevel(win)
        gen_win.title("Jelszó generátor")

        tk.Label(gen_win, text="Hossz:").grid(row=0, column=0)
        length_entry = tk.Entry(gen_win)
        length_entry.insert(0, "10")
        length_entry.grid(row=0, column=1)

        use_upper = tk.BooleanVar(value=True)
        use_digits = tk.BooleanVar(value=True)
        use_symbols = tk.BooleanVar(value=True)

        tk.Checkbutton(gen_win, text="Nagybetűk", variable=use_upper).grid(row=1, column=0)
        tk.Checkbutton(gen_win, text="Számok", variable=use_digits).grid(row=1, column=1)
        tk.Checkbutton(gen_win, text="Szimbólumok", variable=use_symbols).grid(row=2, column=0)

        result_label = tk.Label(gen_win, text="")
        result_label.grid(row=3, column=0, columnspan=2, pady=5)

        def generate():
            try:
                length = int(length_entry.get())
            except ValueError:
                messagebox.showerror("Hiba", "A hossz szám legyen!")
                return
            pw = generate_password(length, use_upper.get(), use_digits.get(), use_symbols.get())
            result_label.config(text=pw)

        def copy_pw():
            root.clipboard_clear()
            root.clipboard_append(result_label.cget("text"))
            root.update()
            tk.messagebox.showinfo("Másolva", "A szöveg a vágólapra került!")

        tk.Button(gen_win, text="Generálás", command=generate).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(gen_win, text="Generált kód másolása", command=copy_pw).grid(row=5, column=0, columnspan=2, pady=5)

    def password_change():
        pw_win = tk.Toplevel(win)
        pw_win.title("Jelszó beállítása")
        pw_win.geometry("200x150")
        tk.Label(pw_win, text="Állítsd be az alkalmazás jelszavát:").pack(pady=5)
        pw_entry = tk.Entry(pw_win, show="*")
        pw_entry.pack(pady=5)

        def save_password():
            pw = pw_entry.get().strip()
            if not pw:
                messagebox.showerror("Hiba", "A jelszó nem lehet üres!")
                return
            with open(PASSWORD_FILE, "w", encoding="utf-8") as f:
                f.write(pw)
            messagebox.showinfo("OK", "Jelszó beállítva!")
            win.destroy()
            login_window(root)

        tk.Button(pw_win, text="Mentés", command=save_password).pack(pady=5)

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Hozzáadás", command=add_entry).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Módosítás", command=update_entry).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Törlés", command=delete_entry).grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Megjelenítés", command=show_password).grid(row=0, column=3, padx=5)
    tk.Button(win, text="Jelszó generátor", command=generate_new).pack(pady=5)
    tk.Button(win, text="Jelszó módosítása", command=password_change).pack(pady=5)

    refresh()
    win.protocol("WM_DELETE_WINDOW", root.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    if not os.path.exists(PASSWORD_FILE):
        create_password_window(root)
    else:
        login_window(root)

    root.mainloop()