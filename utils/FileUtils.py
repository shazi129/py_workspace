# -*- coding: utf-8 -*-
import os
import shutil

class FileCheckParam:
    def __init__(self, **kwargs):
        self.exclude_extends = () #排除文件的后缀名
        self.exclude_paths = () #排除路径
        self.exclude_pattern = [] #排除的正则表达，影响效率，尽量少用

    def add_exclude_ext(self, ext_list):
        cur_exts = list(self.exclude_extends)
        cur_exts.extend(ext_list)
        self.exclude_extends = tuple(cur_exts)

    def check_file(self, file):
        if (file.endswith(self.exclude_extends)):
            return False
        return True


"""
拷贝文件
src 源路径
dest 目标路径
copy_param FileCheckParam
"""
def copy_files(src, dest, copy_param):

    if copy_param == null:
        
    #创建目标文件夹
    if not os.path.isdir(dest):
        os.makedirs(dir)

    #如果是拷贝文件
    if os.path.isfile(src):
        src_filename = os.path.basename(src)
        shutil.copy(src, "%s/%s" % (dest, src_filename))


if __name__ == "__main__":
    check_param = FileCheckParam()
    check_param.add_exclude_ext([".pdb"])
    print(check_param.check_file("C:/a.pdb"))