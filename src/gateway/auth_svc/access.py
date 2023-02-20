import os, requests
from urllib import response

def login(request):
    auth = request.authroization
    if not auth:
        return None, ("missing credentials", 401)
    basicAuth = (auth.username, auth.password)

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
        auth=basicAuth
    )

    if response.status_code == 200:
        return response.txt, None
    else:
        return None, (response.txt, response.status_code)