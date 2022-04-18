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
	createdAt: Optional[date]
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

class UpdateClientModel(BaseModel):
	name: Optional[str]
	email: Optional[EmailStr]
	phone: Optional[str]
	address: Optional[str]
	userId: List[str] = []
	class Config:
		arbitrary_types_allowed = True
		json_encoders = {ObjectId: str}
		schema_extra = {
			"example": {
				"name": "Jane Doe",
				"email": "jdoe@example.com",
				"phone": "7891009270",
				"address": "fatehpur"
            }
        }
		
class UserModel(BaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	name: str = Field(...)
	email: EmailStr = Field(...)
	password: str = Field(...)
	resetToken: Optional[str] 
	expireToken: Optional[date] 
	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders = {ObjectId: str}
		schema_extra = {
			"example": {
				"name": "Jane Doe",
				"email": "jdoe@example.com",
				"password": "password"
            }
        }


class CreateUserModel(BaseModel):
	email: EmailStr = Field(...)
	password: str 
	confirmPassword: str 
	firstName: str 
	lastName: str 
	bio: str 
	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		schema_extra = {
			"example": {
				"email": "jdoe@example.com",
				"password": "password",
				"confirmPassword": "confirmPassword",
				"firstName": "firstName",
				"lastName": "lastName",
				"bio": "bio"
            }
        }

class UserAuthModel(BaseModel):
	email: EmailStr = Field(...)
	password: str = Field(...)
	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True 
		schema_extra = {
			"example": {
				"email": "harsh@gmail.com",
				"password": "password"
			}
		}

class ProfileModel(BaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	name: str
	email: EmailStr
	phoneNumber: Optional[str]
	businessName: Optional[str]
	contactAddress: Optional[str]
	paymentDetails: Optional[str]
	logo: Optional[str]
	website: Optional[str]
	userId: List[str] = []
	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True 
		json_encoders = {ObjectId: str}
		schema_extra = {
			"example": {
				"name": "harsh",
				"email": "harsh@gmail.com",
				"phoneNumber": "7894561230",
				"contactAddress": "address"
			}
		}

class UpdateProfileModel(BaseModel):
	name: Optional[str]
	email: Optional[EmailStr]
	phoneNumber: Optional[str]
	businessName: Optional[str]
	contactAddress: Optional[str]
	paymentDetails: Optional[str]
	logo: Optional[str]
	website: Optional[str]
	userId: List[str] = []
	class Config:
		arbitrary_types_allowed = True 
		json_encoders = {ObjectId: str}
		schema_extra = {
			"example": {
				"name": "harsh",
				"email": "harsh@gmail.com",
				"phoneNumber": "7894561230",
				"contactAddress": "address"
			}
		}

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
	items: List[Item] = []
	rates: str 
	vat: int 
	total: int 
	subTotal: int 
	notes: Optional[int] 
	status: Optional[int]
	invoiceNumber: Optional[int]
	type: Optional[str]
	creator: List[str] = []
	totalAmountReceived: Optional[int] 
	client: Optional[Client] = None
	paymentRecords: List[Record] = []
	createdAt: Optional[str] = str(date.today())
	class Config:
		allow_population_by_field_name=True
		arbitrary_types_allowed=True
		json_encoders={ObjectId:str}
		schema_extra={
			"example" : {
				"currency": "inr",
				"rates": "100",
				"vat": "100",
				"total": 1000,
				"subTotal": 1500,
			}
		}

class UpdateInvoiceModel(BaseModel):
	dueDate: Optional[date]
	currency: Optional[str]
	items: List[Item] = []
	rates: Optional[str] 
	vat: Optional[int] 
	total: Optional[int] 
	subTotal: Optional[int] 
	notes: Optional[int] 
	status: Optional[int]
	invoiceNumber: Optional[int]
	type: Optional[str]
	creator: List[str] = []
	totalAmountReceived: Optional[int] 
	client: Optional[Client] = None
	paymentRecords: List[Record] = []
	createdAt: Optional[str] = str(date.today())
	class Config:
		arbitrary_types_allowed=True
		json_encoders={ObjectId:str}
		schema_extra={
			"example" : {
				"currency": "inr",
				"rates": "100",
				"vat": "100",
				"total": 1000,
				"subTotal": 1500,

			}
		}