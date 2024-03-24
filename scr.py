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

    if not os.path.exists(structure_file):
        print(f"❌ Error: structure.json file not found in the script directory.")
        return

    depth_level = int(input("Enter the depth level (1 or 2): "))

    with open(structure_file, 'r', encoding='utf-8') as file:
        structure_data = json.load(file)

    extracted_data = scrape_important_files(structure_data, project_root_folder, depth_level)
    save_extracted_data(extracted_data, output_file)

    print(f"✅ Extracted data saved to: {output_file}")

if __name__ == '__main__':
    main()
