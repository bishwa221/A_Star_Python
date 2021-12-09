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
    if ("4" and "7") not in[line.strip().split(',')]:
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
            
        
