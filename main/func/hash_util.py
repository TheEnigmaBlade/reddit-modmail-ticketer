import hashids

hasher = hashids.Hashids(salt="WOW  SO MAD  SUCH SALT", min_length=5)

def id_to_hash(id):
	return hasher.encode(id)

def hash_to_id(hash):
	ids = hasher.decode(hash)
	if len(ids) > 0:
		return ids[0]
	return None
