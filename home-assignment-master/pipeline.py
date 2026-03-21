import utils_local
import utils_app_api

utils= utils_local.UtilsLocal()
api_mock = utils_app_api.UtilsAppApi()

lead = utils.get_lead_from_json(0)
enrichment = api_mock.call_enrichment_api(lead.get("Email"), lead.get("Phone"), lead.get("Area"))
enrichment_score = api_mock.analyze_score_by_enrichment(enrichment)
car_score = utils.analyze_score_by_car(lead["AskedCar"])
score_final=car_score+enrichment_score
assigned_final = utils.analyze_assigned_by_score(score_final,lead)
utils.set_final_enriched_lead_object(lead,enrichment,assigned_final,score_final)

print ("**** Pipeline completed successfully ****")