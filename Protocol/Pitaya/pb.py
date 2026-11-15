from pathlib import Path

from google.protobuf import descriptor_pb2, descriptor_pool, json_format, message_factory

pool = descriptor_pool.DescriptorPool()
desc = descriptor_pb2.FileDescriptorSet.FromString(Path(__file__).with_name('pb.bin').read_bytes())
todo = list(desc.file)
while todo:
    size = len(todo)
    for fd in todo[:]:
        try:
            pool.Add(fd)
        except TypeError:
            continue
        todo.remove(fd)
    if len(todo) == size:
        raise RuntimeError('unresolved protobuf dependencies')


def typ(name):
    name = name if '.' in name else 'protos.' + name
    return message_factory.GetMessageClass(pool.FindMessageTypeByName(name))


def mk(cls, **vals):
    obj = typ(cls)()
    return fill(obj, vals)


def fill(obj, vals):
    for key, val in vals.items():
        fld = next((fld for fld in obj.DESCRIPTOR.fields
                    if fld.name.lower() == key.lower() or fld.json_name.lower() == key.lower()), None)
        if fld is None:
            raise KeyError(obj.DESCRIPTOR.full_name + '.' + key)
        dst = getattr(obj, fld.name)
        if fld.is_repeated:
            if fld.message_type and fld.message_type.GetOptions().map_entry:
                dst.update(val)
            elif fld.message_type:
                for item in val:
                    if isinstance(item, dict):
                        fill(dst.add(), item)
                    else:
                        dst.add().CopyFrom(item)
            else:
                dst.extend(val)
        elif fld.message_type:
            if isinstance(val, dict):
                fill(dst, val)
                dst.SetInParent()
            else:
                dst.CopyFrom(val)
        else:
            setattr(obj, fld.name, val)
    return obj


def dec(name, data):
    return typ(name).FromString(data)


def enc(obj):
    return obj.SerializeToString()


def js(obj):
    return json_format.MessageToDict(obj, descriptor_pool=pool)
