import os
def get_parent_abs(file):
    return os.path.abspath(os.path.join(file, "../"))