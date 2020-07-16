#  Documentation


## Architecture of the pipeline

![alt text](https://github.com/Modius22/nlp-pipeline/blob/master/img/nlp_pipeline.png?raw=true)

## create nlp-pipeline docker container

1. Change to the directory with the dockerfile
2. run ```docker build . -t nlp-pipeline```
3. start docker container ```docker run -p 127.0.0.1:5000:5000 --name nlp-engine nlp-engine```

## pull docker image from dockerhub and start

1. download docker image ```docker pull modius22/nlp-pipeline```
2. start docker container ```docker run -p 127.0.0.1:5000:5000 --name nlp-pipeline modius22/nlp-pipeline```

## start api from terminal 
1. change in the src directory
2. run ```python control.py```

## example run of each function

### standard function

create new project: 
```curl -i 'http://127.0.0.1:5000/nlp/create_project?project_name=project_a'```

get list of projects:
```curl -i 'http://127.0.0.1:5000/nlp/get_project'```

get list of all files of an project:
```curl -i 'http://127.0.0.1:5000/nlp/get_project_files?project_name=project_a'```


remove existing project:
```curl -i 'http://127.0.0.1:5000/nlp/delete_project?project_name=project_a'```

### nlp function

load data to new project:
``` curl -i 'http://127.0.0.1:5000/nlp/project_a/load?text=text&sentiment=airline_sentiment' -F file=@./Tweets.csv -X POST -H 'enctype:multipart/form-data ; Content-Type:multipart/form-data'```

explore data:
```curl -i 'http://127.0.0.1:5000/nlp/project_a/exploartion'```

clean data:
```curl -i 'http://127.0.0.1:5000/nlp/project_a/clean'```

vectorize data:
```curl -i 'http://127.0.0.1:5000/nlp/project_a/vectorize'```

learn model:
```curl -i 'http://127.0.0.1:5000/nlp/project_a/model?algorithm=LR'```

predict:
``` curl 'http://127.0.0.1:5000/nlp/project_a/predict?algorithm=LR&text=told%20work%20joke%20fail' -X POST -v ```

learn model MNB
```curl -i 'http://127.0.0.1:5000/nlp/project_a/model?algorithm=MNB'```

predict MNB
```curl 'http://127.0.0.1:5000/nlp/project_a/predict?algorithm=MNB&text=told%20work%20joke%20fail' -X POST -v ```

# known problems
## macOS curl on terminal "zsh: no matches found:"
 On macOS the curl command may cause problems. The solution is to set the URL in '.
 
 e.g. 
```curl -i 'http://127.0.0.1:5000/nlp/create_project?project_name=project_a'```

## no access to the working folder
This problem can occur if you start the API from a development environment. In this case the working directory for the development environment must be set to the ./src folder.
