# README
This is an example of Azure Function Application.

It is ok to create local function application first and Azure instance later, the order is not important. Both have to exist prior to deployment (check deployment section).

Azure functions require Python version 3.11 at most right now (3.12 is standard, 3.13 exists). For this to work the following is needed (OS has python 3.12 installed):
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
That means that azure-functions-core-tools is needed. These tools are installed by NPM and can be updated, but the automatic update will most likely fail because Visual Studio Code does it without sudo permissions. So to update run:
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
To deploy, the function app has to be defined/exist on Azure. Select the function app it in resources in Azure Extension, left click on it, select deployment, select function app name again in the command dropdown and then confirm overriding target data. The deployment process should start. 

Deployment uses settings.json file from .vscode folder
## Errors
If the deployment fails because it can not find host.json in root folder of ZIP, the cause is most likely azureFunctions.deploySubpath value in settings.json. It should contain the name of the subfolder of the project root that contains function app (and that folder should include host.json).