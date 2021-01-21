import time

from _Camera import Camera
from _render import Field


class RenderObj:
    def __init__(self, model, anglex=0, angley=0, fieldSize=(500, 500, 400), camPos=(0, 0, -100), res=(500, 500),
                 fileName="pic", colorGradient=True, rDis=False, scaleTO=150):
        startTime = time.time()
        field = Field(*fieldSize)
        field.drawModel("models/" + model, ax=angley, ay=anglex, scaleTO=scaleTO)
        camera = Camera(field, camPos, a=0, fov=80, res=res, colorGradient=colorGradient, rDis=rDis)
        camera.renderImage(fileName, consec=True)
        #print(camera.getInfo())

        input(f"The execution took {time.time() - startTime} s / {(time.time() - startTime) / 60} min!")


# with open("ironman.obj") as f:
#    [print(f.readline()) for n in range(10000)]

if __name__ == "__main__":
    RenderObj("deer.obj", angley=30, anglex=0, camPos=(0, -85, -150), colorGradient=True, fileName="pic", rDis=False,
              scaleTO=200)
