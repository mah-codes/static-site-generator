import os
import shutil
import re

from md_processing import markdown_to_html_node

# Crawl through content_path, creating HTML's based on MarkDown files in public_path
# use the SAME file-structure

# Delete the public tree
# then from static, recreate the public tree

def clone_filestructure(from_path, to_path, basepath):
    # Delete public/
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    os.mkdir(to_path)
    # Generate from static/
    file_paths = build_html_from_md(from_path, "", to_path, basepath)
    print("files successfully copied to", to_path)

def create_public_files(from_path, to_path):
    filepaths = []
    dirs = os.scandir(from_path)
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

def build_html_from_md(origin_fp, template_path, dest_fp, basepath):
    filepaths = []
    dirs = os.scandir(origin_fp)
    for item in dirs:
        next_dest_fp = f"{dest_fp}/{item.name}"
        if item.is_file():
            # Check if path/dir exists in destination
            print("-- checking if dest-path exists:", dest_fp)
            prep_filepath(next_dest_fp)
            # if Markdown file, need static version to be HTML based on template
            if re.search(r"\w+\.(md)", item.name) is not None: 
                # print("Generating HTML", item.path)
                generate_page(item.path, template_path, next_dest_fp, basepath)
            # If it's some other content (just needing a cp command)
            else: 
                shutil.copy(item.path, next_dest_fp)
            filepaths.append(item.path)
        elif item.is_dir():
            # Recursive element, passing it updated dest_fp
            filepaths.extend(build_html_from_md(
                item.path,
                template_path,
                next_dest_fp,
                basepath
            ))
    return filepaths

def extract_title(markdown_file):
    with open(markdown_file, "r") as file:
        markdown = file.read()
    for line in markdown.split("\n"):
        if line.strip().startswith("#"):
            return line.strip()[1:].strip()
    raise Exception("No title found in markdown file")
    
def generate_page(from_path, template_path, dest_path, basepath):
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
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')


    prep_filepath(dest_path)
    # Change extension from .md to .html
    dest_path = dest_path[:-2] + "html"
    with open(dest_path, 'w') as dest_file:
        dest_file.write(page)

def prep_filepath(tgt_path):
    """Takes an absolute path, creating directories as needed"""
    # Get the directory path, removing the filename if present
    dir_path = os.path.dirname(tgt_path)
    
    # Create directories if they don't exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        print(f"\nCreated directory: {dir_path}")
    else:
        print(f"\nDirectory exists: {dir_path}")
