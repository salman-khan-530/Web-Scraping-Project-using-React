# E-Commerce Product Scraper

A full-stack web scraping application that searches and collects product data from supported e-commerce sources. The project uses a **React + Vite frontend**, **FastAPI backend**, and a modular Python scraper architecture.

The application provides a web interface where users can select a source, enter a search query, and retrieve structured product information.

## 🌐 Live Demo

**Frontend:**
https://web-scraping-project-using-react-6q.vercel.app/

**Backend API:**
https://web-scraping-project-using-react.vercel.app/

## 📌 Project Overview

The **E-Commerce Product Scraper** is designed as a modular full-stack application for collecting and processing product information.

The project currently uses **Books to Scrape** as the test/demo source. It is a practice website specifically designed for web scraping projects.

The application follows an API-based architecture:

```text
React Frontend
      ↓
FastAPI Backend
      ↓
ScraperManager
      ↓
Selected Scraper
      ↓
Product Data
      ↓
React UI
```

The architecture also provides adapters for future authorized integrations with e-commerce platforms such as Amazon, Flipkart, and Alibaba.

> **Important:** The project does not attempt to bypass CAPTCHAs, authentication, anti-bot systems, or other access controls. Production e-commerce integrations should use authorized APIs or approved data-access methods.

---

## ✨ Key Features

### Frontend

* React-based user interface
* Vite development and build system
* Website/source selection
* Product search
* Configurable maximum number of products
* Product result display
* API integration with FastAPI
* Responsive interface
* Production deployment on Vercel

### Backend

* FastAPI REST API
* CORS configuration for local and production frontend
* Query validation
* Maximum product limit validation
* Error handling with HTTP exceptions
* Modular scraper management
* Production deployment on Vercel

### Scraper System

* Object-oriented scraper architecture
* `BaseScraper` interface
* Centralized `ScraperManager`
* Books to Scrape test scraper
* Pagination support
* HTTP request handling
* robots.txt checking
* Polite request delays
* Product data extraction
* Data cleaning and normalization
* Duplicate handling
* CSV and Excel export functionality

---

## 🛠️ Technologies Used

### Frontend

* **React**
* **Vite**
* **JavaScript**
* **HTML**
* **CSS**

### Backend

* **Python 3.12**
* **FastAPI**
* **Uvicorn**
* **Requests**
* **BeautifulSoup4**
* **Pandas**
* **OpenPyXL**
* **Python-dotenv**

### Development & Deployment

* **Git**
* **GitHub**
* **Vercel**
* **VS Code**

---

## 📂 Project Directory Structure

```text
Web-Scraping-Project-React/
│
├── backend/
│   └── main.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── ...
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── scraper/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── scraper_manager.py
│   ├── test_scraper.py
│   ├── amazon_scraper.py
│   ├── flipkart_scraper.py
│   ├── alibaba_scraper.py
│   ├── http_client.py
│   ├── robots_checker.py
│   ├── data_processor.py
│   ├── exporter.py
│   ├── analyzer.py
│   ├── config.py
│   └── logger.py
│
├── tests/
│   └── ...
│
├── notebooks/
│   └── ...
│
├── output/
│   └── ...
│
├── logs/
│   └── ...
│
├── .env.example
├── .gitignore
├── requirements.txt
├── vercel.json
└── README.md
```

> The `frontend/` directory contains the React application, while `backend/` contains the FastAPI API. The `scraper/` directory contains the reusable scraping and data-processing logic.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/salman-khan-530/Web-Scraping-Project-using-React.git
```

Move into the project:

```bash
cd Web-Scraping-Project-using-React
```

---

### 2. Create Python Virtual Environment

```powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment again:

```powershell
.venv\Scripts\Activate.ps1
```

---

### 3. Install Backend Dependencies

```powershell
pip install -r requirements.txt
```

---

### 4. Install Frontend Dependencies

Open a terminal inside the `frontend` directory:

```powershell
cd frontend
```

Install the Node.js dependencies:

```powershell
npm install
```

---

## ▶️ Running the Project Locally

The backend and frontend run separately.

### Start the FastAPI Backend

From the project root:

