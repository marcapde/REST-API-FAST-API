from asyncio.windows_events import NULL
import binhex
from msilib.schema import Binary
import string
from tkinter import image_types
from typing import List, Optional
from unicodedata import name
import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image

import random
app=FastAPI(title='REST API')

##########CLASSES###############
class image (BaseModel):
    id : Optional [int];
    name: str
    desc: str
    location: str
    width: int
    height:int
    img: bytes | None = None

class gallery (BaseModel):
    id : Optional [int];
    name: str;
    desc : str;
    images : list[image] | None = None
##########CLASSES###############

galleries = []

#defining main page
@app.get('/')
async def root():
    return {"WELCOME":"go to /galleries for more data"}


#defining galleries page
@app.get('/galleries')
async def get_galleries():
    result =[]
    for g in galleries:
       result.append(dict(name=g.get("name"),desc=g.get("desc")))
    
    return result

@app.post('/galleries')
async def post_gallery(prop:gallery):
    #to make it comfy for testing id will be a random int within this small range
    #for more scalability use uuid instead.
    prop.id=random.randint(0,9999)
    galleries.append(dict(prop))
    return prop.id

#############/galleries/{g_id}##################

@app.get('/galleries/{g_id}')
async def get_gallery(g_id: int):
    for g in galleries:
        if(g.id==g_id):
            return dict(name=g.get("name"),desc=g.get("desc"))

@app.delete('/galleries/{g_id}')
async def del_gallery(g_id: int):
    for g in galleries:
        if(g.get("id")==g_id):
            galleries.remove(g)
            return g_id

##############/galleries/{g_id}/images#################

@app.get('/galleries/{g_id}/images')
async def get_images(g_id: int):
    result =[]
    for g in galleries:
        if (g.get("id")==g_id):
            for i in g.get("images"):
                aux = dict(i)               
                result.append(dict(name=aux["name"],
                desc=aux["desc"],
                location=aux["location"],
                width=aux["width"],
                height=aux["height"]))
          
                    
    return result

@app.post('/galleries/{g_id}/images')
async def post_images(g_id:int,image:image):
    #to make it comfy for testing id will be a random int within this small range
    #for more scalability use uuid instead.
    image.id=random.randint(0,9999)
    for g in galleries:
        if (g.get("id")==g_id):
            print(g["images"])
            if (g["images"]!= None):
                print(image)
                g["images"].append(image)
                print(g["images"]) 
                #lista = g["images"]
    	        #print(g["images"])               
                #g["images"]=lista                
            else:                
                g["images"]=[image]
            print(g["images"])
            
            return image.id

###############################

#defining galleries page
@app.get('/galleries/{g_id}/images/{i_id}')
def get_image():
    return {"WELCOME":"Welcome to my API"}


#defining galleries page
@app.get('/galleries/{g_id}/images/{i_id}/fle')
def root():
    return {"WELCOME":"Welcome to my API"}