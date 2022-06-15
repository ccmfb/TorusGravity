import shutil
import os
import sys


class VideoTools:
    def __init__(self):
        pass

    def create_folder(self, name):
        if not os.path.exists(name):
            os.mkdir(name)
        else:
            print("Directory already exists")

    def remove_folder(self, path):
        try:
            shutil.rmtree(path)
        except OSError as e:
            print('ERROR ({path}): {e.strerror}')

    def create_mp4(self, images_path, fps):
        import cv2

        images = [img for img in os.listdir(images_path) if img.endswith('.png')]
        images.sort(key = lambda x: int(x[:x.rfind('.')]))

        frame = cv2.imread(os.path.join(images_path, images[0]))
        h, w, l = frame.shape

        video = cv2.VideoWriter('videos/video.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (w,h))

        for image in images:
            video.write(cv2.imread(os.path.join(images_path, image)))

        cv2.destroyAllWindows()
        video.release()


def progressbar(it, prefix="", size=60, out=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, u"#"*x, "."*(size-x), j, count), 
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)
