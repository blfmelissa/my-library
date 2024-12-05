from fastapi import FastAPI
import pyodbc
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur le site de gestion de livres!"}

# Connexion à la base de données
@app.on_event("startup")
async def startup_db():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=tcp:mlizsqlserver.database.windows.net,1433;'
        'DATABASE=books-db;'
        'UID=melissa;'
        'PWD=781227moi!'
    )
    print("Database connection etablished!")

@app.on_event("shutdown")
def shutdown_db():
    connection.close()

