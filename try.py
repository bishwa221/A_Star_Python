import random as rd
for yt in range(-500,500,100):
    for xt in range(-500,500,100):
        for i in range(6):
            x = round(rd.randrange(xt,xt+100)*0.001,3)
            y = round(rd.randrange(yt,yt+100)*0.001,3)
            print(x,y)
