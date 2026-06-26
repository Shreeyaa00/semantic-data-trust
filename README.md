# Semantic Data Intelligence Platform 

An interactive research-oriented platform for semantic dataset discovery, relationship mining, and trust assessment across heterogeneous datasets. 

Built using Python, Streamlit, Plotly, and graph-based analytics. 

## Motivation 

Modern organisations collect massive amounts of data from different sources. However, discovering trustworthy datasets and understanding how datasets relate to one another remains a major challenge.
Traditional approaches often rely solely on metadata or column similarity, which can miss important semantic relationships hidden within the data.
This project explores how dataset quality assessment, relationship discovery, and semantic matching can be combined into a unified framework for intelligent data discovery.
The work was inspired by research in semantic data integration and data lake discovery systems, particularly relationship-aware approaches to identifying meaningful connections between datasets.


## Key Features

### Dataset Trust Scoring

Evaluates dataset quality using multiple dimensions 
- completeness
- uniqueness
- consistency

Generates an overall trust score that helps users assess dataset reliability before analysis 


### Relationship discovery engine 

Automatically identifies potential relationships between attributes within the datasets 
capabilities include:
- Column dependency discovery
- Relationship confidence scoring
- Semantic relationship visualisation
- interactive graph exploration

The platform constructs relationship networks that help uncover hidden structure within large datasets 


### Semantic Dataset Matching

Ranks datasets based on structural and semantic similarity.

Instead of relying only on dataset names or metadata, the platform analyzes:

- Attribute structure
- Relationship patterns
- Dataset characteristics

to identify potentially related datasets.

### Geospatial Intelligence Module

Supports exploration of large urban datasets containing geographic information.

Current implementation includes:

- NYC Motor Vehicle Collision Data
- NYPD Arrest Data

Features:

- Interactive density mapping
- Spatial hotspot visualization
- Urban activity exploration

Interactive Analytics Dashboard

Built using Streamlit and Plotly.

Provides:

- Trust score visualizations
- Relationship confidence analysis
- Semantic similarity rankings
- Dataset exploration tools
- Geographic analytics


## Technology Stack 
### Data Processing

- Python
- Pandas
- NumPy

### Visualization

- Streamlit
- Plotly
- Streamlit-Agraph

### Analytics

- Semantic Matching
- Relationship Mining
- Data Quality Assessment

## Datasets

This project currently uses publicly available New York City Open Data datasets, including:

- Motor Vehicle Collisions
- NYPD Arrest Data
- Additional urban analytics datasets

These datasets were selected because they contain heterogeneous schemas, real-world data quality challenges, and rich relational structure.








