# 07_sports_data_backup
**Week 3 - Day 3:** Building an automated Sports Data Backup

## Automated Sports Data Backup
![Project Structure](05_azure_highlight_processor.drawio.png)

## Project Overview
This project automates the process of fetching sports highlights, storing the data in **Azure Blob Storage**, **CosmosDB**. It also processes the data to retrieve and save the video files (higlights) in **Azure Blob Storage**. The application is containerized using **Docker** and deployed to **Azure Container Apps**. It runs on a schedule using **Azure Container Apps Jobs**.

## Features
- Fetch Highlights: Retrieve sports highlights from a RapidAPI endpoint.
- Store Data: Save JSON data and processed videos in Azure Blob Storage, and CosmosDB.
- Containerized: The application is containerized using Docker.
- Scheduled Jobs: Run tasks on a schedule using Azure Container Apps Jobs.

## Technologies Used
**Azure Services:**
- Azure Blob Storage
- Azure Cosmos DB
- Azure Container Registry
- Azure Container Apps

**Programming Language:** Python 3.x

**Containerization:** Docker

**Infrastructure as Code:** Azure CLI

## Prerequisites
- Azure Account: An Azure account with sufficient permissions to create resources.
- Azure CLI: Installed and configured on your local machine.
- Docker: Installed locally for building and pushing the container image.
- RapidAPI Key: A valid API key for the RapidAPI Sports API.
- Python 3.x: Installed locally for development.

## Dependencies
- requests
- azure-cosmos
- azure-storage-blob
- azure-identity
- azure-mgmt-storage
- azure.mgmt.resource
- python-dotenv

## Project Structure
```shell
07_sports_data_backup/
├── config.py           # Configures environment variables
├── fetch.py            # Fetch highlights from RapidAPI and store in cosmosdb and azure blob storage
├── process_videos.py   # Extracts video from url in data and save video in azure blob storage
├── run_all.py          # Runs the entire workflow in sequence
├── Dockerfile          # Dockerfile for containerizing the app
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables file
├── .env
└── README.md           # Project documentation
```

## steps
1. Clone the repository
  ```shell
  git clone git@github.com:Jekwulum/07_sports_data_backup.git
  cd 07_sports_data_backup
  ```
2. Log in via Azure CLI
  ```shell
  az login
  ```
3. Create a resource group
  ```shell
  az group create --name <ResourceGroupName> --location <Location> # e.g. location -> eastus
  az group show --name <ResourceGroupName> # view resource group
  ```
4. Create a Cosmos DB Account
  ```shell
  az cosmosdb create --name <CosmosDBAccountName> --resource-group <ResourceGroupName> --locations regionName=<Location>
  ```
5. Create a Database and Container
  ```shell
  az cosmosdb sql database create --account-name <CosmosDBAccountName> --name <DatabaseName> --resource-group <ResourceGroupName>

  az cosmosdb sql container create --account-name <CosmosDBAccountName> --database-name <DatabaseName> --name <ContainerName> --resource-group
  ```

6. Create an Azure storage account
  ```shell
  az storage account create --name <StorageAccountName> --resource-group <ResourceGroupName> --location <Location>
  ```
7. Build and push your Docker image to ACR (Azure Container Registry)
  ```shell
  # create a container registry for the docker image
  az acr create --resource-group <ResourceGroupName> --name <ACRName> --sku Basic

  # log in to ACR
  az acr login --name <ACRName>

  # build the docker image
  docker build -t highlights-app .

  # tag the image
  docker tag highlights-app <ACRName>.azurecr.io/highlights-app:latest

  # push to ACR
  docker push <ACRName>.azurecr.io/highlights-api:latest
  ```
8. Create a container environment
  ```shell
  az containerapp env create --name <EnvName> --resource-group <ResourceGroupName> --location <Location>
  ```
9. Create the **Container App Job** in the Azure Portal