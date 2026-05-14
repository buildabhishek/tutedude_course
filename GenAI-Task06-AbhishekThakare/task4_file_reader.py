# This program demonstrates file reading with exception handling

try:
    file_name = input("Enter file name: ")

    file = open(file_name, "r")

    lines = file.readlines()

    print("First 3 lines of the file:")

    for line in lines[:3]:
        print(line.strip())

    file.close()

except FileNotFoundError:
    print("Error: File not found")

except PermissionError:
    print("Error: Permission denied")

finally:
    print("File operation attempted")
