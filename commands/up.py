#!/usr/bin/env python3
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
