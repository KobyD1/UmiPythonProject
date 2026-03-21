Solution for Car Dealer Lead Processing Automation
Setup Instruction
provide test data with relevant information located as define at globals.py file (default value is /data)
in case of local running without Docker :
Python installation
all modules as define at requirement.txt file or by running in root folder PIP install -r ./requirments.text
3. in case of docker :

docker should be installed
running commands :
run : docker-compose up --build .

build pipeline only : docker build -t pipeline .

run pipeline only :docker run pipeline

API
General

URL prefix : http://mock-api:8001

Auth. : None

Headers : Content-Type-application/json (other keys at default value )

in order to get enrichment info
**Method :**Post

URL suffix : /api/enrich

Body (according the following example) :

{


"Email": "danny.cohen@gmail.com",

"Phone": "0542100319",

"asked_car":"90962_101",

"Area": "1"

}

Response example :

{

"enriched": true,

"data": {

"customer_profile": {

"likely_first_time_buyer": true,

"interest_level": "Medium",

"recommended_contact_time": "Evening (16-19)"

},

"lead_priority": "Low",

"enriched_at": "2026-03-21T09:21:49.541347+00:00"

},

"error": null

}

Implement decisions
implemented in modular way according :
pipline - the main part of the pipeline

utils class for any part (API and general)

globals - for globals parameters

2. files not found - will send default values

3. the pipeline run only over the first lead - can be set by globals (LEAD_ID) , or go over all leads by adding loop

4. cars data into cars model file converted to EXCEL file with import details only - more easy to handle

5. Postman collection for testing is in : data/umi.postman_collection.json 

6. Stability : the pipe line start and stop with killing port 8001

retry with delay for the API request

7. Maintenance:

default values in case of coding error at some critical methods

logs per each method with information

comments adding


