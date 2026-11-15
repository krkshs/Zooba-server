import hashlib
import secrets
import sqlite3
import time
from pathlib import Path


def key(tok):
    return hashlib.sha256(tok.encode()).hexdigest()


class Db:
    def __init__(self, path=None):
        self.db = sqlite3.connect(path or Path(__file__).with_name('plr.db'))
        self.db.row_factory = sqlite3.Row
        self.db.execute('create table if not exists plr (id text primary key, tok text unique, '
                        'name text, loc text, chr text, born integer)')
        self.db.commit()

    def reg(self, name='Player', loc='ru'):
        tok = secrets.token_urlsafe(32)
        uid = secrets.token_hex(16)
        self.db.execute('insert into plr values (?, ?, ?, ?, ?, ?)',
                        (uid, key(tok), name[:32], loc[:16], 'buffalo', int(time.time())))
        self.db.commit()
        return self.get(tok), tok

    def get(self, tok):
        if not tok:
            return None
        row = self.db.execute('select * from plr where tok=?', (key(tok),)).fetchone()
        return dict(row) if row else None

    def lgn(self, tok, name='Player', loc='ru'):
        row = self.get(tok)
        return (row, tok) if row else self.reg(name, loc)

    def set(self, uid, fld, val):
        if fld not in ('name', 'loc', 'chr'):
            raise ValueError('invalid player field')
        self.db.execute('update plr set ' + fld + '=? where id=?', (val, uid))
        self.db.commit()

    def cls(self):
        self.db.close()
