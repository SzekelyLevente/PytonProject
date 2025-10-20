# Jelszókezelő alkalmazás

**Hallgató neve:** Székely Levente  
**Nyelv:** Python  
**Grafikus modul:** Tkinter  
**Fájlkezelés:** Egyszerű szöveges fájlok (`txt`)

---

## 🎯 Feladat rövid leírása

A program egy jelszókezelő alkalmazás, amelyben a felhasználó:
- be tud jelentkezni egy fő jelszóval (ami a `pwd.txt` fájlban van tárolva),
- ha ez a fájl nem létezik, új jelszót tud beállítani,
- a bejelentkezés után kezelni tudja a mentett bejegyzéseket (név–jelszó párok),
- CRUD műveleteket (hozzáadás, módosítás, törlés, megjelenítés) végezhet,
- új, véletlenszerű jelszót is tud generálni a jelszógenerátor segítségével,
- és megváltoztathatja az alkalmazás jelszavát.

A jelszavak és felhasználónevek egy `data.txt` fájlban vannak eltárolva egyszerű formátumban:

---

## 🧩 Modulok és főbb funkciók

### `main.py`
- A program **belépési pontja**.
- Tartalmazza az ablakok létrehozását és az eseménykezeléseket.

**Főbb függvények:**
- `create_password_window(root)` – jelszó beállító ablak létrehozása, ha még nincs `pwd.txt`.
- `login_window(root)` – bejelentkezési ablak, amely a jelszót ellenőrzi.
- `open_main_window(root)` – fő jelszókezelő ablak, amelyben a CRUD műveletek és a jelszógenerátor található.
- `generate_new()` – jelszógenerátor ablak létrehozása.
- `password_change()` – alkalmazás jelszavának módosítása.

---

### `model.py`
- Tartalmazza a `PasswordModel` **osztályt**, ami a fájlműveleteket kezeli (`data.txt`).

**Osztály:** `PasswordModel`

**Főbb metódusai:**
- `load()` – beolvassa a jelszó-bejegyzéseket a fájlból.
- `save(data)` – elmenti az adatokat a fájlba.
- `add(name, password)` – új bejegyzés hozzáadása.
- `delete(index)` – bejegyzés törlése.
- `update(index, new_name, new_pw)` – bejegyzés módosítása.

---

### `Password_gen.py`
- Modul, amely jelszavakat generál különböző beállításokkal.

**Függvény:**
- `generate_password(length=10, use_upper=True, use_digits=True, use_symbols=True)`  
  → Véletlenszerű jelszót generál a megadott hossz és karaktertípusok alapján.

---

## 🪟 Használat
1. Futtasd a `main.py` fájlt:
   ```bash
   py main.py
