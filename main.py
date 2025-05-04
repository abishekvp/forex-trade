import requests
from datetime import datetime, timedelta

username = 'securefields'
token = 'eaa6e9582de5ac38648336301494b0030f9bd4cb'

response = requests.get(
    'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(
        username=username
    ),
    headers={'Authorization': 'Token {token}'.format(token=token)}
)
if response.status_code == 200:
    print('CPU quota info:')
    print(response.content)
else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
    def trigger_webapp_reload():
        end_date = datetime.now() + timedelta(days=90)
        while datetime.now() < end_date:
            reload_response = requests.post(
                'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{username}.pythonanywhere.com/reload/'.format(
                    username=username
                ),
                headers={'Authorization': 'Token {token}'.format(token=token)}
            )
            if reload_response.status_code == 200:
                print('Webapp reloaded successfully.')
            else:
                print('Failed to reload webapp. Status code {}: {!r}'.format(
                    reload_response.status_code, reload_response.content
                ))
            break  # Remove this break to allow continuous execution until the end date

    trigger_webapp_reload()