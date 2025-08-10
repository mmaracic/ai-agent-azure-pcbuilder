# README
This is an example of Azure Function Application with Azure AI agents.  
https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstart?pivots=programming-language-python-azure

It is ok to create local function application first and Azure instance later, the order is not important. Both have to exist prior to deployment (check deployment section).

It is important to note that the virtual environment folder and .vscode folders have to be under workspace root folder so vs code vould recognise configuration and virtual environment correctly

Azure-functions-core-tools version limits python version that can be used.

To install alternative python version (OS has python 3.12 installed):
* install pyenv
* install Python 3.11 using pyenv with
```
pyenv install 3.11
```
* Set system (3.12) and 3.11 as globally available versions with 3.12 being first (default):
```
pyenv global system 3.11
```
* Create python virtual environment with:
```
python3.11 -m venv .venv
```
* Activate python environment with:
```
source .venv/bin/activate
```
## Errors
If error like this happens:
```
azure python No job functions found. Try making your job classes and methods public. If you're using binding extensions (e.g. Azure Storage, ServiceBus, Timers, etc.) make sure you've called the registration method for the extension(s) in your startup code (e.g. builder.AddAzureStorage(), builder.AddServiceBus(), builder.AddTimers(), etc.).
```
Or if python version is limited below versions currently generally available

Both these errors mean that update to azure-functions-core-tools is needed. These tools are installed by NPM and can be updated, but the automatic update will most likely fail because Visual Studio Code does it without sudo permissions. So to update run:
```
npm i -g azure-functions-core-tools@4 --unsafe-perm true
```
Packages installed can be checked with
```
npm list -g --depth=0 --json
```
NPM update will not update whennode used without -g switch. Package is here:  
https://www.npmjs.com/package/azure-functions-core-tools

# Local deploy and debug
Uses launch.json and tasks.json from .vscode folder.

Run the function app using Run and Debug extension on the left of VS Code.

# Deployment
To deploy, the function app has to be defined/exist on Azure. Select the function app it in resources in Azure Extension, left click on it, select "Deploy to Function App", select function app name again in the command dropdown and then confirm Deploying and overriding target data. The deployment process should start. 

Deployment uses settings.json file from .vscode folder

## Errors
If the deployment fails because it can not find host.json in root folder of ZIP, the cause is most likely azureFunctions.deploySubpath value in settings.json. It should contain the name of the subfolder of the project root that contains function app (and that folder should include host.json).

# Environment variables
There is no need to use something like dotenv. Env variables for local deployment can be specified in local.settings.json under "Values". During deployment env variables are defined in Settings -> Environment variables in Azure dashboard. 

# Security
When we enable function application security, it will create app registration and enterprise app in Microsoft Entra. App registration identity with secret (under Certificates and secrets) can be given additional api permissions (under API permissions) but these apply mostly to graph apis.  

That identity will not have permissions to access e.g. AI Foundry project because we can not assign to it Cognitive Services User permissions or Azure AI User permissions and it can not be used as credential for them (by specifying tennant_id, client_id and client_secret as env variables).

Using token of the authorised user for the function app as credential will also not work because the scope of that access token is function app, not AI Foundry, so it will get 401 response from the foundry.

Instead we should use system assigned managed identity under Function App -> Settings -> Identity. First enable it by setting status to On, and then add Cognitive Services User permissions or Azure AI User permissions by clicking Azure roles assignment button. On the screen that will open use Add role assignment and then use subscription as scope and select role from the list on the bottom (note: it takes a bit for the dropdown to fill in but it is all there). Refresh the screen with the permissions if needed to see updates. Note: This credential will work as soon as it is enabled, it is not required to add any environment variables to application to this credential to be picked up, just do not define env variables that would trigger credentials earlier in the priority list of DefaultAzureCredential() such as client secret.


## To secure function application access
Enabling function application security is done in Settings -> Authentication. Set authentication to Enabled, Restrict Acess to Require Authentication. Add Microsoft as Identity provider (this will create app registration and enterprise app in Microsoft Entra).

The authentication works out of the box using sidecar approach built into azure https://learn.microsoft.com/en-us/azure/app-service/overview-authentication-authorization, triggers browser login through provider if needed and completes with jwt access and refresh tokens being available in subsequent request headers (without provider SDK flow). No additional code or configuration required.

App keys (Functions -> App keys) can also be used a a lower level of protection of Function App:
https://learn.microsoft.com/en-us/azure/azure-functions/function-keys-how-to?tabs=azure-portal
