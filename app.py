from tkinter import ttk
from tkinter import *
import db
from models import Producto

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    root = Tk()  # ventana principal
    app = Producto(root)  # Se envia a la clase Producto el control sobre la ventana root
    root.mainloop()  # Mantiene la ventana abierta
