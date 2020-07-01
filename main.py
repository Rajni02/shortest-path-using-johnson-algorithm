'''
program : Shortest path all pair by Floyd-Warshall and Johnson's method
'''




#--importing packages
import os
import sys
from random import *
from datetime import datetime
import time
import matplotlib.pyplot as plt


#--Dijkstra's algorithm to find pairwise shortest path
def short_path_dijkstra(n,source,E,neighbours):
    max_wt = max([x[2] for x in E])
    max_wt = max_wt*(len(E)+1)

    sd_source = [max_wt for x in range(0,n)]
    prev = [0 for x in range(0,n)]

    
    sd_source[source] = 0
    Q = list(sd_source)
    rem = [x for x in Q if x!=-1]
    
    while len(rem) != 0:
        u = Q.index(min(rem))
        Q[u] = -1
        for e in neighbours[u]:
            mod_d = sd_source[u]+e[2]
            if(mod_d < sd_source[e[1]]):
                sd_source[e[1]] = mod_d
                Q[e[1]] = mod_d
                prev[e[1]] = e[2]
                
        rem = [x for x in Q if x!=-1]

    return sd_source
        

#--Bellman Ford algorithm to find shortest path
def short_path_Bell_Ford(n,source,E):

    #--keeping infinity value as 'n^2'
    max_wt = max([x[2] for x in E])
    max_wt = max_wt*(len(E)+1)
    
    #--creating weight matrix
    w = [max_wt for x in range(0,n)]
    #--Assuming '0' is source of the graph
    w[source] = 0
    
    #--Readjusting weights iteratively
    for i in range(0,n):
        for e in E:
            if(w[e[0]] < max_wt):
                if(w[e[0]]+e[2]<w[e[1]]):
                    w[e[1]] = w[e[0]]+e[2]

    #--Detecting if graph contains a cycle with negative weight cycle
    for e in E:
        if (w[e[0]]+e[2] < w[e[1]]):
            print "Graph contains a negative weight cycle"
            return []

    return w



#--Function to retrieve the final paths in floyd_Warshall algorithm
def get_final_path(i,j,mid_sd,sd):
    if(mid_sd[i][j] == -1):
        return sd[i][j]
    else:
        return get_final_path(i,mid_sd[i][j],mid_sd,sd)+get_final_path(mid_sd[i][j],j,mid_sd,sd)




#--shortest path using Floyd-Warshell algo
def short_path_floyd(n,E):

    #--creating distance matrix
    max_wt = max([x[2] for x in E])
    max_wt = max_wt*(len(E)+1)
    
    sd = [[max_wt for x in range(0,n)] for y in range(0,n)]
    for i in range(0,n):
        sd[i][i] = 0

    for e in E:
        sd[e[0]][e[1]] = e[2]

    mid_sd = [[-1 for x in range(0,n)] for y in range(0,n)]
    for k in range(0,n):
        for i in range(0,n):
            for j in range(0,n):
                if(sd[i][k]+sd[k][j] < sd[i][j]):
                    sd[i][j] = sd[i][k]+sd[k][j]
                    mid_sd[i][j] = k

    for i in range(0,n):
        for j in range(0,n):
            sd[i][j] = get_final_path(i,j,mid_sd,sd)
            
    return sd


def short_path_john(n,E):

    sd = []

    #adding 0 weight edges from extra vertex to rest of the vertices
    E_mod = list(E)
    for a0 in range(0,n):
        E_mod.append([n,a0,0])
    
    source = n
    weights = short_path_Bell_Ford(n+1,source,E_mod)

    for e in E_mod:
        e[2] += weights[e[0]] - weights[e[1]]

    #removing dummy edges
    E_mod = E_mod[0:len(E_mod)-n]

    neighbours = {}
    for i in range(0,n):
        neighbours[i] = []
            

    for e in E_mod:
        neighbours[e[0]].append(e)
        
        
    for source in range(0,n) :

        sd_source = short_path_dijkstra(n,source,E_mod,neighbours)

        #--Restoring weights
        
        for s in range(0,n):
            sd_source[s] = sd_source[s]+weights[s] - weights[source]
            
        sd.append(sd_source)

    return sd        

