import subprocess
import time
import sys
import utils_local
import utils_app_api


def run_pipeline():
    utils = utils_local.UtilsLocal()
    app_api = utils_app_api.UtilsAppApi()
    app_api.kill_process_on_port(8001)

    print("Starting Mock API Server")
    server_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "mock-api.main:app",
        "--host", "0.0.0.0",
        "--port", "8001"
    ])

    time.sleep(3)  # adding delay in order to get stable results in case of slow response by app. server

    print("**** Executing Pipeline Logic ****")

    lead = utils.get_lead_from_json(0)
    enrichment = app_api.call_enrichment_api(lead.get("Email"), lead.get("Phone"), lead.get("Area"))
    enrichment_score = app_api.analyze_score_by_enrichment(enrichment)
    car_score = utils.analyze_score_by_car(lead["AskedCar"])
    score_final = car_score + enrichment_score
    assigned_final = utils.analyze_assigned_by_score(score_final, lead)
    utils.set_final_enriched_lead_object(lead, enrichment, assigned_final, score_final)
    app_api.kill_process_on_port(8001)
    print("**** Pipeline completed successfully ****")

if __name__ == "__main__":
    run_pipeline()