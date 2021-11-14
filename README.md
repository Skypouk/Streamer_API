# Stream API 

## Requirements

In order to run the project, the user need to install docker 

### Step 1: Building the application image
The user need to build the my-app image by running the following command :

```
docker build -t my-api:1.0 .
```
This command uses Dockerfile in order to build the image "my-api" with the tag "1.0".

### Step 2: Lunching the application

In order to lunch the application, the user need to run the images: "my-api" and "sqlite3".
To facilitate this step and avoid pasting multiple long commands in the terminal, we used a .yaml file.

```
 docker-compose -f docker-compose.yaml up -d
```
### Step 3: Using the app

We can now execute the commands in "test_commands.txt" file to fetch data from the API

example of command:
```
curl --header "Content-Type: application/json" --request POST http://127.0.0.1:6000/streamers?username=LeFrenchRestream
```
