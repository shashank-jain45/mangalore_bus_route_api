from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from sqlite3 import Connection, Cursor, connect, OperationalError
from typing import List, Optional
import math

app = FastAPI()

class BusRoute(BaseModel):
    bus_number: str
    from_location: str
    to_location: str
    route: str

class PaginatedBusRoutes(BaseModel):
    total: int
    page: int
    size: int
    total_pages: int
    routes: List[BusRoute]

def get_db() -> Connection:
    try:
        db = connect(database="bus_routes.db", check_same_thread=False)
        return db
    except OperationalError as e:
        raise HTTPException(status_code=500, detail="Database connection failed") from e


# Get all bus routes with pagination
@app.get("/bus_routes/", response_model=PaginatedBusRoutes)
async def get_all_bus_routes(
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    size: int = Query(10, ge=1, le=100, description="Number of routes per page"),
    db: Connection = Depends(get_db)
):
    limit = size
    offset = (page - 1) * size

    cursor = db.cursor()
    try:
        # Get total count of bus routes
        cursor.execute("SELECT COUNT(*) FROM bus_routes")
        total = cursor.fetchone()[0]

        if offset >= total:
            raise HTTPException(status_code=404, detail="Page not found")

        cursor.execute(
            """
            SELECT bus_number, from_location, to_location, route 
            FROM bus_routes 
            LIMIT ? OFFSET ?
            """,
            (limit, offset)
        )
        routes = cursor.fetchall()

        total_pages = math.ceil(total / size) if size else 1

        bus_routes = [
            BusRoute(
                bus_number=row[0],
                from_location=row[1],
                to_location=row[2],
                route=row[3]
            )
            for row in routes
        ]

        return PaginatedBusRoutes(
            total=total,
            page=page,
            size=size,
            total_pages=total_pages,
            routes=bus_routes
        )
    except OperationalError as e:
        raise HTTPException(status_code=500, detail="Error accessing bus routes") from e
    finally:
        cursor.close()
        db.close()


# Search bus routes based on `from_location` and `to_location`
@app.get("/bus_routes/search/", response_model=List[BusRoute])
async def search_bus_routes(
    from_location: Optional[str] = Query(None),
    to_location: Optional[str] = Query(None),
    db: Connection = Depends(get_db)
):
    cursor = db.cursor()
    try:
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

        if not routes:
            raise HTTPException(status_code=404, detail="No matching routes found")

        return [
            BusRoute(
                bus_number=row[0],
                from_location=row[1],
                to_location=row[2],
                route=row[3]
            )
            for row in routes
        ]
    except OperationalError as e:
        raise HTTPException(status_code=500, detail="Error performing search") from e
    finally:
        cursor.close()
        db.close()


# Get route details for a specific bus number
@app.get("/bus_routes/{bus_number}", response_model=BusRoute)
async def get_route_for_bus(bus_number: str, db: Connection = Depends(get_db)):
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT bus_number, from_location, to_location, route FROM bus_routes WHERE bus_number = ?",
            (bus_number,)
        )
        route = cursor.fetchone()

        if route is None:
            raise HTTPException(status_code=404, detail="Bus route not found")

        return BusRoute(
            bus_number=route[0],
            from_location=route[1],
            to_location=route[2],
            route=route[3]
        )
    except OperationalError as e:
        raise HTTPException(status_code=500, detail="Error accessing bus route") from e
    finally:
        cursor.close()
        db.close()
