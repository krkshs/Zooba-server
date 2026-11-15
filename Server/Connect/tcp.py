import asyncio

from google.protobuf.message import DecodeError
from Logic.Method.routes import run
from Protocol.Connect.hs import hs
from Protocol.Pitaya.pkt import MAX, pkg, req, rsp
from Protocol.Pitaya.pb import enc, mk


class Conn:
    def __init__(self, db, opt):
        self.db = db
        self.opt = opt
        self.row = None
        self.tok = None

    async def run(self, reader, writer):
        ready = False
        ack = False
        try:
            while True:
                head = await asyncio.wait_for(reader.readexactly(4), 90)
                kind = head[0]
                size = int.from_bytes(head[1:], 'big')
                if size > MAX:
                    break
                body = await reader.readexactly(size)
                if kind == 1 and not ready:
                    writer.write(pkg(1, hs(self.opt['hb'])))
                    ready = True
                elif kind == 2 and ready:
                    ack = True
                elif kind == 3 and ready:
                    writer.write(pkg(3))
                elif kind == 4 and ack:
                    rid, route, data = req(body)
                    print('req ' + route, flush=True)
                    err = False
                    try:
                        obj = run(self, route, data)
                    except PermissionError:
                        obj = mk('Error', code='BAT-400', msg='authenticate first')
                        err = True
                    except LookupError:
                        obj = mk('Error', code='BAT-404', msg='unsupported route',
                                 metadata={'route': route})
                        err = True
                    if rid:
                        writer.write(rsp(rid, enc(obj), err))
                else:
                    break
                await writer.drain()
        except (asyncio.IncompleteReadError, asyncio.TimeoutError, ConnectionError,
                ValueError, DecodeError) as err:
            if not isinstance(err, asyncio.IncompleteReadError):
                print('drop ' + str(err), flush=True)
        finally:
            writer.close()
            await writer.wait_closed()
