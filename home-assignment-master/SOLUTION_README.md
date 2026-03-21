# Solution for  Car Dealer Lead Processing Automation 

##### *Setup Instruction* 

1. provide test data with relevant information located as define at globals.py file (default value is **/data**)
2. in case of local running without Docker  : 
* &#x20;Python installation 
* all modules as define at requirement.txt file or by running in root folder  **PIP install -r ./requirments.text** 

3\. in case of docker : 

* docker should be installed 
* running commands :

&#x20;        run : docker-compose up --build .

&#x20;        build pipeline only : docker build -t pipeline .

&#x20;        run pipeline only :docker run pipeline





##### *API*

General 

URL prefix : **http://mock-api:8001** 

Auth.  : None

Headers : Content-Type-application/json (other keys at default value )



* in order to get enrichment info 

**Method :**Post 

**URL suffix :** /api/enrich

**Body (according the following example)** : 

{

&#x20;   

&#x20;   "Email": "danny.cohen@gmail.com",

&#x20;   "Phone": "0542100319",

&#x20;   "asked\_car":"90962\_101",

&#x20;   "Area": "1"

}



**Response example**  :



{

&#x20;   "enriched": true,

&#x20;   "data": {

&#x20;       "customer\_profile": {

&#x20;           "likely\_first\_time\_buyer": true,

&#x20;           "interest\_level": "Medium",

&#x20;           "recommended\_contact\_time": "Evening (16-19)"

&#x20;       },

&#x20;       "lead\_priority": "Low",

&#x20;       "enriched\_at": "2026-03-21T09:21:49.541347+00:00"

&#x20;   },

&#x20;   "error": null

}

##### *Implement decisions* 



1. implemented in modular way according : 

&#x20;pipline - the main part of the pipeline 

utils class for any part (API and general)

globals - for globals parameters

2\. files not found - will send default values 

3\. the pipeline run only over the first lead - can be set by globals (LEAD\_ID) , or go over all leads  by adding loop 

4\. cars data into cars model file  converted  to EXCEL file with import details only  - more easy to handle 

5\. Postman collection  for testing is in : data/umi.postman\_collection.json

6\. Stability :
the pipe line start and stop with killing port 8001 

retry with delay for the API request 

7\. Maintenance: 

&#x20;default values in case of coding error at some critical methods

logs per each method with information 

comments adding 







&#x20;





