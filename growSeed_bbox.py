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

        
        self.im_height, self.im_width = self.im.shape
        self.im_label = np.full_like(self.im, 0, dtype=int)
        self.im_area = self.im.size

        self.max_label = 0
        self.label_area = {}
        self.label_color = {}


    def imread(self, img_path):
        self.im_path = im_path
        self.im = cv2.imread(im_path)

    def output(self, threshold=0.05):
        im_out = np.zeros_like(self.im)
        im_out = np.stack((im_out,im_out,im_out),axis=2)
        for label_idx in range(1,self.max_label+1):
            if self.label_area[label_idx]/self.im_area > threshold: # areas smaller than threshold will be treated as background!!!
                rand_color = np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)
                im_out[np.where(self.im_label==label_idx)]=rand_color

                self.label_color[label_idx] = rand_color
        
        #cv2.imshow('output',im_out)
        #cv2.waitKey(0)

    def drawBbox(self, threshold=0.05):
        im_out = self.im.copy()
        im_out = im_out[:,:,np.newaxis].repeat(3, axis=2)
        for label_idx in range(1,self.max_label+1):
            if self.label_area[label_idx]/self.im_area > threshold: # areas smaller than threshold will be treated as background!!!
                ys, xs = np.where(self.im_label==label_idx)
                xmin = xs.min()
                xmax = xs.max()
                ymin = ys.min()
                ymax = ys.max()
                #print(xmin,ymin,xmax,ymax)

                rand_color = self.label_color[label_idx]
                cv2.rectangle(im_out, (xmin,ymin), (xmax,ymax), rand_color, 2)      


                cv2.imshow('bbox', im_out)
                cv2.waitKey(100) 

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
                        #if self.max_label == 256:
                            #import ipdb; ipdb.set_trace()
                        tmp_area += self.grow(x,y)

                    self.label_area[self.max_label] = tmp_area

                    #print(self.max_label)
                    #cv2.imshow('growseed',self.im_label/self.max_label)
                    #cv2.waitKey(1)

        threshold = 0
        self.output(threshold)
        self.drawBbox(threshold)

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
    ori_im = cv2.imread('img/rice.jpg',0)
    #cv2.imshow('ori_im',ori_im)
    #cv2.waitKey(0)
    bin_im = ((ori_im>128)*255).astype(np.uint8)
    
    # sometimes background is white not black
    # random sample a few points, to decide whether to inverse the picture
    num_random_pts = 100
    np.random.seed(10)
    random_sample_pts = [np.random.choice(bin_im.shape[0], num_random_pts), np.random.choice(bin_im.shape[1], num_random_pts)]
    inverse = True if np.mean(bin_im[random_sample_pts]) > 128 else False
    if inverse:
        bin_im = 255 - bin_im

    #cv2.imshow('bin_im',bin_im)
    #cv2.waitKey(0)

    gs = GrowSeedAlgo(im=bin_im)
    gs.start()

if __name__ == '__main__':
    main()