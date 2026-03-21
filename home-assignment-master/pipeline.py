
import utils_local
import utils_app_api
import globals


def run_pipeline():

    utils = utils_local.UtilsLocal()
    app_api = utils_app_api.UtilsAppApi()
    app_api.kill_process_on_port(globals.APP_PORT)
    app_api.start_app()

    print("**** Executing Pipeline Logic ****")
    lead = utils.get_lead_from_json(0)
    enrichment = app_api.call_enrichment_api(lead.get("Email"), lead.get("Phone"), lead.get("Area"))
    enrichment_score = app_api.analyze_score_by_enrichment(enrichment)
    car_score = utils.analyze_score_by_car(lead["AskedCar"])
    score_final = car_score + enrichment_score
    assigned_final = utils.analyze_assigned_by_score(score_final, lead)
    utils.set_final_enriched_lead_object(lead, enrichment, assigned_final, score_final)
    print("**** Pipeline completed successfully ****")

    app_api.kill_process_on_port(globals.APP_PORT)

if __name__ == "__main__":
    run_pipeline()