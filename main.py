from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import motor.motor_asyncio
from models import ClientModel, UserModel, CreateUserModel, UserAuthModel, ProfileModel, InvoiceModel

app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MONGODB_URL = "mongodb+srv://hvt16:printfhvt@cluster0.vpsbs.mongodb.net/cluster0?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.arc

@app.get("/")
def home():
	return "server is running"

# client part
@app.get("/clients/", response_description="List of clients", response_model=List[ClientModel])
async def getClients(page: int = 1):
	limit = 8
	start_index = (page-1)*limit
	try:
		total = await db["clients"].estimated_document_count()
		clients = await db["clients"].find().to_list(limit)
		return clients
	except Exception as e:
		raise HTTPException(status_code=404, detail=e)
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
		raise HTTPException(status_code=409, detail=h)

@app.put("/clients/{id}")
def updateClient(id: int):
	pass 

@app.delete("/clients/{id}")
async def deleteClient(id: str):
	delete_client = await db["clients"].delete_one({"_id": id})
	if delete_client.deleted_count == 1:
		return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
	raise HTTPException(status_code=404, detail=f"client {id} not fount")

# invoices
@app.get("/invoices/")
def getInvoicesByUser():
	pass 

@app.get("/invoices/count/")
def getTotalCount():
	pass 

@app.get("/invoices/{id}")
async def getInvoice(id: str):
	invoice = await db["invoices"].find_one({"_id": id})
	if invoice is not None:
		return JSONResponse(status_code=200, content=invoice)
	raise HTTPException(status_code=400, detail="invoice does not exist")

@app.post("/invoices/", response_description="create invoice", response_model=InvoiceModel)
async def createInvoice(invoice: InvoiceModel = Body(...)):
	invoice = jsonable_encoder(invoice)
	new_invoice = await db["invoices"].insert_one(invoice)
	created_invoice = await db["invoices"].find_one({"_id": new_invoice.inserted_id})
	return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_invoice)

@app.put("/invoices/{id}")
async def updateInvoice(id: int):
	pass 

@app.delete("/invoices/{id}")
async def deleteInvoice(id: str):
	delete_invoice = await db["invoices"].delete_one({"_id": id})
	if delete_invoice.deleted_count == 1:
		return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
	raise HTTPException(status_code=404, detail=f"invoice {id} not fount")


# users
@app.post("/users/signin/", response_description="Signin user")
async def signin(auth_user: UserAuthModel = Body(...)):
	auth_user_json = jsonable_encoder(auth_user)
	print(auth_user_json)
	find_user = await db["users"].find_one({"email": auth_user_json["email"]})
	if find_user is not None:
		return JSONResponse(status_code=200, content=find_user)
	raise HTTPException(status_code=400, detail="user not found")

@app.post("/users/signup/", response_description="Add new User", response_model=UserModel)
async def signup(_user: CreateUserModel = Body(...)):
	user = UserModel(email=_user.email, name=_user.firstName + " " + _user.lastName, password=_user.password)
	user = jsonable_encoder(user)
	new_user = await db["users"].insert_one(user)
	created_user = await db["users"].find_one({"_id": new_user.inserted_id})
	return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)

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
async def getProfile(id: str):
	profile = await db["profiles"].find_one({"_id": id})
	if profile is not None:
		return JSONResponse(status_code=200, content=profile)
	raise HTTPException(status_code=400, detail="profile does not exist")

@app.post("/profiles/", response_description="create profile", response_model=ProfileModel)
async def createProfile(profile: ProfileModel = Body(...)):
	profile = jsonable_encoder(profile)
	new_profile = await db["profiles"].insert_one(profile)
	created_profile = await db["profiles"].find_one({"_id": new_profile.inserted_id})
	return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_profile)

@app.post("/profiles/{id}")
def updateProfile(id: int):
	pass 

@app.delete("/profiles/{id}")
async def deleteProfile(id: str):
	delete_profile = await db["profiles"].delete_one({"_id": id})
	if delete_profile.deleted_count == 1:
		return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
	raise HTTPException(status_code=404, detail=f"profile {id} not fount")