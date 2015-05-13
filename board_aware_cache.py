"""
Cache expensive, board-dependent operations.
"""

CACHE = dict()


def get(operation, board, extra):
    md5 = board.md5()
    key = (operation, md5, extra)
    if key in CACHE:
        return CACHE[key]
    return None


def set(operation, board, extra, val):
    md5 = board.md5()
    key = (operation, md5, extra)
    CACHE[key] = val
