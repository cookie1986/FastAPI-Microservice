# FastAPI-Microservice
Starter point for setting up a FastAPI microservice on a cloud platform such as Azure.


## Installation
Navigate to an appropriate directory and use ```git clone``` to clone the repo. Then ```CD``` into the repo.

Next, create a virtual environment with ```python3 -m venv venv```.

Activate the venv with ```source venv/bin/activate```.

Check you are using the correct version of python by entering ```which python``` in your terminal. 

Then, install packages in the requirements file by running ```pip install -r requirements.txt```.

## Start server (local)
Run ```uvicorn main:app --reload``` to start the server on your local machine.