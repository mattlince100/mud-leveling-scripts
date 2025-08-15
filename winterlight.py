

class Winter:     
    
    
    def func_winter(self):

        if self.clericon:
            if self.MV < 100:
                self.cleric.rod.write("cast refresh %s\ttrance\n"%self.name)

        if self.phase == 0:
            self.status_msg = "Preparing to go -- Wintermist"
            self.check_affect()
            self.phasedir = {}
            self.phase = 1
            # go to mithril
            
            self.whereami()
            
            # cleric will wait outside in case cursed
            #if not self.clericon:
            #    return 'dhaven'

            if self.clericon:
                # while cleric is not following us
                while True:
                    self.whereami()
                    try: self.cleric.whereami()
                    except:
                        self.clericon = False
                        self.printc("Restart because cleric has some problems...")
                        return 'dhaven'
                    
                    if self.location == "Thoth's Rune on Vertic Avenue" and self.cleric.location == "Thoth's Rune on Vertic Avenue":
                        self.cleric.rod.write("follow %s\nver\n"%self.name)
                        rl = ''
                        while True:
                            rl += self.cleric.read()
                            if "SMAUG 2.6" in rl:
                                self.sys.stdout.write("\n%s: %s\n"%(self.name,rl))
                                if "You now follow" in rl:
                                    success = True
                                    self.cleric.following = True
                                else:
                                    success = False
                                break
                        if success:
                            self.phase = 1
                        else:
                            self.phase = 0
                            self.cleric.godh("recall")
                        break
                    elif self.location == "Darkhaven Square":
                        self.go("n")
                    elif self.cleric.location != "Thoth's Rune on Vertic Avenue":
                        self.cleric.godh("recall")
                    elif self.location != "Thoth's Rune on Vertic Avenue":
                        self.godh("recall")
                    self.time.sleep(1)
            

            self.godh()
            self.go("#6 s;ne;#2 s;se;#2 e;s;#2 sw;s;#4 sw;#4 s;#5 se;#2 s;d;s;se;s;#3 se;#3 e;#2 s;#2 e;d;se;ne;s;d;se;s")
            
             
        elif self.phase == 1:
            # initialize the circuit
            self.status_msg = "Initializing circruit -- Winterlight"
            self.phase = 2
            self.whereami()
            

            if self.support != None:
                self.support.whereami()
                if self.support.location != "An Ice-Spired Lake":
                    return 'dhaven'

            if self.location != "An Ice-Spired Lake":
                # did not get to place                                                                                                                                 
                return 'dhaven'
            elif self.phase == 2:
            
                self.phasedir = {}
            
                dirs = "*sw;*sw;*sw;*sw;*sw;*s;*open ne;*ne;s;n;*sw;*sw;*open e;*e;*s;n".split(";")
                self.cankill= ['A small chubby','A worried-looking woman','A young blonde','A handsome young']
                for i in range(len(dirs)):
                    self.phasedir[i+2] = dirs[i]

                               
                
        elif self.phase >= 2 and not self.fight:
            # now go through shattered refuge one room at the time
            # 1) check no one else is in my room
            # 2) check mobs
            # 3) kill mobs if there
            # 4) move
            self.status_msg = "Killing stuff -- Winterlight"
            mobnames = {"A small chubby":"Xantrin",
                        "A worried-looking woman":"phaeba",
                        "A young blonde":"shanja",
                        "A handsome young": "javen"
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
                    
                if self.stats['CON'] >= 20 and (self.stats['CON'] >= 22 or self.charclass != "Barbarian"):
                    getlvl = False

                if getsanc and not getlvl:
                    if self.clericon:
                        self.cleric.rod.write("c sanc %s\n"%self.name)
                    else:
                        self.rod.write("quaff sanc %s\n"%self.container)
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
                        if character in [self.name.capitalize(),self.cleric.name]:
                            continue
                    else:
                        if character in [self.name.capitalize()]:
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
                            self.printc("Spells refreshed, returning to Winterlight...", 'green')
                            return "continue"  # Stay in this area and re-evaluate
                        
                        self.rod.write("kill %s\n"%(startfight)) 
                        self.target = startfight
                        self.fight = True
            else:
                if self.clericon:
                    self.cleric.godh()

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
    
    
        
