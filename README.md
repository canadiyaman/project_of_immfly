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

## 1.5 Running with docker.

A. Building docker image. Move to project main path and run following command.
It takes little bit time.

    A.1
        docker build --tag poi:latest .

    A.2 (For list available images)
        docker image ls
B. Run docker image.

    B.1
        docker run --name project_of_immfly -d -p 8000:8000 poi:latest
    B.2 (checking running conrainer)
        docker container ps


### Directory Layout
~~~

project_of_immfly/
└── .github
│   ... test and healtcheck CI process with github Actions
├── apps
│   ... core folder (models, apis, serializers etc.)
└── project_of_immfly
│   ... project settings (setting, wsgi, routers, urls etc.)
└── docker-entrypoint.sh
└── Dockerfile
└── manage.py
└── README.md
└── requirements.txt
~~~