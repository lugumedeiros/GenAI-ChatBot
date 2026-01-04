from functions.get_files_info import get_files_info

test_a = get_files_info("calculator", ".")
print(test_a, "\n")
test_b = get_files_info("calculator", "pkg")
print(test_b, "\n")
test_c = get_files_info("calculator", "/bin")
print(test_c, "\n")
test_d = get_files_info("calculator", "../")
print(test_d, "\n")