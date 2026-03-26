from random import randrange
import numpy as np

def generate_table()-> dict:
    """
    Generate a random 5x5 Voltorb Flip board and its clue totals.

    The board contains:
    - 0 for voltorbs
    - 1, 2, 3 for multiplier/value tiles

    Returns:
        dict: A dictionary containing the board (`table`), row/column value totals,
        row/column voltorb totals, and counts of generated 2s/3s/0s.
    """
    total = 25
    # generate numbers of 0s, 2s and 3s
    num_z= randrange(6, min(13, total))
    total = total - num_z
    num_x = randrange(1, 10)
    total = total - num_x
    num_y = randrange(1, total)
    num_list =[2 for x in range(num_x)] + [3 for y in range(num_y)] + [0 for z in range(num_z)]
    # create the table and shuffle it
    mat=np.ones(shape=(5,5), dtype=int)
    mat = mat.flatten()
    num_list = np.array(num_list)
    mat[:len(num_list)] = num_list
    np.random.shuffle(mat)
    mat = mat.reshape((5,5))
    # get the totals and voltrobs present ready
    col_total = np.sum(mat, axis=0)
    row_total = np.sum(mat, axis=1)
    vol_col_total = np.count_nonzero(mat==0, axis=0)
    vol_row_total = np.count_nonzero(mat== 0, axis=1)
    # making output as dict
    output = {
        "table": mat,
        "col_total": col_total,
        "row_total": row_total,
        "vol_col_total": vol_col_total,
        "vol_row_total": vol_row_total,
        "num_x": num_x,
        "num_y": num_y,
        "num_z": num_z
    }
    return output


