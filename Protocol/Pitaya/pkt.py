import zlib

MAX = 8 * 1024 * 1024


def inf(data):
    try:
        infl = zlib.decompressobj(47)
        body = infl.decompress(data, MAX + 1)
    except zlib.error as err:
        raise ValueError('invalid compressed message') from err
    if len(body) > MAX or infl.unconsumed_tail:
        raise ValueError('message too large')
    if not infl.eof or infl.unused_data:
        raise ValueError('invalid compressed message')
    return body


def vint(num):
    buf = bytearray()
    while num > 127:
        buf.append((num & 127) | 128)
        num >>= 7
    buf.append(num)
    return bytes(buf)


def rdv(buf, pos):
    num = 0
    for shift in range(0, 35, 7):
        if pos >= len(buf):
            raise ValueError('short request id')
        val = buf[pos]
        pos += 1
        num |= (val & 127) << shift
        if not val & 128:
            return num, pos
    raise ValueError('invalid request id')


def pkg(kind, body=b''):
    if len(body) > MAX:
        raise ValueError('packet too large')
    return bytes([kind]) + len(body).to_bytes(3, 'big') + body


def req(body):
    if not body:
        raise ValueError('empty message')
    flag = body[0]
    kind = (flag >> 1) & 7
    if kind not in (0, 1) or flag & 0xe1:
        raise ValueError('unsupported message flags')
    pos = 1
    rid = 0
    if kind == 0:
        rid, pos = rdv(body, pos)
    if pos >= len(body):
        raise ValueError('missing route')
    size = body[pos]
    pos += 1
    if not size or pos + size > len(body):
        raise ValueError('invalid route')
    route = body[pos:pos+size].decode('utf-8')
    data = body[pos+size:]
    if flag & 0x10:
        data = inf(data)
    return rid, route, data


def rsp(rid, body, err=False):
    return pkg(4, bytes([0x24 if err else 4]) + vint(rid) + body)
