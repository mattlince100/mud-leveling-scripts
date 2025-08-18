#!/usr/bin/env python3
import pickle
import os

# Ensure alts directory exists
if not os.path.exists("alts"):
    os.makedirs("alts")

# Load existing alt_info for Mavryck or create new one
try:
    with open("alts/info_Mavryck.pckle", 'rb') as f:
        alt_info = pickle.load(f)
except FileNotFoundError:
    alt_info = {"prac": [], "kills": {}, "buffer": False, "clearbuffer": False}

# Add sect membership
alt_info["sect_member"] = True

# Save it back
with open("alts/info_Mavryck.pckle", 'wb') as f:
    pickle.dump(alt_info, f)

print("Added sect_member=True to Mavryck's alt info!")
print("Current alt_info:", alt_info)