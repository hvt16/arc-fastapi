from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any 
import motor.motor_asyncio
from models import ClientModel, UserModel, CreateUserModel, UserAuthModel, ProfileModel, InvoiceModel, UpdateClientModel, UpdateInvoiceModel, UpdateProfileModel
import json
import math

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
	return jsonable_encoder({"result":"server is running"})

# client part
@app.get("/clients/", response_description="List of clients")
async def getClients(page: int = 1):
	limit = 8
	start_index = (page-1)*limit
	try:
		total = await db["clients"].estimated_document_count()
		clients = await db["clients"].find().to_list(limit)
		return jsonable_encoder({
				"data": clients,
				"currentPage": page,
				"numberOfPages": math.ceil(total/limit)
			})
	except Exception as e:
		return JSONResponse(status_code=404, content=jsonable_encoder({
				"message": e
			}))
		# raise HTTPException(status_code=404, detail=e)

@app.get("/clients/user")
async def getClientsByUser(searchQuery: str):
	print('inside get clients by user')
	try:
		clients = await db["clients"].find({"userId": searchQuery}).to_list(1000)
		return JSONResponse(status_code=200, content= jsonable_encoder({
				"data": clients
			}))
	except Exception as e:
		return JSONResponse(status_code=404, content=jsonable_encoder({
				"message": e
			}))
		# raise HTTPException(status_code=404, detail=e)
	

@app.post("/clients/", response_description="Add new client")
async def createClient(client: ClientModel = Body(...)):
	try:
	    client = jsonable_encoder(client)
	    new_client = await db["clients"].insert_one(client)
	    created_client = await db["clients"].find_one({"_id": new_client.inserted_id})
	    return JSONResponse(status_code=201, content= jsonable_encoder(created_client)) 
	except Exception as h:
		return JSONResponse(status_code=409, content=jsonable_encoder({
				"message": e
			}))
		# raise HTTPException(status_code=409, detail=h)

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
		return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=jsonable_encoder({
				"message": "client deleted successfully"
			}))
	raise HTTPException(status_code=404, detail=f"client {id} not fount")

# invoices
@app.get("/invoices")
async def getInvoicesByUser(searchQuery: str):
	try:
		invoices = await db["invoices"].find({"creator": searchQuery}).to_list(1000)
		return JSONResponse(status_code=200, content=jsonable_encoder({
			"data":invoices
			}))
	except Exception as e:
		return JSONResponse(status_code=404, content=jsonable_encoder({
				"message": e
			}))

@app.get("/invoices/count/")
async def getTotalCount(searchQuery: str):
	try:
		total_count = await db["invoices"].count_documents({"creator": searchQuery})
		return JSONResponse(status_code=200, content= jsonable_encoder(total_count) ) 
	except Exception as e:
		return JSONResponse(status_code=404, content=jsonable_encoder({
				"message" : e
			}))

@app.get("/invoices/{id}")
async def getInvoice(id: str):
	invoice = await db["invoices"].find_one({"_id": id})
	if invoice is not None:
		return JSONResponse(status_code=200, content=invoice)
	raise HTTPException(status_code=400, detail="invoice does not exist")

@app.post("/invoices", response_description="create invoice")
async def createInvoice(invoice: Dict[Any, Any] = Body(...)):
	# print(invoice)
	# invoice = jsonable_encoder(invoice)
	# print(invoice)
	try:
		print("inside try")
		new_invoice = await db["invoices"].insert_one(invoice)
		created_invoice = await db["invoices"].find_one({"_id": new_invoice.inserted_id})
		print("new invoice",created_invoice)
		# return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(
		# 	{
		# 		"newInvoice": created_invoice
		# 	}))
		return JSONResponse(status_code=201, content=jsonable_encoder(created_invoice))
		
	except Exception as e:
		print("Exception occured")
		return JSONResponse(status_code=404, content=jsonable_encoder({
				"message": "why this ?"
			}))

@app.put("/invoices/{id}", response_description="update an invoice")
async def updateInvoice(id: str, invoice: UpdateInvoiceModel = Body(...)):
	invoice_details = {k: v for k, v in invoice.dict().items() if v is not None}
	if len(invoice_details) >= 1:
		update_result = await db["invoices"].update_one({"_id": id}, {"$set": invoice_details})
		if update_result.modified_count == 1:
			updated_invoice = await db["invoices"].find_one({"_id": id})
			if updated_invoice is not None:
				return JSONResponse(status_code=200, content=jsonable_encoder(updated_invoice))
	existing_invoice = await db["invoices"].find_one({"_id": id})
	if existing_invoice is not None:
		return JSONResponse(status_code=200, content=jsonable_encoder(existing_invoice))
	raise HTTPException(status_code=404, detail=f"Invoice {id} not found") 

@app.delete("/invoices/{id}")
async def deleteInvoice(id: str):
	delete_invoice = await db["invoices"].delete_one({"_id": id})
	if delete_invoice.deleted_count == 1:
		return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=jsonable_encoder({
				"message": "invoice delted successfully"
			}))
	raise HTTPException(status_code=404, detail=f"invoice {id} not fount")


