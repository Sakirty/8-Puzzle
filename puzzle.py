import sys
import copy
# this will print out the matrix
def visulize(mystring):
    print("Here is the current matrix:")
    for items in mystring:
        print(items)

# this will returns number of tiles that is out of location
def num_wrong_tiles(start, goal) -> int:
    count = 0
    for i in range(len(start)):
        if start[i] != goal[i]:
            count += 1
    return count

# this will map int to matrix List[List[int]], a 3x3 one
def matrixfy(start):
    start = str(start)
    list1 = []
    list2 = []
    for i in range(9):
        list1.append(start[i])
        if (i+1)%3 == 0:
            list2.append(list1)
            list1 = []
    return list2

# this will revert the matrix to string
def stringfy(mtrx):
    nstr = ""
    for n, i in enumerate(mtrx):
            for k, j in enumerate(i):
                nstr += mtrx[n][k]
    return nstr

# compare 2 same
def cpab(mtrx, ggoal):
    for n, i in enumerate(mtrx):
            for k, j in enumerate(i):
                if ggoal[n][k] != mtrx[n][k]:
                    return False
    return True

# this will get index within that matrix -> tuple
def get_index(target, mtrx): # [(0, 0)]
    target = str(target)
    return [(i, el.index(target)) for i, el in enumerate(mtrx) if target in el][0]

# return total manhattan distance of current matrix with goal matrix
def manhattan_distance(start, goalin) -> int:
    total = 0
    start = stringfy(start)
    goalin = stringfy(goalin)
    for item in str(start):
        if item != "0":
            aa = get_index(item,start)
            bb = get_index(item,goalin)
            total += abs(int(aa[0])-int(bb[0]))+abs(int(aa[1])-int(bb[1]))   
    return total

# movements
def up(start):
    row = get_index(0,start)[0] # (row, col)
    col = get_index(0,start)[1]
    if row != 2: # if the space is not at the bottom
        start[row][col] = start[row+1][col]
        start[row+1][col] = str(0)
    else: #cant move up since the space is at the bottom
        return None
    return start

def down(start):
    row = get_index(0,start)[0] # (row, col)
    col = get_index(0,start)[1]
    if row != 0: # if the space is not at the top
        start[row][col] = start[row-1][col]
        start[row-1][col] = str(0)
    else: 
        return None
    return start

def left(start):
    row = get_index(0,start)[0] # (row, col)
    col = get_index(0,start)[1]
    if col != 2: # if the space is not at the right
        start[row][col] = start[row][col+1]
        start[row][col+1] = str(0)
    else:
        return None
    return start

def right(start):
    row = get_index(0,start)[0] # (row, col)
    col = get_index(0,start)[1]
    if col != 0: # if the space is not at the left
        start[row][col] = start[row][col-1]
        start[row][col-1] = str(0)
    else:
        return None
    return start

# sort the dict as priority queue, based on value, num high->low
def pqsort(mydic):
    return sorted(mydic.items(), key=lambda x: x[1], reverse=True)

# A* choice 1:manhattan, choice 2: num_wrong_tiles
def astar(choice,mtrx):
    frontier = [str(mtrx)] # frontier stack
    explored = [] # explored stack
    goaltrix = matrixfy(123804765) # goal state 123804765
    matrix = matrixfy(mtrx)
    fn = dict() # fn cost, work with priority queue
    fn[str(mtrx)] = manhattan_distance(matrix,goaltrix) # init gn as 0
    gn = dict()
    gn[str(mtrx)] = 0 # init gn as 0
    step_indicator = 0 #which to appent to total_steps: 0up, 1down, 2left, 3right
    dire = dict()
    dire[str(mtrx)] = "" #record step at each matrix

    while frontier:
        mypq = pqsort(fn) # sort the fn dict, with lowest fn at last
        curr = mypq[-1][0]# get the state string
        del fn[curr] # remove it from fn dict queue
        frontier.remove(curr)
        explored.append(curr)
        dirstr = dire[curr] # get the current node direction
        gval = int(gn[curr]) # distance value
        if(str(curr) == "123804765"):
            return dire[curr][:-2], gn[curr] # return its direction
        curr = matrixfy(curr)
        if up(curr) != None:
            if(stringfy(curr) not in frontier) and (stringfy(curr) not in explored):
                frontier.append(stringfy(curr))
                gval += 1
                gn[stringfy(curr)] = gval
                if choice == "1":
                    fn[stringfy(curr)] = gval + manhattan_distance(curr,goaltrix)
                else:
                    fn[stringfy(curr)] = gval + num_wrong_tiles(curr,goaltrix)
                gval -= 1 # reset g                
                dire[stringfy(curr)] = dirstr +"up, "
            down(curr)
        if down(curr) != None:
            if(stringfy(curr) not in frontier) and (stringfy(curr) not in explored):
                frontier.append(stringfy(curr))
                gval += 1
                gn[stringfy(curr)] = gval
                if choice == "1":
                    fn[stringfy(curr)] = gval + manhattan_distance(curr,goaltrix)
                else:
                    fn[stringfy(curr)] = gval + num_wrong_tiles(curr,goaltrix)
                gval -= 1 # reset g 
                dire[stringfy(curr)] = dirstr +"down, "
            up(curr)
        if left(curr) != None:
            if(stringfy(curr) not in frontier) and (stringfy(curr) not in explored):
                frontier.append(stringfy(curr))
                gval += 1
                gn[stringfy(curr)] = gval
                if choice == "1":
                    fn[stringfy(curr)] = gval + manhattan_distance(curr,goaltrix)
                else:
                    fn[stringfy(curr)] = gval + num_wrong_tiles(curr,goaltrix)
                gval -= 1 # reset g 
                dire[stringfy(curr)] = dirstr +"left, "
            right(curr)
        if right(curr) != None:
            if(stringfy(curr) not in frontier) and (stringfy(curr) not in explored):
                frontier.append(stringfy(curr))
                gval += 1
                gn[stringfy(curr)] = gval
                if choice == "1":
                    fn[stringfy(curr)] = gval + manhattan_distance(curr,goaltrix)
                else:
                    fn[stringfy(curr)] = gval + num_wrong_tiles(curr,goaltrix)
                gval -= 1 # reset g 
                dire[stringfy(curr)] = dirstr +"right, "
            left(curr)
    return None

