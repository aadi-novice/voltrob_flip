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
    # get the table and totals from the output
    table = output['table']
    col_total = output['col_total']
    row_total = output['row_total']
    vol_col_total = output['vol_col_total']
    vol_row_total = output['vol_row_total']
    #
    lst = []
    for i in range(5):
        
        if vol_col_total[i] == 0:
            lst.append([(j,i) for j in range(5)])
        if vol_row_total[i] == 0:
            lst.append([(i,j) for j in range(5)])

        
    unique_lst = list(set([item for sublist in lst for item in sublist]))
    unique_lst = [
    i for i in unique_lst
    if state_matrix[i[0], i[1]] != 1
    ]   
    return unique_lst



def game_loop(output:dict):
    state_matrix = np.zeros((5,5), dtype=int)
    total_numbered_positions = 0
    while True:
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
        
    