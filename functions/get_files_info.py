import os

def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        if not os.path.isdir(os.path.join(working_directory, directory)):
            return f'Error: "{directory}" is not a directory'

        working_dir_abs_path = os.path.abspath(working_directory)
        full_path_target_dir = os.path.normpath(os.path.join(working_dir_abs_path, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs_path,full_path_target_dir]) == working_dir_abs_path

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        else:
            files_info = []
            for entry in os.listdir(full_path_target_dir):
                entry_path = os.path.join(full_path_target_dir, entry)
                size = os.path.getsize(entry_path)
                files_info.append(f"{entry}: file_size={size} bytes, is_dir={os.path.isdir(entry_path)}")
            return "\n".join(files_info) if files_info else "No files found in the directory."
        
    except Exception as e:
        return f"Error: {str(e)}"