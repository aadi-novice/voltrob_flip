from random import randrange
import numpy as np
total = 25

num_z= randrange(6, min(13, total))
total = total - num_z
num_x = randrange(1, 10)
total = total - num_x
num_y = randrange(1, total)
total = total - num_y

num_list =[2 for x in range(num_x)] + [3 for y in range(num_y)] + [0 for z in range(num_z)]
print(f"length of num_list: {len(num_list)} \n total of x,y,z: {num_x + num_y + num_z} ")
mat=np.ones(shape=(5,5), dtype=int)
mat = mat.flatten()

num_list = np.array(num_list)

np.random.shuffle(num_list)

mat[:len(num_list)] = num_list
np.random.shuffle(mat)

mat = mat.reshape((5,5))
print(mat)


col_total = np.sum(mat, axis=0)
print(f"sum of each column: {col_total}")
row_total = np.sum(mat, axis=1)
print(f"sum of each row: {row_total}")
vol_col_total = np.count_nonzero(mat==0, axis=0)
print(f"volume of each column: {vol_col_total}")
vol_row_total = np.count_nonzero(mat== 0, axis=1)
print(f"volume of each row: {vol_row_total}")