# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Python-based MUD (Multi-User Dungeon) automation system for "Realms of Despair". The system manages character leveling, combat, inventory, spell management, and area navigation through telnet connections.

## Common Commands

### Running Characters
- `python connect.py <character_name> <cleric_name> <target_level> <max_time_minutes> <password> <container> <cleric_follow_mode>`
  - Example: `python connect.py Bryann Kaeval 50 60 1q2w3e4r chest follow`
- `python run_ock_new.py` - Runs a specific farming script for the Oakwater area
- `python level_prestige.py` - Handles prestige character leveling

### Character Management
- Characters are automatically managed through the main ROD class in `connect.py`
- Alt character information is stored in `alts/info_<charactername>.pckle` files
- Character variables are saved in `chars/vars_<charactername>.pck` files
- Logs are written to `logs/log_<charactername>_<year>.txt`

### Testing and Development
- No formal test suite - testing is done through live game interaction
- Debug mode can be enabled by setting `self.debug > 0` in character classes
- Use `printc()` method for colored debug output

## High-Level Architecture

### Core Components

**Main Character Class (`connect.py`)**
- `ROD` class - Main character automation engine inheriting from all area classes
- Handles telnet connection, command parsing, movement, combat, and state management
- Manages character lifecycle: login → setup → leveling areas → logout

**Area Modules** - Each area has its own Python module with specific navigation and mob targeting:
- `dhaven.py` - Starting town, equipment management, spell management
- `coral.py` - Underwater coral area (levels 8-13)
- `artgallery.py` - Art gallery area (levels 11-26+)
- `gnome.py` - Gnome village (low levels)
- `mith.py` - Mithril Hall (mid-high levels)
- `king.py` - King's area (high levels)
- `tom.py` - Tomb area (high levels, time-dependent)
- `canyon.py` - Canyon area (buffer clearing)
- `shire.py` - Shire area (buffer clearing)
- `winterlight.py` - Winter area (mid-high levels)
- `toz.py` - Tower of Zenithia (mid levels)

**Support Classes**
- `helper.py` - Contains `Helper` class with login, character management utilities
- `commands.py` - Contains `Commands` class with movement, combat, and utility functions  
- `checks.py` - Contains `Checks` class for status checking, inventory, equipment management
- `level.py` - Contains main leveling logic classes (`dhaven`, `Starting`, `Cleric`, `Support`)

**Specialized Scripts**
- `run_ock_new.py` - Dedicated farming bot for specific high-value mob
- `level_prestige.py` - Handles prestige character mechanics
- `connect_prestige.py` - Prestige character connection handler

### Character State Management

**Phases**: Each area uses a phase system to track progression through the area
- Phase 0: Initialization and setup
- Phase 1+: Area-specific progression states

**Status Messages**: Real-time status reporting through `self.status_msg`

**Persistent Data**: 
- `alt_info` dictionary stores kill counts, buffer status, practice records
- Character variables stored in pickle files for persistence between sessions

### Combat System

**Auto-targeting**: Dynamic mob targeting based on character class and available spells/skills
- Spell casting priority for mage classes (Mage, Augurer, Nephandi, Cleric, Fathomer)
- Skill-based attacks for physical classes (Barbarian, Warrior, Thief)
- Special mechanics for Vampire (feeding) and other unique classes

**Equipment Management**: Automatic weapon re-equipping on disarm, equipment repair

**Healing System**: Automatic potion consumption, cleric healing support

### Multi-Character Coordination

**Cleric Support**: Secondary cleric character provides healing, buffs, sanctuary
- Automatic cleric login and following
- Spell casting coordination (sanc, fly, heal, refresh)
- Mana management through trancing

**Group Support**: Master/support character relationships for power leveling
- Parity checking before area entry
- Coordinated movement and combat

## Key Architecture Patterns

### Class Inheritance
- `ROD` class inherits from all area classes and utility classes
- Each area class implements `func_<areaname>()` method
- Utility classes provide shared functionality (movement, checks, commands)

### State Machine Pattern
- Area functions return next state or False to continue current state
- State transitions: 'dhaven' → specific area → 'dhaven' → next area
- Special states: 'exit' (restart), 'exitexit' (quit), 'support' (support mode)

### Event-Driven Processing
- Main loop reads telnet buffer and processes lines
- Trigger-based responses to game events (combat, death, tells, etc.)
- Automatic spell/skill activation based on game state

### Data Persistence
- Pickle files for character state persistence
- Kill tracking and buffer management for optimal leveling
- Equipment and skill progression tracking

## Important Implementation Notes

### Connection Management
- Uses Python's `telnetlib` for MUD connections
- Automatic reconnection and error handling
- Emergency quit procedures for unexpected situations

### Movement System
- Supports complex movement strings with repeat notation (`#4 n` = north 4 times)
- Force movement option for getting unstuck
- Automatic pathfinding from area to Darkhaven

### Potion and Resource Management
- Automatic restocking when supplies run low
- Multiple container support (chest, basket, portal, etc.)
- Dynamic resource allocation based on character level and class

### Safety Features
- Emergency quit on unexpected tells from other players
- Automatic flee and quit on low health
- Anti-idle mechanisms to prevent game timeouts

This system is designed for fully autonomous character progression with minimal human intervention while maintaining safety and efficiency.