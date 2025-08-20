#!/usr/bin/env python3
import pickle
import os

# Create or update Mavryck's alt_info file
alt_info = {
    "prac": [],  # Practice sessions will be filled as he levels
    "kills": {},  # Kill counts will be tracked during leveling
    "buffer": set(),  # Buffer tracking
    "clearbuffer": False,
    "sect_member": True,  # Set as sect member
    "container": "basket"  # Set container preference
}

# Save the alt_info file
pickle_path = "alts/info_Mavryck.pckle"
with open(pickle_path, 'wb') as f:
    pickle.dump(alt_info, f)

print("Created Mavryck's alt_info file with:")
print("- sect_member: True")
print("- container: basket")
print("- Ready for leveling!")

# Verify it was created correctly
with open(pickle_path, 'rb') as f:
    loaded_info = pickle.load(f)
    
print("\nVerification - Loaded alt_info:")
for key, value in loaded_info.items():
    print(f"  {key}: {value}")