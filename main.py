from fastapi import FastAPI

app = FastAPI()

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

@app.post("/clients/")
def createClient():
	pass 

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

@app.pust("/profiles/{id}")
def updateProfile(id: int):
	pass 

@app.delete("/profiles/{id}")
def deleteProfile(id: int):
	pass 