from Protocol.Pitaya.pb import dec
from Server.Home.home import home


def lgn(ctx, data):
    req = dec('AuthenticatePlayerArgs', data)
    row, tok = ctx.db.lgn(req.accessToken, req.syncPlayer.name or 'Player', req.locale or 'ru')
    if row['chr'] not in ('buffalo', 'gorilla'):
        ctx.db.set(row['id'], 'chr', 'buffalo')
        row['chr'] = 'buffalo'
    ctx.row = row
    ctx.tok = tok
    return home(row, tok)
