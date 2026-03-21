import subprocess
import time
import sys
import os
import requests
import utils_local
import utils_app_api

def kill_process_on_port(port):
    try:
        result = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True).decode()
        lines = result.strip().split('\n')
        for line in lines:
            if 'LISTENING' in line:
                pid = line.strip().split()[-1]
                print(f"--- Cleaning up: Killing process {pid} on port {port} ---")
                subprocess.run(f"taskkill /F /PID {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(f"--- Port {port} is already free ---")

def run_pipeline():
    kill_process_on_port(8001)

    print("--- Starting Mock API Server ---")
    server_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "mock-api.main:app",
        "--host", "0.0.0.0",
        "--port", "8001"
    ])


    time.sleep(3)

    print("**** Executing Pipeline Logic ****")
    utils = utils_local.UtilsLocal()
    api_mock = utils_app_api.UtilsAppApi()
    lead = utils.get_lead_from_json(0)
    enrichment = api_mock.call_enrichment_api(lead.get("Email"), lead.get("Phone"), lead.get("Area"))
    enrichment_score = api_mock.analyze_score_by_enrichment(enrichment)
    car_score = utils.analyze_score_by_car(lead["AskedCar"])
    score_final = car_score + enrichment_score
    assigned_final = utils.analyze_assigned_by_score(score_final, lead)
    utils.set_final_enriched_lead_object(lead, enrichment, assigned_final, score_final)
    kill_process_on_port(8001)
    print("**** Pipeline completed successfully ****")

if __name__ == "__main__":
    run_pipeline()