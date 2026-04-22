#open file and read its contents
file = open('Codingal.txt','r')
print(file.read())
file.close()

#open file and read its beginning 8 characters
file = open('Codingal.txt','r')
print("\n Read in parts \n")
print(file.read(8))
file.close()

#append your name and age in the file
file = open('Codingal.txt','a')
file.write(" Hi! I am Penguin and I am 1 yr old.")
file.close()
