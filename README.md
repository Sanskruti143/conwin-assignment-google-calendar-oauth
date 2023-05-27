# conwin-assignment-google-calendar-oauth

Pre-Requisites:
Python3
pip

To install dependencies: 
**pip install -r requirements.txt**

To run:
**python3 manage.py runserver**

To test:
1. Add a event in your google calendar for today. 
2. Once you start the server, open the browser http://127.0.0.1:8000/rest/v1/calendar/init/ 
3. This will redirect to google login page, login with your gmail, allow the permissions for calendar scopes.
4. After successfull login you will be redirected to http://127.0.0.1:8000/rest/v1/calendar/redirect/ with calendar events as json in the response.
 <img width="1791" alt="image" src="https://github.com/Sanskruti143/conwin-assignment-google-calendar-oauth/assets/109782141/b1215b3d-d04d-4dd9-91b0-f629532ad736">


