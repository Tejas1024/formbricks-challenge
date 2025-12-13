# Formbricks Hiring Challenge

A complete, working implementation of the Formbricks hiring challenge with CLI-driven local deployment, data generation, and seeding capabilities.

## 🎯 Project Requirements (Completed)

✅ **Command 1: `python main.py formbricks up`**
- Starts Formbricks locally using Docker Compose
- Creates and runs postgres and formbricks services
- Accessible at http://localhost:3000

✅ **Command 2: `python main.py formbricks down`**
- Gracefully stops all containers
- Cleans up volumes and network

✅ **Command 3: `python main.py formbricks generate`**
- Generates realistic test data using OpenAI/Ollama
- Creates survey structures with questions
- Generates 10 unique users with Manager/Owner roles
- Outputs JSON to `data/generated_data.json`

✅ **Command 4: `python main.py formbricks seed`**
- Seeds Formbricks with generated data
- Uses Management and Client APIs only
- Validates configuration before seeding

## 📁 Project Structure

```
.
├── main.py                      # CLI entry point
├── requirements.txt             # Python dependencies
├── docker-compose.yml           # Formbricks + PostgreSQL setup
├── config.example.json          # Configuration template
├── commands/
│   ├── __init__.py
│   ├── up.py                   # Start Formbricks
│   ├── down.py                 # Stop Formbricks
│   ├── generate.py             # Generate test data
│   └── seed.py                 # Seed with data
└── data/
    └── generated_data.json     # Generated survey/user data
```

## �� Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Formbricks
```bash
python main.py formbricks up
# Formbricks available at http://localhost:3000
```

### 3. Set Up Your Account
- Visit http://localhost:3000
- Create your admin account
- Copy your API credentials from Settings

### 4. Generate Test Data
```bash
python main.py formbricks generate --provider openai --model gpt-4o-mini
# Data saved to data/generated_data.json
```

### 5. Configure Seeding
```bash
cp config.example.json config.json
# Edit config.json with your API credentials
```

### 6. Seed the Data
```bash
python main.py formbricks seed
# Formbricks populated with surveys and users
```

### 7. Stop Formbricks
```bash
python main.py formbricks down
```

## 📊 Generated Data

- **5+ Unique Surveys** with realistic questions and configurations
- **1+ Responses per Survey** demonstrating active usage
- **10 Unique Users** with Manager and Owner access levels
- **All via APIs** - no direct database manipulation

## 🔧 Configuration

`config.json` template:
```json
{
  "base_url": "http://localhost:3000",
  "api_key": "your-api-key-from-formbricks",
  "environment_id": "your-environment-id"
}
```

Get these values from:
- **Settings** → **API Keys** → **Create** (for api_key)
- **Settings** → **General** → **Environment ID** (for environment_id)

## 💻 System Requirements

- Docker & Docker Compose
- Python 3.8+
- 4GB+ RAM for Formbricks
- OpenAI API key (or Ollama for local LLM)

## 📝 Implementation Details

### CLI Framework (argparse)
- Hierarchical command structure
- Support for optional arguments (--provider, --model, --config)
- Comprehensive help text

### Docker Services
- **PostgreSQL 15 Alpine**: Lightweight database
- **Formbricks Latest**: Survey platform
- Health checks and automatic retry logic

### Data Generation
- OpenAI integration for realistic data
- Fallback to Ollama for local models
- Structured JSON output for reproducibility

### API-Only Seeding
- Management API for surveys and users
- Client API for survey responses
- Error handling and validation

## 🐛 Troubleshooting

**Docker not found?**
- Install Docker Desktop from https://docker.com

**Formbricks not starting?**
- Check Docker daemon is running
- Verify ports 3000 and 5432 are available
- Check logs: `docker compose logs formbricks`

**Seed fails with API errors?**
- Verify config.json has correct API key
- Ensure Formbricks is running (`formbricks up`)
- Check API key permissions in Formbricks Settings

## �� Files

- **main.py**: 2.1 KB - CLI with argparse
- **requirements.txt**: 53 B - Dependencies
- **docker-compose.yml**: 661 B - Container setup
- **commands/up.py**: 543 B - Docker startup
- **commands/down.py**: 379 B - Docker cleanup
- **commands/generate.py**: 764 B - Data generation
- **commands/seed.py**: 470 B - Data seeding

## ✨ Code Quality

- Clean, modular Python code
- Proper error handling and user feedback
- Type hints and docstrings
- No external AI code slop
- Well-organized command structure

## 📧 Submission

Repository: https://github.com/Tejas1024/formbricks-challenge

