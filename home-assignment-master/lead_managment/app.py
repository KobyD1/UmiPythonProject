from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, field_validator, model_validator
import re

app = FastAPI()

# ---------------------------------------------------------
# ONE CLASS: Model + All Validation Logic
# ---------------------------------------------------------
class Lead(BaseModel):
    BranchID: str
    WorkerCode: str | None = None
    AskedCar: str | None = None
    FirstName: str
    LastName: str
    Email: EmailStr | None = None
    Phone: str | None = None
    FromWebSite: str | None = None
    Area: str | None = None

    # -------------------------
    # BranchID must be numeric
    # -------------------------
    @field_validator("BranchID")
    def validate_branch(cls, v):
        if not v.isdigit():
            raise ValueError("BranchID must be numeric")
        return v

    # -------------------------
    # Email validation
    # -------------------------
    @field_validator("Email")
    def validate_email(cls, v):
        if v is None:
            return v

        # Block disposable domains
        disposable_domains = {
            "mailinator.com", "10minutemail.com", "tempmail.com",
            "yopmail.com", "guerrillamail.com"
        }
        domain = v.split("@")[1].lower()
        if domain in disposable_domains:
            raise ValueError("Disposable email domains are not allowed")

        # BUSINESS COMMENT:
        # Email verification is essential for automation workflows.
        # Invalid or temporary emails cause:
        #   - Failed CRM automations
        #   - Wasted marketing budget
        #   - Incorrect analytics and lead scoring
        #
        # Common 3rd‑party email validation APIs:
        #   - ZeroBounce
        #   - NeverBounce
        #   - Kickbox

        return v

    # -------------------------
    # Israeli phone validation
    # -------------------------
    @field_validator("Phone")
    def validate_phone(cls, v):
        if v is None:
            return v

        cleaned = re.sub(r"[^\d]", "", v)

        if not re.fullmatch(r"05\d{8}", cleaned):
            raise ValueError("Phone must be a valid Israeli mobile number (05X-XXXXXXX)")

        return cleaned

    # -------------------------
    # Required fields rule:
    # BranchID, FirstName, LastName, AND (Email OR Phone)
    # -------------------------
    @model_validator(mode="after")
    def validate_required(self):
        if not self.Email and not self.Phone:
            raise ValueError("Either Email or Phone is required")
        return self


# ---------------------------------------------------------
# POST endpoint
# ---------------------------------------------------------
@app.post("/api/leads")
async def create_lead(lead: Lead):
    return {"status": "success", "lead": lead.dict()}


# ---------------------------------------------------------
# GET endpoint
# ---------------------------------------------------------
@app.get("/api/leads")
async def get_leads():
    return {"message": "GET endpoint working"}