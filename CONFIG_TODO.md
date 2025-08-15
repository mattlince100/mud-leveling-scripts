# Configuration System TODO

## Overview
This document outlines the configuration system needed to make the MUD leveling scripts shareable with other players while keeping sensitive data (passwords, character names) secure and local.

## Background Discussion Summary
The codebase currently has many hardcoded values including character names, passwords, container preferences, and navigation paths. After analysis, we determined that most navigation patterns are universal to the game and can remain hardcoded. Only user-specific elements need to be configurable.

## Required Configuration Elements

### 1. **Character Credentials** (REQUIRED)
- **Main Character**
  - Character name
  - Password
  - Preferred container type (`chest`, `basket`, `portal`, etc.)
  
- **Cleric Character** (OPTIONAL)
  - Cleric name
  - Cleric password  
  - Cleric container preference

**Current Hardcoded Examples:**
- Passwords: `"1q2w3e4r"`, `"Elijah"`
- Character names: `Daltin`, `Kaeval`, `Lemaitre`
- Containers: `"chest"`, `"basket"`, `"my.basket"`

### 2. **Sect House Configuration** (CONDITIONAL)
Only needed if character is a sect member (level 10+):
- `is_member`: boolean flag
- `potion_room_path`: Navigation from sect recall to potion room (e.g., `"d;d;s"`)
- `return_path`: Navigation back to sect recall (e.g., `"n;u;u"`)

**Why Variable:** Different sects have different house layouts

### 3. **Spell Bot Location** (CONDITIONAL)
Only needed if NOT a sect member:
- `path_from_dh`: Path from Darkhaven Square to spell bot room (e.g., `"nw;w;w;w"`)
- `path_to_dh`: Return path to Darkhaven Square (e.g., `"e;e;e;se"`)

**Why Variable:** Different player groups may use different spell bot locations

### 4. **Emergency Contacts** (OPTIONAL)
- List of character names to notify in emergencies
- Currently: `["Kaerim", "Kaetas", "Keamval", "Grotok"]`

**Why Variable:** Friend groups differ per player

## Elements That Will Remain Hardcoded
- **Server Connection**: `realmsofdespair.com:4000` (universal)
- **Area Navigation**: All leveling area paths (universal game layout)
- **Darkhaven Navigation**: Shop locations, common areas (universal)
- **Combat Mechanics**: Mob targeting, spell priorities (universal)
- **Portal/Utility Characters**: Currently unused, can be removed

## Proposed Configuration Structure

### Option 1: JSON Configuration
```json
{
    "main_character": {
        "name": "YourCharacter",
        "password": "YourPassword",
        "container": "chest"
    },
    "cleric_character": {
        "enabled": true,
        "name": "YourCleric",
        "password": "ClericPassword",
        "container": "basket"
    },
    "sect_config": {
        "is_member": true,
        "potion_room_path": "d;d;s",
        "return_path": "n;u;u"
    },
    "spell_room": {
        "path_from_dh": "nw;w;w;w",
        "path_to_dh": "e;e;e;se"
    },
    "emergency_contacts": ["Friend1", "Friend2"]
}
```

### Option 2: Python Configuration
```python
# config.py
CONFIG = {
    'MAIN_CHARACTER': 'YourName',
    'MAIN_PASSWORD': 'YourPassword',
    'MAIN_CONTAINER': 'chest',
    
    'CLERIC_ENABLED': True,
    'CLERIC_CHARACTER': 'YourCleric',
    'CLERIC_PASSWORD': 'ClericPassword',
    'CLERIC_CONTAINER': 'basket',
    
    'SECT_MEMBER': True,
    'SECT_POTION_PATH': 'd;d;s',
    'SECT_RETURN_PATH': 'n;u;u',
    
    'SPELL_ROOM_PATH': 'nw;w;w;w',
    'SPELL_ROOM_RETURN': 'e;e;e;se',
    
    'SAFE_TELLS': ['Friend1', 'Friend2']
}
```

## Implementation Tasks

### Phase 1: Configuration System
- [ ] Create configuration file structure (JSON or Python)
- [ ] Create `config.example` template with dummy values
- [ ] Add `config.json` or `config.py` to `.gitignore`
- [ ] Create configuration loader module

### Phase 2: Code Refactoring
- [ ] Replace hardcoded passwords with config values
- [ ] Replace hardcoded character names with config values
- [ ] Replace hardcoded container preferences with config values
- [ ] Update sect house navigation to use config paths
- [ ] Update spell room navigation to use config paths
- [ ] Update emergency contact lists to use config values

### Phase 3: Backward Compatibility
- [ ] Ensure command-line arguments still work for quick runs
- [ ] Add config validation and helpful error messages
- [ ] Create setup wizard for first-time configuration

### Phase 4: Documentation
- [ ] Update README with configuration instructions
- [ ] Create setup guide for new users
- [ ] Document which values are safe to share
- [ ] Add security best practices

## Files Requiring Updates

### High Priority (Core functionality)
- `connect.py` - Main character login, passwords, containers
- `commands.py` - Sect house paths, spell room paths, character references
- `level.py` - Character-specific logic, container references
- `checks.py` - Container lists, character references

### Medium Priority (Supporting features)
- `artgallery.py` - Character-specific targeting logic
- `tom.py`, `mith.py`, `winterlight.py`, etc. - Area-specific character checks
- `helper.py` - Alt character management

### Low Priority (Specialized scripts)
- `run_ock_new.py`, `run_ock_cleric.py` - Standalone farming scripts
- `getarrows.py`, `getbasket.py` - Utility scripts
- Portal creation code - Currently unused, consider removing

## Security Considerations

### What to Protect
- **Passwords**: Never commit to version control
- **Character Names**: Keep private to prevent targeting
- **Sect Membership**: May reveal game affiliations
- **Friend Lists**: Privacy of other players

### Distribution Strategy
1. Repository contains all code with config placeholders
2. `config.example.json` shows structure with dummy values
3. User copies `config.example.json` to `config.json`
4. User fills in their personal values
5. `.gitignore` ensures `config.json` never gets committed

## Testing Requirements
- [ ] Test with fresh install (no existing config)
- [ ] Test migration from hardcoded values
- [ ] Test with minimal config (main character only)
- [ ] Test with full config (all features)
- [ ] Test with different sect house layouts
- [ ] Test with different spell room locations

## Success Criteria
- Friends can clone repository and run with their own characters
- No passwords or personal data in shared code
- Configuration is simple and well-documented
- Existing functionality is preserved
- Setup takes less than 5 minutes for new users

## Notes for Later Implementation
- Consider environment variables as alternative to config files
- May want to support multiple config profiles
- Could add config validation tool
- Might need config migration for updates
- Consider encrypted storage for passwords

---

*This document created from discussion on Aug 12, 2025 to plan configuration system for sharing MUD leveling scripts while protecting user credentials and personal data.*