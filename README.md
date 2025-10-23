![1760896914072](image/README/1760896914072.png)

### **ACERCA DE ESTA PRACTICA**

*Ammu-Nation es una cadena de tiendas de armas ficticia en la serie de videojuegos Grand Theft Auto que opera en varias ciudades del juego y es la principal tienda de armas. Ofrece una amplia variedad de armamento y, en algunos juegos, también incluye galerías de tiro para desafíos específicos de puntería.*

En este proyecto desarrollaremos una **aplicación de gestión** inspirada en dicha franquicia, que permitirá administrar de forma sencilla todo el inventario de la tienda.

El objetivo principal es crear un sistema **CRUD** (Create, Read, Update, Delete) que permita gestionar la información de los productos disponibles en la tienda.

- **Agregar** nuevos productos (armas, munición o accesorios, cada uno de ellos ligados a un código de identificacion único o código de serie).
- **Editar** la información existente. (Nombre del arma, uso del calibre, etc)
- **Eliminar** registros.
- **Consultar** el inventario y detalles de cada artículo.

### USO DEL PROGRAMA

...

#### **INSTRUCCIONES Y CONSEJOS CON GIT**

* Para descargar el proyecto ingresamos en la terminal: git clone https://github.com/GranPatriarca02/Ammu-Nation.git
* Se debe utilizar un entorno aislado: source nombreEntorno/bin/activate
* Para ejecutar el programa se debe verificar que los datos de la clase db.py estan enlazados correctamente, además se debe instalar **envyte** en el entorno (**pip install envyte**).
* En caso de que libsql falle: (**pip install libsql**)
* **IMPORTANTE:** Siempre que se decida trabajar en el proyecto se deben traer los últimos cambios del repositorio, para ello se debe usar **git status** y posteriormente **git pull origin main** para traer los cambios recientes al equipo, pero recuerda que si tu código en local no ha sido guardado perderás todo el progreso que hayas hecho.
* Todos los cambios deben actualizarse en el momento de haberlos terminado (**git add**) (**git commit**) (**git push**) antes de realizar cualquier cambio en el proyecto principal es recomendable practicar en un proyecto desde 0 evitando así entorpecer el trabajo de los demás.
* La descripción de los cambios realizados deben de ser claros y deben tener una descripción sobre el modulo en el que se ha trabajado, además deben estar escritos en inglés: ejemplo: git commit -m "Update .env" -m "Updated main.py to be able to run the program"

#### **CHANGELOG**

19-10-2025: Comienzo del proyecto, se ha creado la estructura, el esqueleto del programa, la conexión con la base de datos con TURSO: https://turso.tech/ y las principales tablas de la base de datos.

19-10-2025: Creado un main temporal donde se puede ejecutar la base de datos con sus tablas y datos ya almacenados, además se han establecido ciertas instrucciones en README.md que puede consultar el resto del equipo.

#### **INTEGRANTES DEL PROYECTO**

* Javier Alcocer Carrero (...)
* Carlos Andrés Rojas Monasterio ([GranPatriarca02](https://github.com/GranPatriarca02))
* Antonio Nikolaev Mitev ([Chevelle1337](https://github.com/Chevelle1337)) ([TonyMN8](https://github.com/TonyMN8))

---
