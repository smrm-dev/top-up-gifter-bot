from hashlib import md5

def make_md5_hash(tel_id:str):
    has_res = md5(bytes(tel_id, 'ascii'))
    return has_res.hexdigest()