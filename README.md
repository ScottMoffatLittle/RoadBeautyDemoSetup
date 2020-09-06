![Logo](https://bitbucket.org/gisfederal/kml/raw/master/logo.png)

# ml-demo-setup-road-beauty


### The repository includes:
1. System tables setup
2. Mapillary Data Ingest to Kinetica DB
3. Image semantic segmentaton model
4. Beauty scores on inferenced images


### System Requirements
```
1. Base Assumption: Access to Kubernetes Cluster (execute "kubectl get nodes" to ensure this is the case)
2. Base Assumption: Access to Kinetica DB (curl http://host:9191 to ensure access)
3. If anything is missing, use KAgent to set up system components

```

### Usage Instructions
```
Option 1: Run Everything
./master_setup.sh

Option 2: Run any part separately
	Pull containers:
	python ./prepull.py

	Set up required tables:
	python ./setup_tables_and_views.py

	Run Ingests:
	python ./start_ingest.py

	Run Models:
	python ./start_models.py

	Get Beauty Scores:
	#echo "Populating sample inferences"
	#python ./sample_inferences.py
```