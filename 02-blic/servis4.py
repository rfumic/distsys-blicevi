import asyncio
import aiohttp
import aiosqlite
from aiohttp import web

routes = web.RouteTableDef()

temp_jokes = []
temp_users = []


@routes.post("/storeData")
async def store_data(request):
    req = await request.json()
    try:
        if "user" in req["data"]:
            temp_users.append(req)
            if temp_jokes != []:
                async with aiosqlite.connect("baza.db") as db:
                    user = temp_jokes[0]["data"]["user"]
                    joke = temp_jokes[0]["joke"]
                    await db.execute(
                        "INSET INTO Tablica (name,city,username,setup,punchline) VALUES (?,?,?,?,?)",
                        (
                            user["name"],
                            user["city"],
                            ["username"],
                            joke["setup"],
                            joke["punchline"],
                        ),
                    )
                    await db.commit()
                    temp_users = []
                    temp_jokes = []
                    async with db.execute("SELECT * FROM Tablica") as cur:
                        noOfRows = len(cur)
                        await db.commit()

                    return web.json_response(
                        {"status": "ok", "data": {"numberOfRowsInTable": noOfRows}}
                    )
            else:
                return web.json_response(
                    {"status": "Failed", "message": "Joke not present"}
                )

        if "joke" in req["data"]:
            temp_jokes.append(req)
            if temp_users != []:
                async with aiosqlite.connect("baza.db") as db:
                    user = temp_jokes[0]["data"]["user"]
                    joke = temp_jokes[0]["joke"]
                    await db.execute(
                        "INSET INTO Tablica (name,city,username,setup,punchline) VALUES (?,?,?,?,?)",
                        (
                            user["name"],
                            user["city"],
                            ["username"],
                            joke["setup"],
                            joke["punchline"],
                        ),
                    )
                    await db.commit()
                    temp_users = []
                    temp_jokes = []
                    async with db.execute("SELECT * FROM Tablica") as cur:
                        noOfRows = len(cur)
                        await db.commit()

                    return web.json_response(
                        {"status": "ok", "data": {"numberOfRowsInTable": noOfRows}}
                    )
            else:
                return web.json_response(
                    {"status": "Failed", "message": "User not present"}
                )

    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)})


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8083)
