from pydantic import BaseModel, EmailStr, field_validator, model_validator

class LeadCreate(BaseModel):
    BranchID: str
    WorkerCode: str | None = None
    AskedCar: str | None = None
    FirstName: str
    LastName: str
    Email: EmailStr | None = None
    Phone: str | None = None
    FromWebSite: str | None = None
    Area: str | None = None

    # BranchID numeric
    @field_validator("BranchID")
    def validate_branch(cls, v):
        return LeadValidator.validate_branch_id(v)

    # Email validation
    @field_validator("Email")
    def validate_email(cls, v):
        return LeadValidator.validate_email(v)

    # Phone validation
    @field_validator("Phone")
    def validate_phone(cls, v):
        return LeadValidator.validate_phone(v)

    # Required fields rule
    @model_validator(mode="after")
    def validate_required(cls, values):
        return LeadValidator.validate_required_fields(values)