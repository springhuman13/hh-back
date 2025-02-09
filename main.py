from FastApi import FastAPI

app = FastAPI()

@@app.get()
def root():
    return "Hello World"