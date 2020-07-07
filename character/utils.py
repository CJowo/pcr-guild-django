import os
import json

import cv2
import numpy as np

from admin.views import admin


TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template')


class BoxImage:
    __image = None
    __image_gray = None
    __character_images = []

    def __init__(self, *, image=None, src=None, threshold=0.8, client=None):
        if image is not None:
            self.__pretreat(image)
        elif src is not None:
            self.read(src)
        self.threshold = threshold
        self.client = client
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

    @property
    def characters(self):
        """识别图像"""
        characters_list = []
        if self.__image_gray is None:
            raise ValueError('未载入图像')
        for (name, image) in self.__character_images:
            res = self.__character(image)
            if res is None: continue
            # 剪裁图片
            image_cut = self.__image[res[0]-32:res[0]+96, res[1]-32:res[1]+96]
            star = self.__star(image_cut)
            rank = self.__rank(image_cut)
            characters_list.append({
                'name': name,
                'star': star,
                'rank': rank
            })
        return characters_list

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
        if self.client is None: return 0
        image = cv2.imencode(".png" ,image)[1].tobytes()
        res = self.client.basicGeneral(image)
        if len(res.get('words_result', [])) > 0:
            word = res['words_result'][0]['words']
            number = ''.join(filter(lambda x: x in '0123456789', word))
            if number:
                return int(number)
        return 0
