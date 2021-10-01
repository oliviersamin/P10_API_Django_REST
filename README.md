# Secured REST API based on Django rest API framework
#

#### This API is the 10th project of a training to obtain a diploma
The API follows issues encountered in several projects of clients.   
**The deliverables are listed below:**
* This is a secured API and only authenticated users can use it
* This is secured with JWT to respect OWASP issues
* This API must respect the RGPD rules
* This API shall be use by three platforms: website, Android and IOS
* This API allows users to create projects, add users to them, create issues for each projects giving them tags and priorities...
* only the author of the project can add users to it (contributors)
* only the author of a project/issue or comment can update or delete it. All the contributors to this projects can only see it.
* Every contributor to a project can create issues and / or comments
* Each issue has an assignee (by default = the author of the issue)
* These three applications will exploit URI that will provide data
* **The POSTMAN documentation is available [here](https://documenter.getpostman.com/view/16015714/UUxzB8Bu)**
* The following table shows all the available URI, methods and actions associated



## Installation

This locally-executable API can be installed using the following steps.

### Installation and execution using venv and pip

1. Clone this repository using `$ git clone https://github.com/oliviersamin/P10_API_Django_REST.git` (you can also download the code using [as a zip file](https://github.com/oliviersamin/P10_API_Django_REST/archive/refs/heads/main.zip))
2. 2. Move to the P10_API_Django_REST folder with `$ cd P10_API_Django_REST`
3. Create a virtual environment for the project with `$ py -m venv env` on windows or `$ python3 -m venv env` on macos or linux.
4. Activate the virtual environment with `$ env\Scripts\activate` on windows or `$ source env/bin/activate` on macos or linux.
5. Install project dependencies with `$ pip install -r requirements.txt`
6. perform migrations with `$ python manage.py migrate`
7. Run the server with `$ python manage.py runserver`

When the server is running after step 7 of the procedure, the API can be requested from endpoints starting with the following base URL: http://127.0.0.1:8000/softdesk/v1/

Steps 1, 3, 5 and 6 are only required for initial installation. For subsequent launches of the API, you only have to execute steps 4 and 7 from the root folder of the project.

## Usage and detailed endpoint documentation

You can read the documentation through the POSTMAN documentation of the API by visiting [this page](https://documenter.getpostman.com/view/16015714/UUxzB8Bu).


#### list of all the action to perform, method to use and the associated URI
| ACTION PERFORMED | METHOD | URI |  
| ---------------- | ----------- |  ----------- | 
| User signup | POST | softdesk/v1/signup/ |   
| User login | POST | softdesk/v1/login/ |  
| User refresh token | POST | softdesk/v1/login/refresh/  |  
| Get the list of all related projects | GET | softdesk/v1/projects/ |  
| Create a project | POST | softdesk/v1/projects/ |  
| Get a project details | GET | softdesk/v1/projects/{project_id} |  
| Update a project | PUT | softdesk/v1/projects/{project_id} |  
| Delete a project and all its issues | DELETE | softdesk/v1/projects/{project_id} |  
| Get all the users related to a project | GET | softdesk/v1/projects/{project_id}/users/ |  
| Add a user to a project | POST | softdesk/v1/projects/{project_id}/users/ |  
| Delete a user from a project | DELETE | softdesk/v1/projects/{project_id}/users/{user_id} |  
| Get all the issues related to a project | GET | softdesk/v1/projects/{project_id}/issues/ |  
| Create an issue related to a project | POST | softdesk/v1/projects/{project_id}/issues/ |  
| Get details of an issue | GET | softdesk/v1/projects/{project_id}/issues/{issue_id} |  
| Update an issue of a project | PUT | softdesk/v1/projects/{project_id}/issues/{issue_id} |  
| Delete an issue related to a project | DELETE | softdesk/v1/projects/{project_id}/issues/{issue_id} |  
| Get all the comments related to an issue | GET | softdesk/v1/projects/{project_id}/issues/{issue_id}/comments/ |  
| Create a comment related to an issue | POST | softdesk/v1/projects/{project_id}/issues/{issue_id}/comments/ |  
| Get details of a comment | GET | softdesk/v1/projects/{project_id}/issues/{issue_id}/comments/{comment_id} |
| Update a comment related to an issue | PUT | softdesk/v1/projects/{project_id}/issues/{issue_id}/comments/{comment_id} |  
| Delete a comment related to an issue | DELETE | softdesk/v1/projects/{project_id}/issues/{issue_id}/comments/{comment_id} |
| Logout | POST | softdesk/v1/logout/ | 

