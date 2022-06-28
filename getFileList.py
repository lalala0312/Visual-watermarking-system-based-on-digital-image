# -*- coding: utf-8 -*-
# @Time : 2022/6/26 17:43
import os
import cv2


class getFileList(object):
    def getList(self, dir, Filelist, ext=None):
        """
        获取文件夹及其子文件夹中文件列表
        :param dir: 文件夹根目录
        :param Filelist: 文件列表(用于存储)
        :param ext: 扩展名
        :return: 文件路径列表
        """
        newDir = dir
        if os.path.isfile(dir):
            if ext is None:
                Filelist.append(dir)
            else:
                if ext in dir[-3:]:
                    Filelist.append(dir)

        elif os.path.isdir(dir):
            for s in os.listdir(dir):
                newDir = os.path.join(dir, s)
                self.getList(newDir, Filelist, ext)

        return Filelist


if __name__ == '__main__':
    org_img_folder = './'  # 图片文件夹的路径
    test = getFileList()
    # 检索文件
    imglist = test.getList(org_img_folder, [], 'png')
    print('本次执行检索到 ' + str(len(imglist)) + ' 张图像\n')

    print(imglist)

    for imgpath in imglist:
        imgname = os.path.splitext(os.path.basename(imgpath))[0]
        print(imgname)
        img = cv2.imread(imgpath)
        # 对每幅图像执行相关操作