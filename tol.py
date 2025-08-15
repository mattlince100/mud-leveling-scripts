

class Tree:     
    
    
    def func_tree(self):

        if self.clericon:
            if self.MV < 100:
                self.cleric.rod.write("cast refresh %s\ttrance\n"%self.name)

        if self.phase == 0:
            self.status_msg = "Preparing to go -- TOL"
            self.phasedir = {}
            self.phase = 1
            
            if not self.cleric_follow():
                self.phase = 0
            else:
                self.go("ne")
                self.rod.write("say invis\n")
                self.time.sleep(5)
                self.go("sw")
                self.go("#50 w;#5 s;#2 w")
            
             
        elif self.phase == 1:
            # initialize the circuit
            self.status_msg = "Initializing circruit -- TOL"
            self.phase = 2
            self.whereami()
            

            if self.support != None:
                self.support.whereami()
                if self.support.location != "At The Roots":
                    return 'dhaven'

            if self.clericon:
                self.cleric.get_loc()
                if self.cleric.location != "At The Roots":
                    return 'dhaven'
        
            if self.location != "At The Roots":
                # did not get to place                                                                                                                                 
                return 'dhaven'
            elif self.phase == 2:
            
                self.phasedir = {}
            
                dirs = "w;w;w;w;w;w;*open w;w;w;n;*open north;n;n;n;n;n;u;u;u;u;u;e;pestilence;w;w;w;famine;e;e;n;n;s;s;u;e;d;d;eris".split(";")
                if self.level >= 45:
                    self.cankill= ['dragon','eris','death']
                else:
                    self.cankill = ['dragon','eris']
                for i in range(len(dirs)):
                    self.phasedir[i+2] = dirs[i]

                               
                
        elif self.phase >= 2 and not self.fight:
            # now go through shattered refuge one room at the time
            # 1) check no one else is in my room
            # 2) check mobs
            # 3) kill mobs if there
            # 4) move
            self.status_msg = "Killing stuff -- TOL"
            mobnames = {"A huge dragon-shaped":"dragon",
                        "The Incarnation of":"death",
                        "Eris, the Goddess":"eris",
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
                        if self.aff['sanctuary'] < 5:
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
                    if character in [self.name.capitalize(),"Kaeval","Kaetas"]:
                        continue
                    if self.loc_dic[character] == self.location:
                        alone = False
                print(self.loc_dic)
                print("Alone?", alone)
                # should I fight?
                if alone:
                    startfight = None
                    if True:
                        for mob in mobs:
                            print("MOB", mob)
                            if mobs[mob] > 0:
                                if mob in self.cankill:
                                    startfight = mobnames[mob]
                                    break
                    if startfight != None:
                        if startfight == "death":
                            self.cleric.write("cast shockshield %s\n"%self.name)
                        self.rod.write("kill %s\n"%(startfight)) 
                        self.target = startfight
                        self.fight = True
            else:

                if self.check_cleric():
                    self.cleric.quit("trance")

                self.sys.stdout.write("\nDONE THIS ROUND...\n")
                #self.rod.write("quit\n")
                self.time.sleep(5)

                print(self.read())
                self.time.sleep(10)
                return 'dhaven'

            if not self.fight:
                d = self.phasedir[self.phase]
                movecleric = None
                if d == "pestilence":
                    self.target = "pestilence"
                    if not self.fight:
                        if self.clericon:
                            self.cleric.rod.write("sit\n")
                            self.time.sleep(5)
                            movecleric = "e"
                        d = "e"
                    else:
                        d = "*look"
                elif d == "famine":
                    self.target= "famine"
                    if not self.fight:
                        if self.clericon:
                            self.cleric.rod.write("sit\n")
                            self.time.sleep(5)
                            movecleric = "w"
                        d = "w"
                    else:
                        d = "*look"
                elif d == "eris":
                    self.target = 'eris'
                    self.cleric.rod.write("kill eris\n")
                    self.time.sleep(2)
                    self.rod.write("kill eris\n")
                if "*" in d:
                    self.rod.write(d[1:]+'\n')
                else:
                    self.go(self.phasedir[self.phase])

                if movecleric != None:
                    self.cleric.rod.write("wake\n")
                    self.cleric.rod.write(movecleric+'\n')

                
                self.phase += 1
                #self.time.sleep(.5)  
        return False
    
    
        
