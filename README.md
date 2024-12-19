# Fake News Detection Project

Welcome to the **Fake News Detection** project! 🎉

This repository contains both the **frontend** and **backend** components needed to run the project. Before you can run the code, you will need to download a couple of files and set up the project folder structure.

## 🚀 Getting Started

To get started, follow these simple steps:

### Step 1: Download the Necessary Files

1. Download the **frontend** folder from the [Fake-News-Detection-FE repository](https://github.com/azzansm/Fake-News-Detection-FE).
2. Download the **backend** folder from this repository (this one) to your local machine.

### Step 2: Organize the Files

Once you've downloaded both folders, your folder structure should look like this:

project/
│
├── frontend/         # All frontend-related code
│   ├── [React, Vite files...]
│
├── backend/          # All backend-related code
│   ├── [API, models, server files...]
│
└── docker-compose.yml  # Docker Compose file (at the root level)


### Step 3: Set Up Docker

Inside the root of the **project** folder, you will find the **docker-compose.yml** file. This file helps you easily run both the frontend and backend in containers, making the setup seamless.

### Step 4: Run the Project

Now that your folder structure is set up, you can run the project using Docker. Simply run the following command from the **project** folder:

```bash
docker-compose up


