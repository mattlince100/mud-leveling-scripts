

class Toz:     
    
    
    def func_toz(self):
        

        if self.phase == 0:
            self.check_affect()
            self.phasedir = {}
            self.phase = 1
            # go to TOZ                                                                                                                                                                                                                                                                                                                                                                                                      
            self.godh()
            self.go("nw;w;w;w")
            self.rod.write("say refresh\n")
            self.time.sleep(2)
            self.go("e;e;e;se")                
            self.go("#6 n;#3 nw;w;n;#4 e;s;w;sw;s;sw;s;s;e;se;se;#4 e;n;nw;n;n;sw;e;ne;s;s;se;s;se;s;e;e;se;ne")
            self.rod.write("give 100 coin boy\nn\n")

        elif self.phase == 1:

            # initialize the circuit
            self.phase = 2
            self.whereami()

            if self.support != None:
                self.support.whereami()
                if self.support.location != "The Road of Tents":
                    return 'dhaven'
            if self.location != "The Road of Tents":
                # did not get to place                                                                                                                               
                return 'dhaven'
            elif self.phase == 2:
                self.phasedir = {}
                
                if self.level <= 15:
                    dirs = 'n;n;w;w;w;w;e;e;n;s;e;e;e;*open s;s'.split(";")
                    self.cankill = ["A tiny girl","A Jester juggles",
                                    "A frail old","A small man"]
                elif self.level <=17: 
                    dirs = '*give 100 coin boy;*n;n;e;*open s;s;n'.split(";")
                    self.cankill = ["A tiny girl","A Jester juggles","A frail old","A small man"]
                else:
                    dirs = '*give 100 coin boy;*n;n;e;*open s;*config +autoloot;s;u;*drop swirled;*u;*u;*u;*n;*n;*config -autoloot;*n;s;*s;*s;*s;*s;*s;*e;*config +autoloot;w;*drop wisdom;*n;*n;*n;*e;*e;e;e;n;*config -autoloot;*drop all.orchid'.split(";")
                    self.cankill = ["A tiny girl","A Jester juggles","A frail old",
                                    "A small man","An old wizard","A beast of"]
                    
                
                                    
                for i in range(len(dirs)):
                    self.phasedir[i+2] = dirs[i]

                               
                
        elif self.phase >= 2 and not self.fight:
            # now go through shattered refuge one room at the time
            # 1) check no one else is in my room
            # 2) check mobs
            # 3) kill mobs if there
            # 4) move

            mobnames = {"A tiny girl":"girl","A Jester juggles":"jester",
                        "A frail old":"woman",
                        "A small man":"man",
                        "An old wizard":"wizard",
                        "A beast of":"beast"
                }

            mobs = {}
            for k in mobnames:
                mobs[k] = 0
            
            if self.phase % 3 == 0:
                # every     
                
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

                if getsanc and not self.fight:
                    self.check_spells()
                    self.time.sleep(2)
                    self.check_affect()
                    if "sanctuary" not in self.aff:
                        if self.clericon:
                            self.cleric.quit()
                            self.clericon = False
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
                
                
                for item in self.roomitems:
                    mob = " ".join(item.split()[:3])
                    if mob in mobs:
                        mobs[mob] += 1

                
                # am I alone here?
                alone = True
                for character in self.loc_dic:
                    if self.clericon:
                        if character in [self.name.capitalize(), self.cleric.name]:
                            continue
                    else:
                        if character in [self.name.capitalize()]:
                            continue

                    if self.loc_dic[character] == self.location:
                        alone = False
                
                self.sys.stdout.write("\nAlone? "+str(alone)+'\n')
                self.sys.stdout.write("\t".join(["%s: %s"%(x,self.loc_dic[x]) for x in self.loc_dic])+'\n')

                # should I fight?
                if alone:
                    for mob in mobs:
                        if mobs[mob] > 0 and mob in self.cankill:
                            # Check if leveling spells need refreshing before combat
                            self.check_affect()  # Update current spell durations
                            needs_refresh, low_spells = self.check_leveling_spells()
                            if needs_refresh:
                                self.printc("Low critical spells detected before combat: %s" % ", ".join(low_spells), 'red')
                                self.refresh_leveling_spells()
                                self.printc("Spells refreshed, returning to Tower of Zenithia...", 'green')
                                return "continue"  # Stay in this area and re-evaluate
                            
                            self.rod.write("kill %s\n"%(mobnames[mob]))
                            self.fight = True
            else:
                self.sys.stdout.write("\nDONE THIS ROUND...Waiting 10s\n")
                
                self.time.sleep(10)
                return 'dhaven'

            if not self.fight:
                d = self.phasedir[self.phase]
                if "*" in d:
                    self.rod.write(d[1:]+'\n')
                else:
                    self.go(self.phasedir[self.phase])
                self.phase += 1
                
        return False
