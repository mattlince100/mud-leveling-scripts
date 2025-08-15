#!/usr/bin/env python3
import pickle

# Load existing alt_info for Derran
try:
    with open("alts/info_Derran.pckle", 'rb') as f:
        alt_info = pickle.load(f)
except FileNotFoundError:
    alt_info = {"prac": [], "kills": {}, "buffer": False, "clearbuffer": False}

# Add sect membership
alt_info["sect_member"] = True

# Save it back
with open("alts/info_Derran.pckle", 'wb') as f:
    pickle.dump(alt_info, f)

print("Added sect_member=True to Derran's alt info!")
print("Current alt_info:", alt_info)