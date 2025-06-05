import os
import shutil
from md_processing import markdown_to_html_node
# Remembering, this will be called from main.py
def public_generator():
    # Delete public
    fp_public = os.path.abspath("./public/")
    if os.path.exists(fp_public):
        shutil.rmtree(fp_public)
    os.mkdir(fp_public)
    # copy from static
    copy_path = os.path.abspath("./static/")
    file_paths = create_public_files(copy_path)
    print("files successfully copied to", fp_public)

def create_public_files(fp):
    filepaths = []
    dirs = os.scandir(fp)
    for item in dirs:
        full_fp = item.path
        if not item.is_dir():
            # based on static path, create a directory string for static
            static_dir_path = item.path[:-len(item.name)]
            public_dir_path = static_dir_path.replace("/static/", "/public/")
            # Check if path/dir exists in public
            if not os.path.exists(public_dir_path):
                os.mkdir(public_dir_path)
            shutil.copy(item.path, f"{public_dir_path}/{item.name}")
            filepaths.append(full_fp)
        else:
            filepaths.extend(create_public_files(full_fp))
    return filepaths

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path}")
    print(f"Generated with template {template_path}")
    with open(from_path, 'r') as content_file:
        content = content_file.read()
    with open(template_path, 'r') as template_file:
        template = template_file.read()

    # Take content and generate HTML string
    html_node = markdown_to_html_node(content)
    content_html_string = html_node.to_html()

    title = extract_title(from_path)
    page = template.replace("{{ Content }}", content_html_string)
    page = page.replace("{{ Title }}", title)

    prep_filepath(dest_path)
    with open(dest_path, 'w') as dest_file:
        dest_file.write(page)

def extract_title(markdown_file):
    with open(markdown_file, "r") as file:
        markdown = file.read()
    for line in markdown.split("\n"):
        if line.strip().startswith("#"):
            return line.strip()[1:].strip()
    raise Exception("No title found in markdown file")
    

def prep_filepath(tgt_path):
    """Takes an absolute path, creating directories as needed"""
    # Break down path to list (regex? or os lib?)
    path_so_far = ""
    path_list = tgt_path.split("/")
    # Check if tgt_path indicates a file, removing it from scope of this fn
    if "." in path_list[-1]:
        path_list = path_list[:-1]

    if not os.path.exists(tgt_path):
        # start from index 1 below, assuming "root" already exists
        for dir in path_list[1:]:
            path_so_far = os.path.join(path_so_far, dir)
            if not os.path.exists(path_so_far):
                os.mkdir(path_so_far)
