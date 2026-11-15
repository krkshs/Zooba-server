from aiohttp import web

from Protocol.Pitaya.pb import js
from Server.Home.home import home
from Server.Theme.cfg import cfg, txt


def app(db):
    async def conf(req):
        return web.Response(text=txt, content_type='application/json')

    async def reg(req):
        data = await req.json()
        row, tok = db.reg(data.get('name', 'Player'), data.get('locale', 'ru'))
        return web.json_response(js(home(row, tok)))

    async def lgn(req):
        data = await req.json()
        row = db.get(data.get('token', ''))
        if row is None:
            return web.json_response({'code': 'BAT-400'}, status=401)
        return web.json_response(js(home(row, data['token'])))

    async def view(req):
        hdr = req.headers.get('Authorization', '')
        tok = hdr[7:] if hdr.startswith('Bearer ') else ''
        row = db.get(tok)
        if row is None:
            return web.json_response({'code': 'BAT-400'}, status=401)
        return web.json_response(js(home(row, tok)))

    async def ping(req):
        return web.json_response({'code': 'BAT-200', 'version': '7.6.0'})

    srv = web.Application(client_max_size=1024 * 1024)
    srv.add_routes([web.get('/health', ping), web.post('/reg', reg),
                    web.post('/lgn', lgn), web.get('/home', view),
                    web.get('/{hash:[0-9a-f]{64}}', conf), web.get('/cfg', conf)])
    return srv
