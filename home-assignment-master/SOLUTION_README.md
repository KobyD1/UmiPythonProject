# Solution for Car Dealer Lead Processing Automation Setup

### Instruction

&#x20;   1. provide test data with relevant information located as define at globals.py file (default value is /data)

&#x20;   2. in case of port is in use run the following command by PowerShell 

&#x20;       Stop-Process -Id (Get-NetTCPConnection -LocalPort 8001).OwningProcess -Force

&#x20;   3. in case of local running without Docker : 

&#x20;       Install Python 

&#x20;      install all modules as define at requirement.txt file or by running in root folder PIP install -r ./requirements.txt

&#x20;   4. in case of docker :

&#x20;        docker should be installed

&#x20;        docker  commands

&#x20;        run : docker-compose up --build .

&#x20;        build pipeline only : docker build -t pipeline .

&#x20;        run pipeline only :docker run pipeline





### API

Mock

&#x20;Method :Post

URL  : http://mock-api:8001/api/enrich



Headers : Content-Type-application/json (other keys at default value )

Auth. : None

Body:

{

&#x20; "email": "test@example.com",

&#x20; "phone": "0542100319",

&#x20; "area": "1"

}



&#x20;Leads

&#x20;Method :Post

URL  : http://127.0.0.1:8000/api/leads

Headers : Content-Type-application/json (other keys at default value )

Auth. : None



Body (according the following example) :



{

&#x20;   "BranchID": "400",

&#x20;   "WorkerCode": "910290",

&#x20;   "AskedCar": "90962\_101",

&#x20;   "FirstName": "ניר",

&#x20;   "LastName": "פריידי",

&#x20;   "Email": "customer@example.com",

&#x20;   "Phone": "0542100319",

&#x20;   "FromWebSite": "forthing",

&#x20;   "Area": "1"

}



### Implement decisions

&#x20;1. implemented in modular way according :

pipline - the main part of the pipeline

utils class for any part (API and general)

globals - for globals parameters



2\. files not found - will send default values



3\. the pipeline run only over the first lead - can be set by globals (LEAD\_ID) , or go over all leads by adding loop



4\. cars data into cars model file converted to EXCEL file with import details only - more easy to handle



5\. Stability :

the pipe line start and stop with killing port 8001

retry with delay for the API request



6\. Maintenance:

default values in case of coding error at some critical methods

logs per each method with information

comments adding



7\. Postman collection for testing is in : data/umi.postman\_collection.json



### General 



1\. Explain for business benefits (step 2) by comments in app.phy file



