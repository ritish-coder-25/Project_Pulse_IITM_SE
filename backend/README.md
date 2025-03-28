## Setting Up the Project

1. **Create a virtual environment:**
    ```sh
    python -m venv env  or python3 -m venv env 
2. **Activate the virtual environment:** 

        - **Linux:**
            ```sh
            source ./env/bin/activate
            ```
        - **Windows:**
            ```sh
            .\env\Scripts\Activate.ps1
            ```

3. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```sh
    python main.py
    ```

5. **Login to Groq and get GROQ_API_TOKEN**
6. **Get Github Token**
Logun to github-> Settings -> Developer Settings -> Personal Access Token -> Fine Grained Tokens -> Create -->Repo Access(All Repositiories) --> Account Permissions(Select Appropriate Permissions(Atleast Commit statuses, contents, issues, metadata, etc  )

7. ** Replace the .env.example with a .env file inside Backend/ and put your keys. 
GROQ_API_KEY=''
GITHUB_TOKEN=''


8. Generate openapi yaml
> flask openapi write --format=yaml openapi.yaml 
if you get an error saying could not find flask project please run 
> $env:FLASK_APP = "main.py" for windows or set FLASK_APP=main.py for ubuntu and try again

After generating yaml you can run it in 
> https://editor-next.swagger.io/
or
> https://redocly.github.io/redoc/#tag/Tickets/operation/getTicketCode

9. Testing
Warning: 
A. Please execute the pytest command under virtual environment. 
B. Ensure requirements are installed.

To run all the tests you can use the command 
> pytest -v
To exclude warnings use: 
> pytest .\backend\tests\ -v -p no:warnings
-v can be removed, it is used for more or less information
For running a specific file use
> pytest tests/test_register.py -v




FOr lijnux:
install redis-server, start redis-server in a terminal

then in a new terminal
celery -A tasks.celery worker --loglevel=info

or 

celery -A main.celery worker -l debug -P solo