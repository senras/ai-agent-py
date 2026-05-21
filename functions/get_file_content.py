import os

def get_file_content(working_directory: str, file_path: str) -> str:

    working_dir_abs_path = os.path.abspath(working_directory)
    full_path_target_dir = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs_path,full_path_target_dir]) == working_dir_abs_path

    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(full_path_target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(full_path_target_dir, 'r', encoding='utf-8') as f:
            content = f.read(10000)
            if f.read(1):
                content += f'[File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f"Error: {str(e)}"