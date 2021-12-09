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
        
        if distance(point,i) <= i[2]:
            #if point is within radius distance of any obstacle, return 'not free'
            decision = False   
            break

    return decision

def neighborC(point,Cfree):
    #returns neighborlist for point in Cfree
    #neighbors required to  be closer than 0.25
    nbrlist =[]
    for i in Cfree:
        if i != point:
            if distance(point,i) <=0.25:
                nbrlist.append(i)
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
points=[]

#randomly select points from C-space
for i in range(100):
    x = round((rd.random()-0.5),3)
    y = round((rd.random()-0.5),3)
    points.append([x,y])
    print([x,y])


#check if any of these points lie in C-free or not
obstacle = [ [0, 0, 0.2], [0, 0.1, 0.2], [0.3, 0.2, 0.2], [-0.3, -0.2, 0.2], [-0.1,-0.4,0.2],[-0.2,0.3,0.2],[0.3,-0.3,0.2],[0.1,0.4,0.2]]
C_free_points=[startp]
for p in points:
    if free_point(p,obstacle) == True:
        C_free_points.append(p)
C_free_points.append(goalp)        
print(C_free_points)


#fill free Cspace points into nodes list
nodes  = []
for i in range(len(C_free_points)):
    nodes.append([i+1,C_free_points[i][0],C_free_points[i][1],distance(startp,C_free_points[i])])
    
print("nodes number")
print(nodes)
#write  this nodes into nodes1 csv
with open('nodes1.csv', 'w', newline='') as fileh:###write edges into csv
    writer = csv.writer(fileh)
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
            edges.append([nump,nume,distance(p,member)])
            
print("edges")
print(edges)

with open('edges1.csv', 'w', newline='') as fileh:###write edges into csv
    writer = csv.writer(fileh)
    for i in edges:
        writer.writerow(i)
