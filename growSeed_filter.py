# -*- coding: utf-8 -*-
'''
 * @Author: ZQ.Pei 
 * @Date: 2018-06-03 16:59:32 
 * @Last Modified by:   ZQ.Pei 
 * @Last Modified time: 2018-06-03 16:59:32 
'''

from _stack import Stack
import cv2
import numpy as np


class GrowSeedAlgo(object):
    '''
        only for binary image
    '''
    def __init__(self, im=None, im_path=None):
        self.stack = Stack()

        if im is not None:
            self.im = im
        elif im_path is not None:
            self.imread(im_path)
        else:
            raise ValueError("No Input image!")

        
        self.im_size = self.im.shape
        self.im_height, self.im_width = self.im_size
        self.im_label = np.full_like(self.im, 0)

        self.max_label = 0
        self.label_area = {}


    def imread(self, img_path):
        self.im_path = im_path
        self.im = cv2.imread(im_path)

    def output(self, threshold=20):
        im_out = np.zeros_like(self.im)
        im_out = np.stack((im_out,im_out,im_out),axis=2)
        for label_idx in range(1,self.max_label+1):
            if self.label_area[label_idx] > threshold:
                rand_color = np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)
                im_out[np.where(self.im_label==label_idx)]=rand_color
        
        cv2.imshow('output',im_out)
        cv2.waitKey(0)


    def start(self):
        for x0 in range(self.im_height):
            for y0 in range(self.im_width):
                if self.im_label[x0,y0] == 0 and self.im[x0,y0] != 0: # ignoring the background
                    self.max_label += 1
                    self.im_label[x0,y0] = self.max_label
                    self.stack.push((x0,y0))
                    tmp_area = 1        # tmp_area is the area of growned region in this round
                    while not self.stack.is_empty():
                        x,y = self.stack.pop()
                        tmp_area += self.grow(x,y)

                    self.label_area[self.max_label] = tmp_area
                    #cv2.imshow('growseed',self.im_label/self.max_label)
                    #cv2.waitKey(0)

        self.output(threshold=20)

    def grow(self, x0,y0):
        tmp = 0
        current_label = self.im_label[x0,y0]
        for x,y in self._get_neighbour(x0,y0):
            if self.im_label[x,y] == 0 and self.im[x,y] == self.im[x0,y0]:  # threshold
                self.im_label[x,y] = current_label
                self.stack.push((x,y))
                tmp += 1
                #cv2.imshow('growseed',self.im_label/self.max_label)
                #cv2.waitKey(1)
        return tmp

    def _get_neighbour(self, x0, y0):
        neighbour = []
        for i in (-1,0,1):
            for j in (-1,0,1):
                if (i,j) == (0,0): 
                    continue
                x = x0+i
                y = y0+j
                if self._in_region(x,y):
                    neighbour.append((x,y))
        return neighbour

    def _in_region(self, x,y):
        return True if 0<=x<self.im_height and 0<=y<self.im_width else False
    


def main():
    ori_im = cv2.imread('img/test1.bmp'， flag=0)
    #cv2.imshow('ori_im',ori_im)
    #cv2.waitKey(0)
    bin_im = ((ori_im>125)*255).astype(np.uint8)
    #cv2.imshow('bin_im',bin_im)
    #cv2.waitKey(0)

    gs = GrowSeedAlgo(im=bin_im)
    gs.start()

if __name__ == '__main__':
    main()
