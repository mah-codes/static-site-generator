import os
import shutil
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