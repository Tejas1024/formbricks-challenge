#!/usr/bin/env python3
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
