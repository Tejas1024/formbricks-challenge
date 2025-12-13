#!/usr/bin/env python3
"""
Formbricks Challenge Project Setup Script
Run with: python3 setup.py
"""

import os
import sys

def create_file(path, content):
    """Create a file with given content"""
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"✓ Created {path}")

def setup_project():
    """Create all project files"""
    
    print("🚀 Setting up Formbricks Challenge Project\n")
    
    # main.py
    create_file('main.py', '''#!/usr/bin/env python3
"""
Formbricks Challenge - Main CLI Entry Point
"""
import sys
import argparse
from commands.up import up_command
from commands.down import down_command
from commands.generate import generate_command
from commands.seed import seed_command


def main():
    parser = argparse.ArgumentParser(
        description='Formbricks Challenge CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='service', help='Service to manage')
    
    # Formbricks subcommand
    formbricks_parser = subparsers.add_parser('formbricks', help='Manage Formbricks instance')
    formbricks_subparsers = formbricks_parser.add_subparsers(dest='command', help='Command to execute')
    
    # Up command
    formbricks_subparsers.add_parser('up', help='Start Formbricks locally')
    
    # Down command
    formbricks_subparsers.add_parser('down', help='Stop Formbricks and clean up')
    
    # Generate command
    generate_parser = formbricks_subparsers.add_parser('generate', help='Generate realistic data using LLM')
    generate_parser.add_argument('--provider', default='openai', choices=['openai', 'ollama'], 
                                help='LLM provider to use')
    generate_parser.add_argument('--model', default='gpt-4o-mini', 
                                help='Model to use for generation')
    
    # Seed command
    seed_parser = formbricks_subparsers.add_parser('seed', help='Seed Formbricks with generated data')
    seed_parser.add_argument('--data-file', default='generated_data.json',
                           help='Path to generated data file')
    
    args = parser.parse_args()
    
    if args.service != 'formbricks':
        parser.print_help()
        sys.exit(1)
    
    if not args.command:
        formbricks_parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'up':
            up_command()
        elif args.command == 'down':
            down_command()
        elif args.command == 'generate':
            generate_command(provider=args.provider, model=args.model)
        elif args.command == 'seed':
            seed_command(data_file=args.data_file)
        else:
            formbricks_parser.print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        print("\\n\\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
''')

    # commands/__init__.py
    create_file('commands/__init__.py', '''"""
Commands package for Formbricks Challenge CLI
"""
''')

    # commands/up.py
    create_file('commands/up.py', '''"""
Command to start Formbricks locally using Docker Compose
"""
import subprocess
import time
import os
import sys
import requests
from pathlib import Path


def check_docker():
    """Check if Docker and Docker Compose are available"""
    try:
        subprocess.run(['docker', '--version'], capture_output=True, check=True)
        subprocess.run(['docker', 'compose', 'version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def create_docker_compose():
    """Create docker-compose.yml for Formbricks"""
    compose_content = """version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: formbricks
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  formbricks:
    image: formbricks/formbricks:latest
    restart: always
    depends_on:
      postgres:
        condition: service_healthy
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/formbricks?schema=public
      NEXTAUTH_SECRET: mysecretkey123456789012345678901234567890
      NEXTAUTH_URL: http://localhost:3000
      ENCRYPTION_KEY: encryptionkey12345678901234567890123
      CRON_SECRET: cronsecret123456789012345678901234567
      WEBAPP_URL: http://localhost:3000
      NEXT_PUBLIC_WEBAPP_URL: http://localhost:3000
      PRIVACY_URL: 
      TERMS_URL: 
      IMPRINT_URL: 
      GITHUB_ID: 
      GITHUB_SECRET: 
      GOOGLE_CLIENT_ID: 
      GOOGLE_CLIENT_SECRET: 
      AZUREAD_CLIENT_ID: 
      AZUREAD_CLIENT_SECRET: 
      AZUREAD_TENANT_ID: 
      NODE_ENV: production
    volumes:
      - uploads:/home/nextjs/apps/web/uploads/
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/api/health"]
      interval: 10s
      timeout: 5s
      retries: 10

volumes:
  postgres_data:
  uploads:
"""
    
    with open('docker-compose.yml', 'w') as f:
        f.write(compose_content)
    
    print("✓ Created docker-compose.yml")


def create_env_file():
    """Create .env file with necessary configuration"""
    env_content = """# Formbricks Environment Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/formbricks?schema=public
NEXTAUTH_SECRET=mysecretkey123456789012345678901234567890
NEXTAUTH_URL=http://localhost:3000
ENCRYPTION_KEY=encryptionkey12345678901234567890123
WEBAPP_URL=http://localhost:3000
NEXT_PUBLIC_WEBAPP_URL=http://localhost:3000
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✓ Created .env file")


def wait_for_formbricks(max_wait=180):
    """Wait for Formbricks to be ready"""
    print("\\n⏳ Waiting for Formbricks to be ready...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            response = requests.get('http://localhost:3000/api/health', timeout=2)
            if response.status_code == 200:
                print("✓ Formbricks is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        elapsed = int(time.time() - start_time)
        sys.stdout.write(f"\\r⏳ Waiting... ({elapsed}s)")
        sys.stdout.flush()
        time.sleep(5)
    
    return False


def up_command():
    """Start Formbricks locally"""
    print("🚀 Starting Formbricks Challenge Setup\\n")
    
    # Check Docker
    print("📋 Checking prerequisites...")
    if not check_docker():
        print("❌ Docker or Docker Compose not found. Please install Docker Desktop.")
        sys.exit(1)
    print("✓ Docker and Docker Compose are available")
    
    # Create necessary files
    create_docker_compose()
    create_env_file()
    
    # Stop any existing containers
    print("\\n🧹 Cleaning up any existing containers...")
    subprocess.run(['docker', 'compose', 'down', '-v'], 
                  capture_output=True, stderr=subprocess.DEVNULL)
    
    # Start containers
    print("\\n🐳 Starting Docker containers...")
    result = subprocess.run(
        ['docker', 'compose', 'up', '-d'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Failed to start containers: {result.stderr}")
        sys.exit(1)
    
    print("✓ Containers started successfully")
    
    # Wait for Formbricks
    if not wait_for_formbricks():
        print("\\n❌ Formbricks failed to start within timeout period")
        print("Check logs with: docker compose logs formbricks")
        sys.exit(1)
    
    print("\\n" + "="*60)
    print("✅ Formbricks is now running!")
    print("="*60)
    print("\\n📍 Access Formbricks at: http://localhost:3000")
    print("\\n💡 Next steps:")
    print("   1. Set up your account at http://localhost:3000")
    print("   2. Run: python main.py formbricks generate")
    print("   3. Run: python main.py formbricks seed")
    print("\\n📝 Note: Save your API key from Formbricks settings for seeding")
    print("="*60)
''')

    # commands/down.py
    create_file('commands/down.py', '''"""
Command to stop Formbricks and clean up resources
"""
import subprocess
import sys
import os


def down_command():
    """Stop Formbricks and clean up"""
    print("🛑 Stopping Formbricks...\\n")
    
    # Check if docker-compose.yml exists
    if not os.path.exists('docker-compose.yml'):
        print("⚠️  No docker-compose.yml found. Nothing to stop.")
        return
    
    # Stop and remove containers, networks, volumes
    print("🐳 Stopping Docker containers...")
    result = subprocess.run(
        ['docker', 'compose', 'down', '-v'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Failed to stop containers: {result.stderr}")
        sys.exit(1)
    
    print("✓ Containers stopped and removed")
    print("✓ Volumes cleaned up")
    print("✓ Networks removed")
    
    # Optional: Clean up generated files
    cleanup_files = []
    for file in cleanup_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✓ Removed {file}")
            except Exception as e:
                print(f"⚠️  Could not remove {file}: {e}")
    
    print("\\n" + "="*60)
    print("✅ Formbricks stopped successfully!")
    print("="*60)
    print("\\n💡 To start again, run: python main.py formbricks up")
    print("="*60)
''')

    # commands/generate.py
    create_file('commands/generate.py', '''"""
Command to generate realistic data using LLM
"""
import json
import os
import sys
from openai import OpenAI


SURVEY_GENERATION_PROMPT = """Generate 5 unique, realistic surveys for a product feedback platform. Each survey should be well-designed with a clear purpose.

Return ONLY valid JSON (no markdown, no explanation) in this exact format:
{
  "surveys": [
    {
      "name": "Survey Name",
      "type": "app|website|link",
      "description": "Brief description",
      "questions": [
        {
          "type": "openText|multipleChoiceSingle|multipleChoiceMulti|nps|rating|cta",
          "headline": "Question text",
          "required": true|false,
          "choices": ["Option 1", "Option 2"] (only for multiple choice),
          "range": 5|7|10 (only for rating),
          "dismissButtonLabel": "Skip" (optional),
          "buttonLabel": "Next" (optional)
        }
      ]
    }
  ]
}

Survey types: "app" (in-app), "website" (website widget), "link" (shareable link)
Question types available: openText, multipleChoiceSingle, multipleChoiceMulti, nps, rating, cta

Requirements:
- Create 5 diverse surveys (product feedback, NPS, feature request, user onboarding, customer satisfaction)
- Each survey should have 3-5 questions
- Mix different question types appropriately
- Make questions realistic and professionally worded
- Include relevant choice options for multiple choice questions
- Use appropriate ranges for rating questions (5, 7, or 10)"""


USER_GENERATION_PROMPT = """Generate 10 unique, realistic users for a SaaS platform team.

Return ONLY valid JSON (no markdown, no explanation) in this exact format:
{
  "users": [
    {
      "name": "Full Name",
      "email": "email@example.com",
      "role": "Manager|Owner"
    }
  ]
}

Requirements:
- Create 10 users with realistic names
- Use professional email addresses
- Mix of Manager and Owner roles (at least 2 Owners, rest Managers)
- Diverse, realistic names
- Professional email format (firstname.lastname@company.com)"""


RESPONSE_GENERATION_PROMPT = """Generate realistic survey responses for the following survey:

Survey: {survey_name}
Questions: {questions}

Return ONLY valid JSON (no markdown, no explanation) with realistic, thoughtful responses:
{{
  "responses": [
    {{
      "questionId": "will be filled by system",
      "value": "response value - text for openText, choice label for multiple choice, number 0-10 for nps, number for rating"
    }}
  ]
}}

Requirements:
- Provide thoughtful, realistic responses
- For NPS: use numbers 0-10
- For ratings: use appropriate numbers based on the question
- For multiple choice: use exact choice labels
- For open text: write 1-3 realistic sentences
- Make responses coherent and professional"""


def generate_with_openai(prompt, model="gpt-4o-mini"):
    """Generate data using OpenAI API"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)
    
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a data generation assistant. Always return valid JSON only, no markdown formatting, no explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        # Clean any potential markdown formatting
        content = content.strip()
        if content.startswith('```'):
            lines = content.split('\\n')
            content = '\\n'.join(lines[1:-1]) if len(lines) > 2 else content
        
        return json.loads(content)
    except Exception as e:
        print(f"❌ Error calling OpenAI API: {e}")
        sys.exit(1)


def generate_with_ollama(prompt, model="llama2"):
    """Generate data using Ollama (local LLM)"""
    try:
        import requests
        
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'stream': False,
                'format': 'json'
            },
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"❌ Ollama API error: {response.status_code}")
            sys.exit(1)
        
        result = response.json()
        content = result.get('response', '{}')
        return json.loads(content)
    except Exception as e:
        print(f"❌ Error calling Ollama API: {e}")
        print("   Make sure Ollama is running: ollama serve")
        sys.exit(1)


def generate_command(provider='openai', model='gpt-4o-mini'):
    """Generate realistic data using LLM"""
    print("🤖 Generating realistic data with LLM...\\n")
    
    generate_func = generate_with_openai if provider == 'openai' else generate_with_ollama
    
    # Generate surveys
    print("📝 Generating surveys...")
    surveys_data = generate_func(SURVEY_GENERATION_PROMPT, model)
    surveys = surveys_data.get('surveys', [])
    print(f"✓ Generated {len(surveys)} surveys")
    
    # Generate users
    print("👥 Generating users...")
    users_data = generate_func(USER_GENERATION_PROMPT, model)
    users = users_data.get('users', [])
    print(f"✓ Generated {len(users)} users")
    
    # Generate responses for each survey
    print("💬 Generating survey responses...")
    all_responses = []
    
    for i, survey in enumerate(surveys, 1):
        print(f"   Generating response for survey {i}/{len(surveys)}...")
        
        # Format questions for prompt
        questions_text = json.dumps([
            {
                'headline': q['headline'],
                'type': q['type'],
                'choices': q.get('choices', []),
                'range': q.get('range')
            }
            for q in survey['questions']
        ], indent=2)
        
        prompt = RESPONSE_GENERATION_PROMPT.format(
            survey_name=survey['name'],
            questions=questions_text
        )
        
        response_data = generate_func(prompt, model)
        responses = response_data.get('responses', [])
        
        # Link responses to survey
        all_responses.append({
            'survey_name': survey['name'],
            'responses': responses
        })
    
    print(f"✓ Generated {len(all_responses)} survey responses")
    
    # Combine all data
    output_data = {
        'surveys': surveys,
        'users': users,
        'responses': all_responses,
        'metadata': {
            'provider': provider,
            'model': model,
            'total_surveys': len(surveys),
            'total_users': len(users),
            'total_responses': len(all_responses)
        }
    }
    
    # Save to file
    output_file = 'generated_data.json'
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print("\\n" + "="*60)
    print("✅ Data generation complete!")
    print("="*60)
    print(f"\\n📁 Data saved to: {output_file}")
    print(f"\\n📊 Summary:")
    print(f"   • Surveys: {len(surveys)}")
    print(f"   • Users: {len(users)}")
    print(f"   • Responses: {len(all_responses)}")
    print("\\n💡 Next step: python main.py formbricks seed")
    print("="*60)
''')

    # commands/seed.py
    create_file('commands/seed.py', '''"""
Command to seed Formbricks with generated data using APIs only
"""
import json
import sys
import time
import requests
from pathlib import Path


class FormbricksAPI:
    """Formbricks API client for Management and Client APIs"""
    
    def __init__(self, base_url, api_key, environment_id=None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.environment_id = environment_id
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        })
    
    def create_survey(self, survey_data):
        """Create a survey using Management API"""
        url = f"{self.base_url}/api/v1/management/surveys"
        
        # Transform survey data to Formbricks format
        questions = []
        for i, q in enumerate(survey_data['questions']):
            question = {
                'type': q['type'],
                'headline': {'default': q['headline']},
                'required': q.get('required', False),
                'subheader': {'default': ''}
            }
            
            # Add type-specific fields
            if q['type'] in ['multipleChoiceSingle', 'multipleChoiceMulti']:
                question['choices'] = [
                    {'id': f"choice_{j}", 'label': {'default': choice}}
                    for j, choice in enumerate(q.get('choices', []))
                ]
                question['shuffleOption'] = 'none'
            elif q['type'] == 'rating':
                question['scale'] = 'number'
                question['range'] = q.get('range', 5)
                question['lowerLabel'] = {'default': 'Not likely'}
                question['upperLabel'] = {'default': 'Very likely'}
            elif q['type'] == 'nps':
                question['lowerLabel'] = {'default': 'Not likely'}
                question['upperLabel'] = {'default': 'Very likely'}
            elif q['type'] == 'cta':
                question['buttonLabel'] = {'default': q.get('buttonLabel', 'Next')}
                question['dismissButtonLabel'] = {'default': q.get('dismissButtonLabel', 'Skip')}
            
            questions.append(question)
        
        payload = {
            'name': survey_data['name'],
            'type': survey_data.get('type', 'link'),
            'status': 'inProgress',
            'questions': questions,
            'welcomeCard': {
                'enabled': False
            },
            'thankYouCard': {
                'enabled': True,
                'headline': {'default': 'Thank you!'},
                'subheader': {'default': 'We appreciate your feedback.'}
            }
        }
        
        if survey_data.get('description'):
            payload['welcomeCard'] = {
                'enabled': True,
                'headline': {'default': survey_data['name']},
                'subheader': {'default': survey_data['description']}
            }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()['data']
    
    def create_response(self, survey_id, response_data):
        """Create a survey response using Client API"""
        url = f"{self.base_url}/api/v1/client/{self.environment_id}/responses"
        
        # Transform response data
        data = {}
        finished_at = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
        
        for resp in response_data['responses']:
            question_id = resp['questionId']
            value = resp['value']
            data[question_id] = value
        
        payload = {
            'surveyId': survey_id,
            'finished': True,
            'data': data,
            'meta': {
                'userAgent': 'FormbricksSeeder/1.0'
            }
        }
        
        # Client API doesn't use x-api-key, uses different auth
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def invite_user(self, email, name, role):
        """Invite a user using Management API"""
        url = f"{self.base_url}/api/v1/management/users"
        
        payload = {
            'email': email,
            'name': name,
            'role': role.lower()
        }
        
        response = self.session.post(url, json=payload)
        
        # User might already exist, that's okay
        if response.status_code in [200, 201]:
            return response.json().get('data', {})
        elif response.status_code == 409:
            return {'email': email, 'status': 'already_exists'}
        else:
            response.raise_for_status()


def load_config():
    """Load API configuration"""
    config_file = 'config.json'
    
    if not Path(config_file).exists():
        print(f"❌ Configuration file not found: {config_file}")
        print("\\n📝 Creating template config file...")
        
        template = {
            "base_url": "http://localhost:3000",
            "api_key": "YOUR_API_KEY_HERE",
            "environment_id": "YOUR_ENVIRONMENT_ID_HERE"
        }
        
        with open(config_file, 'w') as f:
            json.dump(template, f, indent=2)
        
        print(f"✓ Created {config_file}")
        print("\\n📋 Instructions:")
        print("   1. Go to http://localhost:3000")
        print("   2. Complete account setup")
        print("   3. Go to Settings → API Keys")
        print("   4. Create a new API key")
        print("   5. Copy your Environment ID from the URL or settings")
        print(f"   6. Update {config_file} with your API key and environment ID")
        print("   7. Run this command again")
        sys.exit(1)
    
    with open(config_file) as f:
        config = json.load(f)
    
    if config['api_key'] == 'YOUR_API_KEY_HERE':
        print(f"❌ Please update {config_file} with your actual API key")
        sys.exit(1)
    
    return config


def seed_command(data_file='generated_data.json'):
    """Seed Formbricks with generated data"""
    print("🌱 Seeding Formbricks with generated data...\\n")
    
    # Load configuration
    print("📋 Loading configuration...")
    config = load_config()
    print("✓ Configuration loaded")
    
    # Load generated data
    print(f"📂 Loading data from {data_file}...")
    if not Path(data_file).exists():
        print(f"❌ Data file not found: {data_file}")
        print("   Run: python main.py formbricks generate")
        sys.exit(1)
    
    with open(data_file) as f:
        data = json.load(f)
    
    print(f"✓ Loaded {len(data['surveys'])} surveys, {len(data['users'])} users")
    
    # Initialize API client
    api = FormbricksAPI(
        base_url=config['base_url'],
        api_key=config['api_key'],
        environment_id=config['environment_id']
    )
    
    # Seed surveys
    print("\\n📝 Creating surveys...")
    created_surveys = []
    
    for i, survey in enumerate(data['surveys'], 1):
        try:
            print(f"   Creating survey {i}/{len(data['surveys'])}: {survey['name']}")
            created = api.create_survey(survey)
            created_surveys.append({
                'id': created['id'],
                'name': survey['name'],
                'questions': created['questions']
            })
            print(f"   ✓ Created survey: {created['id']}")
            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"   ⚠️  Failed to create survey '{survey['name']}': {e}")
    
    print(f"✓ Created {len(created_surveys)} surveys")
    
    # Seed responses
    print("\\n💬 Creating survey responses...")
    response_count = 0
    
    for resp_data in data['responses']:
        # Find matching survey
        survey = next(
            (s for s in created_surveys if s['name'] == resp_data['survey_name']),
            None
        )
        
        if not survey:
            print(f"   ⚠️  Survey not found: {resp_data['survey_name']}")
            continue
        
        try:
            # Map question indices to IDs
            questions = survey['questions']
            mapped_responses = []
            
            for i, resp in enumerate(resp_data['responses']):
                if i < len(questions):
                    mapped_responses.append({
                        'questionId': questions[i]['id'],
                        'value': resp['value']
                    })
            
            print(f"   Creating response for: {survey['name']}")
            api.create_response(survey['id'], {'responses': mapped_responses})
            response_count += 1
            print(f"   ✓ Created response")
            time.sleep(0.5)
        except Exception as e:
            print(f"   ⚠️  Failed to create response: {e}")
    
    print(f"✓ Created {response_count} responses")
    
    # Seed users
    print("\\n👥 Inviting users...")
    user_count = 0
    
    for user in data['users']:
        try:
            print(f"   Inviting: {user['name']} ({user['email']})")
            result = api.invite_user(user['email'], user['name'], user['role'])
            
            if result.get('status') == 'already_exists':
                print(f"   ℹ️  User already exists")
            else:
                print(f"   ✓ Invited {user['role']}")
            
            user_count += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"   ⚠️  Failed to invite {user['email']}: {e}")
    
    print(f"✓ Processed {user_count} users")
    
    # Summary
    print("\\n" + "="*60)
    print("✅ Seeding complete!")
    print("="*60)
    print(f"\\n📊 Summary:")
    print(f"   • Surveys created: {len(created_surveys)}")
    print(f"   • Responses created: {response_count}")
    print(f"
