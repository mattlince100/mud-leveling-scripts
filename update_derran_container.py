#!/usr/bin/env python3
import pickle

# Load existing alt_info for Derran
with open("alts/info_Derran.pckle", 'rb') as f:
    alt_info = pickle.load(f)

# Add container preference
alt_info["container"] = "basket"

# Save it back
with open("alts/info_Derran.pckle", 'wb') as f:
    pickle.dump(alt_info, f)

print("Updated Derran's container to 'basket'!")
print("Current alt_info:", alt_info)