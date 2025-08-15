from telnetlib_compat import Telnet
import time

class Commands:

    def healup(self):
        ''' checks hp and find the amount of heals needed '''

        # Debug: Always show when healup is called for sect members
        if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
            self.printc("DEBUG: HEALUP CALLED for %s HP:%s/%s - pots available: %s" % (self.name, self.HP, self.MAXHP, list(self.pots.keys())), 'red')

        pot = None
        # Debug: Show all available potions for sect members
        if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
            self.printc("DEBUG: All potions found: %s" % list(self.pots.keys()), 'yellow')
        
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
        
        # Debug: Show the exact command being generated
        if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
            self.printc("DEBUG: %s healpot command: '%s'" % (self.name, self.healpot), 'cyan')
        
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
        
        # Debug: Show exact commands being sent for sect members
        if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
            self.printc("DEBUG: %s SENDING HEAL COMMANDS: %s" % (self.name, actions), 'yellow')
            
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
                        # Sect members use 'heal' keyword, others use 'purple'
                        if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
                            self.rod.write("quaff heal %s\n"%self.container)
                        else:
                            self.rod.write("quaff purple %s\n"%self.container)
                    
                
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
        # Debug: Always show when func_fight is called for sect members
        if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
            self.printc("DEBUG: FUNC_FIGHT CALLED for %s" % self.name, 'red')
            
        self.fightcheck()
        print(self.name, self.charclass, self.MP)
        if True:
            if self.random.random() < 0.5:
                self.check_spells()
                if 'sanctuary' not in self.aff and "holy sanctity" not in self.aff:
                    self.rod.write("gt sanc's off\n")
            self.printc("%s: %d/%dhp"%(self.name,  int(self.HP), int(self.MAXHP)))
            
            # Debug: Check healing threshold for sect members
            if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
                heal_threshold = int(self.MAXHP)*0.8
                self.printc("DEBUG: %s HP %d < %d threshold? %s" % (self.name, int(self.HP), heal_threshold, int(self.HP) < heal_threshold), 'magenta')
            
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

    def check_leveling_spells(self):
        """Check if critical leveling spells need refreshing (less than 50 rounds remaining)"""
        needs_refresh = False
        low_spells = []
        
        # Only check the two critical leveling spells
        critical_spells = {
            'trollish vi': 50,    # Trollish vigor - most important for leveling
            'fly': 50,            # Flying - required for movement in many areas
        }
        
        # Check each spell
        for spell, threshold in critical_spells.items():
            if spell in self.aff:
                if self.aff[spell] < threshold:
                    needs_refresh = True
                    low_spells.append("%s (%d rounds left)" % (spell, self.aff[spell]))
                    self.printc("Critical spell running low: %s has only %d rounds remaining" % (spell, self.aff[spell]), 'yellow')
        
        return needs_refresh, low_spells
    
    def refresh_leveling_spells(self):
        """Return to recall room, wait for trollish vigor to expire, then refresh all leveling spells"""
        self.printc("Refreshing critical leveling spells before continuing combat...", 'gold')
        self.status_msg = "Refreshing leveling spells"
        
        # Go to appropriate location
        if self.level >= 10 and hasattr(self, 'sect_member') and self.sect_member:
            # Go to sect house
            self.printc("Going to sect house for spell refresh...", 'cyan')
            self.rod.write("secthome\n")
            self.time.sleep(3)
            
        else:
            # Go to Darkhaven spell room
            self.godh()
            self.go("nw;w;w;w")
        
        # Check if we have trollish vigor and wait for it to expire for clean refresh
        self.check_affect()
        if 'trollish vi' in self.aff and self.aff['trollish vi'] > 0:
            troll_rounds = self.aff['trollish vi']
            wait_time = int(troll_rounds * 3)  # Each round is ~3 seconds
            self.printc("Waiting %d seconds for trollish vigor (%d rounds) to expire for clean refresh..." % (wait_time, troll_rounds), 'yellow')
            self.time.sleep(wait_time + 5)  # Add 5 seconds buffer
            
        # Now request all buffs and shields for a clean slate
        if self.level >= 10 and hasattr(self, 'sect_member') and self.sect_member:
            self.printc("Requesting full spell refresh from sect bots...", 'cyan')
            self.rod.write("say buffs!\nsay shields!\n")
        else:
            self.printc("Requesting full spell refresh from Darkhaven bots...", 'cyan')
            self.rod.write("say buffs!\nsay shields!\n")
            
        self.printc("Waiting 45 seconds for all spells to be cast...", 'cyan')
        self.time.sleep(45)
        
        # Navigate back if in Darkhaven
        if not (self.level >= 10 and hasattr(self, 'sect_member') and self.sect_member):
            self.go("e;e;e;se")
        
        # Re-check affects after getting spells
        self.check_affect()
        self.printc("Spell refresh complete! Current critical spells:", 'green')
        for spell in ['trollish vi', 'fly']:
            if spell in self.aff:
                self.printc("  %s: %d rounds" % (spell, self.aff[spell]), 'green')
            else:
                self.printc("  %s: NOT ACTIVE!" % spell, 'red')
        
        self.status_msg = "Ready for combat"

    def ensure_spring_exists(self):
        """Ensure a spring exists in the room before combat"""
        # Check if spring already exists in room items
        spring_exists = False
        for item in self.roomitems:
            if "A mystical spring flows majestically from a glowing circle of blue" in item:
                spring_exists = True
                self.printc("Spring already exists in room", 'cyan')
                break
            
        if not spring_exists:
            # Check if we have an icicle staff to create spring
            if self.container in self.containers:
                if "an icicle staff" in self.containers[self.container]:
                    self.printc("No spring in room - creating one with staff...", 'gold')
                    # Use the pattern from existing code - get icicle, wear, brandish, remove, put back
                    self.rod.write("get icicle %s\nwear icicle\nbrandish icicle\nremove icicle\nput icicle %s\nwear all\n" % (self.container, self.container))
                    
                    # Wait for the brandish to complete with MUD lag
                    self.time.sleep(3)
                    
                    # Now check the room to see if spring was actually created
                    self.look()
                    spring_created = False
                    for item in self.roomitems:
                        if "A mystical spring flows majestically from a glowing circle of blue" in item:
                            spring_created = True
                            self.printc("Spring verified created with icicle staff!", 'green')
                            break
                    
                    if not spring_created:
                        self.printc("Warning: Spring creation may have failed", 'red')
                        
                elif self.clericon and self.cleric:
                    # Use cleric to create spring if available
                    self.printc("No spring in room - having cleric create one...", 'gold')
                    self.cleric.rod.write("c 'create spring'\ntrance\n")
                    
                    # Wait for cleric spell to complete
                    self.time.sleep(3)
                    
                    # Check if spring was created
                    self.look()
                    spring_created = False
                    for item in self.roomitems:
                        if "A mystical spring flows majestically from a glowing circle of blue" in item:
                            spring_created = True
                            self.printc("Spring verified created by cleric!", 'green')
                            break
                    
                    if not spring_created:
                        self.printc("Warning: Cleric spring creation may have failed", 'red')
                else:
                    self.printc("No spring in room and no way to create one", 'yellow')

    def autotarget(self, attack):
        # Check if leveling spells need refreshing before combat
        self.check_affect()  # Update current spell durations
        needs_refresh, low_spells = self.check_leveling_spells()
        if needs_refresh:
            self.printc("LOW SPELLS detected before combat: %s" % ", ".join(low_spells), 'red')
            self.refresh_leveling_spells()
            # After refreshing spells, return to continue combat
            self.printc("Spells refreshed, continuing with combat...", 'green')
        
        # Check if sect member needs restocking before combat
        if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
            if self.check_sect_potion_supplies():
                self.printc("LOW POTIONS detected before combat! Restocking from sect house...", 'red')
                self.refill_sect_potions()
                # Update container contents after restocking
                self.look_cont(self.container)
                
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
                # Check if character is a sect member level 10+
                if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
                    # Use secthome for sect members
                    self.printc("DEBUG: Sect member using secthome;jig to reach DH Square from %s" % self.location, 'green')
                    self.rod.write("secthome\n")
                    self.time.sleep(2)
                    self.rod.write("jig\n")
                    self.time.sleep(2)
                    self.printc("DEBUG: Sect member should now be at DH Square", 'green')
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
        

    def check_sect_potion_supplies(self):
        """Check if sect member has enough potions and return True if restocking is needed"""
        if not (hasattr(self, 'sect_member') and self.sect_member and self.level >= 10):
            return False
            
        if self.container not in self.containers:
            return True  # Need to check container contents
            
        container_contents = self.containers[self.container]
        
        # Check healing potions (sect members use different names)
        heal_count = 0
        heal_names = ["a heal potion", "heal potion", "the elixir of sanctuary"]
        for heal_name in heal_names:
            if heal_name in container_contents:
                heal_count += container_contents[heal_name]
        
        # Check mana potions (sect members use different names)  
        mana_count = 0
        mana_names = ["the essence of forest", "harvest melomel", "a mana potion", "mana potion"]
        for mana_name in mana_names:
            if mana_name in container_contents:
                mana_count += container_contents[mana_name]
        
        self.printc("DEBUG: Sect potion check - Heals: %d, Mana: %d" % (heal_count, mana_count), 'yellow')
        
        # Mages have lower heal target due to weight constraints
        heal_threshold = 5 if self.charclass == "Mage" else 5
        mana_threshold = 5
        
        # Need restock if either type is below threshold
        return heal_count < heal_threshold or mana_count < mana_threshold

    def refill_sect_potions(self):
        """Refill potions from sect house when supplies are low"""
        self.printc("Refilling potions from sect house...", 'gold')
        
        # Check current potion counts to calculate what's needed
        current_mana_total = 0
        current_heal_total = 0
        if self.container in self.containers:
            container_contents = self.containers[self.container]
            
            # Count mana potions
            if "the essence of forest" in container_contents:
                current_mana_total += container_contents["the essence of forest"]
            if "harvest melomel" in container_contents:
                current_mana_total += container_contents["harvest melomel"]
            
            # Count heal potions
            heal_names = ["a heal potion", "heal potion", "the elixir of sanctuary"]
            for heal_name in heal_names:
                if heal_name in container_contents:
                    current_heal_total += container_contents[heal_name]
        
        # Go to sect house
        self.rod.write("secthome\n")
        self.time.sleep(2)
        
        # Calculate healing potions needed (target 15 for mages due to weight constraints)
        target_heals = 15 if self.charclass == "Mage" else 20
        heal_amount = max(target_heals - current_heal_total, 0)
        
        if heal_amount > 0:
            self.printc("Current heals: %d, filling %d to reach %d (Class: %s)" % (current_heal_total, heal_amount, target_heals, self.charclass), 'cyan')
            self.rod.write("fill %s %d heal-potion shell\n" % (self.container, heal_amount))
            self.time.sleep(2)
        else:
            self.printc("Already have sufficient healing potions (%d), skipping heal fill" % current_heal_total, 'cyan')
        
        # Go to potion storage room for mana and sanctuary potions
        self.printc("Going to sect house potion storage for mana and sanctuary potions...", 'cyan')
        self.go("d;d;s")
        
        # Calculate mana potions needed to reach 100 total
        mana_needed = max(100 - current_mana_total, 30)  # At least 30, or enough to reach 100
        self.printc("Current mana potions: %d, filling %d to reach 100+" % (current_mana_total, mana_needed), 'cyan')
        self.rod.write("fill %s %d mana\n" % (self.container, mana_needed))
        self.time.sleep(2)
        
        # Also top up sanctuary potions while we're here
        self.printc("Topping up sanctuary potions...", 'cyan')
        self.rod.write("fill %s 5 sanctuary-potion shelf-potion\n" % self.container)
        self.time.sleep(2)
        
        # Return to recall room
        self.go("n;u;u")
        
        self.printc("Sect house potion refill complete!", 'green')

    def restock(self):
        
        # Check if sect member needs restocking due to low supplies
        if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
            if not self.check_sect_potion_supplies():
                self.printc("DEBUG: Sect member has sufficient potions, skipping restock", 'magenta')
                return
            else:
                self.printc("DEBUG: Sect member has low potions, proceeding with restock", 'red')
    	
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
        
        # Check if sect member needs restocking due to low supplies
        if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
            if not self.check_sect_potion_supplies():
                self.printc("DEBUG: Sect member has sufficient potions, skipping refillpots", 'magenta')
                return
            else:
                self.printc("DEBUG: Sect member has low potions, proceeding with sect house restocking", 'red')
                # Use sect house restocking instead of Darkhaven shops
                self.refill_sect_potions()
                return
            
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
        # Check if sect member needs restocking due to low supplies
        if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
            if not self.check_sect_potion_supplies():
                self.printc("DEBUG: Sect member has sufficient potions, skipping refillpotsunorder", 'magenta')
                return
            else:
                self.printc("DEBUG: Sect member has low potions, using sect house restocking", 'red')
                self.refill_sect_potions()
                return
            
        if True:
            rod = Telnet("realmsofdespair.com",4000) 
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
