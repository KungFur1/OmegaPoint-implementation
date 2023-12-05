from pydantic import BaseModel, Field

class BlogSchema(BaseModel):
    id : int = Field(default=None)
    title : str = Field(default=None)
    content : str = Field(default=None)
    class Config:
        json_schema_extra = {
            "blog_demo" : {
                "title" : "some title about cars",
                "content" : "some content about cars"
            }
        }
