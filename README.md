<p align="center">
    <h1 align="center">SIT VolunteerVerse</h1>
</p>

<p align="center">
    <i>Enter the VolunteerVerse</i><br />
    <img src="https://img.shields.io/badge/Coded%20By%20Humans-100%25-brightgreen" />
</p>

## Folder structure

You can see the most important files and it's locations in the diagram below. Some files were hidden to make it easier to understand.

```
📦ict3x03-project
 ┣ 📂backend
 ┃ ┣ 📂api
 ┃ ┣ 📂backend
 ┃ ┣ 📜db.sqlite3
 ┃ ┣ 📜manage.py
 ┃ ┣ 📜Dockerfile
 ┣ 📂frontend
 ┃ ┣ 📂.next
 ┃ ┣ 📂node_modules
 ┃ ┣ 📂app
 ┃ ┣ 📂public
 ┃ ┣ 📜Dockerfile
 ┃ ┗📜package.json
 ┣ 📂venv
 ┣ 📜requirements.txt
 ┗ 📜docker-compose.yml
 ```
## Installation

### DJANGO API Backend
1. Make and run a python environment using 
```python -m venv venv```
2. Activate the virtual environment
3. Run `pip install -r requirements.txt`
4. Enter the backend directory `cd backend`
5. Run the server with `python manage.py runserver`
6. Visit http://localhost:8000

### NEXTJS Frontend

1. Enter the frontend directory `cd frontend`
2. Install node packages using `npm install`
3. Run the development  with `npm run dev`
4. Visit http://localhost:3000
> NEXTJS will take around 20s

### Installing on Docker
Run `docker-compose up`

## <b>Contributors</b>

🧑 **BENNY LIM YI JIE - 2101955**  
🧑 **CHEN JIAJUN - 2101351**  
🧑 **Greger Chen - 2100641**  
🧑 **LAI WEN JUN - 2102989**  
🧑 **Lim Zhen Guang - 2100755**  
👩 **Lynette Lim - 2102477**  
🧑 **Nur Afif Azfar - 2100822**  