```powershell
uvicorn backend.main:app --reload
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

### Start the React Frontend

Open another terminal:

```powershell
cd frontend
```

Then:

```powershell
npm run dev
```

Vite will provide a local URL, normally:

```text
http://localhost:5173
```

---

## 🔗 API Configuration

The React frontend uses the `VITE_API_URL` environment variable to determine which FastAPI backend it should communicate with.

For local development, create:

```text
frontend/.env
```

and add:

```env
VITE_API_URL=http://127.0.0.1:8000
```

For production, the Vercel frontend uses:

```env
VITE_API_URL=https://web-scraping-project-using-react.vercel.app
```

### Important

Environment variables beginning with `VITE_` are exposed to the frontend. Therefore, **never put private API keys or secrets in `VITE_*` variables.**

---

## 🔌 API Endpoints

### Home

```http
GET /
```

Returns a message confirming that the API is running.

Example response:

```json
{
  "message": "E-Commerce Product Scraper API is running!"
}
```

---

### Search Products

```http
GET /products
```

Parameters:

| Parameter      | Type    | Description                |
| -------------- | ------- | -------------------------- |
| `website`      | string  | Scraper/source to use      |
| `query`        | string  | Product search query       |
| `max_products` | integer | Maximum number of products |

Example:

```text
/products?website=test&query=book&max_products=10
```

Example response structure:

```json
{
  "website": "test",
  "query": "book",
  "count": 10,
  "products": []
}
```

---

## 🧩 Scraper Architecture

The scraper system is designed using a modular architecture.

```text
ScraperManager
      │
      ├── TestScraper
      │
      ├── AmazonScraper
      │
      ├── FlipkartScraper
      │
      └── AlibabaScraper
```

The `ScraperManager` selects the appropriate scraper based on the requested website.

Each scraper follows the common `BaseScraper` interface, allowing different data sources to produce a consistent product structure.

---

## 📦 Product Data

The scraper is designed to return structured product records containing fields such as:

```text
name
price
rating
availability
url
category
description
source
```

This standardized structure makes it easier to process and display products from different sources.

---

## 🧹 Data Processing

The project includes data-processing functionality for:

* Text cleaning
* Price normalization
* Rating normalization
* Availability normalization
* Missing-value handling
* Duplicate removal
* Data validation
* Structured output generation

---

## 🤖 Test Website

The current working scraper uses:

**Books to Scrape**

https://books.toscrape.com/

Books to Scrape is used as the project's demonstration source because it is specifically designed for practicing web scraping.

The application can:

* Search products
* Extract product information
* Navigate product pages
* Handle pagination
* Return structured product data

---

## 🔐 Authorized E-Commerce Integrations

The project includes scraper adapter modules for:

* Amazon
* Flipkart
* Alibaba

These integrations are intended for **authorized API access**.

API credentials should be stored in environment variables and should never be committed to GitHub.

Example:

```env
AMAZON_API_KEY=your_key_here
FLIPKART_API_KEY=your_key_here
ALIBABA_API_KEY=your_key_here
```

The actual `.env` file should remain private.

---

## 🧪 Testing

Automated tests are located inside the:

```text
tests/
```

Run the test suite with:

```powershell
python -m unittest discover tests -v
```

The tests cover different components of the scraping system, including HTTP handling, robots.txt checking, scraping logic, data processing, exporting, and scraper management.

---

## 🚀 Deployment

The project uses two separate Vercel deployments.

### Frontend

The React/Vite frontend is deployed from:

```text
frontend/
```

Live frontend:

https://web-scraping-project-using-react-6q.vercel.app/

### Backend

The FastAPI backend is deployed from:

```text
backend/main.py
```

Live backend:

https://web-scraping-project-using-react.vercel.app/

The frontend communicates with the backend through the `VITE_API_URL` environment variable.

---

## 🌐 Deployment Architecture

```text
                    User
                      │
                      ▼
            ┌─────────────────┐
            │  React + Vite   │
            │    Frontend     │
            └────────┬────────┘
                     │
                     │ HTTP Request
                     ▼
            ┌─────────────────┐
            │     FastAPI     │
            │     Backend     │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ ScraperManager  │
            └────────┬────────┘
                     │
             ┌───────┴────────┐
             ▼                ▼
      Test Scraper       API Adapters
             │          Amazon / etc.
             ▼
        Product Data
             │
             ▼
       JSON Response
             │
             ▼
        React Frontend
```

---

## 🛡️ Security & Responsible Scraping

This project follows responsible web-scraping practices.

* No CAPTCHA bypassing
* No anti-bot protection bypassing
* No credential exposure
* API keys are stored through environment variables
* The test website is used for scraping practice
* Production e-commerce integrations should use authorized APIs
* `robots.txt` rules are considered by the scraping system
* Requests are handled with controlled delays

---

## 🔮 Future Improvements

Possible future improvements include:

* Add more authorized API integrations
* Add advanced product filtering
* Add sorting by price and rating
* Add product category filters
* Add user authentication
* Add database storage
* Add search history
* Improve mobile responsiveness
* Add automated CI/CD testing
* Add more comprehensive API documentation
* Add product analytics and visualization

---

## 👨‍💻 Author

**Salman Khan**

BS Computer Science (Artificial Intelligence)
Abdul Wali Khan University Mardan

---

## 📄 License

This project was developed as part of **Internship Task 11** for educational and demonstration purposes.

The project is intended to demonstrate full-stack development, web scraping, API development, data processing, and deployment.
