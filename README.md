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


## Screenshots 
<img width="1918" height="846" alt="image" src="https://github.com/user-attachments/assets/2743ca18-0491-410b-8e49-9ce9983ff110" />
<img width="1918" height="875" alt="image" src="https://github.com/user-attachments/assets/16c43062-e4b2-47d9-8132-d5c4a0b9c3c8" />
<img width="1918" height="840" alt="image" src="https://github.com/user-attachments/assets/2d887e9d-c115-4bbd-866b-825e63676ab1" />
<img width="1912" height="872" alt="image" src="https://github.com/user-attachments/assets/20964278-7c90-4d12-bc03-298c0058fbba" />
<img width="1913" height="868" alt="image" src="https://github.com/user-attachments/assets/34b7c229-50c8-4f79-8419-cf0686b92c5b" />
<img width="1902" height="762" alt="image" src="https://github.com/user-attachments/assets/b64ec88f-785e-4500-a965-eff4cf3ae9aa" />
<img width="1918" height="836" alt="image" src="https://github.com/user-attachments/assets/820ec44b-1e2f-4547-b7aa-e69d542d06f4" />
<img width="1910" height="841" alt="image" src="https://github.com/user-attachments/assets/5869f1ff-af2c-4ab1-a63c-c6e83d907e90" />
<img width="1912" height="853" alt="image" src="https://github.com/user-attachments/assets/0dadbbf2-da32-469e-9bda-84602a765639" />
<img width="1917" height="851" alt="image" src="https://github.com/user-attachments/assets/2613a005-ec08-4306-9734-fed95c4333bd" />


## Future Work 

### Knowledge Graph Construction 
Transform discovered relationships into a unified semantic knowledge graph 

### Relationship-aware dataset search 
Incorporate graph-based matching techniques inspired by semantic table discovery research 

### Machine Learning for Semantic Similarity 
Use an embedding-based representation of columns and datasets to improve matching performance 

## Automated Data Integration 
Recommend dataset joins and unions based on discovered semantic relationships 

## Explainable Data Discovery 
Generate interpretable explanations for dataset recommendations 


## Running the Project 

1. Clone the repository
   git clone
   
2. Install Dependencies
   pip install -r requirements.txt
   
3. Launch the application
   streamlit run src/app.py


## Research interests 
This project was developed as a part of my exploration of:
1. Data Management
2. Data Discovery
3. Semantic Data Integration
4. Data Quality Assessment
5. Applied Machine Learning
6. Large-Scale Data Systems

I am particularly interested in how semantic understanding, graph-based methods, and machine learning can be combined to improve data discovery and integration in modern data ecosystems. 








