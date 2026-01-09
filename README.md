# AISQLite

An intelligent security analysis system that combines OWASP ZAP security scanning, SQLite data management, and Azure AI agents to provide natural language querying and automated reporting of security vulnerabilities.

## Overview

AISQLite is a full-stack application that:
1. **Runs security scans** using OWASP ZAP on web applications
2. **Stores scan results** in a SQLite database
3. **Processes natural language queries** using Azure AI agents
4. **Generates SQL queries** automatically from NLP requests
5. **Creates visual reports** (graphs/charts) from security data

This project transforms raw security vulnerability data into actionable insights through an intuitive natural language interface.

## Features

- 🔒 **Security Scanning**: Integration with OWASP ZAP for comprehensive web security assessments
- 🗄️ **Data Management**: SQLite-based storage for vulnerability data and alerts
- 🤖 **AI-Powered Queries**: Azure AI agents convert natural language to SQL automatically
- 📊 **Visual Reporting**: Automatic chart and graph generation from query results
- ☁️ **Cloud-Ready**: Azure-native architecture using Azure AI Services
- 🔄 **Automated Pipeline**: End-to-end workflow from scanning to reporting

## Project Structure

```
AISQLite/
├── azureVersion/              # Main Azure-integrated implementation
│   ├── main.py               # Application entry point
│   ├── backend/              # Backend services
│   │   ├── backend_ai.py     # Azure AI agent orchestration
│   │   ├── produce_chart.py  # Chart generation using AI
│   │   ├── run_query.py      # SQL query execution
│   │   ├── XML_to_db.py      # ZAP XML to SQLite conversion
│   │   ├── zap.db            # SQLite database
│   │   └── sql_to_use.txt    # SQL query templates
│   ├── frontend/             # Frontend interface
│   │   └── frontend_ai.py    # User interface
│   ├── middleware/           # Middleware services
│   │   └── run_zap.py        # OWASP ZAP execution
│   ├── instructions/         # AI instruction templates
│   │   ├── SQL_CREATION_INSTRUCTIONS.txt
│   │   └── GET_YAML_INSTRUCTIONS.txt
│   └── output/               # Generated outputs
│       ├── report.xml        # ZAP scan report
│       └── updated_zap.yaml  # ZAP configuration
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

## Prerequisites

- **Python 3.8+**
- **OWASP ZAP** - Security scanning tool
- **SQLite3** - Database engine
- **Azure Account** with:
  - Azure AI Services configured
  - Azure AI Project with Foundry setup
  - Project connection string

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AISQLite
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Azure Credentials

Create a `.env` file in the `azureVersion` directory:

```env
PROJECT_CONNECTION_STRING=your_azure_project_connection_string
AZURE_SUBSCRIPTION_ID=your_subscription_id
```

### 4. Install OWASP ZAP

**Linux:**
```bash
sudo apt-get install zaproxy
```

**macOS:**
```bash
brew install zaproxy
```

**Windows:** Download from [OWASP ZAP](https://www.zaproxy.org/)

### 5. Initialize Database

The database is created automatically on first run when XML data is imported.

## Quick Start

### Basic Usage

```bash
cd azureVersion
python main.py
```

The application will:
1. Launch the frontend interface
2. Execute OWASP ZAP scan
3. Convert ZAP XML output to SQLite database
4. Start the backend AI system
5. Wait for your natural language query

### Example Query

```
What do you want to know about the database? Show me the most common XSS vulnerabilities
```

The system will:
1. Convert your question to SQL using Azure AI
2. Execute the query against the vulnerability database
3. Generate a visual chart of the results

## Components

### Backend (`azureVersion/backend/`)

- **backend_ai.py**: Orchestrates Azure AI agents for query generation and processing
- **XML_to_db.py**: Parses OWASP ZAP XML reports and imports into SQLite
- **produce_chart.py**: Uses AI agents to generate visualization charts
- **run_query.py**: Executes SQL queries and returns results

### Frontend (`azureVersion/frontend/`)

- **frontend_ai.py**: User interface for query input and result display

### Middleware (`azureVersion/middleware/`)

- **run_zap.py**: Orchestrates OWASP ZAP security scanning

## Database Schema

The SQLite database includes the following main table:

**alerts**
- `id` - Alert identifier
- `site_name` - Website being scanned
- `alerts` - Alert/vulnerability type
- `riskcode` - Risk severity code
- `affected_url` - URL affected by vulnerability

## Configuration

### SQL Queries

Modify `azureVersion/backend/sql_to_use.txt` to change the default SQL template used for data analysis.

### AI Instructions

Update `azureVersion/instructions/SQL_CREATION_INSTRUCTIONS.txt` to customize how the AI generates SQL from natural language.

### ZAP Configuration

Edit `azureVersion/output/updated_zap.yaml` to customize OWASP ZAP scanning behavior.

## Authentication

The application uses Azure Identity with `DefaultAzureCredential()` which supports:
- Environment variables
- Azure CLI authentication
- Managed Identity (when running on Azure)
- Visual Studio Code login
- Shared credentials

Ensure you're authenticated: `az login`

## Troubleshooting

### Database Not Found
```
Error: Database file not found
```
Solution: Ensure OWASP ZAP has completed scanning and XML_to_db.py has been executed.

### Azure Connection Error
```
Error: Failed to connect to Azure AI
```
Solution: Verify PROJECT_CONNECTION_STRING in `.env` and ensure `az login` is executed.

### ZAP Not Running
```
Error: ZAP process not found
```
Solution: Install ZAP and ensure it's in your system PATH.

## Performance Considerations

- First run takes longer due to AI agent initialization
- Large scan reports may take time to import into SQLite
- Chart generation varies based on query complexity

## Security Notes

- Store Azure credentials securely (use `.env` with `.gitignore`)
- Never commit sensitive credentials to the repository
- Use managed identities in production environments
- Restrict database file permissions

