
# coding: utf-8

# ### Given a matrix: produce a matrix in row echelon form (REF).###
# 
# By using elementary row operations: interchange, scaling and replacement.<br>
# **Definition:** A matrix is in REF if it satisfies the following conditions:<br>
# -  If it has zero rows, it must be at the bottom of the matrix.<br>
# -  Leading entry in each row non-zero row is 1. <br>
# -  Each leadin is the to the right of all leading 1's above it.<br>
# 

# In[31]:

import numpy as np
import copy
def print_useful(g):
    'after one iteration, before update:' 
    print 'g.row',g.row,'g.col',g.col
    print 'g.leading',g.leading
    print g.m
    print 'done:',g.done()
    print '-------------------------------------'

class REF:
    def __init__(self, matrix):
        self.m = np.array(self.float_it(matrix))
        self.col = 0
        self.row = 0
        self.leading = None
        self.num_zero_rows = self.number_zero_rows()
    
    #True if matrix is all zeros
    def all_zeros(self):
        return not np.any(self.m)
    #Count the number of initial zero rows in matrix
    def number_zero_rows(self):
        count = 0
        for row in self.m:
            if (not np.any(row)):
                count +=1
        return count
    
    #converts every interger in matrix to float       
    def float_it(self,matrix):
        for i,row in enumerate(matrix):
            for j,col in enumerate(row):
                matrix[i][j] = float(matrix[i][j])
        return matrix
    
    #row_i <--> row_j
    def interchange(self,row_i,row_j):
        tmp = self.m[row_j].copy()
        self.m[row_j] = self.m[row_i]
        self.m[row_i] = tmp
    
    #row_i -> K*row_i
    def scale(self,K,row_i):
        scaled_row = K*self.m[row_i]
        self.m[row_i] = scaled_row
    
    #k*row_i, witout affecting original matrix
    def scale_for_rep(self,K,row_i):
        matrix = self.m.copy()
        return -K*matrix[row_i]
    #K*row_i + row_j
    def replace(self,K,row_i,row_j):
        scaled_row = self.scale_for_rep(K,row_i)
        replace_row = self.m[row_j]
        self.m[row_j] = [i + j for i,j in zip(scaled_row, replace_row)]
        if (not np.any(self.m[row_j])):
            self.num_zero_rows +=1
    #finds first none zero element in column            
    def first_none_zero_elt(self,col):
        for r_idx,elt in enumerate(col):
            if (elt != 0 and r_idx >= self.row ):
                return r_idx,elt
        return "WTF","WTF"
    #sets current leading and it's position
    def update(self,r,c,l):
        if (not isinstance(r,str)):
            self.row = r
        if (not isinstance(c,str)):
            self.col = c
        self.leading = l
    #reset leading and increaments position 
    def reset_leading(self):
        self.leading = None
        self.row +=1
        self.col +=1
        
    #if there exists a 1 in column below current leading
    #Then we interchange it with current leading's row
    #Otherwise scale leading to 1
    def find_one(self):
        for r_idx,elt in enumerate (self.m.T[self.row]):
            if (elt == 1):
                self.interchange(r_idx,self.row)
                self.leading = 1
                break
        if (self.leading != 1 and self.leading != None):
            K = 1/float(self.leading)
            self.scale(K,self.row)
    
    #in current leading's column: makes every integer 0
    def do_replacements(self):
        for r_idx,elt in enumerate(self.m.T[self.col]):
            if (elt != 0 and r_idx > self.row):
                K = elt
                self.replace(K,self.row,r_idx)
    #pushes zero rows to bottom          
    def zero_to_bot(self,r_idx):
        while (r_idx > self.row):
            new_r_idx = r_idx - 1
            self.interchange(r_idx,new_r_idx)
            r_idx -= 1
        return r_idx
        
        
    #find leading variables
    def find_leading(self):
        
        for c_idx,col in enumerate(self.m.T):
            not_all_zero = np.any(col)
            if (not_all_zero and c_idx >= self.row):
                r_idx,elt = self.first_none_zero_elt(col)
                r_idx = self.zero_to_bot(r_idx)
                self.update(r_idx,c_idx,elt)
                break
        if (self.leading !=1):
            self.find_one()
        

    #checks if we done producing a matrix in REF
    def done(self):
        return min(self.col,self.row) >= max(len(self.m),len(self.m[0]))
        
    #main function: produces a matrix in REF
    def produce_REF(self):
        if (self.all_zeros()):
            return self.m
        while(not self.done()):
            self.find_leading()
            self.do_replacements()
            self.reset_leading()
        return self.m
    def produce_REF_step_by_step(self):
        if (self.all_zeros()):
            print_useful(self)
        while(not self.done()):
            self.find_leading()
            print_useful(self)
            self.do_replacements()
            self.reset_leading()
        return self.m
    
    


# In[32]:

def solve_REF(matrix):
    g = REF(matrix)
    return g.produce_REF()
def step_by_step_REF(matrix):
    g = REF(matrix)
    return g.produce_REF_step_by_step()


# ### Given a matrix: produce a matrix in reduced row echelon form (RREF).###
# 
# By using elementary row operations: interchange, scaling and replacement.<br>
# **Definition:** A matrix is in RREF if it satisfies the following conditions:<br>
# -  The matrix is in REF 
# -  Each leading 1 is the only non zero number in it's column

# In[33]:

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
        


# In[34]:

def solve_RREF(matrix):
    #solve for it's REF
    ref_matrix = solve_REF(matrix)
    #inverse rows and column
    inverse = RREF(ref_matrix)
    inv_rref_mat = solve_REF(inverse.m)
    rref = RREF(inv_rref_mat)
    return np.array(rref.m)


# In[35]:

matrix2 = [[1,0,10,5],[3,1,-4,-1],[4,1,6,1]]
#step_by_step_REF(matrix2)


# In[36]:

def test(matrix):
    g = REF(matrix)
    g.find_leading()
    print_useful(g)
    g.do_replacements()
    g.reset_leading()
    
    g.find_leading()
    print_useful(g)
    g.do_replacements()
    g.reset_leading()
    print "------interestin stuff------"
    g.find_leading()
    print_useful(g)
    g.do_replacements()
    #print_useful(g)
    g.reset_leading()
    
    
test(matrix2)


# In[ ]:




# In[ ]:



