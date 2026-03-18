from pydantic import BaseModel


class leadJson(BaseModel):
    BranchID: str
    WorkerCode: str
    AskedCar: str
    FirstName: str
    LastName: str
    Email: str
    Phone: str
    FromWebSite: str
    Area: str
