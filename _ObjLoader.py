from _resources import *

class ObjLoader:
    def __init__(self, name, factor=1):
        self.name = name
        self.factor = factor
        
        self.polys = self.load()
        
        if self.factor != 1: self.scale(self.polys, self.factor)
        
        
        
    def load(self):
        print("Loading model!")
    
        import re
    
        flt = r"-?[\d\.]+"
        vertex_pattern = r"v\s+(?P<x>{})\s+(?P<y>{})\s+(?P<z>{})".format(flt, flt, flt)
        face_pattern = r"f\s+((\d+/*\d*/*\d*\s*){3,})"
        #vt_pattern = r"vt\s+(?P<x>{})\s+(?P<y>{})".format(flt, flt)
        
        self.vertices = []
        self.faces = []
        #self.vt = []
    
        with open(self.name, "r") as file:
            for line in map(str.strip, file):
                match = re.match(vertex_pattern, line)
                if match is not None:
                    vTuple = list(map(float, match.group("x", "y", "z")))
                    vTuple[1] = -vTuple[1]
                    self.vertices.append(vTuple)
                    continue
                match = re.match(face_pattern, line)
                if match is not None:
                    self.faces.append(tuple(map(int, [s for s in vertex.split("/") if s])) for vertex in match.group(1).split())
                    continue
                #match = re.match(vt_pattern, line)
                #if match is not None:
                #   t = tuple(map(float, match.group("x", "y")))
                #   t = (t[0],t[1],t[2])
                   
        polys = []
        for n in self.faces:
            sub = []
            for vertex in n:
                sub.append(roundPoint(self.vertices[vertex[0]-1])) # -1 because in the OBJ spec, collections start at index 1 rather than 0 
            polys.append(sub)
        
        print("Removing duplicate polys!")
        return list({tuple(sorted(x)) for x in polys})
        
    def scale(self, polygons, factor):
        #if factor == 1: self.polygons = polygons;return
        
        nPolys = []
        for poly in polygons:
            nPolys.append([[c*factor for c in p] for p in poly])
            
        self.polys = nPolys
    