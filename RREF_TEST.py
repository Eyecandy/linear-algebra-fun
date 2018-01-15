
# coding: utf-8

# In[127]:

get_ipython().magic(u"run 'RREF.ipynb'")


# In[132]:

matrix = [[1,2,3],[0,4,8],[9,5,6]]
matrix2 = [[1,0,10,5],[3,1,-4,-1],[4,1,6,1]]


# In[135]:

solve_RREF(matrix)


# In[139]:

step_by_step_REF(matrix2)


# ### Given a matrix: produce a matrix in row echelon form (REF).###
# 
# By using elementary row operations: interchange, scaling and replacement.<br>
# **Definition:** A matrix is in REF if it satisfies the following conditions:<br>
# -  If it has zero rows, it must be at the bottom of the matrix.<br>
# -  Leading entry in each row non-zero row is 1. <br>
# -  Each leadin is the to the right of all leading 1's above it.<br>

# ### Given a matrix: produce a matrix in reduced row echelon form (RREF).###
# 
# By using elementary row operations: interchange, scaling and replacement.<br>
# **Definition:** A matrix is in RREF if it satisfies the following conditions:<br>
# -  The matrix is in REF 
# -  Each leading 1 is the only non zero number in it's column

# In[ ]:

class RREF:
    def __init__(self,REF_matrix):
        self.m = self.make_non_np(self.inverse(REF_matrix))
    def inverse(self,matrix):
        for r_idx,row in enumerate(matrix):
            matrix[r_idx] = row[::-1]
        return matrix[::-1]
    
    def make_non_np(self,np_mat):
        matrix = []
        for row in np_mat:
            nr = []
            for col in row:
                nr.append(col)
            matrix.append(nr)
        return matrix
    
def solve_RREF(matrix):
    #solve for it's REF
    ref_matrix = solve_REF(matrix)
    #inverse rows and column
    inverse = RREF(ref_matrix)
    inv_rref_mat = solve_REF(inverse.m)
    rref = RREF(inv_rref_mat)
    return np.array(rref.m)
matrix2 = [[1,0,10,5],[3,1,-4,-1],[4,1,6,1]]
step_by_step_REF(matrix2)

