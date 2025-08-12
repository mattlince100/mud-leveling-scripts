import telnetlib

class Checks:
    pcontainers = ['my.basket','my.draco','my.container', 'my.case']

    potionsdic = {"cure blindness":0, "blazeward":0, "inner warmth": 0,"shadowform": 0,
               "valiance":0, "demonskin":0, "dragonskin": 0, "ethereal web":0,
               "true sight":0, "grounding":0, "eldritch sphere":0, "ethereal shield":0,
               "sanctuary":0, "create spring":0
            }

    damage = ['run down','bit of a wear', 'good', 'very good','excellent','superb','worthless', 'dire need']

    def find_item(self, item):
        conts = []
        for cont in self.pcontainers:
            self.check_cont(cont)
            if self.debug > 0:
                self.printc("[find items] checking %s"%cont)
        for cont in self.containers:
            if item in self.containers[cont]:
                conts.append(cont)
        self.printc("[find items] found %s %s"%(item, conts),'gold')
        return conts #container

    def find_pots(self, p = False):
        # potion and their containers as value
        #print self.name, self.pcontainers
        pot_dic = {
            'a glowing violet potion':("heal",100),
            "Dragons' lament":("heal", 100),
            'a glowing purple potion':("purple",40),
            'the essence of forest':("mana",100),
            'harvest melomel':("mana",100),
            'a glowing blue potion':("blue",100),
            }
        
        self.pots = {}
        
        for cont in self.pcontainers:
            self.check_cont(cont)

            if self.debug > 0:
	            self.printc("checking %s"%cont)

        if self.debug > 0:
	        print(self.name, self.containers)

        for cont in [x for x in list(self.containers.keys())]:
            if len(self.containers[cont]) == 0:
                self.containers.pop(cont)

        for cont in self.containers:
            for potion in list(pot_dic.keys()):
                if potion in self.containers[cont]:
                	if p:
               			self.printc("%s has %d %s."%(cont, self.containers[cont][potion], potion), 'gold')

                	self.pots[(pot_dic[potion][0],cont)] = self.containers[cont][potion]
            for potion in list(self.potionsdic.keys()):
                for p in ["a %s potion"%potion, "an %s potion"%potion]:
                    if p in self.containers[cont]:
                        self.pots[(potion, cont)] = self.containers[cont][p]

    def print_pots(self):
        self.printc("Potion tally:",'gold')
        for pot in self.pots:
            pname, container = pot
            num = self.pots[pot]
            self.printc("%20s (%d)"%(pname, num),'gold')


    def check_group(self):
        #Following Keamval          [hitpnts]   [ magic ] [mst] [mvs] [race]
        #[50  A Pal]  Keamval       1709/1709    971/909   ===    790    elf 
        #[50  A Bar]  Argnok        1534/1534              ===    740  h-orc 
        #[50  A Cle]  Kaeval        1013/1013   1132/1132  ===    590  gnome 

        r = self.waitcmd("group")
        group = {}
        for ln in r.split('\n'):
            if "[" in ln and "Following" not in ln:
                try: 
                    name = ln.split("]")[-1].strip().split()[0]
                    hp = ln.split("]")[-1].strip().split()[1].split('/')
                    group[name] = (int(hp[0]),int(hp[1]), int(hp[0])/float(hp[1]))
                except:
                    pass
        return group


    def check_affectby(self, p = False):
        r = self.waitcmd("aff by", p)
    
        aff = []
        scan = False
        for ln in r.split('\n'):
            if "Imbued with:" in ln:
                scan = True
            elif scan:
                if len(ln.strip()) == 0:
                    break
                aff += ln.strip().split()
        self.affby = aff

    def check_affect(self, p = False):
        N = 0
        while N < 10:
            #self.check_affect_main(p)
            try: self.check_affect_main(p)
            except:
                N += 1
                print("ERROR IN check_affect")
            else:
                return

    def check_affect_main(self, p = False):
        
        aff = {}
        r = self.waitcmd("score", p)
        bsplt = r.split('\n\r')
        #print bsplt
        scan = False
        spells = []
        for i in range(len(bsplt)):

            self.check_disarm(bsplt[i])
            
            if "Deity:" in bsplt[i]:
	        	self.deity = bsplt[i].split("Deity:")[-1].split()[0].strip()
	        	self.favor = bsplt[i].split("Favor:")[-1].split()[0].strip()

            elif "Sect:" in bsplt[i]:
                sect_name = bsplt[i].split("Sect:")[-1].strip()
                if sect_name and sect_name != "None":
                    self.sect_member = True
                    self.printc("Detected sect membership: %s" % sect_name, 'gold')
                    # Save sect membership status
                    self.alt_info["sect_member"] = True
                    self.pickle.dump(self.alt_info, open("alts/info_%s.pckle"%self.name,'wb'))

            elif "Class: " in bsplt[i]:
                self.charclass = bsplt[i].split("Class: ")[-1].split()[0]

            elif "Gold :" in bsplt[i]:
                self.gold = int(bsplt[i].split("Gold : ")[-1].split()[0].replace(",",""))

            elif "AFFECT DATA:" in bsplt[i]:
                spells.append(bsplt[i].split("[")[-1].split("]")[0].split(';'))
                scan = True
            elif scan and "[" in bsplt[i]:
                for x in bsplt[i].split("[")[1:]:
                    spells.append(x.split("]")[0].split(";"))

        aff = {}
        for spell in spells:
            if len(spell) == 2:
                spellname, duration = spell
            elif len(spell) == 3:
                spellname, effect, duration = spell
            try: aff[spellname.strip()] = int(duration.split()[0])
            except: 
                print(spellname.strip()+ " not in spells")
                self.check_affect_main(p)
                continue

        self.affecttime = self.time.time()
        self.aff = aff
        #self.printc("%s %s"%(self.name, self.charclass) +'\n'
        #            +" ".join(["%s (%d)"%(x,self.aff[x]) for x in self.aff if x in ['sanctuary','holy sanctity','fly','trollish vi']]),'gold')
        
    def printaffect(self):

        self.printc("Spells:", 'green')
        for affect, ticks in list(self.aff.items()):
            pticks = float(ticks) - 0.33*(self.time.time()-self.affecttime)
            self.printc("%.20s (%s) (%.2f)"%(affect, ticks,pticks),'green')
        self.check_affect()
        #self.printc("Spells:", 'green')
        #for affect, ticks in self.aff.items():
        #    pticks = float(ticks) - 0.33*(self.time.time()-self.affecttime)
        #    self.printc("2.%.20s (%s) (%.2f)"%(affect, ticks,pticks),'green')

    def check_prac(self):
        r = self.waitcmd("slist 1 %d"%self.level)

        bsplt = r.split('\n')
        slist = []
        for i in range(len(bsplt)):
            if "Skill:" in bsplt[i] or "Weapon:" in bsplt[i] or "Spell:" in bsplt[i]:
                sname, svalue = bsplt[i].split("%: ")
                sname = sname.split(":")[-1].strip()
                svalue = svalue.split()[0]
                slist.append((sname, svalue))
        self.slist = slist

    def printinfo(self):
    	self.printc("%s: %s"%(self.name, self.charclass),'gold')
    	self.printaffect()
    	self.printc("Deity: %s, %s"%(self.deity, self.favor), 'gold')
    	self.printc("%s gold coins"%self.gold, 'gold')

    def check_cont(self, container, p = False):        
        print(self.name, "checking container", "exam %s"%container)
        r = self.waitcmd("exam %s"%container, p)
   
        if "You do not see that here." in r:
            self.containers[container] = []
            if self.debug > 0:
	            self.printc("Could not find %s"%container)
            return
        else:
            bsplt = r.split('\n')
            print(r)
            scan = False
            cont = {}
            for i in range(len(bsplt)):
                if "contains" in bsplt[i] or "holds" in bsplt[i]:
                    scan = True
                elif scan:
                    if len(bsplt[i].strip()) <= 1:
                        break
                    else:
                        item = bsplt[i].strip()
                        if item == "Nothing.":
                            break
                        else:
                            if bsplt[i].strip()[-1] == ")":
                                item = "|".join(bsplt[i].strip().split("(")[:-1])
                                number = bsplt[i].split("(")[-1].split(")")[0]
                            else:
                                number = 1
                            if ")" in item:
                                item = item.split(")")[-1]
                            cont[item.strip()] = int(number)
            self.containers[container] = cont
        return 

    def check_inv(self, p = False):

        r = self.waitcmd("inv")
        inv = []
        bsplt = r.split('\n')
        scan = False
        for i in range(len(bsplt)):
            if "You are carrying" in bsplt[i]:
                scan = True
            elif scan:
                if len(bsplt[i]) <= 1:
                    break
                else:
                    inv.append(bsplt[i].strip()) # probably need to account for multi items
        self.inv = inv
        
    def check_time(self):
        r = self.waitcmd("time")
        self.rod.write("time\nver\n")
        try:
            bsplt = r.split('\n')
            for ln in bsplt:
                if "o'clock" in ln:
                    timehour = ln.split("It is ")[-1].split()[0]
                    ampm = ln.split("o'clock ")[-1].split()[0][:-1]
                    break
            self.printc("Time is %s%s."%(timehour, ampm))
            self.mudtime = (timehour, ampm)
        except:
            self.mudtime = (-1,"am")

    def check_eq(self,p=False):
        for i in range(5):
            try:
                self.check_eq_main()
            except:
                pass
            else:
                break

    def check_eq_main(self, p = False):
        r = self.waitcmd("garb")
        eq = {}
        for ln in r.split('\n'):
            ln = ln.strip()
            if len(ln) == 0: continue
            if ln[0] == '<':
                wearloc = ln.split(">")[0][1:].split()[-1]
                item = ln.split(">")[-1].strip().split(") ")[-1]
                if wearloc in eq:
                    eq[wearloc].append(item)
                else:
                    eq[wearloc] = [item]
        self.eq = eq
        self.weapon = eq['wielded']
        
        return

    def survey(self, p = False):
        r = self.waitcmd("survey")
        eqdam = []
        for ln in r.split('\n'):
            ln = ln.strip()
            if len(ln) == 0: continue
            if ln[0] == '<':
                wearloc = ln.split(">")[0][1:].split()[-1]
                item = ln.split(">")[-1].strip().split(") ")[-1].split("]")[-1].strip()
                if wearloc != "light":
                    dam = ln.split("[")[-1].split("]")[0]
                    if dam in self.damage:
                        eqdam.append((item, dam))
                
        self.eqdam = eqdam
        return

    def printeq(self):
        self.survey()
    	for eq, dam in self.eqdam:
    		self.printc('[%.10s]\t\t%s'%(dam, eq),'gold')

    def get_loc(self, p = False):
        for tries in range(5):
            r = self.waitcmd("where")
            bsplt = r.split('\n')
            done, scanroom = False, False
            for ln in bsplt:
                if self.name in ln and "|" in ln:
                    self.location = ln.split("|")[2].strip()
                    self.printc("%s is at %s"%(self.name,self.location))
                    return
            

    def look(self, direct = None):

        if direct == None:
            r = self.waitcmd("look")
        else:
            r = self.waitcmd("look %s"%direct)
        exits, room, area = None, None, None
        roomitems = []
        loc_dic = {}
        
        
        bsplt = r.split('\n')
        done, scanroom = False, False
        
        for i in range(len(bsplt)):
            if "Exits: " in bsplt[i]:
                exits = bsplt[i].split(":")[-1].strip().split()
                scanroom = True

            elif scanroom:          
                if len(bsplt[i].strip()) <= 1:
                    scanroom = False
                else:
                    if bsplt[i].strip()[-1] == ")":
                        roomitems.append("".join(bsplt[i].strip().split("(")[:-1]).split(")")[-1])
                    else:
                        roomitems.append(bsplt[i].strip().split(")")[-1])

        self.roomitems = roomitems
        self.exits = exits

    def whereami(self, p = False):
        
        r = self.waitcmd("look\nwhere")
        exits, room, area = None, None, None
        roomitems = []
        loc_dic = {}
        
        
        bsplt = r.split('\n')
        done, scanroom = False, False
        
        for i in range(len(bsplt)):
            if "Exits: " in bsplt[i]:
                exits = bsplt[i].split(":")[-1].strip().split()
                scanroom = True

            elif scanroom:          
                if len(bsplt[i].strip()) <= 1:
                    scanroom = False
                else:
                    if bsplt[i].strip()[-1] == ")":
                        roomitems.append("".join(bsplt[i].strip().split("(")[:-1]).split(")")[-1])
                    else:
                        roomitems.append(bsplt[i].strip().split(")")[-1])

                        
            if "Players near you in" in bsplt[i].strip():
                area = bsplt[i].split("Players near you in")[-1].strip().split(":")[0]
                done = True
                continue
                    
            if done and "|" not in bsplt[i]:
                done = False
                    
            elif done:
                try:
                    char = bsplt[i].split("|")[1].split()[0]
                except:
                    char = "?"
                    print("ERROR CHAR", bsplt[i]) 
                try:
                    loc = bsplt[i].split("|")[2].strip()
                except: 
                    loc = "?"
                if self.debug > 0:
                    sys.stdout.write("Found %s in %s..."%(char, loc))
                loc_dic[char.capitalize().strip()] = loc
                        
                
        try: room = loc_dic[self.name.capitalize()]
        except: pass
            
        self.printc("%s is in %s at %s"%(self.name, room,area))
        self.loc_dic = loc_dic
        self.location = room
        self.exits = exits
        self.area = area
        self.roomitems = roomitems


    def check_disarm(self,ln):
        
        if "DISARMS" in ln:
            print("DISARMED!", ln)
            weapon = ln.split("DISARMS your ")[-1].split("!")[0]
            if weapon in self.weapons:
                weaponname = self.weapons[weapon]
                self.rod.write("get %s\nwear %s\n"%(weaponname,weaponname))
            else:
                sys.stdout.write("Could not pick up %s!!\n"%weapon)

        #elif "you." in ln or "you!" in ln:
        #    for k in self.flee:
        #        if k in ln:
        #            self.rod.write("flee\nquit\n")
                        
    def check_hunger(self,ln):
        if ("You are STARVING!" in ln
            or "You are hungry." in ln
            or "You are a mite peckish." in ln
            or "You are a mite peckish." in ln
            or "You are famished." in ln):
            
            self.rod.write("eat turkey %s\n"%self.container)
    
        return

    def check_spells(self):
        self.check_affect()
        if self.clericon:
            if "sanctuary" not in self.aff:
                self.cleric.rod.write("cast sanc %s\ntrance\n"%self.name)
                if "fly" not in self.aff:
                    self.check_affectby()
                    if "flying" not in self.affby:
                        self.cleric.rod.write("cast fly %s\ntrance\n"%self.name)
            if "curse" in self.aff:
                self.cleric.rod.write("cast 'remove curse' %s\ntrance\n"%self.name)
            if "poison" in self.aff:
                self.cleric.rod.write("cast 'cure poison' %s\ntrance\n"%self.name)
            if "blindness" in self.aff:
                self.cleric.rod.write("cast 'cure blindness' %s\ntrance\n"%self.name)

        if self.master != None:
            if self.master.clericon:
                if "sanctuary" not in self.aff:
                    self.master.cleric.rod.write("cast sanc %s\ntrance\n"%self.name)
                    if "fly" not in self.aff:
                        self.master.cleric.rod.write("cast fly %s\ntrance\n"%self.name)
                if "curse" in self.aff:
                    self.cleric.rod.write("cast 'remove curse' %s\ntrance\n"%self.name)