import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

import cv2
import numpy as np

from admin.views import admin


TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template')


class BoxImage:
    """Box图像识别类"""
    def __init__(self, *, image=None, src=None, threshold=0.8, max_workers=5):
        """
        :param image: cv图像对象
        :param src: 图像文件路径，非None则忽略image
        :param threshold: 图像匹配置信度
        :param max_workers: 最多线程数
        """
        if image is not None:
            self.__pretreat(image)
        elif src is not None:
            self.read(src)
        self.threshold = threshold
        self.max_workers = max_workers
        self.read_template()
    
    def read(self, src):
        """从文件读入图像"""
        image = cv2.imread(src)
        self.__pretreat(image)

    def __pretreat(self, image):
        """图像预处理"""
        h, w = image.shape[:2]
        self.__image = cv2.resize(image, (int(735/h*w) ,735))
        self.__image_gray = cv2.cvtColor(self.__image, cv2.COLOR_BGR2GRAY)
    
    def read_template(self):
        """读入模板"""
        self.__character_images = []
        self.__number_images = []

        with open(os.path.join(TEMPLATE_PATH, 'template.json'), 'r', encoding='utf8') as f:
            template_info = json.loads(f.read())

        # 读入角色头像
        for item in template_info['characters']:
            name = item['name']
            for i in item['images']:
                image = cv2.imread(os.path.join(TEMPLATE_PATH, i), 0)
                self.__character_images.append((
                    name,
                    cv2.resize(image, (64, 64)),
                ))
        
        # 读入数字
        for item in template_info['numbers']:
            value = item['value']
            image = cv2.imread(os.path.join(TEMPLATE_PATH, item["image"]), 0)
            self.__number_images.append((
                    value,
                    image
                ))

        # 读入RANK
        self.__rank_image = cv2.imread(os.path.join(TEMPLATE_PATH, template_info["rank"]), 0)

    @property
    def characters(self):
        """识别图像"""
        characters_list = []
        if self.__image_gray is None:
            raise ValueError('未载入图像')
        with ThreadPoolExecutor(max_workers=self.max_workers) as t:
            thread_list = []
            for (name, image) in self.__character_images:
                thread = t.submit(self.character, image, name)
                thread_list.append(thread)
            for future in as_completed(thread_list):
                result = future.result()
                if result is not None:
                    characters_list.append(result)
        return characters_list

    def character(self, image, name):
        res = self.__character(image)
        if res is None: return None
        # 剪裁图片
        if res[0]-32 < 0 or res[1]-32 < 0: return None
        image_cut = self.__image[res[0]-32:res[0]+96, res[1]-32:res[1]+96]
        if image_cut.shape[0] < 128 or image_cut.shape[1] < 128: return None
        star = self.__star(image_cut)
        rank = self.__rank(image_cut)
        return {
                'name': name,
                'star': star,
                'rank': rank
            }

    def __character(self, image):
        """识别角色"""
        res = cv2.matchTemplate(self.__image_gray, image, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= self.threshold)
        try:
            return next(zip(*loc))
        except StopIteration:
            return None

    def __star(self, image):
        """识别星级"""
        for x in range(5):
            b, g, r = image[115, 16*(x+1)]
            if b < 75 or b > 115 \
                    or g < 180 or g > 220 \
                    or r < 215 or r > 255:
                break
        else: x += 1
        return x

    def __rank(self, image):
        """识别RANK"""
        image = cv2.cvtColor(image[:25], cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(image, self.__rank_image, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.87)
        if len(loc[0]) == 0:
            return 0
        numbers = {}
        for item in self.__number_images:
            res = cv2.matchTemplate(image, item[1], cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= 0.87)
            numbers[item[0]] = loc

        res = []
        # 合并x差小于5的结果
        for key in numbers:
            x = list(numbers[key][1])
            l = []
            while len(x) != 0:
                t = x.pop()
                if len(l) == 0 or t - l[0] > 5:
                    l.append(t)
            if len(l) > 0:
                for i in l:
                    res.append((key, i))
        # 位置排序
        res.sort(key=lambda x: x[1])
        
        rank = 0
        for i in res:
            rank = rank * 10 + i[0]
        
        return rank
