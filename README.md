Trato Hecho Web Application
Este es un proyecto web basado en el juego "Deal or No Deal" utilizando Flask, SQLAlchemy y Python.

Requisitos
Python 3.7
Virtualenv (opcional, pero recomendado)

Crea un entorno virtual:
python -m venv venv

Activa el entorno virtual:
En macOS/Linux:
source venv/bin/activate

En Windows:
venv\Scripts\activate

Instala las dependencias:
pip install -r requirements.txt

Configura las variables de entorno creando un archivo .env en el directorio raíz del proyecto con el siguiente contenido:
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3

Inicia la base de datos:
flask db init
flask db migrate -m "Initial migration."
flask db upgrade

Ejecuta la aplicación:
Accede a la aplicación en tu navegador web en http://localhost:5000.
Regístrate e inicia sesión para comenzar a jugar.


Licencia
Programación - Desarrollo de Sofware - 2º año - ISFDyT Nº 27
