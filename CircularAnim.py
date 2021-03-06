# coding=utf-8

import pygame
import os
import gl


# 循环动画精灵
class CircularAnim(pygame.sprite.Sprite):
    def __init__(self, groups, target, circular_max):
        self._layer = 20
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.target = target  # 上层Surface对象
        self.image = None  # Surface对象
        self.master_image = None
        self.rect = None  # Surface矩形
        self.frame = 0  # 当前动画帧索引
        self.old_frame = -1
        self.frame_width = 1  # Surface对象宽度
        self.frame_height = 1  # Surface对象高度
        self.first_frame = 0  # 第一帧索引
        self.last_frame = 0  # 最后一帧索引
        self.columns = 1  # 动画列数
        self.last_time = 0
        self.filepath = None  # 动画图片路径
        self.circular = 0  # 动画循环次数
        self.circular_max = circular_max  # 动画循环最大次数
        self.anim_size = None  # 动画大小
        self.anim_position = None  # 动画位置
        self.anim_deviation = [0, 0]  # 动画偏移位置
        self.anim_move = None  # 动画移动方式
        self.anim_size_multiple = 0  # 动画放大倍数
        self.show = False

    def load(self, filename, width, height, columns):
        self.filepath = os.path.join(gl.source_dir, filename)
        self.master_image = pygame.image.load(self.filepath).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1
        self.image = self.master_image.subsurface((0, 0, self.frame_width, self.frame_height))
        self.rect = self.image.get_rect()

    def update(self, updatePar):
        if 0 < self.circular_max < self.circular:
            self.kill()
            return
        if self.frame == self.last_frame:
            self.circular += 1
        if updatePar.current_time > self.last_time + updatePar.fps:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = updatePar.current_time
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = (frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            if self.anim_size is None and self.anim_size_multiple < 2:
                self.image = pygame.transform.scale(self.image, self.target.img_size)
            elif self.anim_size_multiple < 2:
                self.image = pygame.transform.scale(self.image, self.anim_size)
            img_rect = self.image.get_rect()
            if self.anim_size_multiple > 1:
                self.image = pygame.transform.scale(self.image, [img_rect.width * self.anim_size_multiple,
                                                                 img_rect.height * self.anim_size_multiple])
                img_rect = self.image.get_rect()
            self.show = True
            is_move = False
            if self.anim_move is not None:
                if self.circular == 0 and self.frame == 1:
                    self.rect = img_rect
                    self.rect.x += self.anim_deviation[0]
                    self.rect.y += self.anim_deviation[1]
                    is_move = False
                else:
                    self.rect = self.rect.move(self.anim_move)
                    img_rect.x = self.rect.x
                    img_rect.y = self.rect.y
                    self.rect = img_rect
                    is_move = True
            else:
                self.rect = img_rect
            if is_move is False:
                if self.anim_position is None:
                    self.rect.x = self.target.rect.x
                    self.rect.y = self.target.rect.y
                else:
                    self.rect.x = self.anim_position[0]
                    self.rect.y = self.anim_position[1]
            if self.anim_move is None:
                self.rect.x += self.anim_deviation[0]
                self.rect.y += self.anim_deviation[1]
            self.old_frame = self.frame
