import file_generator
import os

def main():
    # Get the directory where main.py is located
    main_py_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the project root
    project_root = os.path.dirname(main_py_dir)
    
    # Build absolute paths from project root
    content_path = os.path.join(project_root, 'content')
    public_path = os.path.join(project_root, 'public')
    template_path = os.path.join(project_root, 'template.html')
    static_path = os.path.join(project_root, 'static')

    # Recursively generate md files into html using template into public
    file_generator.build_html_from_md(
        origin_fp=content_path,
        template_path=template_path,
        dest_fp=static_path
    )

    # Delete public tree, recreating it with items from static
    file_generator.clone_filestructure(
        from_path=static_path,
        to_path=public_path
    )
        

main()
