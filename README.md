# scalpel



a Python script that helps you quickly understand the structure and contents of an unknown project. It generates a structured representation of the project's files and extracts relevant data from important files, providing a solid foundation for further analysis and exploration.

## Features

- Automatically scans the project directory and generates a JSON file (`structure.json`) representing the project's file structure.
- Extracts important file data, including file contents, functions (for Python files), and classes (for Python files), and saves it to a text file (`extracted_data.txt`).
- Supports a wide range of file extensions and important file names commonly found in various programming languages and frameworks.
- Saves the generated files in the same directory as the script for easy access.

## Usage

1. Clone the repository or download the script file.
2. Run the script using the command: `python project_scraper.py`.
3. A folder selection dialog will appear. Select the root folder of the project you want to scan. ( for level selection choose 1 or 2 they are slmost the same at this point) 
4. The script will generate the project structure and extract important file data.
5. Once the process is complete, you will find the generated files (`structure.json` and `extracted_data.txt`) in the same directory as the script.

## Output

The script generates two files:

1. `structure.json`: A JSON file representing the project's file structure. It includes the relative paths of directories and important files.
2. `extracted_data.txt`: A text file containing the extracted data from important files. It includes file paths, contents, functions (for Python files), and classes (for Python files).

Note: If the script encounters any files that cannot be scraped or omitted during the process, the `structure.json` file will still contain information about those files, ensuring a comprehensive representation of the project structure.

## Customization

You can customize the script to suit your specific needs:

- Modify the `important_extensions` and `important_file_names` lists to include additional file extensions and names relevant to your project.
- Enhance the file content extraction process to handle different file types and extract relevant information based on the file extension or content.
- Integrate with additional analysis techniques or tools to gain deeper insights into the project's structure and functionality.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request on the GitHub repository.
