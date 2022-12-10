# Login System using Speaker Verification
This web app is a simple web application that employs verification using speech.

To run this application:

1. Clone this repo and and follow its instructions to start `speaker verification service`: https://github.com/hoanduy27/speaker_verification_serving

2. Install requirements: `pip install -r requirements.txt`

3. Export global variables: `export dev.env`

4. Create database:
```
python manage.py makemigrations
python manage.py migrate
```

5. Run the web app: `python manage.py runserver`