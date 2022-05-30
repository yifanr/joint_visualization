from venv import create
import joblib
import torch
import trimesh
import pickle
import numpy as np
import os

def create_dirtree_without_files(src, dst):
   
      # getting the absolute path of the source
    # directory
    src = os.path.abspath(src)
     
    # making a variable having the index till which
    # src string has directory and a path separator
    src_prefix = len(src) + len(os.path.sep)
     
    # making the destination directory
    os.makedirs(dst, exist_ok=True)
     
    # doing os walk in source directory
    for root, dirs, files in os.walk(src):
        for dirname in dirs:
           
            # here dst has destination directory,
            # root[src_prefix:] gives us relative
            # path from source directory
            # and dirname has folder names
            dirpath = os.path.join(dst, root[src_prefix:], dirname)
             
            # making the path which we made by
            # joining all of the above three
            os.makedirs(dirpath, exist_ok=True)

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

def make_obj_shape_new(render_items):
    for shape in render_items:
        i = 0
        path = shape[0][0]
        for part in shape:
            part[0] = path
            part[1] = i
            # part[2].show()
            obj_path = "data/" + path + "_" + str(i) + ".obj"
            trimesh.exchange.export.export_mesh(part[2], obj_path, file_type="obj")
            trimesh.exchange.export.export_mesh(trimesh.load_mesh(obj_path, 'obj'), obj_path, file_type='obj')
            part[2] = obj_path
            #print(part)
            i += 1


def make_obj_joint(render_items, name):
    for i in range(len(render_items)):
        joint = render_items[i]
        trimesh.exchange.export.export_mesh(joint[1], "data/"+name+"_"+str(i)+"_base.obj", file_type="obj")
        joint[1] = "data/"+name+"_"+str(i)+"_base.obj"
        trimesh.exchange.export.export_mesh(trimesh.load_mesh(joint[1], 'obj'), joint[1], file_type="obj")
        trimesh.exchange.export.export_mesh(joint[0], "data/"+name+"_"+str(i)+"_move.obj", file_type="obj")
        joint[0] = "data/"+name+"_"+str(i)+"_move.obj"
        trimesh.exchange.export.export_mesh(trimesh.load_mesh(joint[0], 'obj'), joint[0], file_type="obj")

filename = 'faucet_shape_data'
render_items = []
create_dirtree_without_files('tmp/'+filename, 'visualizations/'+filename)
create_dirtree_without_files('tmp/'+filename, 'data/'+filename)
# render_items+=joblib.load('tmp/'+filename+'.joblib')
for dirpath, dirs, files in os.walk('tmp/'+filename): 
    for file in files:
        path = os.path.join(dirpath, file)
        shape = joblib.load(path)
        print(shape)
        path = path[4:-7]
        shape[0][0] = path
        render_items += [shape]
make_obj_shape_new(render_items)
print(len(render_items))
save_object(render_items, 'tmp/'+filename+'.pkl')
