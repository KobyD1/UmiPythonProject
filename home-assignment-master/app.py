from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, field_validator, model_validator
import re

app = FastAPI()


class Lead(BaseModel):
    BranchID: int  # define as an int instead of str , in order to match only digits rule
    WorkerCode: str
    AskedCar: str
    FirstName: str
    LastName: str
    Email: EmailStr
    Phone: str
    FromWebSite: str
    Area: str

    # Email verification is essential for automation workflows.
    # Invalid  emails cause:
    #   - Failed CRM automations
    #   - Wasted marketing budget
    #   - Incorrect analytics and lead scoring
    #
    # Common 3rd‑party email validation APIs:
    #   - ZeroBounce
    #     benefits of ZeroBounce
    # verify that an email address actually exist
    # detect disposable emails
    #  Identifies spam and high risk addresses

    @field_validator("Email")
    def validate_email(cls, email):
        if email is None:
            return email
        return email

    @field_validator("Phone")
    def validate_phone(cls, phone):
        if phone is None:
            return phone

        cleaned = re.sub(r"[^\d]", "", phone)

        if not re.fullmatch(r"05\d{8}", cleaned):
            raise ValueError("Phone must be a valid Israeli mobile number (05X-XXXXXXX)")

        return phone

    @model_validator(mode="after")
    def validate_required(self):
        if not self.Email and not self.Phone:
            raise ValueError("Either Email or Phone is required")
        return self


@app.post("/api/leads")
async def create_lead(lead: Lead):
    return {"status": "success", "lead": lead}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
