def distance(p1,p2):
    #returns euclidean distance between p1 and p2
    dist  =  ( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )**0.5
    return round(dist,3)
    
def free_point(point,obs):
    #pass the obstacle list and point for inquiry
    #returns True is the point is in free Cspace
    #else returns False
    decision = True
    for i in obs :
        
        if distance(point,i) <= (i[2]/2):
            #if point is within radius distance of any obstacle, return 'not free''''0.475
            decision = False   
            break

    return decision

def neighborC(point,Cfree):
    #returns neighborlist for point in Cfree
    #neighbors required to  be closer than 0.13
    nbrlist =[]
    for i in Cfree:
        if i != point and len(nbrlist)<5:
            if distance(point,i)<0.13:
                nbrlist.append(i)
        else:
            break
    return nbrlist


def clearpath(point1,point2,obst):
    #returns True if free path exist between point1 and point 2
    #else returns false
    d   =  True
    x1  =  point1[0]
    x2  = point2[0]
    y1 =  point1[1]
    y2 =  point2[1]
    xlist=[x1,x2]
    ylist=[y1,y2]
    m =  1
    #internally divide the segment(x1,y1) to (x2,y2)
    #using different m and n and get division points
    while m <= 9:
        n = 10 - m
        x = round(((m*x2)+(n*x1))/(m+n),3)
        y = round(((m*y2)+(n*y1))/(m+n),3)
        xlist.append(x)
        ylist.append(y)
        m =  m+1
    for i in range(len(xlist)):
        #check if each division point is collision-free by calling free_point
        if free_point([xlist[i],ylist[i]],obst) == False:
            d = False
            break
    return d  




import random as rd
import csv
startp =  [-0.5,-0.5]
goalp =  [0.5,0.5]
points=[startp]
C_free_points=[startp]

#obstacle copied from csv file as list. The method is used for nodes1.csv and edges1.csv
obstacle = [ [0.3, 0.2, 0.2], [-0.3, -0.2, 0.2], [-0.1,-0.4,0.2],[-0.2,0.3,0.2],[0.3,-0.3,0.2],[0.1,0.4,0.2],[0,0,0.2],[0,0.1,0.2]]


#randomly select points from C-space
#check if any of these points lie in C-free or not
for yt in range(-500,500,100):
    for xt in range(-500,500,100):
        
        x=round((xt+xt+100)*0.001/2,3)
        y=round((yt+yt+100)*0.001/2,3)
        p=[x,y]
        if [x,y] not in C_free_points and (free_point(p,obstacle) == True):
            C_free_points.append([x,y])
            print([x,y])

C_free_points.append(goalp)              
          



#fill free Cspace points into nodes list
nodes  = []
for i in range(len(C_free_points)):
    
    nodes.append([i+1,C_free_points[i][0],C_free_points[i][1],distance(goalp,C_free_points[i])])
    
print("nodes number")
print(nodes)
#write  this nodes into nodes1 csv
with open('nodes1.csv', 'w', newline='') as fileg:###write nodes into csv
    writer = csv.writer(fileg)
    for i in nodes:
        writer.writerow(i)

edges =  []
#get neighbour for each point in C_free_points
for p in  C_free_points:
    nump = C_free_points.index(p) + 1
    neighborlist = neighborC(p,C_free_points)
    for member in neighborlist:
        if clearpath(p,member,obstacle):
            #add path between p and member
            nume = C_free_points.index(member) +  1
            if  [nump,nume,distance(p,member)]  not in edges  and  [nume,nump,distance(p,member)]  not in edges:
                edges.append([nump,nume,distance(p,member)])
            
print("edges")
print(edges)

#write  this edges into edges1 csv
with open('edges1.csv', 'w', newline='') as fileh:###write edges into csv
    writer = csv.writer(fileh)
    for i in edges:
        writer.writerow(i)






##A-star
##        
def insertion_sort(nb,r,A):
    #A takes openlist
    #r takes est_total_cost list
    #nb takes neighbor it to be inserted
    A.append(nb)
    for i in range(len(A)):
        j = i
        while j > 0 and (r[A[j-1]] > r[A[j]]):
            (A[j],A[j-1])  = (A[j-1] , A[j])   
            j=j-1
    return A


def neighbor(n,refer):
    #checks node number in first or second column of edgelist. collects its eighors
    ret = [] #list of neighbors
    #refer = edgelist.
    for i in range(1,len(refer)):
        if refer[i][0] == n:
            ret.append(refer[i][1])
        elif refer[i][1] == n:
            ret.append(refer[i][0])
    return ret


