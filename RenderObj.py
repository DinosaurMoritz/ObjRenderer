from _Camera import Camera
from _render import Field
import time

class RenderObj:
    def __init__(self, model, factor=1, anglex=0, angley=0, fieldSize=(300, 300, 300), camPos=(0,0,-100), res=(300,300), fileName="pic", colorGradient=True, rDis=False):
        startTime = time.time()
        field = Field(*fieldSize)
        field.drawModel("models/"+model, ax=angley, ay=anglex, factor=factor)
        Camera(field,  camPos, a=0, fov=80, res=res, colorGradient=colorGradient, rDis=rDis).renderImage(fileName)
        print(f"The execution took {time.time()-startTime} s / {(time.time()-startTime)/60} min!")
        

#with open("ironman.obj") as f:
#    [print(f.readline()) for n in range(10000)]


RenderObj("deer.obj", factor=0.1, angley=110, anglex=0, camPos=(0, 0, -150), colorGradient=True, fileName="pic", rDis=False)
