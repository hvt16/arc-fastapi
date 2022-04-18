from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import motor.motor_asyncio
from models import ClientModel, UserModel, CreateUserModel, UserAuthModel, ProfileModel, InvoiceModel, UpdateClientModel, UpdateInvoiceModel, UpdateProfileModel

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

@app.get("/clients/user/", response_model=List[ClientModel])
async def getClientsByUser(searchQuery: str):
	clients = await db["clients"].find({"userId": searchQuery}).to_list(1000)
	return JSONResponse(status_code=200, content=clients)
	

@app.post("/clients/", response_description="Add new client", response_model=ClientModel)
async def createClient(client: ClientModel = Body(...)):
	try:
	    client = jsonable_encoder(client)
	    new_client = await db["clients"].insert_one(client)
	    created_client = await db["clients"].find_one({"_id": new_client.inserted_id})
	    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_client) 
	except Exception as h:
		raise HTTPException(status_code=409, detail=h)

@app.put("/clients/{id}", response_description="Update a Client", response_model=ClientModel)
async def updateClient(id: str, client: UpdateClientModel = Body(...)):
	client_details = {k: v for k, v in client.dict().items() if v is not None}
	if len(client_details) >= 1:
		update_result = await db["clients"].update_one({"_id": id}, {"$set": client_details})
		if update_result.modified_count == 1:
			updated_client = await db["clients"].find_one({"_id": id})
			if updated_client is not None:
				return JSONResponse(status_code=200, content=updated_client)
	existing_client = await db["clients"].find_one({"_id": id})
	if existing_client is not None:
		return JSONResponse(status_code=200, content=existing_client)
	raise HTTPException(status_code=404, detail=f"Client {id} not found")

@app.delete("/clients/{id}")
async def deleteClient(id: str):
	delete_client = await db["clients"].delete_one({"_id": id})
	if delete_client.deleted_count == 1:
		return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
	raise HTTPException(status_code=404, detail=f"client {id} not fount")

# invoices
@app.get("/invoices/", response_model=List[InvoiceModel])
async def getInvoicesByUser(searchQuery: str):
	invoices = await db["invoices"].find({"creator": searchQuery}).to_list(1000)
	return JSONResponse(status_code=200, content=invoices)

@app.get("/invoices/count/")
async def getTotalCount(searchQuery: str):
	total_count = await db["invoices"].count_documents({"creator": searchQuery})
	return JSONResponse(status_code=200, content=total_count) 

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

@app.put("/invoices/{id}", response_description="update an invoice", response_model=UpdateInvoiceModel)
async def updateInvoice(id: str, invoice: UpdateInvoiceModel = Body(...)):
	invoice_details = {k: v for k, v in invoice.dict().items() if v is not None}
	if len(invoice_details) >= 1:
		update_result = await db["invoices"].update_one({"_id": id}, {"$set": invoice_details})
		if update_result.modified_count == 1:
			updated_invoice = await db["invoices"].find_one({"_id": id})
			if updated_invoice is not None:
				return JSONResponse(status_code=200, content=updated_invoice)
	existing_invoice = await db["invoices"].find_one({"_id": id})
	if existing_invoice is not None:
		return JSONResponse(status_code=200, content=existing_invoice)
	raise HTTPException(status_code=404, detail=f"Invoice {id} not found") 

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
@app.get("/profiles/", response_model=ProfileModel)
async def getProfileByUser(searchQuery: str):
	profile = await db["profiles"].find_one({"userId": searchQuery})
	return JSONResponse(status_code=200, content=profile)

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

@app.post("/profiles/{id}", response_model=ProfileModel)
async def updateProfile(id: str, profile: UpdateProfileModel = Body(...)):
	profile_details = {k: v for k, v in profile.dict().items() if v is not None}
	if len(profile_details) >= 1:
		update_result = await db["profiles"].update_one({"_id": id}, {"$set": profile_details})
		if update_result.modified_count == 1:
			updated_profile = await db["profiles"].find_one({"_id": id})
			if updated_profile is not None:
				return JSONResponse(status_code=200, content=updated_profile)
	existing_profile = await db["profiles"].find_one({"_id": id})
	if existing_profile is not None:
		return JSONResponse(status_code=200, content=existing_profile)
	raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@app.delete("/profiles/{id}")
async def deleteProfile(id: str):
	delete_profile = await db["profiles"].delete_one({"_id": id})
	if delete_profile.deleted_count == 1:
		return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
	raise HTTPException(status_code=404, detail=f"profile {id} not fount")