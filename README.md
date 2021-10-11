Steps to start the application:

I create a bash file with multiple arguments that are attached on execution. For more info about this bash file you can execute bash run -help

1. First command it is "bash run -build": this comand execute the Docker file to install the python version
and the requirements.txt file where are all the modules that are mandatory for this app to work.

2. Execute the "bash run -compose -d" to run the docker-compose.yml. In this file are the postgres image instaler, the redis cache image
all the necessary configurations that are mandatory for this app to work in the suitably way.

OBS:
In this step at the end of the process you will need to see the db migration status. If you don't sea that please run again the fallowing command:
"bash run -compose -d". On my mac I hade some problem with the postgres docker image.

This is the correct response:
"
    Running migrations:
      Applying contenttypes.0001_initial... OK
      Applying auth.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying admin.0002_logentry_remove_auto_add... OK
      Applying admin.0003_logentry_add_action_flag_choices... OK
      Applying api.0001_initial... OK
      Applying api.0002_auto_20211011_1150... OK
      Applying contenttypes.0002_remove_content_type_name... OK
      Applying auth.0002_alter_permission_name_max_length... OK
      Applying auth.0003_alter_user_email_max_length... OK
      Applying auth.0004_alter_user_username_opts... OK
      Applying auth.0005_alter_user_last_login_null... OK
      Applying auth.0006_require_contenttypes_0002... OK
      Applying auth.0007_alter_validators_add_error_messages... OK
      Applying auth.0008_alter_user_username_max_length... OK
      Applying auth.0009_alter_user_last_name_max_length... OK
      Applying auth.0010_alter_group_name_max_length... OK
      Applying auth.0011_update_proxy_permissions... OK
      Applying auth.0012_alter_user_first_name_max_length... OK
      Applying authtoken.0001_initial... OK
      Applying authtoken.0002_auto_20160226_1747... OK
      Applying authtoken.0003_tokenproxy... OK
      Applying sessions.0001_initial... OK
"

3. In this moment we have the app running and we need to create an user that it will be used to get the api token.
To do that you will need to execute the next bash command "bash run -user -c" where you will be asked to add a
username, an email, a password and a password confirmation (NOTE: please a strong password because Django has a password verificationd and it will
ask for a strong password ).
OBS:
    - If the app is not working you can run the fallowing command "bash run -compose" to execute the docker-compose.ylm not in detach mode
    - If you want to kill all the images you can execute the fallowing command "bash run -kill -i" and all the created images it will be removed
    ( NOTE: check if you have another images created in your docker because those images will be removed )

4. After the step 3 we will have a username and a password and we can use those credentials to get the token that it is necessary to execute the
Django command. In this command it is included a request to an api link where the token is required. To get the toke execute the fallowing command
"bash run -t username password", where the username and the password you will need to complete with your credentials.

5. Execute the app main purpose. After the step 4 we will receve a response with an token. We need to copy that token and then execute the fallowing commnad
"bash run -command token pageSize", where the page size it is the size number of entries results that we what to get from redis and move them to database.

COMMAND EXAMPLE: "bash run -command 7d8e391849d63ba92e0cfdb6cf9614e4a7e86f2a 10000"


OBS:
For more info about all commands you can run "bash run command_name -help", where I tried to set same indications about how to use the bash file.





I HOPE NOT TO HAVE MANY ENGLISH GRAMATICAL ERRORS :) It was writen in hurry :))
