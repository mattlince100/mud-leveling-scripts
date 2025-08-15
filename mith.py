

class Mithril:     
    
    
    def func_mith(self):
        self.flee = ["Wulfgar", "Drizzt", "Catti-Brie","Bruenor", "Guenhwyvar", "Artemis"]

        if self.clericon:
            if self.MV < 100:
                self.cleric.rod.write("cast refresh %s\ttrance\n"%self.name)

        print("\nMithril Hall: phase",self.phase)
        if self.phase == 0:
            self.check_affect()
            self.phasedir = {}
            self.phase = 1

            
            self.godh()
            self.go("#6 s;ne;s;s;se;e;e;s;sw;sw;u;nw;ne;w;w;sw;#3 s;se;se;sw;u;u;w;nw;w;w;w;w;n;open passage;n;e;n;n;w;d;e;e;n")
             
        elif self.phase == 1:
            # initialize the circuit
            self.phase = 2
            self.whereami()
            

            if self.support != None:
                self.support.whereami()
                if self.support.location != "Entryway to Mithril Hall":
                    return 'dhaven'

            if self.location != "Entryway to Mithril Hall":
                # did not get to place                                                                                                                                 
                return 'dhaven'
            elif self.phase == 2:
            
                self.phasedir = {}
            
                dirs = "*config +autoloot;w;*n;*w;*n;*n;s;*s;*e;*s;*e;n;n;n;e;n;e;w;n;w;e;*config -autoloot;*look".split(";")
                if self.level <= 21:
                    dirs = 'w;*n;*w;*n;*n;s;'.split(";")
                    self.cankill = ["A rotund dwarf","An irate dwarf","The Hall weaponsmith"]
                elif self.level <= 26:                     
                    self.cankill = ["A Gutbuster Brigade","A rotund dwarf","The Hall weaponsmith","A proud-looking dwarf","A bored dwarf"]
                else:
                    self.cankill = ["A rotund dwarf","The Hall weaponsmith","A proud-looking dwarf","A bored dwarf"]
                    
            
                                    
                for i in range(len(dirs)):
                    self.phasedir[i+2] = dirs[i]

                               
                
        elif self.phase >= 2 and not self.fight:
            # now go through shattered refuge one room at the time
            # 1) check no one else is in my room
            # 2) check mobs
            # 3) kill mobs if there
            # 4) move

            mobnames = {"A Gutbuster Brigade":"gut","The Hall weaponsmith":"weapon",
                        "A rotund dwarf":"grocer",
                        "A proud-looking dwarf":"blacks",
                        "A bored dwarf":"blacks",
                        "A Mithril Hall":"sentry",
                        "Catti-Brie Battlehammer stands":"cattie",
                        "Drizzt Do'Urden, the": "drizzt",
                        "Wulfgar, the towering": "wulfgar",
                        "Bruenor Battlehammer, Eighth": "bruenor",
                        "Artemis Entreri stands":"artemis"
                }

            mobs = {}
            for k in mobnames:
                mobs[k] = 0

            if True:
                # every few rooms check effects                                                                                                                                                                        
                self.check_affect()

                if "curse" in self.aff:
                    if self.clericon:
                        self.cleric.rod.write("c 'remove curse' %s\n"%self.name)
                    else:
                        self.rod.write("sleep\n")
                        self.time.sleep(self.aff['curse']*3.1)
                        self.rod.write("wake\n")
                        return 'dhaven'

                getsanc = False
                # Skip sanctuary wait if we have potions or cleric
                has_sanctuary_support = False
                if self.level >= 10 and self.sect_member:
                    sanctpotname = "a sanctuary potion"
                    if sanctpotname in self.containers.get(self.container, {}):
                        if self.containers[self.container][sanctpotname] > 0:
                            has_sanctuary_support = True
                
                if has_sanctuary_support or self.clericon:
                    # We have sanctuary support, just refresh when needed
                    if "sanctuary" not in self.aff:
                        getsanc = True
                else:
                    # Only wait if no sanctuary support available
                    if "sanctuary" in self.aff:
                        if self.aff['sanctuary'] < 30:
                            getsanc = True
                            self.sys.stdout.write("\nWaiting sanc to run out...\n")
                            self.time.sleep(self.aff['sanctuary']*3.1)
                    else:
                        getsanc = True

                getlvl = False
                if "trollish vi" in self.aff:
                    if self.aff['trollish vi'] < 20:
                        self.time.sleep(self.aff['trollish vi']*3.2)
                        getlvl = True
                else:
                    getlvl = True
                    
                
                if getsanc and not getlvl:
                    if self.clericon:
                        self.cleric.rod.write("c sanc %s\n"%self.name)
                    self.time.sleep(5)
                    self.check_affect()
                    getsanc = False
                    if "sanctuary" in self.aff:
                        if self.aff['sanctuary'] < 30:
                            getsanc = True
                    else:
                        getsanc = True
                    if getsanc:
                        return "dhaven"
                if getsanc or getlvl:
                        
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
                    if self.clericon:
                        if character in [self.name.capitalize(),self.cleric.name,"Kaetas"]:
                            continue
                    else:
                        if character in [self.name.capitalize(),"Kaetas"]:
                            continue
                    if self.support != None:
                        if character == self.support.name:
                            continue
                    if self.loc_dic[character] == self.location:
                        alone = False
                print(self.loc_dic)
                print("Alone?", alone)
                # should I fight?
                if alone:
                    startfight = None
                    print(sum(mobs.values()))
                    if sum(mobs.values()) <= 3:
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
                            self.printc("Spells refreshed, returning to Mithril Hall...", 'green')
                            return "continue"  # Stay in this area and re-evaluate
                        
                        self.rod.write("kill %s\n"%(startfight)) 
                        self.target = startfight
                        self.fight = True
            else:
                if self.clericon:
                    self.cleric.godh()
                
                self.sys.stdout.write("\nDONE THIS ROUND...\n")
                self.rod.write("put all.flask %s\n"%self.container)
                return 'dhaven'

            if not self.fight:
                self.check_inv()
                print(self.inv)
                self.rod.write("put all.flask %s\n" % self.container)
                d = self.phasedir[self.phase]
                if "*" in d:
                    self.rod.write(d[1:]+'\n')
                else:
                    self.go(self.phasedir[self.phase])
                self.phase += 1
                #self.time.sleep(.5)  
        return False
    
    
        
