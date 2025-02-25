path = r"Uni-Courses\Data Mining\Python\File Handling\content.txt"

file = open(path, 'r')
x = file.read()
file.close()

x = x.upper() # HELLO

file = open(path, 'w')
file.write(x)
file.close()