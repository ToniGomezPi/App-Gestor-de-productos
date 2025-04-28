import db  # importamos el contenido de db.py para que podamos acceder a el
from sqlalchemy import Column, Integer, String, Boolean, Date
from tkinter import ttk
from tkinter import *


class Producto(db.Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    precio = Column(Integer)
    categoria = Column(String(50))

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")  # Título de la ventana
        self.ventana.resizable(1, 1)  # Activa la redimensión de la ventana. Para desactivarla: (0,0)
        self.ventana.wm_iconbitmap("recursos/M6_P2_icon.ico")
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(0, weight=1)

        # Creacion del Sizegrip ( Agrandamiento de la pestaña )
        sg = ttk.Sizegrip(root)
        sg.grid(row=7, column=1, sticky=S + E)

        # Creación del contenedor frame principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=("Calibri", 16, "bold"))
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=("Calibri",13))  # Etiqueta de texto del frame
        self.etiqueta_nombre.grid(row=1, column=0)  # Posicionamiento a traves de grid

        # Entry Nombre ( caja de texto que recibira el nombre )
        self.nombre = Entry(frame, font=("Calibri",13))
        self.nombre.focus()  # El foco del raton estará en esta caja
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=("Calibri",13))  # Etiqueta Precio
        self.etiqueta_precio.grid(row=2, column=0)

        # Entry Precio
        self.precio = Entry(frame, font=("Calibri",13))
        self.precio.grid(row=2, column=1)

        # Label Categoria
        self.etiqueta_categoria = Label(frame, text="Categoria: ", font=("Calibri",13))  # Etiqueta Categoria
        self.etiqueta_categoria.grid(row=3, column=0)

        # Entry Categoria
        self.categoria = Entry(frame, font=("Calibri",13))
        self.categoria.grid(row=3, column=1)

        # Boton añadir producto
        s=ttk.Style()
        s.configure("my.TButton", font=("Calibri", 14, "bold"))
        self.boton_anyadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style="my.TButton")
        self.boton_anyadir.grid(row=4, columnspan=2, sticky=W + E)

        # Mensaje informativo para el usuario
        self.mensaje = Label(text="", fg="red")
        self.mensaje.grid(row=4, column=0, columnspan=2, sticky=W + E)

        # Tabla de productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=("Calibri", 11))
        # Se modifica la fuente de las cabeceras
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 13, "bold"))
        # Eliminamos los bordes
        style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})])

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=('#1', '#2'),
                                  style="mystyle.Treeview")  # Quitamos el #0 que ya esta incorporado por default
        self.tabla.grid(row=5, column=0, columnspan=2)
        self.tabla.heading("#0", text="Nombre", anchor=CENTER)  # Encabezado 0
        self.tabla.heading("#1", text="Precio", anchor=CENTER)  # Encabezado 1
        self.tabla.heading("#2", text="Categoria", anchor=CENTER)  # Encabezado 2

        # Botones de eliminar y editar
        boton_eliminar = ttk.Button(text="ELIMINAR", command=self.del_producto, style="my.TButton")
        boton_eliminar.grid(row=6, column=0, sticky=W + E)
        boton_editar = ttk.Button(text="EDITAR", command=self.edit_producto, style="my.TButton")
        boton_editar.grid(row=6, column=1, sticky=W + E)

        # Llamada al metodo get_productos() para obtener el listado de productos al inicio de la app
        self.get_productos()

    def db_consulta(self, consulta, parametros=()):
        with db.engine.connect() as con:  # Iniciamos la conexion con la base de datos con un alias
            resultado = con.execute(consulta, parametros)  # preparar la consulta y la guarda ( sqlalchemy autocommit )
        return resultado

    def get_productos(self):
        # Lo primero, al iniciar la app, vamos a limpiar la tabla por si hubiera datos residuales o antiguos
        registros_tabla = self.tabla.get_children()  # Obtiene todos los datos de la tabla

        for fila in registros_tabla:
            self.tabla.delete(fila)

        # Escribir los datos en pantalla
        # Obtiene todos los datos de la tabla
        productos = db.session.query(Producto).all()
        for producto in productos:
            self.tabla.insert("", 0, text=producto.nombre, values=(producto.precio, producto.categoria))

    def validacion_nombre(self):
        nombre_userInput = self.nombre.get()
        return len(nombre_userInput) != 0

    def validacion_precio(self):
        precio_userInput = self.precio.get()
        return len(precio_userInput) != 0

    def validacion_categoria(self):
        categoria_userInput = self.categoria.get()
        return len(categoria_userInput) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria():
            query = "INSERT INTO producto VALUES(NULL, ?, ?, ?)"  # Consulta SQL ( sin los datos )
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get())
            self.db_consulta(query, parametros)
            print("Datos guardados")
            self.mensaje["text"] = "Producto {} añadido con exito".format(self.nombre.get())
            self.nombre.delete(0, END)  # borra el campo nombre del formulario al guardar
            self.precio.delete(0, END)  # borra el campo precio del formulario al guardar
            self.categoria.delete(0, END)  # borra el campo categoria del formulario al guardar

        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_categoria():
            self.mensaje["text"] = "El precio es obligatorio"
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_categoria():
            self.mensaje["text"] = "El nombre es obligatorio"
        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() == False:
            self.mensaje["text"] = "La categoria es obligatorio"
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_categoria() == False:
            self.mensaje["text"] = "El nombre y la categoria es obligatorio"
        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_categoria() == False:
            self.mensaje["text"] = "El precio y la categoria es obligatorio"
        elif self.validacion_nombre() == False and self.validacion_precio() == False and self.validacion_categoria():
            self.mensaje["text"] = "El nombre y el precio es obligatorio"
        else:
            self.mensaje["text"] = "El nombre, el precio y la categoria son obligatorios"
        self.get_productos()  # Cuando se finalice la insercion de datos volvemos a invocar a este metodo para actualizar
        # el contenido y ver los cambios

    def del_producto(self):

        self.mensaje["text"] = ""  # Mensaje inicialmente vacio
        # Comprobacion de que se seleccione un producto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())["text"][0]
        except IndexError as ie:
            self.mensaje["text"] = "Por favor, seleccione un producto"
            return
        self.mensaje["text"] = ""
        nombre = self.tabla.item(self.tabla.selection())["text"]
        query = "DELETE FROM producto WHERE nombre = ?"  # Consulta SQL
        self.db_consulta(query, (nombre,))  # Ejecutar consulta , el (nombre,) sirve para establecerlo como una tupla
        # Without the comma, (nombre) is just a grouped expression, not a tuple
        self.mensaje["text"] = "Producto {} eliminado con exito".format(nombre)
        self.get_productos()  # actualizamos la tabla de productos

    def edit_producto(self):
        self.mensaje["text"] = ""  # Mensaje inicialmente vacio
        try:
            self.tabla.item(self.tabla.selection())["text"][0]
        except IndexError as ie:
            self.mensaje["text"] = "Por favor, seleccione un producto"
            return
        nombre = self.tabla.item(self.tabla.selection())["text"]
        old_precio = self.tabla.item(self.tabla.selection())["values"][0]
        old_categoria = self.tabla.item(self.tabla.selection())["values"][1]
        # El precio y la categoria se encuentran dentro de una lista

        self.ventana_editar = Toplevel()  # Crear una ventana por delante de la principal
        self.ventana_editar.title("Editar Producto")  # Titulo de la ventana
        self.ventana_editar.resizable(1, 1)  # Activamos la redimension de la ventana
        self.ventana_editar.wm_iconbitmap("recursos/M6_P2_icon.ico")

        titulo = Label(self.ventana_editar, text="Edición de Productos", font=("Calibri", 50, "bold"))
        titulo.grid(column=0, row=0)

        # Creacion del contenedor Frame de la ventana de Editar producto
        frame_ep = LabelFrame(self.ventana_editar,
                              text="Editar el siguiente Producto", font=("Calibri", 16, "bold"))  # frame_ep: Frame editar producto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre antiguo: ", font=("Calibri",13))
        # Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre_antiguo.grid(row=2, column=0)  # posicionamientoa traves de grid
        # Entry nombre antiguo ( texto que no se podra modificar )
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre),
                                          state="readonly", font=("Calibri",13))
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=("Calibri",13))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        # Entry nombre nuevo ( texto que si se podra modificar )
        self.input_nombre_nuevo = Entry(frame_ep, font=("Calibri",13))
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # para que el foco del raton vaya a este entry al inicio

        # Label precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text="Precio antiguo: ", font=("Calibri",13))
        # Etiqueta de precio ubicada en el frame
        self.etiqueta_precio_antiguo.grid(row=4, column=0)  # posicionamiento a traves de grid
        # Entry precio antiguo ( texto que no se podra modificar )
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state="readonly", font=("Calibri",13))
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=("Calibri",13))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        # Entry precio nuevo ( texto que si se podra modificar )
        self.input_precio_nuevo = Entry(frame_ep, font=("Calibri",13))
        self.input_precio_nuevo.grid(row=5, column=1)
        # Label Categoria antiguo
        self.etiqueta_categoria_antiguo = Label(frame_ep, text="Categoria antiguo: ", font=("Calibri",13))
        # Etiqueta de Categoria ubicada en el frame
        self.etiqueta_categoria_antiguo.grid(row=6, column=0)  # posicionamiento a traves de grid
        # Entry Categoria antiguo ( texto que no se podra modificar )
        self.input_categoria_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria),
                                             state="readonly", font=("Calibri",13))
        self.input_categoria_antiguo.grid(row=6, column=1)

        # Label Categoria nuevo
        self.etiqueta_categoria_nuevo = Label(frame_ep, text="Categoria nuevo: ", font=("Calibri",13))
        self.etiqueta_categoria_nuevo.grid(row=7, column=0)
        # Entry Categoria nuevo ( texto que si se podra modificar )
        self.input_categoria_nuevo = Entry(frame_ep, font=("Calibri",13))
        self.input_categoria_nuevo.grid(row=7, column=1)

        # Boton actualizar producto
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", style="my.TButton", command=lambda:
        self.actualizar_productos(self.input_nombre_nuevo.get(),
                                  self.input_nombre_antiguo.get(),
                                  self.input_precio_nuevo.get(),
                                  self.input_precio_antiguo.get(),
                                  self.input_categoria_nuevo.get(),
                                  self.input_categoria_antiguo.get()))
        self.boton_actualizar.grid(row=8, columnspan=2, sticky=W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, nueva_categoria,
                             antigua_categoria):
        producto_modificado = False
        query = "UPDATE producto SET nombre = ?, precio = ?, categoria = ? WHERE nombre = ? AND precio = ? AND categoria = ?"
        if nuevo_nombre != "" and nuevo_precio != "" and nueva_categoria != "":
            # Si el usuario escribe nuevo nombre, nuevo precio y nueva categoria se cambian todos
            parametros = (
                nuevo_nombre, nuevo_precio, nueva_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre != "" and nuevo_precio == "" and nueva_categoria != "":
            # Si el usuario deja vacio el nuevo precio, se mantiene el precio anterior
            parametros = (
                nuevo_nombre, antiguo_precio, nueva_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == "" and nuevo_precio != "" and nueva_categoria != "":
            # Si el usuario deja vacio el nombre nuevo, se mantiene el nombre anterior
            parametros = (
                antiguo_nombre, nuevo_precio, nueva_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == "" and nuevo_precio == "" and nueva_categoria != "":
            # Si el usuario modifica solo la categoria, se mantendrá el nombre y el precio antiguos
            parametros = (
                antiguo_nombre, antiguo_precio, nueva_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre != "" and nuevo_precio != "" and nueva_categoria == "":
            # Si el usuario deja vacio la categoria nueva, se mantiene la categoria anterior
            parametros = (
                nuevo_nombre, nuevo_precio, antigua_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre != "" and nuevo_precio == "" and nueva_categoria == "":
            # Si el usuario modifica solo el nombre, se mantendrá el precio y la categoria antiguas
            parametros = (
                nuevo_nombre, antiguo_precio, antigua_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == "" and nuevo_precio != "" and nueva_categoria == "":
            # Si el usuario modifica solo el precio, se mantendrá el nombre y la categoria antiguas
            parametros = (
                antiguo_nombre, nuevo_precio, antigua_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True

        if (producto_modificado):
            self.db_consulta(query, parametros)
            self.ventana_editar.destroy()  # cerrar la ventana de edicion de productos
            self.mensaje["text"] = "El producto {} ha sido actualizado con éxito".format(antiguo_nombre)
            self.get_productos()  # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy()
            self.mensaje["text"] = "El producto {} NO ha sido actualizado".format(antiguo_nombre)
