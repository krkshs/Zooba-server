import asyncio

from aiohttp import web
from Logic.Player.db import Db
from Server.Connect.http import app
from Server.Connect.tcp import Conn
from Server.Theme.cfg import opt


async def main():
    db = Db()
    async def conn(reader, writer):
        await Conn(db, opt).run(reader, writer)
    srv = await asyncio.start_server(conn, opt['bind'], opt['tcp'])
    runner = web.AppRunner(app(db), access_log=None)
    await runner.setup()
    site = web.TCPSite(runner, opt['bind'], opt['http'])
    await site.start()
    print('pitaya ' + opt['host'] + ':' + str(opt['tcp']))
    print('http ' + opt['host'] + ':' + str(opt['http']))
    try:
        async with srv:
            await srv.serve_forever()
    finally:
        await runner.cleanup()
        db.cls()


if __name__ == '__main__':
    asyncio.run(main())