# Deeping search, with limit, if dont want limit pass in -1 as limit
def limit_dfs(limit, mtrx):
    frontier = [str(mtrx)] # frontier stack
    explored = [] # explored stack
    dpth = dict()
    dpth[str(mtrx)] = 0
    dire = dict()
    dire[str(mtrx)] = "" # record list direction
    i = 0 # root is depth 0
    if limit == -1: #pass in limit = -1 when want to set no limit
        limit = sys.maxsize
    while frontier:
        curr = frontier.pop() # pop the last one
        explored.append(curr)
        if(str(curr) == "123804765"): #123804765
            return dire[curr][:-2] #successfully found one
        if(dpth[curr]<limit): # if not in depth limit, generate new layer
            i+=1
            dirstr = dire[curr]
            curr = matrixfy(curr)
            if up(curr) != None:
                if(stringfy(curr) not in frontier) and (stringfy(curr) not in explored):
                    frontier.append(stringfy(curr))
                    dpth[stringfy(curr)] = i
                    dire[stringfy(curr)] = dirstr +"up, "
                down(curr)
            if down(curr) != None:
                if(stringfy(curr) not in frontier) and (stringfy(curr) not in explored):
                    frontier.append(stringfy(curr))
                    dpth[stringfy(curr)] = i
                    dire[stringfy(curr)] = dirstr +"down, "
                up(curr)
            if left(curr) != None:
                if(stringfy(curr) not in frontier) and (stringfy(curr) not in explored):
                    frontier.append(stringfy(curr))
                    dpth[stringfy(curr)] = i
                    dire[stringfy(curr)] = dirstr +"left, "
                right(curr)
            if right(curr) != None:
                if(stringfy(curr) not in frontier) and (stringfy(curr) not in explored):
                    frontier.append(stringfy(curr))
                    dpth[stringfy(curr)] = i
                    dire[stringfy(curr)] = dirstr +"right, "
                left(curr)
    return False

def iterative_deepening(mtrx):
    limit = 0
    while(limit_dfs(limit,mtrx) ==  False):
        limit += 1
    return limit_dfs(limit,mtrx),limit

# main
if(len(sys.argv) != 2):
    print("Usage: give only the inital state(int)")
    exit()
init_state = str(sys.argv[1])
if(len(str(init_state))!=9):
    if(len(str(init_state))==8):
        init_state = str(init_state).zfill(9) # fill it to 10 digits,(a str)
    else:
        print("input must be 9 digits")
        exit()

print("======A* Using Manhattan:======\n")
rrrslt = astar("1",init_state)
print("Total Steps: "+str(rrrslt[1]))
print("Steps: "+str(rrrslt[0]))

print("\n======A* Using Num Wrong Tiles:======\n")
rrrslt = astar("2",init_state)
print("Total Steps: "+str(rrrslt[1]))
print("Steps: "+str(rrrslt[0]))

print("\n======Iterative Deepening:======\n")
rrrslt = iterative_deepening(init_state)
print("Total Steps: "+str(rrrslt[1]))
print("Steps: "+str(rrrslt[0]))