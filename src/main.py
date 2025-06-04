import generate_files
import os

def main():
    # Get the directory where main.py is located
    main_py_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the project root
    project_root = os.path.dirname(main_py_dir)
    
    # Build absolute paths from project root
    content_path = os.path.join(project_root, 'content', 'index.md')
    template_path = os.path.join(project_root, 'template.html')
    output_path = os.path.join(project_root, 'public', 'index.html')
    
    generate_files.public_generator()
    generate_files.generate_page(
        content_path,
        template_path,
        output_path
    )

main()
