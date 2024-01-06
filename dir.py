import os

# Define the structure of your Flask app
app_structure = {
    'static': {
        'css': ['style.css'],
        'js': ['script.js']
    },
    'templates': ['index.html'],
    'app.py': None,
    'requirements.txt': None,
    'Procfile': None
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # Create a directory
            os.makedirs(path, exist_ok=True)
            # Recursively create files/directories within
            create_structure(path, content)
        elif isinstance(content, list):
            # Create multiple files in this directory
            for file_name in content:
                file_path = os.path.join(path, file_name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                open(file_path, 'a').close()
        else:
            # Create a single file
            file_path = os.path.join(base_path, name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            open(file_path, 'a').close()

# Use the current directory as the base
current_directory = os.getcwd()
create_structure(current_directory, app_structure)

print("Flask app structure created successfully inside 'dalle3' directory.")