def path(c,prt):
    #node  c has parent on parent list at index c
    #recursively  calls path  function until node 1 is not encountered
    if prt[c] == 1:
        return str(prt[c])
    else:
        return str(prt[c])+","+str(path(prt[c],prt))

    
def cost(a,b,rf):
    #returns cost from node a to node b looking at cost from edgelist
    #rf  =  edgelist
    for i in range(1,len(rf)):
        if rf[i][0] == a and rf[i][1]== b:
            return (rf[i][2])
        elif rf[i][1] == a and rf[i][0]== b:
            return (rf[i][2])


def reverse(d):#reverses a list
    new = []
    for i  in range(-1,-len(d)-1,-1):
        new.append(d[i])
    return  new





##PROGRAM STARTS FROM HERE. ABOVE ARE FUNCTION DEFINITIONS TO BE USED IN THE PROGRAM
#TO CHANGE START AND GOAL NODE,  CHANGE THE VALUE OF START AND GOAL  VARIABLE

import csv
#read data rows from nodes1 csv(the original "nodes" loaded as "nodes1")
#and write only the numeric data from "nodes1" into "nodes"
with open('nodes.csv', 'w', newline='') as file1:
    writer = csv.writer(file1)
    file = open("nodes1.csv")
    for line in file:
        if not line.startswith("#"):
            #print(line)
            writer.writerow(line.strip().split(','))




#read data rows from nodes1 csv(the "edges" loaded "edges1")
#and write only the numeric data from "edges" into "edges"               
with open('edges.csv', 'w', newline='') as file2:
    writer = csv.writer(file2)
    file = open("edges1.csv")
    for line in file:
        if not line.startswith("#"):
            #print(line)
            writer.writerow(line.strip().split(','))



#fill the list edge_list with edge data
edge_list=[[0,0,0]]
ed = open("edges.csv")
for line in ed:
    #if ("4" and "7") not in[line.strip().split(',')]:
    print([int(line.strip().split(',')[0]),int(line.strip().split(',')[1]),float(line.strip().split(',')[2])])
    edge_list.append([int(line.strip().split(',')[0]),int(line.strip().split(',')[1]),float(line.strip().split(',')[2])])
print(edge_list)



#fill the list node_list with node data
node_list=[[0,0,0,0]]
nd = open("nodes.csv")
for line in nd:
    print([int(line.strip().split(',')[0]),float(line.strip().split(',')[1]),float(line.strip().split(',')[2]),float(line.strip().split(',')[3])])
    node_list.append([int(line.strip().split(',')[0]),float(line.strip().split(',')[1]),float(line.strip().split(',')[2]),float(line.strip().split(',')[3])])
print(node_list)


start = 1######
openlist=[start]
#first element of pastcost = 0, the pastcost of node 1 ie index 1 is also zero.
pastcost=[0,0]
for i in range(2,len(node_list)):
    pastcost.append(9999)#infinity past cost for any other nodes accept node 1
print(pastcost)


current = []
closed=[]
goal = node_list[-1][0]######
heu_cost=[0]
est_total_cost=[0]
#fill  heu_cost and est_total_cost
for j in range(1,len(node_list)):
    heu_cost.append(node_list[j][3])
    est_total_cost.append(pastcost[j] + heu_cost[j])



parent = [1]#initialize all elements of list parent to 1
for i in range(1,len(node_list)):
    parent.append(1)

while openlist != []:  #actual algorithms given in book starts from here
    current = openlist[0]#rightmost element = first element of openlist
    openlist=openlist[1:]#removes current from openlost
    closed.append(current)#adds current to closed

    
    if current == goal:
        print ("Success")
        c=str(goal)+","+path(current,parent)#returns path to current
        d=c.split(',')#makes string   c into list d removing comma separator
        with open('path.csv', 'w', newline='') as filep:###write path into csv
            d= reverse(d)
            print(d)
            writer = csv.writer(filep)
            writer.writerow(d)
        
        break
    nbr = neighbor(current,edge_list)
    
    nbr_go=[]
    
    #make a list of nbr element not in closed
    for j in nbr:
        if j not in closed:
            nbr_go.append(j)
            
    for i in nbr_go:
        cs= cost(current,i,edge_list)
        #print(cs)
        tent_past_cost = pastcost[current]  +  cs  
        if   tent_past_cost < pastcost[i]:
            pastcost[i]  = tent_past_cost
            parent[i] = current
            est_total_cost[i] = pastcost[i] + heu_cost[i]
            #put i in sorted openlist according to est_total_cost
            openlist = insertion_sort(i,est_total_cost,openlist)#####write insertion_sort function
else:
    print("Failure")        
            
        
