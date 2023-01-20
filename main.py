from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware

# API KEY and URL 
STIBEE_API_KEY = "ca1c4f9070c852e524c1a9128e7f656e4ffb39c7ff4d3bc0f22224c3a7941bdc6ae484624ff861ff2ada925c1277222320b9279c2cea8c0cabbcc5412b8498da"
STIBEE_URL = "https://api.stibee.com/v1"

app = FastAPI()

# ----------------------------------- 

# Allow CORS 
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------


# Request Body Form
class SubscribeForm(BaseModel) : 
    email : str
    name : Optional[str] = None
    STIBEE_LISTID : str
    STIBEE_GROUPID : str

@app.get("/")
def root(): 
    return {"HELLO" : "JINDO-ME-BACKEND"}


# General Subscription 
@app.post("/SubscribeStibee")
def subscribeStibee(form : SubscribeForm): 
    header = {"AccessToken": STIBEE_API_KEY, "Content-Type": "application/json"}
    body = {
      "eventOccuredBy": "SUBSCRIBER",
      "confirmEmailYN": "N",
      "groupIds": [form.STIBEE_GROUPID],
      "subscribers": [
        {
          "email": form.email,
          "name": form.name,
          "ad_agreed": "N",
          "tag1": "string",
          "tag2": "string",
          "tag3": "string",
        },
      ],
    }
    url = STIBEE_URL+"/lists/"+form.STIBEE_LISTID+"/subscribers"
    res = requests.post(url = url ,headers= header, json = body)
    return (res.content)




#  at last, the bottom of the file/module
 if __name__ == "__main__":
     uvicorn.run(app, host="127.0.0.1", port=8080)