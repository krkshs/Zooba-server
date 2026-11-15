import hashlib
import json
from pathlib import Path

from google.protobuf import json_format
from Protocol.Pitaya.pb import typ, pool, js

root = Path(__file__).resolve().parents[2]
opt = json.loads((root / 'cfg.json').read_text(encoding='utf-8'))
raw = Path(__file__).with_name('cfg.json').read_text(encoding='utf-8')
cfg = json_format.Parse(raw, typ('ConfigGameInfo')(), ignore_unknown_fields=True,
                        descriptor_pool=pool)
cfg.hash = hashlib.sha256(raw.encode()).hexdigest()
cfg.code = 'BAT-200'
cfg.gameRoomClientAsyncLoadEnabled = False
for fld in cfg.DESCRIPTOR.fields:
    if fld.message_type and not fld.is_repeated:
        getattr(cfg, fld.name).SetInParent()
txt = json.dumps(js(cfg), ensure_ascii=False, separators=(',', ':'))
