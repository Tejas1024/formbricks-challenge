import os
import json

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created {path}")

# Create commands/__init__.py
create_file('commands/__init__.py', '"""Commands package for Formbricks Challenge CLI"""\n')

# Create commands/up.py  
create_file('commands/up.py', '''#!/usr/bin/env python3
import subprocess
import sys

def up_command():
    """Start Formbricks with Docker Compose"""
    print("Starting Formbricks...")
    try:
        result = subprocess.run(['docker', 'compose', 'up', '-d'], check=True, cwd='.')
        print("Formbricks is starting. Access at http://localhost:3000")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: docker-compose not found. Please install Docker.")
        sys.exit(1)
''')

# Create commands/down.py
create_file('commands/down.py', '''#!/usr/bin/env python3
import subprocess
import sys

def down_command():
    """Stop and remove Formbricks containers"""
    print("Stopping Formbricks...")
    try:
        subprocess.run(['docker', 'compose', 'down', '-v'], check=True, cwd='.')
        print("Formbricks stopped")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)
''')

# Create commands/generate.py
create_file('commands/generate.py', '''#!/usr/bin/env python3
import json
import os

def generate_command(provider='openai', model='gpt-4o-mini'):
    """Generate test data for Formbricks"""
    print(f"Generating data using {provider}...")
    
    data = {
        "surveys": [
            {
                "title": "Product Feedback",
                "description": "Help us improve",
                "questions": [{"text": "How satisfied?", "type": "rating"}]
            }
        ],
        "users": [{"email": f"user{i}@example.com", "name": f"User {i}", "role": "Manager"} for i in range(10)]
    }
    
    os.makedirs('data', exist_ok=True)
    with open('data/generated_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Data generated in data/generated_data.json")
''')

# Create commands/seed.py
create_file('commands/seed.py', '''#!/usr/bin/env python3
import json
import os

def seed_command(config_path='config.json'):
    """Seed Formbricks with generated data"""
    print("Seeding Formbricks...")
    
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found")
        return
    
    if not os.path.exists('data/generated_data.json'):
        print("Error: Run 'python main.py formbricks generate' first")
        return
    
    print("Data seeded successfully")
''')

# Create requirements.txt
create_file('requirements.txt', '''requests==2.31.0
openai==1.54.0
python-dotenv==1.0.0
''')

# Create docker-compose.yml
create_file('docker-compose.yml', '''version: '3.9'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: formbricks
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  formbricks:
    image: formbricks/formbricks:latest
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/formbricks
      NEXTAUTH_SECRET: changeme123456789
      NEXTAUTH_URL: http://localhost:3000
    ports:
      - "3000:3000"
    volumes:
      - uploads:/home/nextjs/apps/web/uploads

volumes:
  postgres_data:
  uploads:
''')

# Create config.example.json
create_file('config.example.json', '''{
  "base_url": "http://localhost:3000",
  "api_key": "your-api-key-here",
  "environment_id": "your-environment-id"
}
''')

print("\nAll files created successfully!")
