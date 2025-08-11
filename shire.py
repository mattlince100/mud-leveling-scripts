

class Shire:
    
    def func_shire(self):

        self.printc("Going to the shire\n")
        if self.phase == 0:

            if "kills" in self.alt_info:
                killc = list(self.alt_info['kills'].values())
            else:
                killc = {}

            if len(killc) > 0:
                self.killc = sum(killc)
            else:
                self.killc = 0

            self.phasedir = {}
            self.phase = 1

            self.godh()
            self.go("w;w;w;w;w;w;w;w;w;nw;w;w;nw")

            self.whereami()
            
        elif self.phase == 1:
            # initialize the circuit
            self.phase = 2
 
            if self.location != "A Dimly Lit Path":
                # did not get to place
                self.phase = 0
            else:
                self.phasedir = {}
                
                if self.level <= 50:
                    dirs = 'n;n;n;w;w;w;w;w;w;e;n;s;s;n;e;e;s;s;n;n;e;n;n;e;u;d;w;n;w;n;n;s;s;s;w;n'.split(";")
                

                for i in range(len(dirs)):
                    if len(dirs[i]) == 0: continue
                    self.phasedir[i+2] = dirs[i]

            self.cankill = ["A horse becomes"]
            self.killed = []

        elif self.phase >= 2 and not self.fight:
            # now go through shattered refuge one room at the time
            # 1) check no one else is in my room
            # 2) check mobs
            # 3) kill mobs if there
            # 4) move
                        
            
            mobnames = {'A horse becomes':"horse",
                        "A chicken sits":"chicken",
                        "A cow is":"cow",
                        "A pig wallows":"pig",
                        "A halfling youth":"youth",
                        "A member of":"vil",
                        "A shiriff of ":"shir",
                        "A halfling beauty":"beauty",
                        "The Miller is":"miller",
                        "The mill worker":"mill",
                        "A chic urbanite":"urbanite",
                        "A seasoned adventurer":"advent",
                        "The receptionist sits":"recept",
                        "Farmer Gamgee sniffs":"farmer",
                             }

            mobs = {}

            for mob in mobnames:
                mobs[mob] = 0

            if "kills" in self.alt_info:
                killc =list(self.alt_info['kills'].values())
            else:
                killc ={}
            if len(killc) > 0:
                killc =sum(killc)
            else:
                killc = 0

            self.printc("Killed %s mobs here\n"%(killc-self.killc))
            

            if self.phase in self.phasedir:
                self.whereami()
                print("roomitems:", self.roomitems, self.exits)
                self.printc("\n%s: roomitems: %s\n"%(self.name, ",".join(self.roomitems)),'green')
                for item in self.roomitems:
                    mob = " ".join(item.split()[:3]).strip()
                    if mob in mobs:
                        mobs[mob] += 1

                # am I alone here?
                alone = True
                for character in self.loc_dic:
                    if self.clericon:
                        if character in [self.name.capitalize(),'Kaeval',self.cleric.name]:
                            continue
                    else:
                        if character in [self.name.capitalize(),'Kaeval']:
                            continue
                    if self.loc_dic[character] == self.location:
                        alone = False
                
                
                # should I fight?
                print("alone?", alone)
                if not alone:
                    pass
                else:
                    startfight = None
                    if True:
                        for mob in mobs:
                            if mobs[mob] > 0:
                                if mob in mobnames:
                                    if mobnames[mob] not in self.killed:
                                        startfight = mobnames[mob]
                                    else:
                                        startfight = None
                                else:
                                    startfight = None
                                    break
                    if startfight != None:
                        self.rod.write("kill %s\n"%(startfight)) 
                        self.killed.append(startfight)
                        self.target = startfight
                        self.fight = True
            else:
                self.sys.stdout.write("DONE THIS ROUND...\n")
                #self.rod.write("quit\n")
                self.time.sleep(5)
                #if "kills" in self.alt_info:
                #    self.alt_info['kills'] = {}
                #print self.rod.read_very_eager()
                self.time.sleep(10)
                return 'dhaven'

            if not self.fight:
                if self.phasedir[self.phase] in ["n","e","w","s","d","u","sw","se","nw","ne","enter"]:
                    self.go(self.phasedir[self.phase])
                    self.phase += 1
                else:
                    self.rod.write("%s\n"%self.phasedir[self.phase])
                    self.phase += 1

                #self.time.sleep(.5)            
            
        return False
