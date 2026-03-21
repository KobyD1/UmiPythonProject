import pandas as pd
import json
import globals


class UtilsLocal:
    def __init__(self, path=globals.PATH_DATA):
        self.path = path

    def get_car_info_by_car_model(self, car_model):

        try:

            data_frame = pd.read_excel(self.path + "cars_models_parsed.xlsx")

            row = data_frame[data_frame["Model_ID"] == car_model]
            return dict(row.iloc[0])


        except Exception as e:
            print("Something went wrong at car model set it at default values ")
            default_car = {
                'Availability': 'In Stock',
                'Category': 'SUV',
                'Model_ID': '90962_101',
                'model_name': 'U-Tour',
                'price_range': '165,000 - 185,000 ILS'
            }
            return default_car

    def analyze_score_by_car(self, car_model):
        score = 0
        car_as_dict = self.get_car_info_by_car_model(car_model)

        if ((car_as_dict["Availability"]) == "In Stock"):
            score += 10

        if (car_as_dict["Category"]) == "Electric":
            score += 15

        if (car_as_dict["Category"]) == "Luxury":
            score += 20
        print(f"Score after car model calculate is {score}")

        return score

    def get_lead_from_json(self, id, file="sample_leads.json"):
        with open(self.path + file, "r", encoding="utf-8") as f:
            data = json.load(f)

        leads = data["leads"]

        print(f"lead found in {file} , lead details = {leads[id]}")
        return leads[id]

    def get_branch_info_by_lead(self, lead):
        try:
            branch_id = lead["BranchID"]
            data_frame = pd.read_excel(self.path + "branch_config.xlsx")
            if branch_id not in data_frame["BranchID"].values:
                branch_id = 400
            branch = data_frame[data_frame["BranchID"] == int(branch_id)]
            return dict(branch.iloc[0])
        except Exception as e:
            print("Something went wrong at getting branch set it at default values branch ID=400")
            default_branch = {'Address': 'Menachem Begin Rd 132, Tel Aviv',
                              'BranchID': 400,
                              'City': 'Tel Aviv',
                              'Email': 'telaviv@dealership.co.il',
                              'Languages': 'Hebrew, English, Russian',
                              'Manager': 'David Cohen',
                              'Name': 'Tel Aviv Showroom',
                              'Phone': '03-5551234',
                              'Region': 'Center',
                              'Specialties': 'Luxury, Electric, SUV',
                              'Working Hours': 'Sun-Thu 9:00-19:00, Fri 9:00-14:00'
                              }
            return default_branch

    def analyze_assigned_by_score(self, score, lead):
        assigned = {}

        if score > 100: score = 100
        if score > globals.HOT_SCORE_LIMIT:
            print("Hot lead found - assigned to branch manager")
            assigned["priority"] = "Hot"
            assigned["assigned_to"] = self.get_branch_info_by_lead(lead)["Manager"]

        elif score > globals.WARM_SCORE_LIMIT:
            print("Warm lead found - assigned to worker")
            assigned["assigned_to"] = lead["WorkerCode"]
            assigned["priority"] = "Warm"

        else:
            print("Cold lead found - assigned to pool")
            assigned["assigned_to"] = "pool"
            assigned["priority"] = "Cold"

        return assigned

    def set_final_enriched_lead_object(self, lead, enrichment_data, assigned, score):

        branch = self.get_branch_info_by_lead(lead)
        car_row = self.get_car_info_by_car_model(lead["AskedCar"])
        branch_info = {}
        car_info = {}
        # define final message /branch part
        branch_info["branch_id"] = str(branch["BranchID"])
        branch_info["name"] = branch["Name"]
        branch_info["Manager"] = branch["Manager"]
        branch_info["region"] = branch["Region"]

        # define final message /car part

        car_info["model_id"] = car_row["Model_ID"]
        car_info["model_name"] = car_row["model_name"]
        car_info["category"] = car_row["Category"]
        car_info["price_range"] = car_row["price_range"]

        # define final message /enrichment part
        enrichment = {}
        geographic = {}
        email_insights = {}
        phone_insights = {}

        email_insights["trust_level"] = enrichment_data["data"]["email_insights"]['trust_level']
        phone_insights["carrier"] = enrichment_data["data"]["phone_insights"]["carrier"]
        phone_insights["verified"] = enrichment_data["data"]["phone_insights"]["verified"]

        geographic["region"] = branch["Region"]
        geographic["city"] = branch["City"]

        enrichment["email_insights"] = email_insights
        enrichment["phone_insights"] = phone_insights

        # integration of all parts
        final_enriched_lead = {
            "original_lead": {},
            "branch_info": branch_info,
            "car_info": car_info,
            "enrichment": enrichment,
            "score": score,
            "priority": assigned["priority"],
            "assigned_to": assigned["assigned_to"],
            "status": "processed"

        }
        print("********** final_enriched_lead **********")
        print(final_enriched_lead)
        print("*****************************************")
