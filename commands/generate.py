#!/usr/bin/env python3
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
