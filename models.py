from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from bson import ObjectId
from datetime import date

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ClientModel(BaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	name: str
	email: EmailStr
	phone: str
	address: Optional[str]
	userId: List[str] = []
	createdAt: Optional[date] = date.today()
	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders = {ObjectId: str}
		schema_extra = {
			"example": {
				"name": "Jane Doe",
				"email": "jdoe@example.com",
				"phone": "7891009270",
				"address": "fatehpur",
				"createdAt": date.today()
            }
        }
		
class UserModel(BaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	name: str = Field(...)
	email: EmailStr = Field(...)
	password: str = Field(...)
	resetToken: str 
	expireToken: date 

class ProfileModel(BaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	name: str
	email: EmailStr
	phoneNumber: str
	businessName: str
	contactAddress: str
	paymentDetails: str 
	logo: str
	website: str
	userId: List[str] = []

class Item(BaseModel):
	itemName: str 
	unitPrice: str 
	quantity: str 
	discount: str 

class Client(BaseModel):
	name: str  
	email: str  
	phone: str  
	address: str 

class Record(BaseModel):
	amountPaid: int 
	datePaid: date 
	paymentMethod: str  
	note: str 
	paidBy: str 
    
class InvoiceModel(BaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	dueDate: Optional[date]
	currency: str
	items: List[Item]
	rates: str 
	vat: int 
	total: int 
	subTotal: int 
	notes: int 
	status: int 
	invoiceNumber: int 
	type: str 
	creator: List[str]
	totalAmountReceived: int 
	client: Client
	paymentRecords: List[Record]
	createdAt: Optional[date] = date.today()