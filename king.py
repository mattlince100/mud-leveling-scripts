

class King:     
    
    
    def func_king(self):

        if self.clericon:
            if self.MV < 100:
                self.cleric.rod.write("cast refresh %s\ntrance\n"%self.name)

        if self.phase == 0:
            self.status_msg = "Preparing to go -- King's Castle"
            self.phasedir = {}
            self.phase = 1
            
            
            self.godh()
            self.go("#13 e;#3 s;#3 e;ne;ne;#3 se;e;s;s;sw;s;se;s;se;e;e;ne;ne;e")
            
             
        elif self.phase == 1:
            # initialize the circuit
            self.status_msg = "Initializing circruit -- King's Castle"
            self.phase = 2
            self.get_loc()
            

            if self.support != None:
                self.support.whereami()
                if self.support.location != "A Narrow Path of Dirt and Stone":
                    return 'dhaven'

            if self.location != "A Narrow Path of Dirt and Stone":
                # did not get to place                                                                                                                                 
                return 'dhaven'
            elif self.phase == 2:
            
                self.phasedir = {}
            
                dirs = "*e;e;n;n;e;w;n;w;n;w;n;s;e;s;e;e;n;*look".split(";")
                
                self.cankill= ['A castle guard',"A tall man","A templar sits",'One of the']
                if self.level > 44 and self.level < 49:
                    self.cankill = ["A tall man","A templar sits",'One of the']
                
                for i in range(len(dirs)):
                    self.phasedir[i+2] = dirs[i]

                               
                
        elif self.phase >= 2 and not self.fight:
            # now go through shattered refuge one room at the time
            # 1) check no one else is in my room
            # 2) check mobs
            # 3) kill mobs if there
            # 4) move
            self.status_msg = "Killing stuff -- King's castle"
            mobnames = {"A castle guard":"guard",
                        "A tall man":"herald",
                        "A templar sits":"templar",
                        "Sir Pereval, bearing": "pereval",
                        "One of the":"ranger"
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
                    elif self.charclass != "Barbarian":
                        self.rod.write("sleep\n")
                        
                        # Break the wait into 10-second chunks and check if curse is still active
                        total_wait = self.aff['curse']*3.1
                        waited = 0
                        while waited < total_wait:
                            chunk_time = min(10, total_wait - waited)
                            self.time.sleep(chunk_time)
                            waited += chunk_time
                            
                            # Check if curse is still active
                            self.check_affect()
                            if "curse" not in self.aff:
                                self.printc("Curse removed! Continuing...", 'green')
                                break
                        
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
                    
                if self.stats['CON'] >= 20 and (self.stats['CON'] >= 22 or self.charclass != "Barbarian"):
                    getlvl = False

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
                    if self.loc_dic[character] == self.location:
                        alone = False
                print(self.loc_dic)
                print("Alone?", alone)
                # should I fight?
                if alone:
                    startfight = None
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
                            self.printc("Spells refreshed, returning to King area...", 'green')
                            return "continue"  # Stay in this area and re-evaluate
                        
                        self.rod.write("kill %s\n"%(startfight)) 
                        self.target = startfight
                        self.fight = True
            else:

                self.sys.stdout.write("\nDONE THIS ROUND...\n")
                #self.rod.write("quit\n")
                self.time.sleep(5)

                print(self.read())
                self.time.sleep(10)
                return 'dhaven'

            if not self.fight:
                d = self.phasedir[self.phase]
                self.rod.write("get %s\nwear %s\n"%(self.weaponkey,self.weaponkey))
                if "*" in d:
                    self.rod.write(d[1:]+'\n')
                else:
                    self.go(self.phasedir[self.phase])
                self.phase += 1
                #self.time.sleep(.5)  
        return False
    
    
        
