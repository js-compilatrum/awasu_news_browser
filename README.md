# About

This is web interface for Awasu application. It's used to browse and basic export articles. Without Awasu will not work and some functionalities will be broken.

https://awasu.com/

## Installation

pip install -r requirements.txt

Withoud it can't work. After that create file

#### config.py
Open awasu directory, change example config.py and put in root (app.py, manipulators.py locations). Use comments inside setup file to get information how manually configure all options.

#### Details how run read in Flask documentation:
https://flask.palletsprojects.com/en/1.1.x/quickstart/

Default:
C:\path\to\app>set FLASK_APP=hello.py
python -m flask run

or try simple:
python app.py (it's work for me on Windows 7)

Tested on Python 3.7.2 and 3.8.1

### Awasu configuration

---
Use JSON.template an Awasu => 3.2 from awasu directory:

#### Search Agents ####

If you like use Search Agents name it with prefix 'M > ' (add one with name in this convention to start working with, in other place [SA] option will be failed). If you curious why I use M. It is because M is from Meta as I see from beginning agregation a lot of channels in other one.

#### Performance ####
It's typical than when updating script is slowing down. Typical processing time on second generation i7 quad core with 32 GB RAM is below 120 sec to get data from Awasu.

## History
-
### 0.3.1 dev
At branch development features I will start transition to Quark:
https://pgjones.gitlab.io/quart/index.html

General ideas and construction are similar to Flask (see provided doc above). It will be changed:
1. New views design based on bootstrap
2. New system of selecting and processing data (SQLite)

Currently I finish new API skeleton and I create base for tests with pytest and start creating DB support. API system use two way of communicate with Awasu - using async and sync calls.

Awasu API call library

Use AwasuAPI to makes calls and ParamsBuilder to prepare list of api calls

**Examples:**

Preparing to calls is by use ParamsBuilder. Yo have to pass api name from documentation and params. As result it will be dict with necessary options.

    pb = ParamsBuilder()
    pb.make(api_name="search/query", query="Donald Trump", max=100)
    pb.make(api_name="search/query", query="Europe", max=100)
    pb.make(api_name="search/query", query="USA", max=100)
    
    new_params = pb.prepared_params # Pass here to call_api()/acall_api()

Typical API declaration is convention which I want to use in project:

`
api = AwasuAPI()
`

Synchronous API call (blocking) is used when you want play with api in single calls fx. run reports or modify old design with Flask (main branch).

`
print(api.call_awasu("buildInfo"))
`

Async gathering data (non blocking) is use to short delay in response. Typically it is for get basic information like structure folders, information about channels. It is important that order is not matter here. If you want run report and after that use call related to this operation you have to call once run report or you can miss something. It is how async works and it is not by design. For better input what is going to console use print_colored. It has predefined colors to use in console to get information from inside what is going on. When you with Params Builder create your calls you only have to get it to multicall. As I tested this design limit max number to 208 API calls. Above that you will be get app crash. It is walkaround it with Semaphore in Trio (I use it in place asyncio to get in future skeleton for background tasks and to simplify code) which can you use to limit calls to Awasu, but for the most case it is simply do not make sence. Using session do not improve calls. It is real in typical scenarion that your calls will be finish in time around 4 seconds. Using requests I get for 8 calls around 4 minutes. It is related to activity on PC and in Awasu itself. You have to observe when Awasu is updating and when has idle time. Typical errors when updating can slow down API and you have to be aware this type of problems.

    print_colored("PROCESSING", new_params)
    api.start_multicalls(new_params)  # Here put ParamsBuilder.prepared_params when you finish make items on list to call
    result = api.gathered_data
    print_colored("INFO", result)


#### Atention!
Use old branch to test configuration and play with structure. Changes are necessary to add autoconfiguration, new error system reports. Development-features branch - it is design coded from scratch.

### 0.3
Create layout based on Pandas DataFrame as backend.
### 0.2

Add Flask as web server.

### 0.1

Static generated files. No webserver.

