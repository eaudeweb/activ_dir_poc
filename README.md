# Django + Azure AD PoC

This is a Proof of Concept (PoC) Django application that connects to Azure Active Directory (AD) for user authentication and retrieves a list of users using the Microsoft Graph API. 
It uses cookie-based session management, so no database is required for session storage.

## Prerequisites

Before running this PoC, ensure you have the following:

1. **Azure AD Tenant**: Access to an Azure Active Directory tenant (company or personal).
2. **Azure App Registration**: An Azure AD application registered with the necessary API permissions (`User.Read`).
3. **Python**: Python 3.7+ installed.
4. **Django**: Installed and set up on your machine.
5. **Required Packages**: `requests`, `django`, `python-decouple`


## Setup Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/ad-poc.git
cd ad-poc
```

### Step 2: Clone the Repository

```
pip install django requests
pip install python-decouple
```

### Step 3: Azure AD App Registration

1. Log in to the [Azure Portal](https://portal.azure.com/).
2. Go to **Azure Active Directory** > **App registrations** > **New registration**.
3. Register your app:
   - **Name**: Provide a meaningful name (e.g., `DjangoAzurePoC`).
   - **Supported account types**: Choose **Accounts in this organizational directory only**.
   - **Redirect URI**: Set to `http://localhost:8000/get_token/`.
4. Once the app is created, go to **Certificates & Secrets** and generate a new **client secret**. Make sure to note the secret as it will only be visible once.
5. Go to **API permissions** and add the following Microsoft Graph API permission:
   - **Delegated Permissions**: `User.Read`
   - Grant admin consent for the permission if required by clicking on **Grant admin consent**.
6. Note down the following details from your Azure AD app registration:
   - **Client ID** (Application ID)
   - **Client Secret** (from the secret value created in Step 4)
   - **Tenant ID** (found in **Overview** or **Endpoints**)

### Step 4: Configure Django Settings

1. **Create a `.env` File**: In the root directory of your Django project, create a file named `.env` to securely store your Azure AD credentials. This prevents sensitive information from being hardcoded in your source files.

**.env File Example**:
```plaintext
   AZURE_CLIENT_ID=your_client_id        # Replace with your Azure Client ID
   AZURE_CLIENT_SECRET=your_client_secret  # Replace with your Azure Client Secret
   AZURE_TENANT_ID=your_tenant_id        # Replace with your Tenant ID
   AZURE_REDIRECT_URI=http://localhost:8000/get_token/  # Must match the registered Redirect URI in Azure AD
```

### Step 5: Run the Application

Run the Django development server using the following command:

```bash
python manage.py runserver
```

This will start the server on `http://localhost:8000/`. You can visit this URL in your web browser.


### Step 6: Test the Application

1. Open your web browser and go to `http://localhost:8000/login/`.
2. You will be redirected to Microsoft's login page. Enter your Azure AD credentials to log in.
3. After successfully logging in, you will be redirected back to your app's `get_token` view. The application will exchange the authorization code for an access token and store it in the session.
4. You will then be redirected to `http://localhost:8000/get_users/`, where you can view the list of users from your Azure AD.

Make sure to handle any errors that may occur during the login or token retrieval process.
