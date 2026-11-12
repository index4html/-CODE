from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os

app = FastAPI(title="Evaluación - Parte 2")

# Modelo de datos de Persona
class Persona(BaseModel):
    rut: str
    nombre: str
    edad: int
    genero: str
    profesion: str

# Diccionario para almacenar las personas usando el RUT como llave para acceso rápido
db_personas = {}

# a) Método para leer el archivo Personas.txt y guardarlo
@app.post("/SubirArchivo", tags=["Personas"])
def subir_archivo():
    """Lee el archivo local Personas.txt y carga los datos en la memoria."""
    if not os.path.exists("Personas.txt"):
        raise HTTPException(status_code=404, detail="El archivo Personas.txt no existe en el directorio.")
    
    try:
        with open("Personas.txt", "r", encoding="utf-8") as file:
            lineas = file.readlines()
            for linea in lineas:
                # Limpiamos saltos de línea y separamos por coma
                datos = linea.strip().split(',')
                if len(datos) == 5:
                    rut, nombre, edad, genero, profesion = datos
                    db_personas[rut] = Persona(
                        rut=rut.strip(),
                        nombre=nombre.strip(),
                        edad=int(edad.strip()),
                        genero=genero.strip(),
                        profesion=profesion.strip()
                    )
        return {"mensaje": "Archivo leído y datos cargados exitosamente.", "total_cargados": len(db_personas)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")

# b) Método para mostrar a todas las personas ordenadas por edad
@app.get("/MostrarPorEdad", response_model=List[Persona], tags=["Personas"])
def mostrar_por_edad():
    """Devuelve la lista de personas ordenadas de menor a mayor edad."""
    if not db_personas:
        raise HTTPException(status_code=404, detail="No hay datos cargados aún.")
    
    # Convertimos los valores del diccionario a lista y los ordenamos por el atributo 'edad'
    personas_ordenadas = sorted(db_personas.values(), key=lambda p: p.edad)
    return personas_ordenadas

# c) Método para cambiar TODOS los datos de una persona por Rut
@app.put("/CambiarRut/{rut}", tags=["Personas"])
def cambiar_rut(rut: str, datos_nuevos: Persona):
    """Reemplaza todos los datos de una persona existente identificada por su RUT."""
    if rut not in db_personas:
        raise HTTPException(status_code=404, detail="Persona no encontrada con el RUT proporcionado.")
    
    # Reemplazamos los datos completos
    db_personas[rut] = datos_nuevos
    # Si el rut en el JSON cambió, actualizamos la llave del diccionario
    if rut != datos_nuevos.rut:
        db_personas[datos_nuevos.rut] = db_personas.pop(rut)

    return {"mensaje": "Datos actualizados exitosamente", "persona": datos_nuevos}

# d) Método para eliminar persona por rut
@app.delete("/EliminarRut/{rut}", tags=["Personas"])
def eliminar_rut(rut: str):
    """Elimina los datos de una persona identificada por su RUT."""
    if rut not in db_personas:
        raise HTTPException(status_code=404, detail="Persona no encontrada.")
    
    persona_eliminada = db_personas.pop(rut)
    return {"mensaje": "Persona eliminada exitosamente", "persona": persona_eliminada}