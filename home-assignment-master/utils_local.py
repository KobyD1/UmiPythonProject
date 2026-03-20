import pandas as pd
import json

class UtilsLocal:
    def __init__(self, path="./data/" ):
        self.path = path

    def get_car_info_by_car_model(self,car_model):
        data_frame = pd.read_excel(self.path+"cars_models_parsed.xlsx")
        row = data_frame[data_frame["Model_ID"] == car_model]
        return dict(row.iloc[0])

    def set_car_score(self,car_model):
        score=0
        car_as_dict = self.get_car_info_by_car_model(car_model)

        if ((car_as_dict["Availability"])=="In Stock"):
            score += 10

        if (car_as_dict["Category"])=="Electric":
            score += 15

        if (car_as_dict["Category"]) == "Luxury":
            score += 20
        print (f"Score after car model calculate is {score}")

        return score

    def get_lead_from_json(self,id ,file="sample_leads.json"):
        with open(self.path+file, "r", encoding="utf-8") as f:
            data = json.load(f)

        leads = data["leads"]

        print(f"lead found in {file} , lead details = {leads[id]}")
        return leads[id]

    def get_branch_by_lead(self,lead):
        branch_id = lead["BranchID"]
        data_frame = pd.read_excel(self.path + "branch_config.xlsx")
        branch = data_frame[data_frame["BranchID"] == int(branch_id)]
        return dict(branch.iloc[0])


    def set_enrichment_final(self,enrichment_data):
        # branch = self.get_branch_by_lead(lead)

        enrichment={}
        email_insights={}
        phone_insights={}
        geographic= {}
        "phone_insights"

        email_insights["trust_level"]=enrichment_data["data"]["email_insights"]['trust_level']
        phone_insights["carrier"]=enrichment_data["data"]["phone_insights"]["carrier"]
        phone_insights["verified"]=enrichment_data["data"]["phone_insights"]["verified"]

        # ": {"trust_level": "High"},
        # "geographic": {"city": "Tel Aviv", "region": "Center"},
        enrichment["email_insights"]=email_insights
        enrichment["phone_insights"]=phone_insights


        return enrichment

    def set_final_enriched_lead_object(self,lead,assigned,score,enrichment):
        branch = self.get_branch_by_lead(lead)
        branch_info = {}
        car_info = {}
        enrichment = {}

        branch_info["branch_id"] = branch["BranchID"]
        branch_info["name"] = branch["Name"]
        branch_info["Manager"] = branch["Manager"]
        branch_info["region"] = branch["Region"]

        car_row = self.get_car_info_by_car_model(lead["AskedCar"])
        car_info["model_id"] = car_row["Model_ID"]
        car_info["model_name"] = car_row["model_name"]
        car_info["category"] = car_row["Category"]
        car_info["price_range"] = car_row["price_range"]

        final_enriched_lead = {
            "original_lead": {},
            "branch_info": branch_info,
            "car_info": car_info,
            "score": score,
            "status": "processed",
            "priority": assigned["priority"]

        }
        print("******* final_enriched_lead *******")
        print(final_enriched_lead)
        print("***********************************")


    def set_assigned_final(self,score,lead):
        assigned = {}

        if score > 100:score=100
        if score > 69 :
            print ("Hot lead found - assigned to branch manager")
            assigned["priority"]="Hot"
            assigned["assigned_to"] =self.get_branch_by_lead(lead)["Manager"]

        elif score >40 :
            print ("Warm lead found - assigned to worker")
            assigned["assigned_to"] = lead["WorkerCode"]
            assigned["priority"]="Warm"


        else:
            print("Cold lead found - assigned to pool")
            assigned["assigned_to"] = "pool"
            assigned["priority"]="Cold"

        return assigned



# {
#   "original_lead": { ... },
#   "branch_info": {
#     "branch_id": "400",
#     "name": "Tel Aviv Showroom",
#     "manager": "David Cohen",
#     "region": "Center"
#   },
#   "car_info": {
#     "model_id": "90962_101",
#     "model_name": "U-Tour",
#     "category": "SUV",
#     "price_range": "165,000 - 185,000 ILS"
#   },
#   "enrichment": {
#     "geographic": {"city": "Tel Aviv", "region": "Center"},
#     "email_insights": {"trust_level": "High"},
#     "phone_insights": {"carrier": "Orange", "verified": true},
#     "lead_priority": "High"
#   },
#   "score": 85,
#   "priority": "HOT",
#   "assigned_to": "David Cohen",
#   "status": "processed"
# }