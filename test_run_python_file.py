from functions.run_python import run_python_file

print(run_python_file("calculator", "main.py"), '\n')
print(run_python_file("calculator", "main.py", ["3 + 5"]), '\n')
print(run_python_file("calculator", "tests.py"), '\n')
print(run_python_file("calculator", "../main.py"), '\n')
print(run_python_file("calculator", "nonexistent.py"), '\n')
print(run_python_file("calculator", "lorem.txt"), '\n')