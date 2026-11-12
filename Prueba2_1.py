from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Inicializamos la aplicación FastAPI
app = FastAPI(title="Evaluación - Parte 1")

# Modelo de datos para la Actividad
class Actividad(BaseModel):
    id_actividad: int
    nombre_actividad: str
    cantidad_personas: int
    dia_realizar: str
    duracion_dias: int
    realizado: bool

# Base de datos simulada en memoria (lista de diccionarios/objetos)
db_actividades = []

# a) Método para guardar datos de una nueva actividad
@app.post("/NuevaActividad", response_model=Actividad, tags=["Actividades"])
def nueva_actividad(actividad: Actividad):
    """Guarda una nueva actividad en la base de datos simulada."""
    # Validación simple para no repetir ID
    for act in db_actividades:
        if act.id_actividad == actividad.id_actividad:
            raise HTTPException(status_code=400, detail="El ID de la actividad ya existe.")
    
    db_actividades.append(actividad)
    return actividad

# b) Método para modificar la cantidad de personas por Id
@app.put("/ModificarActividad/{id_actividad}", tags=["Actividades"])
def modificar_actividad(id_actividad: int, nueva_cantidad: int):
    """Modifica la cantidad de personas de una actividad existente buscando por su ID."""
    for act in db_actividades:
        if act.id_actividad == id_actividad:
            act.cantidad_personas = nueva_cantidad
            return {"mensaje": "Cantidad de personas actualizada exitosamente", "actividad": act}
    
    raise HTTPException(status_code=404, detail="Actividad no encontrada.")

# c) Método para eliminar una actividad por Id
@app.delete("/EliminarActividad/{id_actividad}", tags=["Actividades"])
def eliminar_actividad(id_actividad: int):
    """Elimina una actividad de la lista usando su ID."""
    for i, act in enumerate(db_actividades):
        if act.id_actividad == id_actividad:
            actividad_eliminada = db_actividades.pop(i)
            return {"mensaje": "Actividad eliminada", "actividad": actividad_eliminada}
            
    raise HTTPException(status_code=404, detail="Actividad no encontrada.")

# d) Método para mostrar actividades con más de 10 personas
@app.get("/MostrarMayor10", response_model=List[Actividad], tags=["Actividades"])
def mostrar_mayor_10():
    """Filtra y devuelve las actividades cuya cantidad de personas sea estrictamente mayor a 10."""
    actividades_filtradas = [act for act in db_actividades if act.cantidad_personas > 10]
    return actividades_filtradas

# e) Método para mostrar todas las actividades
@app.get("/MostrarTodo", response_model=List[Actividad], tags=["Actividades"])
def mostrar_todo():
    """Devuelve todas las actividades almacenadas."""
    return db_actividades