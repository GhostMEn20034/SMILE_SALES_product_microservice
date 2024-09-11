# Microservice: Product Catalog of Smile Sales e-commerce
This microservice provides a public API for users to interact with product information.
# A Brief Overview Of The Features
 The microservice offers functionalities like:
- **Product Listing:** Displays a list of products, potentially filtered by facets.
- **Autocomplete Search:** Enables efficient product search with suggestions based on user input.
- **Faceted Search:** Allows users to refine their search using dynamic facets that adapt based on the chosen category, search input, and previously selected facets.
- **Product Details:** Provides detailed information about specific products, including variations (the same products, but with small differences such as color, size, etc.).
- **Product Categories:** Lists available product categories.
- **Deals and Events:** Highlights special offers and events related to products.

# Technology Stack

### Programming Languages
[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

### Frameworks
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)

### Testing Framework
![Static Badge](https://img.shields.io/badge/Pytest-8.3.2-white?style=plastic&logo=pytest&logoColor=white&color=white)

### Databases
![Static Badge](https://img.shields.io/badge/MongoDB-7.0-green?logo=mongodb)
![Static Badge](https://img.shields.io/badge/Redis-8.0-%23FF4438?logo=redis&labelColor=black)

# Setup
### 1. Clone repository with:
```bash
git clone https://github.com/GhostMEn20034/SMILE_SALES_product_microservice.git
```
### 2. Create .env file:
on Windows (PowerShell), run:
```powershell
New-Item -Path ".env" -ItemType "File"
```
on Unix or MacOS, run:
```bash
touch .env
```
### 3. Open any editor and paste the next variables:
```sh
mongodb_url=YourMongoDbURL
redis_cache_url=YourRedisUrl
atlas_search_product_index_name=some_index_name # The name of the search index for product search in your MongoDB cluster
atlas_search_search_terms_index_name=other_index_name # The name of the search index for search terms autocomplete in your MongoDB cluster
allowed_origins='["http://localhost:3000"]' # List of allowed origins (REMOVE SINGLE QUOTES IF YOU GONNA RUN THE APP AS DOCKER IMAGE)
relevance_threshold=0.22 # Determines minimum relevance score of search item to be not excluded
```

# Running The app
If you want to run this app you have two options:
 - Run it with `python` command
 - Run it as Docker Image

### 1. Running with `python` command
#### 1.1 Create Python's virtual environment:
```bash
python -m venv venv
```
#### 1.2. Activate the virtual environment:
on Windows (PowerShell), run:
```powershell
.\venv\Scripts\activate.ps1
```
on Unix or MacOS, run:
```bash
source venv/bin/activate
```
### 1.3 Install all dependencies:
```bash
pip install -r requirements.txt
```
#### 1.4 export all .env values as environment variables, you can do that with command:
```bash
export $(xargs < .env)
```
#### 1.5 Enter the command to run the app:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### 2. Running as Docker Image
#### 2.1 Build the docker image
```bash
docker build -f DockerfileLocal -t your-image-name:latest .
```
if you want to run the container in the production environment, build the image with the command:
```bash
docker build -f DockerfileProd -t your-image-name:latest .
```

#### 2.2 Run the built image
```
docker run -d -p 8000:8000 --env-file ./.env your-image-name:latest
```

# Testing
Before running tests, you need to export the environment variable that indicates we run the app in the test mode:
```bash
export TEST_MODE=1
```
**Note**: It's highly recommended to run tests with temporary MongoDB instance that don't store any data. Because if you forget to set `TEST_MODE=1`, tests will populate data in the database where you store data, and delete all data after that.
To replace your MongoDB instance, just replace the `mongodb_url` value in `.env` file with the temporary instance's url.

To run tests use command:
```
pytest /tests
```



