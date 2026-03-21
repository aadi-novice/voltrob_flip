from funcs import *
import numpy as np

output = generate_table()
arr = np.array(output['table'])
arr = np.reshape(arr, (5,5))
print(f"Table: {arr} \nColumn Totals: {output['col_total'].tolist()} \nRow Totals: {output['row_total'].tolist()} \nVoltrob Column Totals: {output['vol_col_total'].tolist()} \nVoltrob Row Totals: {output['vol_row_total'].tolist()}")


# solver_output = solver(output)
# print(f"Guaranteed safe positions: {solver_output}")

# for i in range(len(solver_output)):
#     print(f"Position: {solver_output[i]} Value: {arr[solver_output[i][0], solver_output[i][1]]}")
# #print(arr[solver_output[0][0], solver_output[0][1]])


print(game_loop(output))