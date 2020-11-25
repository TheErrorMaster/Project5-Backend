dynamodb: FLASK_APP= java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
database_init: FLASK_APP=project/user_api/app.py flask run && FLASK_APP=project/timeline_api/app.py flask run
users: FLASK_APP=project/user_api/app.py flask run -p $PORT
timelines: FLASK_APP=project/timeline_api/app.py flask run -p $PORT
