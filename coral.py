

class Coral:
    
    def func_coral(self):


        if self.phase == 0:


            self.phasedir = {}
            self.phase = 1
            self.check_affect()
            self.whereami()
            # check aqua and fly and go to coral depths

            if self.location == "A watery tangle of caves":
                # try to get out
                while self.location != "A dark cave":
                    dir = self.random.choice(["n","w","s","e"])
                    self.go(dir)
                    self.time.sleep(1)
                    self.whereami()
                self.go("e;e;n;w;u")

                if self.support != None:
                    self.support.goDH = True

                return "dhaven"

            if self.location in ['The bottom of the vortex', 'A Dark passage','Surrounded in dark water','An escape??','A dark cave']:
                self.sys.stdout.write("Emergency get out of here...\n")
                self.go("#3 d;#3 n;#2 e;#3 n;#2 w;#3 n",force = True)
                self.godh()
                return "dhaven"

            self.phasedir = {}
            self.phase = 1

            if not self.cleric_follow():
                self.phase = 0
                return
            else:
                self.godh()

            #if self.clericon and self.level < 10:
            #    self.cleric.quit()
                
            getspells = False
            for spell in ['aqua breath']:
                if spell in self.aff:
                    if spell != "aqua breath":
                        if self.aff[spell] < 30:
                            self.time.sleep(self.aff[spell]*3.2)
                        getspells = True
                        break
                    else:
                        if self.aff[spell] < 300:
                            getspells = True
                            break
                else:
                    getspells = True
                    break

            getfly = False
            if "fly" in self.aff:
                if self.aff['fly'] < 30:
                    self.sys.stdout.write("waiting for fly to run out...\n")
                    self.time.sleep(self.aff['fly']*3.1)
                    getfly = True
            
            if getfly:
                self.check_affectby()
                if "flying" in self.affby and not getspells:
                    getspells = False

            
            self.go("nw;w;w;w")
            if getspells:
                self.sys.stdout.write("GETTING SPELLS...\n")
                self.rod.write("say refresh\nsay aqua\n")
                self.time.sleep(15)
            if self.support != None:
                self.support.rod.write("say refresh\n")
            self.time.sleep(4)
            self.go("e;e;e;se")
            self.go("#6 s;ne;s;s;se;e;e;s;sw;sw;s;e;e;u;#3 e;ne;e;e;e;s;se;s;e;e;s;e;e;enter;s;s;s;se;s;d;d;d")

            self.whereami()
            
        elif self.phase == 1:
            # initialize the circuit
            self.phase = 2
 
            if self.support != None:
                self.support.whereami()
                if self.support.location != "The bottom of the vortex":
                    self.phase = 0
            if self.location != "The bottom of the vortex":
                # did not get to place
                self.phase = 0
            elif self.phase == 2:
                self.phasedir = {}
                #if self.level <= 8:
                #    # don't go in the watery tangles
                #    dirs = 's;s;e;e;s;s;s;w;w;e;e;n;w;u;w'.split(";")
                if self.level < 10:
                    # just go eels
                    dirs = 's;s;e;e;s;s;s;w;w;s;n;s;s;e;n;w;s;s;n;s;w;e;w;n;e;w;n;n;s;s;e;e;n;w;u;w'.split(";")
                elif self.level <= 50:
                    dirs = 'n;open rock;e;e;n;ne;n;e;e;e;s;se;sw;u;config +autoloot;s;unlockcrab;config -autoloot;s;w;e;s;n;e;w;unlock n;open n;n;n;d;ne;enter;e;n;n;w;n;s;s;n;e;e;n;s;s;n'.split(";")
                #else:
                #    dirs = 'nw;w;s;s;s;e;e;w;s;n;w;s;n;w;e;n;n;n;w;n;w;w;e;e;e;e;w;w;n;w;w;e;e;n;s;e;e'.split(";")

                for i in range(len(dirs)):
                    if len(dirs[i]) == 0: continue
                    self.phasedir[i+2] = dirs[i]

                self.cankill = ['A sinuous grey', "The eel attacks,", "A long, snakelike",
                                "A handsome young","A little mermaid","This vicious looking",
                                "A beautiful little"]

                if self.level >= 16:
                    self.cankill += ['An exquisitely beautiful']
                if self.level >= 25:
                    self.cankill += ['An adult mermaid','This merman makes']

                
        elif self.phase >= 2 and not self.fight:
            # now go through shattered refuge one room at the time
            # 1) check no one else is in my 
            
            if self.phase % 5 == 0 and self.phase >= 10:
                # every few rooms check effects     

                self.check_affect()
                getsanc = False
                if "sanctuary" in self.aff:
                    if self.aff['sanctuary'] < 10:
                        self.time.sleep(self.aff['sanctuary']*3.2)
                        getsanc = True
                else:
                    getsanc = True

                if self.clericon:
                    getsanc = False

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
            
            mobs = {"A sinuous grey":0,
                         "The eel attacks,":0,
                         "A long, snakelike": 0,
                         'This vicious looking':0,
                         'An exquisitely beautiful': 0,
                         'A beautiful little':0,
                         'This merman makes':0,
                         'A little mermaid':0,
                         'A handsome young':0,            
                    "An adult mermaid":0,
                         }
            
            mobnames = {"A sinuous grey":"eel",
                             "The eel attacks,":"eel",
                             "A long, snakelike":"eel",
                             'This vicious looking':"crab",
                             'An exquisitely beautiful': "mermaid",
                             'A beautiful little':"mermaid",
                             'This merman makes':"merman",
                             'A little mermaid':"mermaid",
                             'A handsome young':"young",
                        'An adult mermaid':"adult",
                             }

            if self.phase in self.phasedir:
                self.whereami()
                self.sys.stdout.write("\n%s: roomitems: %s\n"%(self.name, ",".join(self.roomitems)))
                
                for item in self.roomitems:
                    mob = " ".join(item.split()[:3])
                    if mob in mobs:
                        mobs[mob] += 1

                # am I alone here?
                alone = True

                if self.clericon:
                    trusted = [self.name.capitalize(), self.cleric.name]
                else:
                    trusted = [self.name.capitalize()]
                for character in self.loc_dic:
                    if self.support != None:
                        trusted += [self.support.name]
                    
                    if character in trusted:
                        continue
                    if self.loc_dic[character] == self.location:
                        alone = False
                
                self.sys.stdout.write("\nAlone? "+str(alone)+'\n')
                self.sys.stdout.write("\t".join(["%s: %s"%(x,self.loc_dic[x]) for x in self.loc_dic])+'\n')
                    

                # should I fight?
                if not alone:
                    pass
                else:
                    startfight = None
                    print(sum(mobs.values()))
                    if sum(mobs.values()) <= 2:
                        for mob in mobs:
                            if mobs[mob] > 0:
                                if mob in self.cankill:
                            #self.rod.write("kill %s\n"%(mobnames[mob]))
                                    startfight = mobnames[mob]
                                else:
                                    startfight = None
                                    break
                    if startfight != None:
                        self.rod.write("kill %s\n"%(startfight)) 
                        self.fight = True
            else:

                
                self.sys.stdout.write("\nDONE THIS ROUND...\n")
                #self.rod.write("quit\n")
                self.time.sleep(5)
                
                if len(self.inv) > 3:
                    self.rod.write("wear oar\nwear oar\nwear hammer\nwear hammer\nwear all\ndrop all\nget %s\nget recall\n"%self.container)
                    self.time.sleep(2)

                return 'dhaven'

            if not self.fight:
                if self.phasedir[self.phase] in ["e","w","s","d","u","sw","se","nw","ne","enter"]:
                    self.go(self.phasedir[self.phase])
                    self.phase += 1
                else:
                    if self.phasedir[self.phase] == "unlockcrab":
                        self.rod.write("unlock s\nopen s\nver\n")
                        r = ''
                        done = False
                        while True:
                            r += self.read()
                            if "SMAUG 2.6" in r:
                                self.sys.stdout.write("\n%s: %s\n"%(self.name,r))
                                for ln in r.split("\n"):
                                    if "You unlock" or "already open" in ln:
                                        done = True
                                        break
                                break
                        if done:
                            self.phase += 1
                        else:
                            self.phase += 9
                    elif self.phasedir[self.phase] == "open rock":
                        if self.support != None:
                            # must tell support to also open
                            self.support.rod.write("open rock\ne\n")
                            self.time.sleep(2)
                        if self.clericon:
                            self.cleric.rod.write("open rock\ne\n")
                            self.time.sleep(2)
                        self.rod.write("%s\n"%self.phasedir[self.phase])
                        self.phase += 1
                    else:
                        self.rod.write("%s\n"%self.phasedir[self.phase])
                        self.phase += 1

                #self.time.sleep(.5)
            
            
        return False
