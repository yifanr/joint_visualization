import joblib
import torch
import trimesh
import pickle
import numpy as np
import os
def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

def make_obj_shape(render_items):
    for shape in render_items:
        for part in shape:
            # part[2].show()
            trimesh.exchange.export.export_mesh(part[2], "data/"+str(part[0])+"_"+str(part[1])+".obj", file_type="obj")
            part[2] = "data/"+str(part[0])+"_"+str(part[1])+".obj"
            trimesh.exchange.export.export_mesh(trimesh.load_mesh(part[2], 'obj'), part[2], file_type='obj')
            #print(part)
def make_obj_joint(render_items, name):
    for i in range(len(render_items)):
        joint = render_items[i]
        trimesh.exchange.export.export_mesh(joint[1], "data/"+name+"_"+str(i)+"_base.obj", file_type="obj")
        joint[1] = "data/"+name+"_"+str(i)+"_base.obj"
        trimesh.exchange.export.export_mesh(trimesh.load_mesh(joint[1], 'obj'), joint[1], file_type="obj")
        trimesh.exchange.export.export_mesh(joint[0], "data/"+name+"_"+str(i)+"_move.obj", file_type="obj")
        joint[0] = "data/"+name+"_"+str(i)+"_move.obj"
        trimesh.exchange.export.export_mesh(trimesh.load_mesh(joint[0], 'obj'), joint[0], file_type="obj")

filename = 'final_shape_data5'
render_items = []
# render_items+=joblib.load('tmp/'+filename+'.joblib')
for file in os.listdir('tmp/'+filename):
    render_items+=[joblib.load('tmp/'+filename+"/"+file)]
make_obj_shape(render_items)
print(len(render_items))
save_object(render_items, 'tmp/'+filename+'.pkl')
