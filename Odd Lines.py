# Program to copy odd lines of one file to another
# open file in read mode
fn = open('Codingal.txt', 'r')

# open other file in write mode
fn1 = open('CodingalUpdated.txt', 'w')

# read the content of the file line by line
cont = fn.readlines()
type(cont)
for i in range(1, len(cont)+1):
if(i % 2 != 0):
fn1.write(cont[i-1])
else:
pass

# close the file
fn1.close()

# open file in read mode
fn1 = open('CodingalUpdated.txt', 'r')

# read the content of the file
cont1 = fn1.read()

# print the content of the file
print(cont1)

# close all files
fn.close()
fn1.close()

