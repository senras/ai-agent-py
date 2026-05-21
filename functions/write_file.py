import os

def write_file(working_directory: str, file_path: str, content: str) -> str:

    working_dir_abs_path = os.path.abspath(working_directory)
    full_path_target_dir = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs_path,full_path_target_dir]) == working_dir_abs_path

    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(full_path_target_dir):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    parent_dir = os.path.dirname(full_path_target_dir)
    os.makedirs(parent_dir, exist_ok=True)

    try:
        with open(full_path_target_dir, 'w', encoding='utf-8') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"