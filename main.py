from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
from models import ClientModel

app = FastAPI()
MONGODB_URL = "mongodb+srv://hvt16:printfhvt@cluster0.vpsbs.mongodb.net/cluster0?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.arc

@app.get("/")
def home():
	return "server is running"

# client part
@app.get("/clients/")
def getClients():
	pass

@app.get("/clients/user/")
def getClientsByUser():
	pass 

@app.post("/clients/", response_description="Add new client", response_model=ClientModel)
async def createClient(client: ClientModel = Body(...)):
	try:
	    client = jsonable_encoder(client)
	    new_client = await db["clients"].insert_one(client)
	    created_client = await db["clients"].find_one({"_id": new_client.inserted_id})
	    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_client) 
	except Exception as h:
		raise HTTPException(status_code=409, details=h)

@app.put("/clients/{id}")
def updateClient(id: int):
	pass 

@app.delete("/clients/{id}")
def deleteClient(id: int):
	pass 

# invoices
@app.get("/invoices/")
def getInvoicesByUser():
	pass 

@app.get("/invoices/count/")
def getTotalCount():
	pass 

@app.get("/invoices/{id}")
def getInvoice(id: int):
	pass 

@app.post("/invoices/")
def createInvoice():
	pass 

@app.put("/invoices/{id}")
def updateInvoice(id: int):
	pass 

@app.delete("/invoices/{id}")
def deleteInvoice(id: int):
	pass 


# users
@app.post("/users/signin/")
def signin():
	pass 

@app.post("/users/signup/")
def signup():
	pass 

@app.post("/users/forgot/")
def forgotPassword():
	pass 

@app.post("/users/reset/")
def resetPassword():
	pass 

# profiles
@app.get("/profiles/")
def getProfileByUser():
	pass 

@app.get("/profiles/{id}")
def getProfile(id: int):
	pass 

@app.post("/profiles/")
def createProfile():
	pass 

@app.post("/profiles/{id}")
def updateProfile(id: int):
	pass 

@app.delete("/profiles/{id}")
def deleteProfile(id: int):
	pass 