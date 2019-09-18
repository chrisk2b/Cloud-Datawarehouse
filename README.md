# Purpose of the Repository

This repository contains the results of the "Cloud Data Warehouse" Project which is part of the [Udacity](https://www.udacity.com/) Data Engineering Nanodegree. Its’s purpose is to give the reviewers access to the code. 

# Summary of the Project
The project deals with a start up called Sparkify which is an online music provider. Sparkify wants to collect and analyze data about its user activities. It is e.g. interested in a detailed understanding of which songs users are currently listening. 

Sparkify has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

The task of the project is to create a cloud data warehouse based on Amazon Redshift and to build an ETL pipeline that extracts data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for the analytics team to continue finding insights in what songs users are listening to.

# Files in the Repository
The following files are contained in the repository:

 - [sql_queries.py](https://github.com/chrisk2b/Cloud-Datawarehouse/blob/master/sql_queries.py): This file contains SQL statements which:
 a) create staging tables in Amazon Redshift
 b) create tables for a dimensional data model in Amazon Redshift
 c) load data from S3 into the staging tables
 e) transform and load data from the staging tables into the dimensional tables
 - [create_tables.py](https://github.com/chrisk2b/Cloud-Datawarehouse/blob/master/create_tables.py): This file uses the SQL statements defined in sql_queries.py which define the staging and dimensional tables and executes them. 
 - [etl.py](https://github.com/chrisk2b/Cloud-Datawarehouse/blob/master/etl.py): Contains code which executes the ETL-process to populate the staging tables and the dimensional tables with data.
 - [IaC.ipynb](https://github.com/chrisk2b/Cloud-Datawarehouse/blob/master/IaC.ipynb): A Jupyter Notenook which defines the Amazon Redshift Cluster in terms of Infrastructure as Code (IaC). The python [boto3 library](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html?id=docs_gateway)  is used to define the data warehouse cluster, the necessary IAM roles and policies to allow redshift to access S3 and the VPC security group settings to interact with the cluster from outside the VPC.
 - [dwh.cfg](https://github.com/chrisk2b/Cloud-Datawarehouse/blob/master/dwh.cfg): A config file with contains all necessary configurations which define the cluster (e.g. number of nodes etc.).
 - requirements.txt: Contains all dependencies, cf. below.
# Packages
The following packages are necessary to run the scripts (cf. the "how to Execute" section below)

 - psycopg2
 - configparser
 - pandas
 - boto3
 
The can be installed by using the requirements.txt file by using the command `pip install -r requirements.txt`

# How to Execute the Scripts
This section describes the steps which are necessary to build the datawarehouse on AWS, create all necessary table and execute the ETL pipeline.

 1. Execute all cells in the Notebook [IaC.ipynb](https://github.com/chrisk2b/Cloud-Datawarehouse/blob/master/IaC.ipynb). This will create a Redshift cluster on AWS as configured in [dwh.cfg](https://github.com/chrisk2b/Cloud-Datawarehouse/blob/master/dwh.cfg). 
 2. Run the command `python create_tables.py` in a terminal. This will create the staging tables and dimensional tables in the Redshift cluster which has been created in step 1.
 3. Run the command `python etl.py` in a terminal. This will execute the ETL-process which extracts the raw data from S3 and loads them into staging tables. From there, the data gets transformed and loaded into dimensional tables.  
 
 After executing the above steps, the datawarehouse exists and is populated with data. The dimensional tables can be used for analytical queries.

 

	 


 

The major part of the proj
