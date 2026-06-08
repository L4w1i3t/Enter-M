# python script to take a file as an input (relative to this script's location) and remove all empty lines from it, then save the result to a new file with the same name but with "_noempty" appended before the file extension.
import os
def remove_empty_lines(file_path):
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return

    # Read the file and remove empty lines
    with open(file_path, 'r') as file:
        lines = file.readlines()
        non_empty_lines = [line for line in lines if line.strip() != '']

    # Create the new file name
    base, ext = os.path.splitext(file_path)
    new_file_path = f"{base}_noempty{ext}"

    # Write the non-empty lines to the new file
    with open(new_file_path, 'w') as new_file:
        new_file.writelines(non_empty_lines)

    print(f"Empty lines removed. New file saved as {new_file_path}")
if __name__ == "__main__":    # Example usage: remove_empty_lines('input.txt')
    while True:
        whichone = input("Do you want to process a single file or a directory? (file/directory): ").strip().lower()
        if whichone == 'file':
            file_name = input("Enter the relative path of the file to process: ")
        elif whichone == 'directory':
            directory = input("Enter the relative path of the directory to process (leave blank to skip, type './' for root): ")
        else:
            print("Invalid option. Please choose 'file' or 'directory'.")
            continue

        if whichone == 'file':
            remove_empty_lines(file_name)
        elif whichone == 'directory':
            if not os.path.isdir(directory):
                print(f"Directory {directory} does not exist.")
                continue
            for root, _, files in os.walk(directory):
                for file in files:
                    # ignore this script itself to prevent infinite loop
                    if file == os.path.basename(__file__):
                        continue
                    file_path = os.path.join(root, file)
                    remove_empty_lines(file_path)