def clean():
    file_path_to_read = "sql_to_use.txt"
    file_path_to_write = "sql_cleaned.txt"

    with open(file_path_to_read, 'r') as file:
        lines = file.readlines()
        
    filtered_lines = [line for line in lines if not line.strip().startswith("```")]

    with open(file_path_to_write, 'w') as file:
        file.writelines(filtered_lines)