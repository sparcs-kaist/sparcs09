def to_int(string, default):
    try:
        return int(string)
    except:
        return default


def get_limit_offset(query):
    return (
        to_int(query.get('limit', ''), 10),
        to_int(query.get('offset', ''), 0),
    )
