import os
import json
import ast
from tkinter import Tk, filedialog

def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {file_path}")
        print(f"Error: {str(e)}")
        return None

def extract_functions(file_content):
    try:
        tree = ast.parse(file_content)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return functions
    except SyntaxError:
        return []

def extract_classes(file_content):
    try:
        tree = ast.parse(file_content)
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        return classes
    except SyntaxError:
        return []

def generate_structure(source_dir, extensions, file_names):
    structure = {}
    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        important_files = [
            f for f in files
            if any(f.endswith(ext) for ext in extensions) or f in file_names
        ]
        if important_files:
            structure[relative_path] = {
                "important_files": important_files
            }
        for dir_name in dirs:
            if any(dir_name.startswith(prefix) for prefix in [".", "_"]):
                dir_path = os.path.join(root, dir_name)
                relative_dir_path = os.path.relpath(dir_path, source_dir)
                structure[relative_dir_path] = {
                    "important_files": []
                }
    return structure

def save_to_json(structure, filename):
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(structure, outfile, indent=2)

def scrape_important_files(structure_data, base_path, depth_level):
    extracted_data = {}
    for relative_path, data in structure_data.items():
        important_files = data.get('important_files', [])
        for file_name in important_files:
            file_path = os.path.join(base_path, relative_path, file_name)
            file_content = read_file_content(file_path)
            if file_content is not None:
                extracted_data[file_path] = {
                    'content': file_content
                }
                if depth_level >= 2:
                    # Level 2: Extract additional information about the file
                    functions = extract_functions(file_content)
                    classes = extract_classes(file_content)
                    extracted_data[file_path]['functions'] = functions
                    extracted_data[file_path]['classes'] = classes
    return extracted_data

def save_extracted_data(extracted_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for file_path, data in extracted_data.items():
            file.write(f"File: {file_path}\n")
            file.write(f"Content:\n{data['content']}\n")
            if 'functions' in data:
                file.write(f"Functions: {', '.join(data['functions'])}\n")
            if 'classes' in data:
                file.write(f"Classes: {', '.join(data['classes'])}\n")
            file.write("-" * 80 + "\n")

def main():
    print("🔍 Important File Scraper")
    print("Select the root folder of the project to be scanned.")

    # Open a folder selection dialog for the project root folder
    root = Tk()
    root.withdraw()
    project_root_folder = filedialog.askdirectory(title="Select the root folder of the project")

    if not project_root_folder:
        print("❌ No folder selected. Exiting.")
        return

    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    structure_file = os.path.join(script_dir, 'structure.json')
    output_file = os.path.join(script_dir, 'extracted_data.txt')

    important_extensions = [
        '.py', '.js', '.html', '.css', '.json', '.yml', '.yaml', '.csv', '.xlsx',
        '.txt', '.md', '.rst', '.ini', '.cfg', '.toml', '.xml', '.sql',
        '.sh', '.bat', '.cmd', '.ps1', '.rb', '.java', '.cpp', '.c', '.h',
        '.cs', '.ts', '.dart', '.kt', '.swift', '.go', '.php', '.pl', '.scala',
        '.r', '.lua', '.perl', '.lisp', '.hs', '.clj', '.erl', '.ex',
        '.vim', '.emacs', '.org', '.tex', '.bib', '.cls', '.sty',
        '.vim', '.zsh', '.bash', '.fish', '.gitignore', '.dockerignore',
        '.env', '.env.example', '.envrc', '.editorconfig', '.eslintrc',
        '.flake8', '.pylintrc', '.pypirc', '.babelrc', '.jshintrc',
        '.npmignore', '.htaccess', '.conf', '.cfg', '.ini', '.properties',
        '.gradle', '.m', '.mm', '.proto', '.rs', '.graphql', '.sol',
        '.asm', '.wat', '.wasm'
    ]
    important_file_names = [
        'README', 'LICENSE', 'CONTRIBUTING', 'CHANGELOG', 'MANIFEST',
        'setup.py', 'requirements.txt', 'pyproject.toml', 'poetry.lock',
        'package.json', 'package-lock.json', 'yarn.lock', 'Gemfile', 'Gemfile.lock',
        'Cargo.toml', 'Cargo.lock', 'build.gradle', 'pom.xml', 'build.sbt',
        'project.clj', 'project.scm', 'Makefile', 'Dockerfile', 'docker-compose.yml',
        '.gitignore', '.gitattributes', '.gitmodules', '.npmrc', '.yarnrc',
        'jest.config.js', 'tsconfig.json', 'tslint.json', '.babelrc', '.eslintrc',
        '.prettierrc', '.stylelintrc', 'webpack.config.js', 'gulpfile.js',
        'gruntfile.js', 'netlify.toml', 'vercel.json', 'now.json', '.travis.yml',
        '.circleci', 'appveyor.yml', 'Jenkinsfile', 'Procfile', 'Pipfile', 'Pipfile.lock',
        'config.yml', 'mkdocs.yml', 'spec.yml', 'swagger.yml', 'serverless.yml'
    ]

    print("🔎 Generating structure for directory: {}".format(project_root_folder))
    project_structure = generate_structure(project_root_folder, important_extensions, important_file_names)
    save_to_json(project_structure, structure_file)
    print("✅ Structure file created: {}".format(structure_file))
    print("All done! The important files have been found. 😄")

    depth_level = int(input("Enter the depth level (1 or 2): "))
    extracted_data = scrape_important_files(project_structure, project_root_folder, depth_level)
    save_extracted_data(extracted_data, output_file)
    print(f"✅ Extracted data saved to: {output_file}")

if __name__ == '__main__':
    main()
