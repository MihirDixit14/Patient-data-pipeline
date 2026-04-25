# FHIR Ingestion Pipeline

A pipeline that pulls patient data from a public FHIR server, cleans it, loads it into SQLite, and surfaces clinical insights via SQL.

# Dataset

For this project, I am using Fast Healthcare Interoperability Resources (FHIR) particularly using HAPI FHIR API, which is used to securely exchange Electronic health records. In this dataset, each record is stored in JSON format.
For more info: https://hapifhir.io/

# Problem Statement
Healthcare systems generate large volumes of clinical data across 
disconnected sources — patient records, lab results, and hospital visits are rarely in one place or in a queryable format.
This pipeline addresses that by:
1. Pulling real-world structured data from a FHIR-compliant API
2. Standardizing and flattening deeply nested JSON into relational tables
3. Enabling clinical queries that would otherwise require manual data wrangling
The goal is to make raw FHIR data immediately useful for analysis — 
detecting out-of-range lab values, flagging readmission risks, and 
identifying documentation gaps like missing discharge dates.

# Transform
The transform layer sits between fetch and the database. It takes a list of raw FHIR resources and returns a a pandas dataframe with columns defined in the SQL schema. Real FHIR data is deeply nested and frequently has missing fields such as three transform functions extract values defensively using chained  '.get()' defaults, ensuring missing addresses, reference ranges, or  patient references never crash the pipeline.

# Load
The load layer loads the cleaned dataframes into a local sqlite database vis SQLAlchemy. The load method uses upsert strategy where we can insert new records and also update new records which avoids duplication. 