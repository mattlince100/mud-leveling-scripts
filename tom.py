

class Tom:     
    
    
    def func_tom(self):

        if self.clericon:
            if self.MV < 100:
                self.cleric.rod.write("cast refresh %s\ttrance\n"%self.name)

        if self.phase == 0:
            self.status_msg = "Preparing to go -- Temple of the Moon"
            self.check_affect()
            self.phasedir = {}
            self.phase = 1
            # go to mithril
            
            #if not self.cleric_follow():
            #    self.phase = 0
            #else:
            self.godh()
            self.go("nw;w;w;#4 n;e")
            self.time.sleep(4)
            self.go("look painting;open n;n;#49 w;#8 s;sw;#3 w;n")
             
        elif self.phase == 1:
            # initialize the circuit
            self.status_msg = "Initializing circruit -- Temple of the Moon"
            self.phase = 2
            self.get_loc()
            

            if self.support != None:
                self.support.whereami()
                if self.support.location != "Standing Before the Temple Doors":
                    return 'dhaven'

            if self.location != "Standing Before the Temple Doors":
                # did not get to place                                                                                                                                 
                return 'dhaven'
            elif self.phase == 2:
            
                self.phasedir = {}
            
                dirs = "n;n;*w;*sw;ne;*nw;*w;e;*n;*w;e;*ne;*e;*n;n;n;w;e;e;w;n;s".split(";")
                if self.level <= 30:
                    self.cankill = ["Graceful and poised", "A woman covered","A very jolly,", "A serene young"]

                elif self.level <= 35:
                    self.cankill = ["Graceful and poised","A plump, elderly",  "A very jolly,", "A serene young"]
                elif self.level <= 50:                     
                    if self.charclass == "Barbarian" and self.support == None:
                        self.cankill = ["Graceful and poised","A plump, elderly",  "A very jolly,", "A priestess glares"]
                    elif self.level <= 45 and self.charclass in ["Warrior","Ranger","Dread vampire","Vampire"]:
                        self.cankill = ["Graceful and poised","A plump, elderly",  "A very jolly,", "A priestess glares","A priest with"]
                    elif self.level <= 45:
                        self.cankill = ["Graceful and poised","A plump, elderly",  "A very jolly,", "A priestess glares"]
                    else:
                        self.cankill = ["Graceful and poised","A plump, elderly",  "A very jolly,", "A priest with"]
                    dirs = "*n;*n;*e;*se;nw;*w;*w;*sw;ne;*nw;*w;e;*n;*w;e;*ne;*e;*n;n;n;w;e;e;w;n;s".split(";")
                for i in range(len(dirs)):
                    self.phasedir[i+2] = dirs[i]

                               
                
        elif self.phase >= 2 and not self.fight:
            # now go through shattered refuge one room at the time
            # 1) check no one else is in my room
            # 2) check mobs
            # 3) kill mobs if there
            # 4) move
            self.status_msg = "Killing stuff -- Temple of the Moon"
            mobnames = {"Graceful and poised,":"kita",
                        "A woman covered":"vorta",
                        "A plump, elderly":"maseen",
                        "A very jolly,":"revlek",
                        "A priestess glares":"Kyree",
                        "A serene young":"xerra",
                        "A strong, elderly":"oqrin",
                        "A priest with":"palinor"
                }

            mobs = {}
            for k in mobnames:
                mobs[k] = 0
            
            

            
                # every few rooms check effects                                                                                                                                                                        
            if self.phase % 5 == 0 and self.phase >= 10:
                # every few rooms check effects                                                                                                                                                                        

                self.check_affect()
                getsanc = False
                # Skip sanctuary wait if we have potions or cleric
                has_sanctuary_support = self.clericon
                if self.level >= 10 and self.sect_member:
                    sanctpotname = "a sanctuary potion"
                    if sanctpotname in self.containers.get(self.container, {}):
                        if self.containers[self.container][sanctpotname] > 0:
                            has_sanctuary_support = True
                
                if has_sanctuary_support:
                    # We have sanctuary support, just refresh when needed
                    if "sanctuary" not in self.aff:
                        getsanc = True
                else:
                    # Only wait if no sanctuary support available
                    if "sanctuary" in self.aff:
                        if self.aff['sanctuary'] < 10:
                            self.time.sleep(self.aff['sanctuary']*3.2)
                            getsanc = True
                    else:
                        getsanc = True

                if getsanc:
                    self.rod.write("quaff sanctuary %s\n"%self.container)

                if getsanc and not self.fight:
                    self.check_spells()
                    self.time.sleep(2)
                    self.check_affect()
                    if "sanctuary" not in self.aff:
                        return "dhaven"

                getlvl = False
                if "trollish vi" in self.aff:
                    if self.aff['trollish vi'] < 15:
                        getlvl = True
                else:
                    getlvl = True

                if getlvl:
                    return "dhaven"

            if self.phase in self.phasedir:
                self.whereami()
                print("roomitems:", self.roomitems, self.exits)
                
                for item in self.roomitems:
                    mob = " ".join(item.split()[:3])
                    if mob in mobs:
                        mobs[mob] += 1

                
                # am I alone here?
                alone = True
                for character in self.loc_dic:
                    if character in [self.name.capitalize(),"Kaeval","Kaetas"]:
                        continue
                    if self.support != None:
                        if character ==self.support.name:
                            continue
                    if self.loc_dic[character] == self.location:
                        alone = False
                print(self.loc_dic)
                print("Alone?", alone)
                # should I fight?
                if alone:
                    startfight = None
                    print(sum(mobs.values()))
                    if sum(mobs.values()) <= 6:
                        for mob in mobs:
                            if mobs[mob] > 0:
                                if mob in self.cankill:
                                    startfight = mobnames[mob]
                                else:
                                    startfight = None
                                    break
                    if startfight != None:
                        # Check if leveling spells need refreshing before combat
                        self.check_affect()  # Update current spell durations
                        needs_refresh, low_spells = self.check_leveling_spells()
                        if needs_refresh:
                            self.printc("Low critical spells detected before combat: %s" % ", ".join(low_spells), 'red')
                            self.refresh_leveling_spells()
                            self.printc("Spells refreshed, returning to Temple of the Moon...", 'green')
                            return "continue"  # Stay in this area and re-evaluate
                        
                        # Ensure spring exists in THIS room before attacking the mob
                        self.printc("About to fight %s in %s - ensuring spring exists" % (startfight, self.location), 'gold')
                        self.ensure_spring_exists()
                        
                        self.rod.write("kill %s\n"%(startfight)) 
                        self.target = startfight
                        self.fight = True
            else:
                if self.clericon:
                    self.cleric.godh('recall')
                    

                self.sys.stdout.write("\nDONE THIS ROUND...\n")
                #self.rod.write("quit\n")
                self.time.sleep(5)

                print(self.read())
                self.time.sleep(10)
                return 'dhaven'

            if not self.fight:
                d = self.phasedir[self.phase]
                if "*" in d:
                    self.rod.write(d[1:]+'\n')
                else:
                    self.go(self.phasedir[self.phase])
                self.phase += 1
                #self.time.sleep(.5)  
        return False
    
    
        
