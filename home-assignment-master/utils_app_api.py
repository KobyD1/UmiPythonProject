import requests
import subprocess
import time
import sys
import globals


class UtilsAppApi():

    def __init__(self, url_base=globals.ENRICH_BASE_URL, retries=3):
        self.url_base = url_base
        self.retries = retries

    def call_enrichment_api(self, email, phone, asked_car=""):
        payload = {"email": email, "phone": phone, "asked_car": asked_car}

        print(f"Calling enrichment API, payload = {payload}")
        url = self.url_base + globals.ENRICH_URL
        delay = 1

        for attempt in range(1, self.retries + 1):
            try:
                response = requests.post(url, json=payload, timeout=5)
                response.raise_for_status()
                return response.json()

            except Exception as e:
                print(f"Enrichment attempt {attempt} , delay = {delay},failed: {e}")

                if attempt == self.retries:
                    print("Enrichment failed after retries. Continuing pipeline")
                    return None

                time.sleep(delay)
                delay *= 2

    def analyze_score_by_enrichment(self, response_body):
        score = 0
        lead_priority = response_body["data"]["lead_priority"]
        email_trust = response_body["data"]["email_insights"]["trust_level"]
        phone_verifed = response_body["data"]["phone_insights"]["verified"]

        if email_trust == "high":
            score += 20
        if phone_verifed:
            score += 20
        response_body["data"]["phone_insights"]["verified"]
        if lead_priority == "High":
            score += 40
        if lead_priority == "Medium":
            score += 20

        print(f"Score as a result of Enrichment is {score}")
        return score

    def kill_process_on_port(self, port=globals.APP_PORT):
        try:
            result = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True).decode()
            lines = result.strip().split('\n')
            for line in lines:
                if 'LISTENING' in line:
                    pid = line.strip().split()[-1]
                    print(f"Cleaning up: Killing process {pid} on port {port}")
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print(f" Port {port} is  free")

    def start_app(self):
        print("Starting APP Server")
        server_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn",
            "mock-api.main:app",
            "--host", "0.0.0.0",
            "--port", "8001"
        ])
        time.sleep(5)  # adding delay in order to get stable results in case of slow response by app. server
