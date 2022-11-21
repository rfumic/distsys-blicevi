import asyncio
import aiohttp
import aiosqlite
from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/getJokes")
async def get_jokes(request):
    # req = await request.json()
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in range(6):
                jokeTasks = []
                randomUserTasks = []
                for __ in range(2):
                    jokeTasks.append(
                        session.get("https://official-joke-api.appspot.com/random_joke")
                    )
                    randomUserTasks.append(session.get("https://randomuser.me/api/"))

                jokes = await asyncio.gather(*jokeTasks)
                jokes = [await x.json() for x in jokes]

                randomUsers = await asyncio.gather(*randomUserTasks)
                randomUsers = [await x.json() for x in randomUsers]

                tasks.append(
                    session.post("http://localhost:8081/filterUser", json=randomUsers)
                )
                tasks.append(
                    session.post("http://localhost:8082/filterJoke", json=jokes)
                )

            response = await asyncio.gather(*tasks)
            response = [await x.json() for x in response]

        return web.json_response(response)
    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)})


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8080)
