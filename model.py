import os

class PasswordModel:
    def __init__(self, filename="data.txt"):
        self.filename = filename
        self.items=[]
        if not os.path.exists(self.filename):
            open(self.filename, "w").close()

    def load(self):
        items = []
        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if ":" in line:
                    name, pw = line.split(":", 1)
                    items.append((name, pw))
        return items

    def save(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            for name, pw in data:
                f.write(f"{name}:{pw}\n")

    def add(self, name, password):
        data = self.load()
        data.append((name, password))
        self.save(data)

    def delete(self, index):
        data = self.load()
        if 0 <= index < len(data):
            del data[index]
        self.save(data)

    def update(self, index, new_name, new_pw):
        data = self.load()
        if 0 <= index < len(data):
            data[index] = (new_name, new_pw)
        self.save(data)
