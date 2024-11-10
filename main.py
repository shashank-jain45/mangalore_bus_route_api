from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from sqlite3 import Connection, Cursor, connect
from typing import List, Optional

app = FastAPI()

class BusRoute(BaseModel):
    bus_number: str
    from_location: str
    to_location: str
    route: str

class PaginatedResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: List[BusRoute]

def get_db() -> Connection:
    db = connect(database="bus_routes.db",check_same_thread=False,)
    return db



# all bus routes
@app.get("/bus_routes/", response_model=List[BusRoute])
async def get_all_bus_routes(
    limit: int = Query(10, ge=1, le=100),  
    offset: int = Query(0, ge=0),
    db: Connection = Depends(get_db)
):
    cursor: Cursor = db.cursor()

    cursor.execute(
        "SELECT bus_number, from_location, to_location, route FROM bus_routes LIMIT ? OFFSET ?",
        (limit, offset)
    )
    
    routes = cursor.fetchall()

    return [
        BusRoute(bus_number=row[0], from_location=row[1], to_location=row[2], route=row[3])
        for row in routes
    ]



# bus routes based on from_location, to_location query parameters
@app.get("/bus_routes/search/", response_model=List[BusRoute])
async def search_bus_routes(
    from_location: Optional[str] = Query(None),
    to_location: Optional[str] = Query(None),
    db: Connection = Depends(get_db)
):
    cursor: Cursor = db.cursor()

    query = "SELECT bus_number, from_location, to_location, route FROM bus_routes WHERE 1=1"
    params = []

    if from_location:
        query += " AND route LIKE ?"
        params.append(f"%{from_location}%")

    if to_location:
        query += " AND route LIKE ?"
        params.append(f"%{to_location}%")

    cursor.execute(query, params)
    routes = cursor.fetchall()

    return [BusRoute(bus_number=row[0], from_location=row[1], to_location=row[2], route=row[3]) for row in routes]



# route for a specific bus number
@app.get("/bus_routes/{bus_number}", response_model=BusRoute)
async def get_route_for_bus(bus_number: str, db: Connection = Depends(get_db)):
    cursor: Cursor = db.cursor()
    cursor.execute("SELECT bus_number, from_location, to_location, route FROM bus_routes WHERE bus_number = ?", (bus_number,))
    route = cursor.fetchone()

    if route is None:
        raise HTTPException(status_code=404, detail="Bus route not found")

    return BusRoute(bus_number=route[0], from_location=route[1], to_location=route[2], route=route[3])
