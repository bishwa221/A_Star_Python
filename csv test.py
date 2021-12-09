import csv
go=[[1,2,3],[4,5,6]]
with open('pakoda3.csv', 'w', newline='') as filep:###write path into csv
    writer = csv.writer(filep)
    for i in go:
        writer.writerow(i)
