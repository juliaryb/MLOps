# Lab12 - ML pipelines
"This lab concerns creating ML pipelines, useful for organizing dataset creation and model training workflows. We will use Apache Airflow for this purpose, as arguably the most popular workflow orchestrator."

### Exercise 1
The TaskFlow API seems way more convinient than the traditional approach. UI preview:
![](images/image.png)

## Schedulling and backfilling
![alt text](images/image-1.png)
I first set the date to yesterday, which was not enough to observe if the output made sense. When I switched to 2026-1-1, it turned out you need to delete DAG history for it to actually perform a catchup. Afterwards it did show earlier dates in the "Next run" column, but failed due to too many API calls.
![](images/image-2.png)

### Exercise 2
The saving got stuck:
![](images/image-3.png)

So the parameter `max_active_runs=1` was set, and then it worked:
![](images/image-4.png)

But then realised there were duplicates and the end date should be calculated with timedelta(days=6) not 7. Then the resulting csv is correct.

### Exercise 3
It didn't want to work, but there was a bug in the compose.yaml file? 
line 39: `- uv-cache:/opt/airflow/.uv-cache` changed to `- ./uv-cache:/opt/airflow/.uv-cache`

and also:
```
mkdir -p dags logs plugins config .uv_cache
sudo chmod -R 777 logs dags plugins config .uv_cache
```
should be .uv-cache

Eventually, it worked:
![alt text](images/image-5.png)


## Object storage XCom backend
LocalStack S3 functioning:
![alt text](images/image-6.png)

After adding dependencies the docker image needs to be rebuilt:
```
docker compose down -v
docker compose build --no-cache
docker compose up
```

Also then it couldn't write to the bucket due to "missing" credentials, this line helped:
```
AIRFLOW_CONN_AWS_DEFAULT: '{"conn_type": "aws", "login": "test", "password": "test", "extra": {"endpoint_url": "http://localstack:4566", "region_name": "us-east-1"}}'
```

Then it worked:
![alt text](images/image-7.png)


### Exercise 4
Create the weather bucket:
![alt text](images/image-8.png)

Dag working:
![alt text](images/image-9.png)

Results in S3:
![alt text](images/image-10.png)


## Connections, hooks, variables

### Exercise 5
- added the key to .env: `AIRFLOW_VAR_TWELVEDATA_API_KEY=real_api_key_here`
- added postgres-storage to services in yaml and added postgres-storage-volume to volumes
- created a script to created the db on startup in postgres-init and verified if it worked:
    ![alt text](images/image-11.png)
- create airflow connection to the storage db using airflow UI:
    ![alt text](images/image-12.png)
    but it failed, so I added this line to the compose file to establish the connection to the database: 
    ```
    AIRFLOW_CONN_POSTGRES_STORAGE: "postgresql://storage:storage@postgres-storage:5432/storage"
    ```