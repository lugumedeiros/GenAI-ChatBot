from functions.create_files import write_file

print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"), '\n')
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"), '\n')
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"), '\n')
pass