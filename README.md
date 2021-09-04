# Project of Immfly

### 1.1 Development Setup Instructions


A - Create a virtual environment and install dependencies.

       - A.1 
            pip install virtualenv
       - A.2
            virtualenv venv --python=python3
            source path/to/venv/bin/activate
       - A.3 (Move to main directory of the project)
            pip install -r requirements.txt

B - Create db and run server. (As default I used sqlite3. Cause it's best way for practices)

        - B.1
            python manage.py makemigrations
        - B.2
            python manage.py runserver


### 1.2 For testing run following command

A - Basic unit test

    python manage.py test apps

B - Test with coverage

    - B.1 (creating coverate report)
        coverage run --source='.' manage.py test apps
    - B.2 (for see the coverage)
        coverage report

### 1.3 Management command for get list of averages as csv.

    python manage.py export_ratings

    Parameters: 
        --path: Specify the path output csv file.
        --file_name: Specify the csv file name.

### 1.4 API's are requested.

    Channel List
    Method: GET
    Path:   /api/channels/
    Parameters: 
        group_ids=1,2,3

    Content List
    Method: GET
    Path: /api/contents/

### Project Structure
