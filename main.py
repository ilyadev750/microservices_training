import uvicorn
from fastapi import FastAPI, Query, Body


app = FastAPI()


hotels = [
    {'id': 1, 'title': 'Belgrade'},
    {'id': 2, 'title': 'Kragujevac'},
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.patch("/hotels/{hotel_id}")
def update_hotel_partial(
        hotel_id: int,
        name: str = Body(embed=True),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["name"] = name
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def update_hotel_full(
        hotel_id: int,
        title: str = Body(embed=True),
        name: str = Body(embed=True),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
    return {"status": "OK"}




if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)