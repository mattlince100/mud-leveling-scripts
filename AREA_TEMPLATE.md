# Area Template for MUD Leveling System

## Area Information
**Area Name:** [Official area name]  
**File Name:** `[shortname].py` (e.g., `coral.py`, `mith.py`)  
**Recommended Levels:** [Min level] - [Max level]  
**Key Benefits:** [Why level here? Good XP? Special items? Gold?]

## Navigation Data

### Entry Path
**From Darkhaven Square:** `[movement commands]`
Example: `#6 n;#3 nw;w;n;e;e;e;n;n;n;w` (for Mithril Hall)

### Return Path  
**To Darkhaven Square:** `[movement commands or 'recall']`

### Area Layout
```
Phase 1: [Description] - Movement: [commands]
Phase 2: [Description] - Movement: [commands]
Phase 3: [Description] - Movement: [commands]
...
Phase N: [Description] - Movement: [commands]
```

## Mob Information

### Primary Targets (High Priority)
List mobs in order of preference:
1. **[Mob Name]** 
   - Level: [X]
   - HP: ~[estimated]
   - Special: [aggro/wimpy/casts/etc]
   - Good for: [which classes/levels]

2. **[Mob Name]**
   - Level: [X]
   - HP: ~[estimated]
   - Special: [notes]
   - Good for: [which classes/levels]

### Secondary Targets (Kill if no primary available)
1. **[Mob Name]** - [notes]
2. **[Mob Name]** - [notes]

### Avoid/Skip
- **[Mob Name]** - Reason: [too hard/no XP/aggro to lowbies]
- **[Mob Name]** - Reason: [explanation]

## Special Mechanics

### Room-Specific Behaviors
- **[Room name]**: [Special behavior needed]
- **[Room name]**: [Special behavior needed]

### Area Hazards
- [Describe any death traps, aggressive mobs, cursed rooms, etc.]
- [Note any level restrictions or requirements]

### Required Equipment/Spells
- **Must Have:** [fly, boat, pass door, etc.]
- **Recommended:** [sanctuary, detect invis, etc.]

## Combat Strategy

### Phases Structure
```python
# Typical phase progression
Phase 0: Initial setup/entry
Phase 1-N: Combat rooms
Phase N+1: Exit/completion
```

### Special Combat Rules
- Use range attacks for: [mob names]
- Flee immediately from: [mob names]
- Special kill order: [if certain mobs must die first]

## Code Structure Example

```python
def func_[areaname](self):
    """
    Area: [Full area name]
    Levels: [recommended range]
    """
    
    # Phase 0: Setup and entry
    if self.phase == 0:
        self.godh()  # Go to Darkhaven
        self.go("[entry path]")
        self.phase = 1
        return False
    
    # Phase 1-N: Combat phases
    elif self.phase == 1:
        # Movement
        self.go("[movement commands]")
        
        # Combat targeting
        mobs_here = self.mobs_here()
        targets = ["primary mob 1", "primary mob 2"]
        
        for mob in targets:
            if mob in mobs_here:
                self.rod.write("k %s\n" % mob.split()[-1])
                return False
        
        self.phase = 2
        return False
    
    # ... more phases ...
    
    # Final phase: Exit
    elif self.phase == N:
        self.rod.write("recall\n")
        return "dhaven"
    
    return False
```

## Integration Checklist

### Files to Update
- [ ] Create `[areaname].py` with area logic
- [ ] Add to `connect.py` class inheritance
- [ ] Add to `level.py` area selection logic
- [ ] Import in main files that need it

### Level Selection Logic
Add to `level.py` around line 1025+:
```python
elif self.level >= [min] and self.level <= [max]:
    if [conditions]:
        return "[areaname]"
```

### Testing Notes
- [ ] Test with level [min] character
- [ ] Test with level [max] character
- [ ] Verify all mob names match exactly
- [ ] Check phase transitions work
- [ ] Confirm exit/recall works properly

## Data Collection Instructions

To gather this information for a new area:

1. **Navigation**: Walk through area manually, note exact movement commands
2. **Mobs**: Use 'consider' on each mob to check difficulty
3. **Room names**: Use 'look' in each room, note the room title
4. **Special mechanics**: Note any unusual messages or requirements
5. **Combat test**: Fight a few mobs to check for special attacks/behaviors

## Example Notes Format
```
Room 1: "The Entrance Hall"
  Movement IN: n;e;e
  Mobs: 
    - A palace guard (lvl 25, ~500hp, aggro)
    - A servant (lvl 20, ~300hp, wimpy)
  Movement OUT: w;w;s
  
Room 2: "The Throne Room"
  Movement IN: n;u
  Mobs:
    - The king (lvl 35, ~2000hp, casts, !flee)
    - Royal guard x2 (lvl 30, ~800hp, assist)
  Movement OUT: d;s
  Special: King summons adds at 50% health
```

## Additional Considerations

### Performance Optimizations
- Minimize unnecessary movements
- Group similar-level mobs in same phase
- Use phase checks efficiently (every 5 rooms?)

### Safety Features
- Always include recall/exit strategy
- Check for curse before leaving
- Monitor HP/MP thresholds
- Handle death/fleeing scenarios

### Debugging
- Add status messages: `self.status_msg = "Fighting in [room]"`
- Use phase numbers that make sense
- Include printc debug statements during development

---

*Use this template to document new areas before implementing them in code. The more detailed the documentation, the easier the implementation will be.*