def solver(output: dict, state_matrix: np.ndarray, return_meta: bool = False):
    """
    Suggest next move(s) using deterministic rules first, then probabilistic fallback.

    Rule order:
    1) Rule 1: effective voltorbs == 0 in row/col -> all unknown there are safe.
    2) Rule 2: unknown count == effective voltorbs in row/col -> all unknown there are voltorbs.
    3) Rule 3: if no guaranteed safe move exists, choose one lowest-risk unknown tile.

    Args:
        output (dict): Board clues produced by `generate_table`, including
            `vol_row_total` and `vol_col_total`.
        state_matrix (np.ndarray): 5x5 state knowledge matrix where:
            `1` = revealed safe tile, `-1` = known voltorb, `0` = unknown.
        return_meta (bool): If True, also return metadata with whether Rule 3 was used.

    Returns:
        list[tuple[int, int]] | tuple[list[tuple[int, int]], dict]:
            - Default (`return_meta=False`): list of suggested positions.
            - With metadata (`return_meta=True`): `(positions, {"used_rule3": bool})`.
    """
    # Totals from board clues
    vol_col_total = output['vol_col_total']
    vol_row_total = output['vol_row_total']

    # Persistent knowledge from previous turns:
    #   1  => known safe/revealed tile
    #  -1  => known voltorb tile
    known_safe = set(map(tuple, np.argwhere(state_matrix == 1)))
    known_voltorb = set(map(tuple, np.argwhere(state_matrix == -1)))

    # Keep applying Rule 1 and Rule 2 until nothing new is discovered.
    while True:
        start_safe_count = len(known_safe)
        start_voltorb_count = len(known_voltorb)

        # Count already-known voltorbs per row/column.
        known_voltorb_per_row = np.zeros(5, dtype=int)
        known_voltorb_per_col = np.zeros(5, dtype=int)
        for row, col in known_voltorb:
            known_voltorb_per_row[row] += 1
            known_voltorb_per_col[col] += 1

        # Effective voltorbs = clue total minus already known voltorbs.
        effective_vol_row = vol_row_total - known_voltorb_per_row
        effective_vol_col = vol_col_total - known_voltorb_per_col

        # Unknown tiles (neither known safe nor known voltorb).
        unknown_per_row = {
            row: [
                (row, col)
                for col in range(5)
                if (row, col) not in known_safe and (row, col) not in known_voltorb
            ]
            for row in range(5)
        }
        unknown_per_col = {
            col: [
                (row, col)
                for row in range(5)
                if (row, col) not in known_safe and (row, col) not in known_voltorb
            ]
            for col in range(5)
        }

        # Rule 1: no voltorbs left in row/col => all unknown in that row/col are safe.
        for idx in range(5):
            if effective_vol_row[idx] == 0:
                known_safe.update(unknown_per_row[idx])
            if effective_vol_col[idx] == 0:
                known_safe.update(unknown_per_col[idx])

        # Refresh unknown groups after new safe discoveries.
        unknown_per_row = {
            row: [
                (row, col)
                for col in range(5)
                if (row, col) not in known_safe and (row, col) not in known_voltorb
            ]
            for row in range(5)
        }
        unknown_per_col = {
            col: [
                (row, col)
                for row in range(5)
                if (row, col) not in known_safe and (row, col) not in known_voltorb
            ]
            for col in range(5)
        }

        # Rule 2: unknown count equals effective voltorbs => all unknown are voltorbs.
        for idx in range(5):
            if effective_vol_row[idx] > 0 and effective_vol_row[idx] == len(unknown_per_row[idx]):
                known_voltorb.update(unknown_per_row[idx])
            if effective_vol_col[idx] > 0 and effective_vol_col[idx] == len(unknown_per_col[idx]):
                known_voltorb.update(unknown_per_col[idx])

        # If neither safe set nor voltorb set changed, fixed-point reached.
        new_info_found = (len(known_safe) > start_safe_count) or (len(known_voltorb) > start_voltorb_count)
        if not new_info_found:
            break

    # Persist discovered voltorbs back to state matrix for future solver calls.
    for row, col in known_voltorb:
        state_matrix[row, col] = -1

    # Guaranteed-safe moves only (exclude already revealed safe tiles).
    safe_to_return = [
        position for position in known_safe
        if state_matrix[position[0], position[1]] != 1
    ]

    # If we have guaranteed safe moves, prefer them over guessing.
    if len(safe_to_return) > 0:
        if return_meta:
            return safe_to_return, {"used_rule3": False}
        return safe_to_return

    # Rule 3: compute per-tile risk and pick the lowest-risk unknown tile.
    # Recompute effective counts with latest voltorb knowledge.
    known_voltorb_per_row = np.zeros(5, dtype=int)
    known_voltorb_per_col = np.zeros(5, dtype=int)
    for row, col in known_voltorb:
        known_voltorb_per_row[row] += 1
        known_voltorb_per_col[col] += 1

    effective_vol_row = vol_row_total - known_voltorb_per_row
    effective_vol_col = vol_col_total - known_voltorb_per_col

    unknown_per_row = {
        row: [
            (row, col)
            for col in range(5)
            if (row, col) not in known_safe and (row, col) not in known_voltorb
        ]
        for row in range(5)
    }
    unknown_per_col = {
        col: [
            (row, col)
            for row in range(5)
            if (row, col) not in known_safe and (row, col) not in known_voltorb
        ]
        for col in range(5)
    }

    unknown_positions = [
        (row, col)
        for row in range(5)
        for col in range(5)
        if (row, col) not in known_safe and (row, col) not in known_voltorb
    ]

    if len(unknown_positions) == 0:
        if return_meta:
            return [], {"used_rule3": False}
        return []

    # Combined row/column risk heuristic:
    # risk(i,j) = (effective_vol_row[i]/unknown_row_count) * (effective_vol_col[j]/unknown_col_count)
    best_position = None
    best_risk = float('inf')
    for row, col in unknown_positions:
        unknown_row_count = len(unknown_per_row[row])
        unknown_col_count = len(unknown_per_col[col])
        if unknown_row_count == 0 or unknown_col_count == 0:
            continue

        row_risk = effective_vol_row[row] / unknown_row_count
        col_risk = effective_vol_col[col] / unknown_col_count
        risk = row_risk * col_risk

        if risk < best_risk:
            best_risk = risk
            best_position = (row, col)

    if best_position is None:
        if return_meta:
            return [], {"used_rule3": False}
        return []

    if return_meta:
        return [best_position], {"used_rule3": True}
    return [best_position]



def game_loop(output:dict):
    """
    Runs the game by repeatedly asking the solver for next move(s).

    Args:
        output (dict): Board/clue dictionary returned by `generate_table`.

    Returns:
        str: Final game status message (win, loss, or no further safe progress).

    Notes:
        - Solver may return many guaranteed-safe moves or one probabilistic move.
        - If a returned move hits a voltorb, the game ends immediately.
    """
    state_matrix = np.zeros((5,5), dtype=int)
    total_numbered_positions = 0
    while True:
        solver_output = solver(output, state_matrix)
        print(solver_output)
        if len(solver_output) == 0:
            return "No more guaranteed safe positions!"

        # Apply returned moves to game state.
        for i in range(len(solver_output)):
            if output['table'][solver_output[i][0], solver_output[i][1]] != 0:
                state_matrix[solver_output[i][0], solver_output[i][1]] = 1
                if output['table'][solver_output[i][0], solver_output[i][1]] == 2 or output['table'][solver_output[i][0], solver_output[i][1]] == 3:
                    total_numbered_positions += 1
            else:
                return f"Game Over! Position: {solver_output[i]} Value: {output['table'][solver_output[i][0], solver_output[i][1]]}"
                
        
        
        
        if total_numbered_positions == output['num_x'] + output['num_y']:
            return "Congratulations! You have found all the safe positions!"
        
    