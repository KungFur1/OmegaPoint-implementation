import fastapi
from app.blogs.blog_model import BlogSchema
from app.database import blogs

router = fastapi.APIRouter()


# Get blogs
@router.get("/blogs", tags=["blogs"])
async def get_blogs():
    return {"data" : blogs}


# Get blog by {id}
@router.get("/blogs/{id}", tags=["blogs"])
async def get_blog(id:int):
    for blog in blogs:
        if blog["id"] == id:
            return {"data" : blog}
    raise fastapi.HTTPException(status_code=404, detail="Blog with this id does not exist")


# Post a blog
@router.post("/blogs", tags=["blogs"])
async def add_blog(blog : BlogSchema):
    blog.id = len(blogs)
    blogs.append(blog.model_dump()) # save in the database; model_dump() turns object into a dictionary
    return {"info": "Blog added"}
