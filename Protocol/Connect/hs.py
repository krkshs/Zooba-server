import json


def hs(hb):
    return json.dumps({'code': 200, 'sys': {'heartbeat': hb, 'serializer': 'protobuf',
                                        'useDict': False}, 'user': {}},
                      separators=(',', ':')).encode()
