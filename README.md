# BasicLogSystem
About:
This project involves developing a web service designed to collect and analyze log data.
The service will provide an endpoint for receiving log entries, processing them to identify
key information, and offering functionalities for managing and retrieving analysis results.

## General Structure
+ Database is built on 4 models: **IssueBin** (representing a project), **Issue**, **Log** and **Occurrence**. Each of them contain foreign key to previous one.   
+ When new log is ingested, a ticket (Issue), connected to a project(IssueBin) is created. Data is split into lines, filtered for relevant ones and each new Log object is linked to a ticket.  
+ However, before ticket is created, methods checks if a ticket linked to the same project with the same raw log doesn't alread exist in the database.  
+ If that is the case, new occurrence object is created (storing current datetime) and attached to the existing ticket  
+ Webinterface allows to list of the projects, list all the tickets linked to each project and view specific tickets and it's components (status (Open, In progress, Resolved, Closed, Suspended), occurrences, logs)


## Goal Checklist
### Core
- [X] Log Ingestion  
Ticket API accepts logs in a form of plain text, file references and JSON files (that one still has problem with enconding).   
Input size is limited by Django buitl-in fuctionality.    
- [X] Log Processing  
Ticket ingestion function goes trough the payload line by line and looks for keywords(error, warning, callstack etc.). Saves lines containing them.  
- [X] Log Separation  
This is more or less Django built in feature  
- [X] Implementation Language  
Python using Django and DRF libraries  
- [X] Development Timeline (2 weeks)  
Task received on 15.05, delivered on 28th  

### Bonus
- [X] Containerization  
"Production" version of the app deploys to containers suing dockerfile and compose file  
- [X] Data Persistence  
All the data is stored in postgres database (or sqlite3 in development)  
- [X] Issue Deduplication  
Ingestion method compares raw logs and if it finds a match in the database, it simply adds a record of new occurrence rather than creating more tickets and logs  
- [X] Web Interfacev
There is a website. It's a bit basic, but it provides all the necessary funcionalities.  
- [ ] RESTful API  
I got most of them and some extra. One missing is filtering by status.   
Moreover, due to the way data is structured (logs/lines don't store time individually), datetime retrieved from them is the same for entire ticket.  


## Installation (container/"production")
Host machine requires:

+ docker.io
+ docker compose 
+ git (to clone this repo)
+ any requirements apps above have to run.  

You'll also need **sudo/admin permissions** on the machine (to run docker) and make sure **port 8000** is not being used.

## Setup (local/development)
Install python (tested on 3.12) 
Run commands listed below, from implied locations.
```
<root_folder>\BasicLogSystem>python -m venv .venv
<root_folder>\BasicLogSystem>.venv\Scripts\activate
(.venv) <root_folder>\BasicLogSystem>pip install -r requirements.txt
(.venv) <root_folder>\BasicLogSystem>python manage.py migrate
(.venv) <root_folder>\BasicLogSystem>python manage.py createsuperuser
```

## Configuration 
For **local**, just modify BasicLogSystem/BasicLogSystem/settings/local.py  
For **"production"**, it's BasicLogSystem/BasicLogSystem/settings/production.py 
To run in production, you need to set env.Pipeline to "production". This is set by default by docker-compose in the provided configuration. 
There are also enviroment variables set in docker-compose file that you can change before launch.  
> [!CAUTION]
>Make sure to change default credentials listed there before making this public.**  

## Running ("Production")

To start the service, open command line in the cloned repo and run:
```
<root_folder>>cd BasicLogSystem
(linux only)<root_folder>\BasicLogSystem>chmod 776 postgres  
```
Postgres needs to be able to write in postgres folder.  
If you don't care about mounting the docker drive, you can just remove line below from the file
```
   volumes:
     - ./postgres:/bitnami/postgresql
```
To contiune, build docker-compose
```
<root_folder>\BasicLogSystem>docker-compose up
```

Now, wait docker-compose to complete. 
Specifically, for postregs to return:
```
LOG:  database system is ready to accept connections
```
Now, open another console in <repo_root>/BasicLogSystem and run
```
docker exec basiclogsystem-web-1 bash entrypoint.sh
```

If, for one reason or another, you container is not named "basiclogsystem-web-1" (it should be default), change the command to use proper name or dockerID.  
I tried to get this script to run as an entrypoint during composing, but due to postgres liking to restart itself a couple of times before it actuall starts working, 
I couldn't get it to work reliably. Regardless, you only need to do it during initial setup. 

If everthing went without error, you can go to <host_ip>:8000 and you should be able to see the home page.

Use docker-compose stop/start to restart the service. 

## Running (Local)
```
(.venv) <root_folder>\BasicLogSystem>python manage.py runserver
Open "http://127.0.0.1:8000/" in you web browser.
```
## Webpages

**""**, Home page with basic information  
**admin/** Admin panel (Django provided boilerplate)
**"api/"**  API reference
**"projects/"**  Listing of all the existing projects  
**"projects/project_name/"** listing of all the tickets attached to a project  
**"projects/project_name/issues/issue_id/"**  Information about a specif ticket  
> [!TIP]
> Every page has a navigation bar at the top, with links to main sections


## API Endpoints
**'api/projects'; ['GET', 'POST']; List or Add all the projects**  
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/projects -Method Post -ContentType "application/json" -body '{"project_name": "codename"}'
curl http://127.0.0.1:8000/api/projects
  
**'api/projects/<bin_name>/issues'; ['GET', 'POST']; List or add issues**  
curl http://127.0.0.1:8000/api/projects/codename/issues  
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/projects/codename/issues -Method Post -ContentType "text/plain; charset=utf-8" -body 'Warning: just the log in plain text'   
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/projects/codename/issues -Method Post -ContentType "*/*" -body '{ "file":"C://Users//PC//Desktop//Zadanie//logs//log3.log" }'  

**'api/projects/<bin_name>/issues/<issue_id>'; ['GET', 'DELETE', 'PATCH']; Get, delete or update status of a specific issue**  
curl http://127.0.0.1:8000/api/projects/codename/issues/27  
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/projects/codename/issues/27 -Method PATCH -ContentType "application/json" -body '{ "status": "Resolved"}'  
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/projects/codename/issues/28 -Method DELETE   
  
**'api/projects/<bin_name>/issues/<issue_id>/logs'; ['GET']; Get all logs from specific issue**  
curl http://127.0.0.1:8000/api/projects/codename/issues/27/logs  
  
**'api/projects/<bin_name>/issues/<issue_id>/logs/\<log_id>a'; ['GET']; Get specific logs from specific issue**  
curl http://127.0.0.1:8000/api/projects/codename/issues/27/logs/4910  
  
**'api/projects/<bin_name>/issues/<issue_id>/logs/<log_id>/datetime'; ['GET']; Get creation time of an identified log**  
curl http://127.0.0.1:8000/api/projects/codename/issues/27/logs/4910/datetime    
  
**'api/projects/<bin_name>/issues/<issue_id>/logs/<log_id>/line'; ['GET']; Get line number of a specific log**  
curl http://127.0.0.1:8000/api/projects/codename/issues/27/logs/4910/line   

## To do/possible improvements
+ Security! (login, ssl)
+ Bugfixes to JSON ingestion.
+ Unit Testing