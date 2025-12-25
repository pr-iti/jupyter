from urllib import response
from fastapi import APIRouter, Query
from pydantic import BaseModel


from enum import Enum
from typing import Optional

from fastapi import FastAPI,status,Response

router = APIRouter(
    prefix ='/blog',
    tags=['blog -post'])

class BlogModel(BaseModel):
    title:str
    content:str
    published:Optional[bool]
    
      
@router.post('/new' #,status_code= status.HTTP_200_OK
             )
def create_blog(blog: BlogModel):
    return{'data':blog}


@router.post('/new/{id}' )
def create_blog(blog: BlogModel,id:int,version:int = 1):
    
    return{
        'data':blog,
        'id':id,
        'data':blog,
        'version':version
        
        }


@router.post('/new/{id}/comment')
def create_comment(blog:BlogModel,id:int,
                   comment_id:int = Query(None,
                   title='Id of the  comment',
                   description='Description for comment_id',
                   alias='comment_Id',
                   deprecated=True
                   )
   ):
    return {
        'blog':blog,
        'id':id,
        'comment_id':comment_id
    }

# def blog_post_id(id:int,response = Response):
#     blogs =[]
    
#     if(id < 5):
#         response.status_code = status.HTTP_200_OK
#         blogs.insert(id)
#         return {"message" : f" this id {id } is valid"}
#     else:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message" : f" this id {id } is invalid"}