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


class image (BaseModel):
    name: str
    desc: str
    location: str
    width: int
    height:int
    img: Optional [bytes]

class gallery (BaseModel):
    id : Optional [int];
    name: str;
    desc : str;
    images : Optional [List[image]];

galleries = []

#defining main page
@app.get('/')
def root():
    return {"WELCOME":"go to /galleries for more data"}


#defining galleries page
@app.get('/galleries')
def get_galleries():
    result =[]
    for g in galleries:
       result.append(dict(name=g.get("name"),desc=g.get("desc")))
    
    return result

@app.post('/galleries')
def post_gallery(prop:gallery):
    #to make it comfy for testing id will be a random int within this small range
    #for more scalability use uuid instead.
    prop.id=random.randint(0,9999)
    galleries.append(dict(prop))
    return prop.id

###############################

#defining galleries page
@app.get('/galleries/{g_id}')
def get_gallery(g_id: int):
    for g in galleries:
        if(g.id==g_id):
            return dict(name=g.get("name"),desc=g.get("desc"))

@app.delete('/galleries/{g_id}')
def del_gallery(g_id: int):
    for g in galleries:
        if(g.get("id")==g_id):
            galleries.remove(g)
            return g_id

###############################

#defining galleries page
@app.get('/galleries/{g_id}/images')
def get_images():
    return {"WELCOME":"Welcome to my API"}

#defining galleries page
@app.get('/galleries/{g_id}/images/{i_id}')
def get_image():
    return {"WELCOME":"Welcome to my API"}


#defining galleries page
@app.get('/galleries/{g_id}/images/{i_id}/fle')
def root():
    return {"WELCOME":"Welcome to my API"}