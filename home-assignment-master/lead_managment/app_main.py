from fastapi import FastAPI
from lead_json import leadJson

app = FastAPI()
class LeadCreate():


    @app.post("/api/leads")
    async def create_lead(lead: leadJson):
        print("Received lead:", lead.dict())

        return {"status": "success", "received": lead.dict()}

    # add get  for getting lead data as an infra in case of DB availble

    @app.get("/api/leads/{lead_id}")
    async def get_lead(lead_id: int):
        return {"lead_id": lead_id}