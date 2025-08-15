#!/usr/bin/env python3
"""
Run Derran with basket container configuration
"""

import subprocess
import sys

# Configuration for Derran
character = "Derran"
target_level = 50
max_time = 180
password = "1q2w3e4r"  # Update this with actual password
container = "basket"  # Using laundry basket

# Build the command
cmd = [
    sys.executable,
    "connect.py",
    character,
    str(target_level),
    str(max_time),
    password,
    container
]

print(f"Starting {character} with basket container...")
print(f"Command: {' '.join(cmd[:-1])} [password hidden]")

# Run the leveler
subprocess.run(cmd)