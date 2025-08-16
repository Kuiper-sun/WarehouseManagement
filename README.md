# Smart Warehousing & Inventory Management System

![Laravel](https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Metabase](https://img.shields.io/badge/Metabase-5094E3?style=for-the-badge&logo=metabase&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

A full-stack, multi-container application demonstrating a modern smart warehousing solution. This project simulates real-time data flow from IoT sensors and RFID scans, stores it in a robust database, and visualizes the insights through a dynamic web application and a business intelligence dashboard.

---

## System Architecture

This project utilizes a microservices-oriented architecture orchestrated with Docker Compose. Each service runs in its own container, ensuring modularity and scalability.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Flask API     │────│  PostgreSQL     │────│   Metabase      │
│ (Data Generator)│    │ (Data Storage)  │    │ (BI Analytics)  │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        ▲                                                        
        │ HTTP GET (for stats)                                         
        │                                                    
┌─────────────────┐    ┌─────────────────┐                    
│                 │    │                 │                    
│   Laravel App   │────│      Nginx      │<─── User's Browser
│  (Web Dashboard)│    │   (Web Server)  │                    
│                 │    │                 │                    
└─────────────────┘    └─────────────────┘                    
```

### Key Technologies:
*   **Backend:** Laravel (PHP), Flask (Python)
*   **Database:** PostgreSQL
*   **Frontend:** Tailwind CSS
*   **Analytics:** Metabase
*   **Containerization:** Docker & Docker Compose
*   **Web Server:** Nginx

---

## Features

*   **Real-Time Data Simulation:** A Flask service continuously generates realistic RFID scan and sensor data.
*   **Dynamic Web Dashboard:** A beautiful dark-mode dashboard built with Laravel and Tailwind CSS that displays live KPI cards.
*   **Embedded Business Intelligence:** A full Metabase dashboard with multiple charts and visualizations is seamlessly embedded into the Laravel application.
*   **Persistent Data Storage:** PostgreSQL database managed with a Docker volume to ensure data is saved between sessions.
*   **Multi-Container Environment:** The entire system is orchestrated with Docker Compose for easy setup and teardown.
*   **RESTful Principles:** The Flask API provides endpoints for starting/stopping data generation and can be extended to serve data to other services.

---

## Getting Started

Follow these instructions to get the entire system up and running on your local machine.

### Prerequisites

*   [Docker](https://www.docker.com/products/docker-desktop/) installed and running.
*   [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop).
*   A terminal or command prompt (like Git Bash, PowerShell, or Windows Terminal).

### First-Time Setup

This process will build the containers, install all dependencies, and run the necessary setup commands.

**1. Clone the Repository**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
*(Replace the URL with your own repository's URL after you've pushed it to GitHub).*

**2. Copy the Environment File**
The Laravel application requires a `.env` file for its configuration.
```bash
# For Windows (Command Prompt)
copy .env.example .env

# For macOS/Linux
# cp .env.example .env
```
*(Note: The default `.env` file is already configured to work with Docker Compose).*

**3. Build and Start All Services**
This is the main command. It will build all your custom images and start the containers in the background.
```bash
docker-compose up -d --build
```
The first time you run this, it may take several minutes to download all the base images.

**4. Install Laravel Dependencies**
This command runs `composer install` inside the Laravel container to download all the necessary PHP packages.
```bash
docker-compose exec laravel-app composer install
```

**5. Run Laravel Setup Commands**
After the containers are running, we need to run a few commands inside the Laravel container to finalize the setup.

   *   **Generate Application Key:**
     ```bash
     docker-compose exec laravel-app php artisan key:generate
     ```
   *   **Set Permissions:**
     ```bash
     docker-compose exec laravel-app chmod -R 777 storage bootstrap/cache
     ```
   *   **Run Database Migrations:** (This creates the `users`, `sessions`, etc. tables)
     ```bash
     docker-compose exec laravel-app php artisan migrate
     ```

**6. Configure Metabase**
*   Open your browser and navigate to **`http://localhost:3000`**.
*   Follow the on-screen instructions to create your admin account.
*   When prompted to add your data, select **PostgreSQL** and use the details found in your `docker-compose.yml` and `.env` files. The host will be `postgres`.
*   Explore your data and build your dashboards! Remember to **enable public sharing** and **publish** your dashboard to get the embed link, then update it in the `resources/views/analytics.blade.php` file.

---

## How to Use the Application

Once the setup is complete, your system is live.

*   **Main Dashboard:** `http://localhost:8000/analytics`
*   **Metabase:** `http://localhost:3000`
*   **Flask API Health Check:** `http://localhost:5000/health`

**To start the live data flow:**
```bash
curl -X POST http://localhost:5000/api/start-data-generation
```

**To stop the live data flow:**
```bash
curl -X POST http://localhost:5000/api/stop-data-generation
```

**To watch the live logs from the data generator:**
```bash
docker-compose logs -f flask-api
```

---

## Stopping the Environment

To stop the entire application stack, run:
```bash
docker-compose down
```
Your Metabase and PostgreSQL data will be preserved in Docker volumes. If you want to delete **everything** (including all data) for a completely fresh start, use:
```bash
docker-compose down -v
```

---
