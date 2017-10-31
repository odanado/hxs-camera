import sys

sys.path.append('pytorch-yolo2')  # NOQA
import cv2


from darknet import Darknet
from utils import load_class_names, do_detect, plot_boxes_cv2


class YOLO(object):
    def __init__(self, config_file, weight_file,
                 conf_thresh=0.5, nms_thresh=0.4):
        self.darknet = Darknet(config_file)
        self.darknet.load_weights(weight_file)

        self.conf_thresh = conf_thresh
        self.nms_thresh = nms_thresh

        self.class_names = self.load_class_names()

    def load_class_names(self):
        if self.darknet.num_classes == 20:
            names_file = 'pytorch-yolo2/data/voc.names'
        elif self.darknet.num_classes == 80:
            names_file = 'pytorch-yolo2/data/coco.names'
        else:
            names_file = 'pytorch-yolo2/data/names'
        class_names = load_class_names(names_file)
        return class_names

    def detect(self, img):
        width, height = self.darknet.width, self.darknet.height
        sized = cv2.resize(img, (width, height))
        bboxes = do_detect(self.darknet, sized,
                           self.conf_thresh, self.nms_thresh, False)

        draw_img = plot_boxes_cv2(img, bboxes, None, self.class_names)

        return bboxes, draw_img


if __name__ == '__main__':
    config_file = './pytorch-yolo2/cfg/tiny-yolo-voc.cfg'
    weight_file = 'weights/tiny-yolo-voc.weights'
    img_file = './pytorch-yolo2/data/dog.jpg'
    yolo = YOLO(config_file, weight_file)
    yolo.darknet.print_network()

    img = cv2.imread(img_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # print(img)
    bboxes, draw_img = yolo.detect(img)
