import os

class PasswordModelSL:
    def __init__(self, filename="data.txt"):
        self.filename = filename
        self.items=[]
        if not os.path.exists(self.filename):
            open(self.filename, "w").close()

    def loadSL(self):
        items = []
        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if ":" in line:
                    name, pw = line.split(":", 1)
                    items.append((name, pw))
        return items

    def saveSL(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            for name, pw in data:
                f.write(f"{name}:{pw}\n")

    def addSL(self, name, password):
        data = self.loadSL()
        data.append((name, password))
        self.saveSL(data)

    def deleteSL(self, index):
        data = self.loadSL()
        if 0 <= index < len(data):
            del data[index]
        self.saveSL(data)

    def updateSL(self, index, new_name, new_pw):
        data = self.loadSL()
        if 0 <= index < len(data):
            data[index] = (new_name, new_pw)
        self.saveSL(data)
