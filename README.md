Here's documentation for your FastAPI-based Bus Route API, using `https://app-bootcamp.iris.nitk.ac.in` as the base URL.

---

# Bus Route API Documentation

This API allows users to retrieve information on bus routes, including pagination, search functionality, and details for specific routes.

**Base URL**: `https://app-bootcamp.iris.nitk.ac.in`

### Endpoints

1. **Get All Bus Routes (Paginated)**
2. **Search Bus Routes by Location**
3. **Get Route Details by Bus Number**

---

## 1. Get All Bus Routes (Paginated)

Retrieve a list of bus routes with pagination.

- **URL**: `/bus_routes/`
- **Method**: `GET`
- **Response Model**: `PaginatedBusRoutes`

### Parameters

| Parameter | Type | Required | Default | Description |
| --------- | ---- | -------- | ------- | ----------- |
| `page`    | `int`| No       | 1       | Page number, starting from 1 |
| `size`    | `int`| No       | 10      | Number of routes per page (between 1 and 100) |

### Response

```json
{
    "total": 100,
    "page": 1,
    "size": 10,
    "total_pages": 10,
    "routes": [
        {
            "bus_number": "B1",
            "from_location": "Location A",
            "to_location": "Location B",
            "route": "A -> C -> B"
        },
        ...
    ]
}
```

- **total**: Total number of bus routes available.
- **page**: Current page number.
- **size**: Number of bus routes per page.
- **total_pages**: Total pages based on the requested size.
- **routes**: Array of bus route objects for the current page.

### Errors

- **404 Not Found**: If the requested page does not exist.
- **500 Internal Server Error**: If there's a database connection error.

---

## 2. Search Bus Routes by Location

Search for bus routes that match specified `from_location` or `to_location`.

- **URL**: `/bus_routes/search/`
- **Method**: `GET`
- **Response Model**: `List[BusRoute]`

### Query Parameters

| Parameter       | Type    | Required | Description                                   |
| --------------- | ------- | -------- | --------------------------------------------- |
| `from_location` | `str`   | No       | Filter routes containing this location in the route |
| `to_location`   | `str`   | No       | Filter routes containing this location in the route |

**Note**: At least one of `from_location` or `to_location` should be provided.

### Response

```json
[
    {
        "bus_number": "B1",
        "from_location": "Location A",
        "to_location": "Location B",
        "route": "A -> C -> B"
    },
    ...
]
```

Each item includes:
- **bus_number**: Unique identifier for the bus.
- **from_location**: Starting location of the route.
- **to_location**: Ending location of the route.
- **route**: Full route description.

### Errors

- **404 Not Found**: If no matching routes are found.
- **500 Internal Server Error**: If there's a database connection error.

---

## 3. Get Route Details by Bus Number

Retrieve detailed information for a specific bus route.

- **URL**: `/bus_routes/{bus_number}`
- **Method**: `GET`
- **Response Model**: `BusRoute`

### Path Parameter

| Parameter     | Type    | Required | Description             |
| ------------- | ------- | -------- | ----------------------- |
| `bus_number`  | `str`   | Yes      | Unique identifier for the bus route |

### Response

```json
{
    "bus_number": "B1",
    "from_location": "Location A",
    "to_location": "Location B",
    "route": "A -> C -> B"
}
```

This includes:
- **bus_number**: Unique identifier for the bus.
- **from_location**: Starting location of the route.
- **to_location**: Ending location of the route.
- **route**: Full route description.

### Errors

- **404 Not Found**: If the bus route does not exist.
- **500 Internal Server Error**: If there's a database connection error.

---

## Error Codes Summary

- **404 Not Found**: Resource not found (e.g., non-existent page, no matching route).
- **500 Internal Server Error**: Database connection or query error.