# users
@app.post("/users/signin/", response_description="Signin user")
async def signin(auth_user: UserAuthModel = Body(...)):
	auth_user_json = jsonable_encoder(auth_user)
	# print(auth_user_json)
	try:
		# print("finding existing user")
		existingUser = await db["users"].find_one({"email":auth_user_json["email"]})
		# print("existing user found")
		# print("finding user profile")
		userProfile = await db["profiles"].find_one({"userId":existingUser["_id"]})
		# print("user profile found")
		if not existingUser:
			# print("not existingUser")
			return JSONResponse(status_code=404, content=jsonable_encoder({
					"message": "user doesn't exist"
				}))
		# print("checking password")
		if auth_user_json["password"] != existingUser["password"]:
			# print("password mismatch")
			return JSONResponse(status_code=400, content=jsonable_encoder({
					"message": "invalid credentials"
				}))
		# print("returing")
		return JSONResponse(status_code=200, content=jsonable_encoder({
				"result": existingUser,
				"userProfile": userProfile,
				"token": ""
			}))
		# if find_user is not None and auth_user_json["password"] == find_user["password"]:
		# 	userProfile = await db["profiles"].find_one({"userId":auth_user_json["_id"]})
		# 	if userProfile is not None:

		# 		return JSONResponse(status_code=200, content=jsonable_encoder({
		# 				"result": find_user,
		# 				"userProfile": userProfile,
		# 				"token": ""
		# 			}))
		# 	else:
		# 		return JSONResponse(status_code=500,content=jsonable_encoder({
		# 				"message": "profile details not found"
		# 			}))
		# else:
		# 	JSONResponse(status_code=400, content=jsonable_encoder({
		# 			"message": "invalid credentilas"
		# 		}))
	except Exception as e:
		return JSONResponse(status_code=500, content=jsonable_encoder({
				"message": "error occured"
			}))
	raise HTTPException(status_code=400, detail="user not found")

@app.post("/users/signup/", response_description="Add new User")
async def signup(_user: CreateUserModel = Body(...)):
	user = UserModel(email=_user.email, name=_user.firstName + " " + _user.lastName, password=_user.password)
	user = jsonable_encoder(user)
	try:
		new_user = await db["users"].insert_one(user)
		created_user = await db["users"].find_one({"_id": new_user.inserted_id})
		userProfile = await db["profiles"].find_one({"userId": created_user["_id"]})
		return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder({
				"result": created_user,
				"userProfile": userProfile,
				"token": ""
			}))
	except Exception as e:
		return JSONResponse(status_code=500, content=jsonable_encoder({
				"message": e
			}))

@app.post("/users/forgot/")
def forgotPassword():
	pass 

@app.post("/users/reset/")
def resetPassword():
	pass 

# profiles
@app.get("/profiles/")
async def getProfileByUser(searchQuery: str):
	try:
		profile = await db["profiles"].find_one({"userId": searchQuery})
		return JSONResponse(status_code=200, content=jsonable_encoder({
				"data": profile
			}))
	except Exception as e:
		return JSONResponse(status_code=404, content=jsonable_encoder({
				"message": e 
			}))

@app.get("/profiles/{id}")
async def getProfile(id: str):
	try:
		profile = await db["profiles"].find_one({"_id": id})
		return JSONResponse(status_code=200, content=jsonable_encoder(profile))
	except Exception as e:
		return JSONResponse(status_code=404, content=jsonable_encoder({
				"message":  e 
			}))
	if profile is not None:
		return JSONResponse(status_code=200, content=profile)
	raise HTTPException(status_code=400, detail="profile does not exist")

@app.post("/profiles/")
async def createProfile(profile: ProfileModel = Body(...)):
	profile = jsonable_encoder(profile)
	try:
		new_profile = await db["profiles"].insert_one(profile)
		created_profile = await db["profiles"].find_one({"_id": new_profile.inserted_id})
		return JSONResponse(status_code=201, content=jsonable_encoder(created_profile))
	except Exception as e:
		return JSONRespons(status_code=409, content=jsonable_encoder({
				"message": e 
			}))

@app.post("/profiles/{id}", response_model=ProfileModel)
async def updateProfile(id: str, profile: UpdateProfileModel = Body(...)):
	profile_details = {k: v for k, v in profile.dict().items() if v is not None}
	if len(profile_details) >= 1:
		update_result = await db["profiles"].update_one({"_id": id}, {"$set": profile_details})
		if update_result.modified_count == 1:
			updated_profile = await db["profiles"].find_one({"_id": id})
			if updated_profile is not None:
				return JSONResponse(status_code=200, content=jsonable_encoder(updated_profile))
	existing_profile = await db["profiles"].find_one({"_id": id})
	if existing_profile is not None:
		return JSONResponse(status_code=200, content=jsonable_encoder(existing_profile))
	raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@app.delete("/profiles/{id}")
async def deleteProfile(id: str):
	delete_profile = await db["profiles"].delete_one({"_id": id})
	if delete_profile.deleted_count == 1:
		return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=jsonable_encoder({
				"message": "profile deleted succesfully"
			}))
	raise HTTPException(status_code=404, detail=f"profile {id} not fount")