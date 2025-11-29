import json
import os
import binascii

# Read Magic Numbers of a file
def read_magic_numbers_of_file(file_path, byte_count=16):
    try:
        with open(file_path, "rb") as file:
            header = file.read(byte_count)
            return binascii.hexlify(header).upper().decode()
    except FileNotFoundError:
        print("No such file or directory:", file_path)
        return None

# Load default magic numbers
def load_magic_numbers():
    try:
        with open("magic_numbers.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Load default magic numbers first!")
        return None
    except json.JSONDecodeError:
        print("Error decoding magic numbers JSON!")
        return None

# Identify file type by its magic numbers
def identify_file_type(file_path, magic_db):
    if magic_db is None:
        return "Unknown File Type"

    file_header = read_magic_numbers_of_file(file_path)
    if file_header is None:
        return None

    for file_type, signature in magic_db.items():
        # Allow list of signatures if needed
        if isinstance(signature, list):
            for sig in signature:
                if file_header.startswith(sig.upper()):
                    return file_type
        else:
            if file_header.startswith(signature.upper()):
                return file_type

    return "Unknown File Type"

# Logging / user prompt loop
def log(magic_db):
    while True:
        file_type = None
        file_path = None
        print("\n0 - exit")
        while file_type is None:
            file_path = input("Enter File Path: ")
            if file_path == "0":
                print("Exiting program...!")
                return
            file_type = identify_file_type(file_path, magic_db)

        file_name = os.path.basename(file_path)  # safer than manual string slicing
        print("Received File:", file_name)
        print("Type:", file_type)
        print()

def main():
    print("=== Magic Number File Identifier ===\n")
    magic_db = load_magic_numbers()
    if magic_db is None:
        print("No magic numbers loaded. Exiting program.")
        return

    log(magic_db)

if __name__ == "__main__":
    main()
