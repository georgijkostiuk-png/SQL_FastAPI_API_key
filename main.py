from fastapi import FastAPI
from database import Base, engine
from routers import user_router, todo_router,flights_router, hotels_router
#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
 
app = FastAPI()
 
app.include_router(user_router)
app.include_router(todo_router)
app.include_router(flights_router)
app.include_router(hotels_router)



if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",host="127.0.0.1", port=8000,reload=True)


# Go to http:/localhost:8000/docs