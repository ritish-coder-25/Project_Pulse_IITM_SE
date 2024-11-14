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