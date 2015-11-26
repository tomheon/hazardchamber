from criticals import calc_critical_square
from gravity import apply_gravity
from match import find_matches
from tile_destroyer import destroy_tiles
from tiles import CriticalTile


def settle_board(board):
    """
    Useful to just get the board to a settled state, not caring about what
    happens in between (details of which tiles were destroyed etc.)

    Returns the stable board.
    """
    while True:
        matches = find_matches(board)

        if not matches:
            break

        new_board, destroyed_sqs = destroy_tiles(board)
        for match in matches:
            crit = calc_critical_square(match)
            if crit:
                new_board.set_at(crit[0], crit[1], CriticalTile())
        board, _ = apply_gravity(new_board)

    return board
