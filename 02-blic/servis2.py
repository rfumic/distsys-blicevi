import asyncio
import aiohttp
import aiosqlite
from aiohttp import web

routes = web.RouteTableDef()


@routes.post("/filterUser")
async def post_filterUser(request):
    req = await request.json()
    try:
        users = req[0]["results"]
        async with aiohttp.ClientSession() as session:
            tasks = []
            for user in users:
                json_data = {
                    "data": {
                        "user": {
                            "name": user["name"]["first"] + " " + user["name"]["last"],
                            "city": user["location"]["city"],
                            "username": user["login"]["username"],
                        }
                    }
                }
                print(json_data)
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
web.run_app(app, port=8081)
