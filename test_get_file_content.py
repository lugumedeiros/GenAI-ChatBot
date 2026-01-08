from functions.get_file_content import get_file_content

# print (get_file_content("calculator", "lorem.txt"), '\n')
print(get_file_content("calculator", "main.py"), "\n")
print(get_file_content("calculator", "pkg/calculator.py"), "\n")
print(get_file_content("calculator", "/bin/cat"), "\n")
print(get_file_content("calculator", "pkg/does_not_exist.py"), "\n")