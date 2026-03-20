import utils_local
import api_mock_utils

utils= utils_local.UtilsLocal()
api_mock = api_mock_utils.apiMockUtils()

lead = utils.get_lead_from_json(0)
enrichment = api_mock.call_enrichment_api(lead.get("Email"), lead.get("Phone"), lead.get("Area"))
enrichment_score = api_mock.score_calc_by_enrichment(enrichment)
car_score = utils.set_car_score(lead["AskedCar"])
score_final=car_score+enrichment_score
assigned_final = utils.set_assigned_final(score_final,lead)
enrichment_final = utils.set_enrichment_final(enrichment)
utils.set_final_enriched_lead_object(lead,assigned_final,score_final,enrichment_final)

print ("Stop here ")