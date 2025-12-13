#!/usr/bin/env python3
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
