from random import randrange
import numpy as np

def generate_table()-> dict:
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


def solver(output: dict, state_matrix: np.ndarray):
    vol_col_total = output['vol_col_total']
    vol_row_total = output['vol_row_total']

    known_safe = set(map(tuple, np.argwhere(state_matrix == 1)))
    known_voltorb = set(map(tuple, np.argwhere(state_matrix == -1)))
    iteration = 0

    while True:
        iteration += 1
        start_safe_count = len(known_safe)
        start_voltorb_count = len(known_voltorb)

        known_voltorb_per_row = np.zeros(5, dtype=int)
        known_voltorb_per_col = np.zeros(5, dtype=int)
        for row, col in known_voltorb:
            known_voltorb_per_row[row] += 1
            known_voltorb_per_col[col] += 1

        effective_vol_row = vol_row_total - known_voltorb_per_row
        effective_vol_col = vol_col_total - known_voltorb_per_col

        print(f"[solver iter {iteration}] effective_vol_row={effective_vol_row.tolist()} effective_vol_col={effective_vol_col.tolist()} known_voltorb={len(known_voltorb)}")

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

        unknown_len_per_row = [len(unknown_per_row[idx]) for idx in range(5)]
        row_equals = [int(effective_vol_row[idx]) == unknown_len_per_row[idx] for idx in range(5)]
        print(f"[solver iter {iteration}] unknown_len_per_row={unknown_len_per_row} row_effective_equals_unknown={row_equals}")

        # Rule 1 -> add to safe
        for idx in range(5):
            if effective_vol_row[idx] == 0:
                known_safe.update(unknown_per_row[idx])
            if effective_vol_col[idx] == 0:
                known_safe.update(unknown_per_col[idx])

        # Refresh unknown positions after adding new safe tiles
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

        # Rule 2 -> add to voltorb
        for idx in range(5):
            if effective_vol_row[idx] > 0 and effective_vol_row[idx] == len(unknown_per_row[idx]):
                known_voltorb.update(unknown_per_row[idx])
            if effective_vol_col[idx] > 0 and effective_vol_col[idx] == len(unknown_per_col[idx]):
                known_voltorb.update(unknown_per_col[idx])

        # Use voltorb knowledge to update effective counts (happens at top of next iteration)
        new_info_found = (len(known_safe) > start_safe_count) or (len(known_voltorb) > start_voltorb_count)
        if not new_info_found:
            break

    for row, col in known_voltorb:
        state_matrix[row, col] = -1

    safe_to_return = [
        position for position in known_safe
        if state_matrix[position[0], position[1]] != 1
    ]
    return safe_to_return



def game_loop(output:dict):
    state_matrix = np.zeros((5,5), dtype=int)
    total_numbered_positions = 0
    solver_call = 0
    while True:
        solver_call += 1
        print(f"[game_loop] solver_call={solver_call} safe_marked={(state_matrix == 1).sum()} voltorb_marked={(state_matrix == -1).sum()}")
        print(f"[game_loop] state_matrix=\n{state_matrix}")
        solver_output = solver(output, state_matrix)
        print(solver_output)
        if len(solver_output) == 0:
            return "No more guaranteed safe positions!"
        for i in range(len(solver_output)):
            if output['table'][solver_output[i][0], solver_output[i][1]] != 0:
                state_matrix[solver_output[i][0], solver_output[i][1]] = 1
                if output['table'][solver_output[i][0], solver_output[i][1]] == 2 or output['table'][solver_output[i][0], solver_output[i][1]] == 3:
                    total_numbered_positions += 1
            else:
                return f"Game Over! Position: {solver_output[i]} Value: {output['table'][solver_output[i][0], solver_output[i][1]]}"
                
        
        
        
        if total_numbered_positions == output['num_x'] + output['num_y']:
            return "Congratulations! You have found all the safe positions!"
        
    