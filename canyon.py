

class Canyon:
    
    def func_canyon(self):

        self.printc("Going to el canyon\n")
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
            self.go("#13 s;e;e;u;u;w;sw;w;sw;d;d;sw;sw;#4 s;e")

            self.whereami()
            
        elif self.phase == 1:
            # initialize the circuit
            self.phase = 2
 
            if self.location != "A Mountain Path":
                # did not get to place
                self.phase = 0
            else:
                self.phasedir = {}
                
                if self.level <= 50:
                    dirs = 'u;u;e;u;nw;d;n;w;n;e;e;n;w;w;n;e;e;n;w;w;n;e;e;n;w;w'.split(";")
                

                for i in range(len(dirs)):
                    if len(dirs[i]) == 0: continue
                    self.phasedir[i+2] = dirs[i]

            self.cankill = ['A small elemental', "A spark of",
                            "A tiny elemental","A little imp",
                            "A small pebble","An aged alchemist",
                            "An aged alchemist","A glowing mist",
                            "A particle of","An Illusionist seeks",
                            "A warrior of", "A small, flickering",
                            "A particle of","An elemental of",
                            "A mud creature","An eddie current",
                            "A small blob","A small, flickering"]
            self.killed = []

        elif self.phase >= 2 and not self.fight:
            # now go through shattered refuge one room at the time
            # 1) check no one else is in my room
            # 2) check mobs
            # 3) kill mobs if there
            # 4) move
                        
            
            mobnames = {'A small elemental':"small", 
                        "A spark of":"spark",
                        "A tiny elemental":"tiny",
                        "A little imp": "imp",
                        "A small pebble": "pebble",
                        "An aged alchemist":"alchemist",
                        "A glowing mist": "mist",
                        "A particle of": "particle",
                        "An Illusionist seeks": "illusion",
                        "A warrior of": "warrior",
                        "A small, flickering": "element",
                        "A particle of":"particle",
                        "The Elemental Guardian": "guardian",
                        "An elemental of": "elemental",
                        "A mud creature": "mud",
                        "An eddie current": "eddie",
                        "A small blob": "blob",
                        "A small, flickering":"flame"
                             }

            mobs = {}

            for mob in mobnames:
                mobs[mob] = 0
            

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
                                if mob in self.cankill:
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
                if len(self.inv) > 3:
                    self.rod.write("wear oar\nwear oar\nwear hammer\nwear hammer\nwear all\ndrop all\nget %s\nget recall\n"%self.container)
                    self.time.sleep(2)
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
