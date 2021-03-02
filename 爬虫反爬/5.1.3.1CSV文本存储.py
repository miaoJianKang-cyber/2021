# coding:utf-8
import csv

with open('data.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'name', 'age'])
    writer.writerow(['1001', 'name', 'age'])
    writer.writerow(['1002', 'name', 'age'])
    writer.writerow(['1003', 'name', 'age'])

with open('data.csv','r',encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)