from random import shuffle, randrange, random
import math

MAZE_SIZE = 10

def change_to_dict(graph):
    my_dict = {}
    length = len(graph)
    for num in range(length):
        neigh = graph[num]
        my_dict[num] = neigh 
    
     
    return my_dict 


def DFS_search(graph,start_node,end_node):
    victory = change_to_dict(graph)
    length = len(graph) 
    ## explored keeps track of all nodes visited #
    explored = [False] * length
    explored[start_node] = True 
    # my_dict is for back tracking and creating a path from
    # start_node to end_node 
    my_dict = {start_node : None}
    # lst is a stack so that we traverse as far as we can # 
    lst = [start_node]

    while len(lst) > 0:
        current_node = lst.pop(-1)
        ## obtain a list of nodes adjacent to current_node ##
        adjacent = victory[current_node]
        ## reach end of path and need to back track to return a path
        ## between start_node and end_node 
        if current_node == end_node:
            temp = end_node 
            path = [end_node]
            while start_node != path[0]:
                path =  [my_dict[temp]] + path
                temp = my_dict[temp]

            return path 
            

        else:
            ## check if nodes in adjacent has been visited ##
            for node in adjacent:
                if not explored[node]:
                    lst.append(node)
                    ## update explored lst ##
                    explored[node] = True
                    my_dict[node] = current_node 

                else:
                    # should not traverse nodes that has already been
                    # visited 
                    continue

    ## No path exist between start_node and end_node ## 
    return []
        

 

def BFS_search(graph,start_node,end_node):
    victory = change_to_dict(graph)
    length = len(graph)
    explored = [False] * length
    explored[start_node] = True
    queue = [start_node]
    my_dict = {start_node:None} 
    # if len(queue) hits 0 it means that there is no path
    # between start_node and end_node # 
    while len(queue) > 0:
        current_node = queue.pop(0)
        adjacent = victory[current_node]
 
        # End of path, do backtracking 
        if current_node == end_node:
            temp = end_node
            path = [end_node]
            while start_node != path[0]:
                path = [my_dict[temp]] + path
                temp = my_dict[temp]
 
            return path 
 
        else:
            for node in adjacent:
                # unexplored node # 
                if not explored[node]:
                    queue.append(node)
                    explored[node] = True
                    my_dict[node] = current_node
 
                else:
                    continue
 
    return []

 
def make_maze():
    vis = [[0] * MAZE_SIZE + [1] for _ in range(MAZE_SIZE)] + [[1] * (MAZE_SIZE + 1)]
    ver = [["|:"] * MAZE_SIZE + ['|'] for _ in range(MAZE_SIZE)] + [[]]
    hor = [["+-"] * MAZE_SIZE + ['+'] for _ in range(MAZE_SIZE + 1)]
 
    def walk(x, y):
        vis[y][x] = 1
 
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+ "
            if yy == y: ver[y][max(x, xx)] = " :"
            walk(xx, yy)
 
    walk(randrange(MAZE_SIZE), randrange(MAZE_SIZE))
 
    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    
    s_temp = s
    graph = [[] for i in range(MAZE_SIZE*MAZE_SIZE)]
    for col in range(MAZE_SIZE):
        for row in range(MAZE_SIZE):
            if s_temp[(2*row+1)*(2*MAZE_SIZE+2)+(2*col)] == " " or (random() < 1/(2*MAZE_SIZE) and col != 0): 
                graph[col+MAZE_SIZE*row].append(col-1+MAZE_SIZE*row)
                graph[col-1+MAZE_SIZE*row].append(col+MAZE_SIZE*row)
                
            if s_temp[(2*row+2)*(2*MAZE_SIZE+2)+(2*col)+1] == " " or (random() < 1/(2*MAZE_SIZE) and row != MAZE_SIZE-1): 
                graph[col+MAZE_SIZE*row].append(col+MAZE_SIZE*(row+1))
                graph[col+MAZE_SIZE*(row+1)].append(col+MAZE_SIZE*row)
    
    return s,graph
 
   
def print_maze(g, path, players):
      
    s = ""
    for col in range(MAZE_SIZE): s+="+---"
    s+="+\n"
    
    for row in range(MAZE_SIZE): 
        s+="|"
        for col in range(MAZE_SIZE): 
            if row*MAZE_SIZE+col == players[0]: s+="👨 "
            elif row*MAZE_SIZE+col == players[1]: s+="🍒 "
            elif row*MAZE_SIZE+col in path: 
                ind = path.index(row*MAZE_SIZE+col)
                if path[ind+1] == row*MAZE_SIZE+col+1: s+=" → "
                elif path[ind+1] == row*MAZE_SIZE+col-1: s+=" ← "
                elif path[ind+1] == row*MAZE_SIZE+col+MAZE_SIZE: s+=" ↓ "
                elif path[ind+1] == row*MAZE_SIZE+col-MAZE_SIZE: s+=" ↑ "
                else: s+="ppp"
            else: s+="   " 
            if (row*MAZE_SIZE+col+1) in g[row*MAZE_SIZE+col]: s+=" "
            else: s+="|"
                
        s+="\n+" 
        for col in range(MAZE_SIZE): 
            if ((row+1)*MAZE_SIZE+col) in g[row*MAZE_SIZE+col]: s+="   +"
            else: s+="---+"
        s+="\n"
        
        
    print(s)
                
    
    
s, g = make_maze()    
players = [0,MAZE_SIZE*MAZE_SIZE-1]
print(g)

print("\n\n ******** PERFORMING DFS ********" )
path_DFS = DFS_search(g,players[0],players[1])
print_maze(g,path_DFS,players)
print("Path length for DFS is %i" % (len(path_DFS)-1))

print("\n\n ******** PERFORMING BFS ********" )
path_BFS = BFS_search(g,players[0],players[1])
print_maze(g,path_BFS,players)
print("Path length for BFS is %i" % (len(path_BFS)-1))
