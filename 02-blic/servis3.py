import asyncio
import aiohttp
import aiosqlite
from aiohttp import web

routes = web.RouteTableDef()


@routes.post("/filterJoke")
async def filter_joke(request):
    req = await request.json()
    try:
        jokes = req
        print(jokes)
        async with aiohttp.ClientSession() as session:
            tasks = []
            for joke in jokes:
                json_data = {
                    "data": {
                        "joke": {"setup": joke["setup"], "punchline": joke["punchline"]}
                    }
                }
                tasks.append(
                    asyncio.create_task(
                        session.post("http://localhost:8083/storeData", json=json_data)
                    )
                )

            response = await asyncio.gather(*tasks)
            response = [await x.json() for x in response]

        return web.json_response(response)
    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)})


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8082)
