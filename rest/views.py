from django.shortcuts import redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
CLIENT_SECRETS_FILE = "credentials.json"

SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile',
          'openid']
REDIRECT_URL = 'http://127.0.0.1:8000/rest/v1/calendar/redirect'
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'
START_TIME = '2023-04-04T00:00:00Z'
END_TIME = '2023-12-30T00:00:00Z'


@api_view(['GET'])
def GoogleCalendarInitView(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = REDIRECT_URL

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    request.session['state'] = state

    # return Response({"authorization_url": authorization_url})
    return redirect(authorization_url)


@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    print("starting")
    state = request.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = REDIRECT_URL

    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] = {'token': credentials.token,
                                      'refresh_token': credentials.refresh_token,
                                      'token_uri': credentials.token_uri,
                                      'client_id': credentials.client_id,
                                      'client_secret': credentials.client_secret,
                                      'scopes': credentials.scopes}
    if 'credentials' not in request.session:
        return redirect('v1/calendar/init')

    credentials = google.oauth2.credentials.Credentials(
        **request.session['credentials'])

    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    calendar_list = service.calendarList().list().execute()

    print(calendar_list)
    calendar_id = calendar_list['items'][2]['id']
    for calendars in calendar_list['items']:
        print(calendars)
        if calendars['id'].endswith('@gmail.com'):
            calendar_id = calendars['id']
            print("matching calendarId")

    print(calendar_id)

    events = service.events().list(calendarId=calendar_id, timeMin=START_TIME,
                                   timeMax=END_TIME).execute()

    # print(events)
    events_list_append = []
    if not events['items']:
        print('No data found.')
        return Response({"message": "No data found."})
    else:
        for events_list in events['items']:
            # print(events_list)
            # print("\n")
            events_list_append.append(events_list)
        # return Response({"events": events_list_append})
        return JsonResponse({"events": events_list_append})
    return Response({"error": "calendar event aren't here"})

