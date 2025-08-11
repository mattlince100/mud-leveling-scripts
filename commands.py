import telnetlib, time

class Commands:

    def healup(self):
        ''' checks hp and find the amount of heals needed '''

        pot = None
        for (pot, cont) in list(self.pots.keys()):
            if pot in ['heal','purple']:
                break
        if pot not in ['heal','purple']:
            self.printc("%s can't find pots"%self.name)
            self.time.sleep(1)
            self.find_pots()
            self.time.sleep(1)
            return
                        
        self.healpot = "quaff %s %s"%(pot, cont)
        
        if pot == "purple":
            hp = 40
        else:
            hp = 100

        print("Quaffing %s: %d/%d"%(self.name, self.HP, self.MAXHP))
        numpots = min([(self.MAXHP-self.HP)/hp, 12]) # can only drink 12 pots at once for now
        
        actions = []
        self.quaffing = True
        
        if self.full:
            actions.append("drink")
        elif self.gettingfull:
            if numpots > 4:
                actions = [self.healpot]*4+['drink']+[self.healpot]*(numpots-4)
            else:
                actions = [self.healpot]*numpots+['drink']
        else:
            if numpots > 8:
                actions = [self.healpot]*8+['drink']+[self.healpot]*(numpots-4)
            else:
                actions = [self.healpot]*numpots

        print("\n".join(actions))
        self.waitcmd2("\n".join(actions)+'\n')

    def fight(self):
		r = self.read()

    def refavor(self):
        self.check_affect()
        print("FAVOR:", self.favor)
        if self.favor == None:
            return
        elif self.favor not in ["praised", "honored", "loved"]:
            # check if vlaresh of Ae'nari
            if self.deity == "A'enari":
                self.godh()
                self.time.sleep(3)
                self.go("#8 n;ne;w;n;ne;nw;e;ne;n;e;ne;#2 n;#2 ne;#2 e;n;ne;nw;w;#4 n;enter;ne;w")
                self.get_loc()
                if self.location != "Serenity":
                    self.refavor()
                else:
                     self.waitcmd("e\nw\n"*10)
                     self.refavor()
        else:
            self.godh()

    def main_loop(self):
        try:
            self.main_loop2()
        except EOFError:
            self.rod.close()
            try: self.rod.close()
            except: pass
            self.sys.stdout.write("\n\n********CONNECTION CLOSED FOR %s*********\n\n"%self.name)
            #self.quit()
        #except IndexError:
        #    self.sys.stdout.write("Index error, restarting %s"%self.name)
        #    self.quit()
        #    self.status = "restart"
        #except:
        #    self.quit()
        #    self.status = "restart"

            
    def main_loop2(self):

        self.buf = ''
        self.bufln = ''
        
        self.start = time.time()
        newstuff = ''
        terminate = False
        cspring = False
        while not self.stop:
            nextfunc = None

            # read until newline and add to buf
            t = time.time()-self.start
            #self.printc("%f"%t,'gold')
            if self.random.random() < 0.05:
                if t > 10:
                    self.printc("Time without action (%s, %s)..."%(self.name, str(t)))

            if t > 3 and (not self.trancing or t > 17):
                self.rod.write("devote\n")
                self.time.sleep(.2)
            self.bufln += self.read()

            if "\n" in self.bufln:
                
                for ln in self.bufln.split("\n"):
                    if ln.strip() == "": continue
                    #if self.fight:
                    #    self.printc(ln.strip())
                          
                        
                    if "SMAUG 2.6" in ln:
                        self.lag = 0
                        
                    self.check_hunger(ln)
                    self.check_disarm(ln)
                    
                self.bufln = ''
                if self.lag == 0:
                    if self.fight:
                        self.func_fight()
                        nextfunc = None
                    else:
                        nextfunc = self.func()

                        
                if nextfunc in self.funcdic:
                    if self.support != None and nextfunc == "dhaven":
                        self.support.gofunc("dhaven")
                        self.time.sleep(.2)
                    self.phase = 0
                    #self.printc("function %s\n"%(nextfunc),'gold')
                    self.func = self.funcdic[nextfunc]
                ####
                
                self.bufln = ''
                self.start = time.time()
            elif t > 1.2*60:
                self.printc("Long time without action (%s, %s)... stopping"%(self.name, str(t)))
                self.quit()
                self.status = "restart"

            if self.fight:
                time.sleep(.2)
            else:
                time.sleep(2)
                
            if nextfunc == 'exit':
                self.quit()
                self.status = "restart"
                return
            elif nextfunc == 'exitexit':
                self.status = 'quit'
                self.quit()
                return

        

    def move(self,direction, p):
        ''' try to move a direction and return whether successful '''
        if len(direction) == "": return 1
        #self.rod.write(direction+'\nver\n')
        r = ''
        if not self.fight:
            #r = self.waitcmd(direction, p)
            self.rod.write(direction+'\n')
        else:
            r = self.waitcmd("strike",p)
            
        if self.fight:
            if self.random.random() < 0.1:
                self.check_affect(p=False)
                self.sys.stdout.write("Fighting... \n *** AFF ***" + str(self.aff))
                self.check_spells()

            for l in r.split("\n"):
                self.check_disarm(l)
                if "(%s)"%self.name.lower() in l:
                    self.HP, self.MAXHP = l.strip().replace("hp","").split()[1].split("/")
                    self.MP, self.MAXMP = l.strip().replace("mn","").split()[2].split("/")
                    self.sys.stdout.write(r)

                    self.cleric_heal()

                    if int(self.HP) < int(self.MAXHP)*0.4:
                        self.rod.write("flee\nquit\n")
                        self.status = "restart"
                    elif int(self.HP) < int(self.MAXHP)*0.7:
                        self.rod.write(self.heal)
                    
                
            self.start = time.time()
            return 2
        elif "look" in direction or "open" in direction or "enter" in direction:
            return 1
        
        
    def parsedir(self,dirs):
        finaldir = []
        for x in dirs.split(";"):
            if "#" in x:
                N = int(x.split("#")[-1].split()[0])
                direction = x.split()[-1]
            else:
                N = 1
                direction = x

            finaldir += [direction]*N
        return finaldir

    def go(self, directions, force = False, p = False):
        self.read()
        self.movement = 0

        directions = self.parsedir(directions)
        self.sys.stdout.write("\nMoving %s\n"%(";".join(directions)))
        i = 0
        Nloop = 0
        L = len(directions)
        print(directions)
        move = -1
        while len(directions) > self.movement and Nloop < L+10:
            
            #if Nloop % 10 == 0:
            #    self.get_loc()            
            self.read()
            if self.movement > move:
                Nloop += 1
                move = self.movement
                if move == len(directions):
                    break
                direct = directions[move]
                
                if i == len(directions)-1:
                    movestatus = self.move(direct, True)
                    self.printc("Movement: %d %s"%(self.movement, direct),'gold')
                else:
                    movestatus = self.move(direct, p)
                
                if movestatus == -1:
                    self.printc("\n%s: Cannot move that way (%s)...\n"%(self.name, direct))
                if self.fight: #fighting
                    Nloop -= 1
                    pass
            self.time.sleep(0.05)
        return

    def func(self):
        return

    def func_none(self):
        return



    def func_fight(self):
        self.fightcheck()
        print(self.name, self.charclass, self.MP)
        if True:
            if self.random.random() < 0.5:
                self.check_spells()
                if 'sanctuary' not in self.aff and "holy sanctity" not in self.aff:
                    self.rod.write("gt sanc's off\n")
            self.printc("%s: %d/%dhp"%(self.name,  int(self.HP), int(self.MAXHP)))
            if int(self.HP) < int(self.MAXHP)*0.8:
                self.healup()
            else:
                if self.charclass == "Barbarian":
                    if self.forcetarget != None:
                        self.waitcmd("gt rend %s\nrend %s"%(self.forcetarget,self.forcetarget))
                    else:
                        self.autotarget("rend")

                elif self.charclass == "Thief":
                    self.autotarget("circle")
                elif self.charclass in ["Dread","Vampire"]:
                    if self.MP < 10:
                        self.autotarget("feed")
                    else:
                        self.autotarget("grasp")
                elif self.charclass == "Warrior":
                    self.waitcmd("smash")
                elif self.charclass == "Ranger":
                    self.waitcmd("wasp")
                elif self.charclass == "Paladin":
                    self.waitcmd("strike")
                else:
                    self.autotarget("strike")
        return

    def autotarget(self, attack):
        if self.fighting != "":
            if self.fighting in self.autotargetdic:
                tar = self.autotargetdic[self.fighting]
            else:
                trytargets = self.fighting.split() 
                if self.random.random() < 0.5:
                    tar = self.random.choice([x for x in "abcdefghijklmnopqrstuvwxyz"])
                else:
                    tar = self.random.choice(trytargets)
                self.printc("No target for %s, trying %s"%(self.fighting,tar),'gold')
            r = self.waitcmd("%s %s"%(attack, tar))
            #print [r]
            if ("They aren't here." in r or "You wouldn't dare..." in r or "You feel too nice to do that!" in r or "The gods frown on such illegal killing" in r) and self.fight:
                if self.fighting in self.autotargetdic:
                    self.printc("Target was wrong for %s (%s)"%(self.fighting,tar),'gold')
                    self.autotargetdic.pop(self.fighting)
                return
            else:
                self.target = tar
                self.printc("%s %s (%s)"%(attack, self.fighting,tar),'gold')
                if self.fighting not in self.autotargetdic:
                    self.autotargetdic[self.fighting] = tar
                    self.pickle.dump(self.autotargetdic, open("autotarget.pck",'wb'))
                elif tar != self.autotargetdic[self.fighting]:
                    self.autotargetdic[self.fighting] = tar
                    self.pickle.dump(self.autotargetdic, open("autotarget.pck",'wb'))
                return
        self.printc("Could not see who I'm attacking",'gold')
            

    def recall(self):
        self.get_loc()

        if self.location in ["Thoth's Rune on Vertic Avenue",
                            "Atop the Tower of Dragons",
                            "Return to the Tribal Lands"]:
            return
        print(self.vars['recall'])


    def godh(self, loc = "dhsquare"):

        if self.goingback:
            return 
        else:
            self.goingback = True

        if self.fight:
            self.printc("Fighting: %s can't go back to DH %s\n"%(self.name, loc))
            return


        self.printc("%s is going back to DH %s\n"%(self.name, loc))
        self.get_loc()
        self.time.sleep(0.5)
        self.trancing = False

        if loc == "dhsquare":
            if self.location == "Thoth's Rune on Vertic Avenue":
                self.go("s")
            elif  self.location == "Darkhaven Square":
                pass
            else:
                # Debug: Print current location for Kaeval
                if self.name in ["Kaeval", "Lemaitre"]:
                    self.printc("KAEVAL RECALL DEBUG: Currently at '%s'" % self.location, 'red')
                if self.charclass == "Barbarian":
                    self.rod.write("get recall my.basket\nshatter recall\n")
                    self.time.sleep(2)
                    self.go("w;n;n;nw;w;n;nw;n;w")
                    self.time.sleep(2.5)
                    self.rod.write("buy recall\nput recall my.basket\ne\nn\nn\nsay I wish to visit the city dwellers\ns\ndr\n")
                    self.time.sleep(2.5)
                elif self.name in ["Fanmal"]:
                    self.rod.write("recite scroll\nget recall my.basket\n")
                    self.go("s;se;sw;w;sw;sw")
                elif self.name in ["Vanox","Adixe"]:
                    self.printc("RECALLING %s located %s"%(self.name,self.location))
                    self.do("recall scroll;d;d;s;s;s;ne;e;buy recall;w;sw;n;n;n;n",self.rod)
                    self.do("e;say town;s", self.rod)
                else:
                    if self.name in ["Kaeval","Lemaitre"]:
                        self.rod.write("c word\n")
                        self.time.sleep(2)
                        # Navigate from recall location to Darkhaven Square
                        self.whereami()
                        if self.location == "The Stables":
                            self.go("e;s;s;e;se")
                        elif self.location == "The Baptismal Font":
                            self.go("w;w;s;s;e;se")
                        else:
                            self.go("w;w;s;s;e;se")
                    else:
                        self.rod.write("recite scroll\nget recall my.basket\ns\ndr\n")
                    self.time.sleep(2.5)

        self.goingback = False


    def buyblue(self):
        tmp = self.ROD("Salamon","Elijah","chest",'none')
        if self.charclass == "Fathomer":
            self.waitcmd("give 200k coin salamon\nvis")

            r = tmp.waitcmd("buy 20 blue\ngive bag %s"%self.name)
            self.printc(r,"red")
            try: tmp.rod.write("give %d coin %s\n"%(tmp.gold, self.name))
            except: pass
            self.waitcmd("empty bag basket\ndrop bag\n")

            tmp.quit()
        else:
            r = ''
            self.waitcmd("give 500k coin salamon\nvis")        
            r = tmp.waitcmd("buy 50 blue\ngive bag %s"%self.name)
            self.printc(r,"red")
            try: tmp.rod.write("give %d coin %s\n"%(tmp.gold, self.name))
            except: pass
            self.waitcmd("empty bag basket\ndrop bag\n")
        
            tmp.quit()
        

    def printf(self,text, color = None):
        for ln in text.split("\n"):
            self.printc(ln,color)

    def printc(self,text, color = None):
        if color == None:
            color = self.color
        
        if color == 'gold':
            color = bcolors.WARNING
        elif color == "white":
            color = bcolors.WHITE
        elif color == "grey":
            color = bcolors.GREY
        elif color == "green":
            color = bcolors.GREEN
        elif color == "blue":
            color = bcolors.BLUE
        elif color == "red":
            color = bcolors.RED
        elif color == "cyan":
            color = bcolors.CYAN
        elif color == "head":
            color = bcolors.HEADER
        elif color == "magenta":
            color = bcolors.MAGENTA
        elif color == "pink":
            color = bcolors.PINK
        else:
            color = ''
        self.sys.stdout.write(color + text + bcolors.ENDC+'\n')
        return


    def checkready(self, requirements = {"sanctuary":30}):
        # check spells and health before kill
        
        return True


    def emergency_quit(self):
        self.printc("EMERGENCY QUIT")
        self.time.sleep(3)
        msg = self.random.choice(["yes?","hi", "brb", "gtg","?","hello","yeah?","hang on","bbl","got to run"])
        
        if self.fight:
            self.time.sleep(3)
            self.rod.write("reply %s\n"%msg)
            self.rod.write("flee\nquit\n")
            try: self.rod.write("flee\nquit\n"*5)
            except: pass
        else:
            self.time.sleep(10)
            self.rod.write("reply %s\n"%msg)
            self.time.sleep(10000)
        
        self.time.sleep(30*60)


   

    def portal(self):
        tmp = self.ROD("Lore","Elijah","chest",'none')
    
    
        while True:
            r = tmp.waitcmd("cast myst\ncast portal fabric\n")
            if "You utter an incantation, and a portal forms in front of you!" in r:
                break
            elif self.MP < 100:
                tmp.rod.write("trance\n")
                self.time.sleep(16)
            
        tmp.quit()


    def checkdead(self):
        self.survey()
        print(self.eqdam)
        if len(self.eqdam) == 0:
            # dead
            self.suppcorpse()

    def suppcorpse(self):
        if self.favor in ["praised", "honored", "loved"]:
            pass
            #self.do("supp corpse;get all corpse;wear all;get all corpse;wear all;get all corpse;wear all;",self.rod)


    def repair(self):

        self.survey()
        if len([x for x in self.eqdam if x[1] != 'superb']) == 0:
            self.printc("Nothing to repair", 'gold')
            return

        self.godh()
        self.go("#7 s")
        mage = "Dresden"
        self.log_alt(mage)
        
        while True:
            self.look()
            if 'A whirling portal of energy turns slowly, beckoning to the unknown.' in self.roomitems:
                self.go("enter")
                self.get_loc()
                if self.location == "Before the Merchant Gate":
                    break
                else:
                    self.go("enter")
            else:
                self.alt.write("dismiss portal\ncast portal %s\ntrance\n"%self.name)
            self.time.sleep(5)
        self.go("e")
        self.waitcmd("rem all\nrem all\nrepair all\nwear all\nwear all\n")
        self.godh()
        

    def restock(self):
    	
    	# REPAIR
    	#if len([x[0] for x in self.eqdam if x[1] != "superb"]) > 0:
        #    self.go("s;s;e;s")
        #    self.rod.write("rem all\nrem all\nrepair all\nwear all\nwear all\n")
        #    self.time.sleep(3)
        #    self.go("n;w;n;n")

        # FIND POTS AND RESTOCK IF NEEDED
        self.find_pots()
        self.print_pots()
        potstoget = {}

        for pot, cont in self.pots:
        	if pot in self.minpots:
        		potstoget[pot] = max([0,2*(self.minpots[pot]-self.pots[(pot,cont)])])

        for pot in self.minpots:
        	if pot in potstoget: continue
        	potstoget[pot] = self.minpots[pot]

        container = [x[1] for x in list(self.pots.keys())][0]
        print("toget", potstoget)
        self.refillpots(potstoget, container)

    def repairall(self):
        self.do("rem all;rem all;repair all;wear all",self.rod)

    def refillpots(self, potstoget, container):   
        
        self.do("get recall basket;get recall 2.basket;rec scroll;d;d;s;s;s;nw;w",self.rod)
        self.repairall()
        self.do("e;se;ne;e;buy recall;w;sw;n;n;n;n;w",self.rod)
        for pot, num in list(potstoget.items()):
            print(pot, num)
            if num > 0:
                self.rod.write("fill my.%s %d '%s' shelf\n"%(container, num, pot))
                self.time.sleep(.6)
        self.do("e;e;say town;s", self.rod)
        return 

    def dig(self, direction = None, maxtry = 20):
        self.get_loc()
        print("dig", self.location)
        if direction != None:
            self.rod.write("dig %s\n"%direction)
        else:
            self.rod.write("dig\n")
        N, t = 0, 0
        while True:

            s = self.read()
            if N > maxtry:
                return s
            if ("Your dig did not discover any exit." in s or
                "You stop digging" in s or
                "Your dig uncovered nothing." in s
                or t > 5):
                if direction != None:
                    self.rod.write("dig %s\n"%direction)
                else:
                    self.rod.write("dig\n")
                N += 1
                t = 0
            elif "You dig open a passageway!" in s:
                return s
            elif "Your dig" in s:
                self.rod.write("get all\n")
                print(s)
            #print s
            t += 1
            self.time.sleep(1)

    def search(self, direction = None, maxtry = 20):
        print("search", self.location)
        if direction != None:
            self.rod.write("search %s\n"%direction)
        else:
            self.rod.write("search\n")
        N, t = 0, 0
        while True:
            s = self.read()
            if N > maxtry:
                return s
            if ("You find nothing" in s or t > 5):
                if direction != None:
                    self.rod.write("search %s\n"%direction)
                else:
                    self.rod.write("search\n")
                N += 1
                t = 0
            elif "Your search" in s:
                self.rod.write("get all\n")
                print(s)
                return s
            #print s
            t += 1
            self.time.sleep(1)

    def trackon(self,target):
        p = self.waitcmd("track %s"%target)
        print(p)
        if "You sense a trail " in p:
            direct = p.split("You sense a trail ")[-1].split()[0]
            self.printc("tracking %s, going %s"%(target, direct))
            self.go(direct)
        elif "You're already in the same room!" in p:
            return True
        elif "You don't sense" in p:
            return False
        self.trackon(target)

    def refillpotsunorder(self, potstoget, container):
        if True:
            rod = self.telnetlib.Telnet("realmsofdespair.com",4000) 
            self.time.sleep(2)
            rod.write("keamval\n1q2w3e4r\n \n \nlook\n")
            self.godh()

            self.time.sleep(2)

            self.whereami()
            while True:
                try: keamloc = self.loc_dic["Keamval"]
                except: keamloc = None
                if keamloc != "Darkhaven Square":
                    self.do("s;get recall basket;rec scroll;d;d;n;e;say town;s",rod)
                    self.time.sleep(10)
                else:
                    break

            self.waitcmd("give %s keamval"%container)
            self.do("s;get recall basket;get recall 2.basket;rec scroll;d;d;s;s;s;ne;e;buy recall;w;sw;n;n;n;n;w",rod)
            for pot, num in list(potstoget.items()):
                print(pot, num)
                if num > 0:
                    rod.write("fill my.%s %d '%s' shelf\n"%(container, num, pot))
                    self.time.sleep(.6)
            self.do("e;e;say town;s;give %s %s;quit"%(container, self.name), rod)
            return 

    def do(self, cmds, rod):
		for cmd in cmds.split(";"):
			rod.write(cmd+'\n')
			self.time.sleep(0.5)

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREY = '\033[91m'
    WHITE = '\033[97m'
    GREEN = '\033[92m'
    RED = '\033[31;42m'
    CYAN = '\\u001b[36m'
    MAGENTA = '\033[35m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    PINK = '\033[38;5;206m'
