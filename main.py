#!/usr/bin/env python3
"""Formbricks Challenge - Main CLI Entry Point"""
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
    formbricks_parser = subparsers.add_parser('formbricks', help='Manage Formbricks')
    formbricks_subparsers = formbricks_parser.add_subparsers(dest='command', help='Command')

    # Up command
    formbricks_subparsers.add_parser('up', help='Start Formbricks locally')

    # Down command
    formbricks_subparsers.add_parser('down', help='Stop Formbricks and clean up')

    # Generate command
    generate_parser = formbricks_subparsers.add_parser('generate', help='Generate test data using LLM')
    generate_parser.add_argument('--provider', default='openai', choices=['openai', 'ollama'],
                                help='LLM provider to use')
    generate_parser.add_argument('--model', default='gpt-4o-mini',
                                help='LLM model to use')

    # Seed command
    seed_parser = formbricks_subparsers.add_parser('seed', help='Seed Formbricks with generated data')
    seed_parser.add_argument('--config', default='config.json',
                            help='Configuration file path')

    args = parser.parse_args()

    if args.service == 'formbricks':
        if args.command == 'up':
            up_command()
        elif args.command == 'down':
            down_command()
        elif args.command == 'generate':
            generate_command(provider=args.provider, model=args.model)
        elif args.command == 'seed':
            seed_command(config_path=args.config)
        else:
            formbricks_parser.print_help()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