def get_n_m_pair():
    n = sample(range(20,40),10)
    nm_pairs = []
    
    for x in n:
        m = sample(range(x,x*(x-1)//2),10)
        nm_pairs.append([[x,y] for y in m])

    return nm_pairs
        
def random_input_graph(n,m):
    #--Accepting user input
    #n = int(raw_input("Enter no of vertices (greater than 4) : ").strip())

    #--Exit from main() if n<4
    if(n<=4):
        print "Enter value greater than 4"
        sys.exit(0)
        
    #-- getting all posible edges and assigning random weights
    all_edge_pairs = [[i,j] for i in range(0,n) for j in range(0,n) if i!=j]
    weights = [randint(1,n) for x in range(0,len(all_edge_pairs))]
    
    for i in range(0,len(all_edge_pairs)):
        all_edge_pairs[i].append(weights[i])

    #print all_edge_pairs
    
    #-- selecting random number of pairs in 
    edge_count = sample(range(0,len(all_edge_pairs)),10)
    
    E = sample(all_edge_pairs,m)

    #short_dist = shortest_path_floyd(n,E)
    '''
    weights = short_path_Bell_Ford(n,E)

    #--Modifying weights to eleminate negative edges if any
    for e in E:
        e[2] += weights[e[0]]-weights[e[1]]
    
    
    #--building dictionary to keep track of neighbours of each vertex
    #--for Dijkstra's algo
    ighbours = {}
    for i in range(0,n):
        neighbours[i] = []

    for e in E:
        neighbours[e[0]].append(e)
    '''
    
    return n,E


def user_input_graph():
    print "Enter the graph data : "
    V = map(int,raw_input().strip().split())
    E = []

    #reading edges
    for a0 in range(0,V[1]):
        e = map(int,raw_input().strip().split())
        e[0] = e[0]-1
        e[1] = e[1]-1
        E.append(e)

    return V[0],E


def file_read(filename):
    with open(filename) as fp:
        lines = fp.readlines()

    line0 = map(int,str(lines[0]).split())
    lines.pop(0)

    E = []
    for e in lines:
        x = map(int,str(e).split())
        E.append([x[0]-1,x[1]-1,x[2]])

    return line0[0],E 


'''
Used to generate plots
'''
def get_plot(plt,x1,y1,name):
    
    xy_sorted = sorted(zip(x1,y1))
    x = [a for a,b in xy_sorted]
    y = [b for a,b in xy_sorted]

    #print xy_sorted
    plt.plot(x,y,label=name)
    
    plt.xlabel("Edge count")
    plt.ylabel("Time consumed (in seconds)")
    plt.title("Time analysis")

    plt.legend()

    
if __name__ == "__main__":

    files = ["input1.txt","input2.txt","input3.txt"]
    vertex_count,edge_count,FloydWar_time,John_time = [],[],[],[]

    '''
    for a0 in range(len(files)):
        tup = file_read(files[a0])

        print "\n\nInput - ",files[a0]
        edge_count.append(len(tup[1]))
        
        start_time = datetime.now()
        sd = short_path_floyd(tup[0],tup[1])
        end_time = datetime.now()
        
        FloydWar_time.append((end_time - start_time).total_seconds())
        print "shortest distance path matrix by Floyd Warshall : "
        print sd

        start_time = datetime.now()
        sd = short_path_john(tup[0],tup[1])
        end_time = datetime.now()

        John_time.append((end_time - start_time).total_seconds())
        print "shortest distance path matrix by Johnson : "
        print sd

    get_plot(plt,edge_count,FloydWar_time,"Floyd-Warshall")
    get_plot(plt,edge_count,John_time,"Johnson")
    plt.show()
    
    
    '''
    #Calculate average time taken on random graphs
    nm_pair = get_n_m_pair()
    tmp_fw_time,tmp_john_time = [],[]
    
    for a0 in range(0,10):
        vertex_count.append(nm_pair[a0][0][0])
        
        for b0 in range(0,10):
            
            tup = random_input_graph(nm_pair[a0][b0][0],nm_pair[a0][b0][1])
            
            start_time = datetime.now()
            sd = short_path_floyd(tup[0],tup[1])
            end_time = datetime.now()
            
            tmp_fw_time.append((end_time - start_time).total_seconds())
            #print sd

            start_time = datetime.now()
            sd = short_path_john(tup[0],tup[1])
            end_time = datetime.now()

            tmp_john_time.append((end_time - start_time).total_seconds())
            
        FloydWar_time.append(sum(tmp_fw_time)/10.0)
        John_time.append(sum(tmp_john_time)/10.0)

        
    get_plot(plt,vertex_count,FloydWar_time,"Floyd-Warshall")
    get_plot(plt,vertex_count,John_time,"Johnson")
    plt.show()
    

    
