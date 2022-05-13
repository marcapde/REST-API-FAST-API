from asyncio.windows_events import NULL
from tkinter import image_types
from typing import List, Optional
from unicodedata import name
from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi import File, UploadFile, HTTPException

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
#for more efficiency as probably we will repaet oprations with the same gallery
#we will save always de last gallery viewed.
cache = {"id":-1} 
#For even more efficiency it could also be implemented with an Image cache

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
    prop.id=random.randint(0,99999)
    galleries.append(dict(prop))
    return prop.id

#############/galleries/{g_id}##################

@app.get('/galleries/{g_id}')
async def get_gallery(g_id: int):
    global cache 
    if (cache !=None and cache.get("id")==g_id):
        return dict(name=g.get("name"),desc=g.get("desc"))
    #else
    for g in galleries:
        if(g.get("id")==g_id):
            cache = g
            return dict(name=g.get("name"),desc=g.get("desc"))
    
    raise HTTPException(status_code=404, detail="Gallery not found")

@app.delete('/galleries/{g_id}')
async def del_gallery(g_id: int):
    global cache 

    if (cache != None and cache.get("id")==g_id):
        galleries.remove(cache)
        return g_id
    #else
    for g in galleries:
        if(g.get("id")==g_id):
            galleries.remove(g)
            return g_id
    raise HTTPException(status_code=404, detail = "Gallery not found") 
##############/galleries/{g_id}/images#################

@app.get('/galleries/{g_id}/images')
async def get_images(g_id: int):
    global cache 

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
          
    if (result == []):
        raise HTTPException(status_code=404, detail="Gallery not found")
    else:   
        return result

@app.post('/galleries/{g_id}/images')
async def post_images(g_id:int,image:image):
    global cache 

    #to make it comfy for testing id will be a random int within this small range
    #for more scalability use uuid instead.
    image.id=random.randint(0,99999)
    if (cache != None and cache.get("id")==g_id):
        g = cache
    else: 
        for g in galleries:
            if (g.get("id")==g_id):
                cache = g
                break
    if (g["images"]!= None):
        g["images"].append(image)               
    else:                
        g["images"]=[image]
    
    return image.id

############/galleries/{g_id}/images/{i_id}###################

@app.get('/galleries/{g_id}/images/{i_id}')
async def get_image_byId(g_id:int,i_id:int):
    global cache 
    found=0
    if (cache != None and cache.get("id")==g_id):
        g = cache
    else: 
        for g in galleries:
            if (g.get("id")==g_id):
                cache = g
                found = 1
                break
    if(found==0):
        raise HTTPException(status_code=404, detail="Gallery not found")
    for i in g["images"]:
        if(i.id == i_id):
            aux = dict(i)               
            return (dict(name=aux["name"],
                desc=aux["desc"],
                location=aux["location"],
                width=aux["width"],
                height=aux["height"]))
    #if not found
    raise HTTPException(status_code=405, detail="Image not found")


@app.delete('/galleries/{g_id}/images/{i_id}')
async def del_image_byId(g_id:int,i_id:int):   
    index = 0
    for g in galleries:
        if (g.get("id")==g_id):
            break
        index+=1
    for i in g["images"]:
        if(i.id == i_id):
            galleries[index]["images"].remove(i)
            return i_id
    #if not found
    return {"405":"image not found"}


###########/galleries/{g_id}/images/{i_id}/file################
#defining galleries page


@app.post('/galleries/{g_id}/images/{i_id}/file')
async def post_file(g_id:int, i_id:int, file: bytes = File(...)):
    #image(name="A",desc="B",location="C",width=3, height=3, img= str(file))
    index = 0
    for g in galleries:
        if (g.get("id")==g_id):
            cache = g
            break
        index+=1
    ii = 0
    for i in g["images"]:
        if(i.id == i_id):
            i.img = file
            galleries[index]["images"][ii] = i
            return Response(i.img)
        ii+=1
    #if not found
    return {"405":"image not found"}

@app.get('/galleries/{g_id}/images/{i_id}/file')
async def get_file(g_id:int, i_id:int):
    index = 0
    for g in galleries:
        if (g.get("id")==g_id):
            cache = g
            break
        index+=1
    if (index == len(galleries)):
         raise HTTPException(status_code=404, detail="Gallery not found")
    ii = 0
    for i in g["images"]:
        if(i.id == i_id):
            return(Response(galleries[index]["images"][ii].img))
        ii+=1
    #if not found
        raise HTTPException(status_code=404, detail="Image not found")
