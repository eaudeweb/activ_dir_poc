# views.py

from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
import requests
from django.conf import settings


# Login view: Redirects the user to the Microsoft login page
def login_view(request):
    redirect_uri = settings.AZURE_REDIRECT_URI
    client_id = settings.AZURE_CLIENT_ID
    authority = settings.AZURE_AUTHORITY

    # The URL to redirect the user for Microsoft login
    login_url = (
        f"{authority}/oauth2/v2.0/authorize?"
        f"client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=User.Read"
    )
    return redirect(login_url)


# Get Token view: Handles the callback from Microsoft and exchanges the authorization code for an access token
def get_token_view(request):
    code = request.GET.get("code")
    if not code:
        return HttpResponse("Error: No authorization code provided.", status=400)

    url = f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Data needed to exchange the authorization code for an access token
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.AZURE_CLIENT_ID,
        "client_secret": settings.AZURE_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.AZURE_REDIRECT_URI,
        "scope": "User.Read",  # Scope must match what was requested during login
    }

    response = requests.post(url, headers=headers, data=data)
    token_data = response.json()

    if "access_token" in token_data:
        # Store the access token in session or pass it directly
        request.session["access_token"] = token_data["access_token"]
        return redirect("get_users")  # Redirect to fetch users after token is obtained
    else:
        return JsonResponse(token_data, status=400)


# Fetch users view: Uses the access token to retrieve a list of users from Microsoft Graph
def get_users_view(request):
    token = request.session.get("access_token")
    if not token:
        return HttpResponse("Error: No access token. Please log in first.", status=401)

    url = "https://graph.microsoft.com/v1.0/users"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({"error": response.json()}, status=response.status_code)
