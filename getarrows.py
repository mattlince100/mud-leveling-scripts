from telnetlib_compat import Telnet
import time
import sys
import threading
from threading import Thread
import random
import os

class ROD():
    
    def __init__(self, user, pw, container, function, support = None,  take_input_bool = False):


        # weapons and their keywords for disarm checks
        
        self.weapons = {"crude wooden club":"club",
                        "oar": "oar",
                        'chipped hammer':"hammer",
                        "bone blade":"blade",
                        "fishing pole cut from thick reed": "pole",
                        "T-handled blade": "t",
                        "bat claw":'claw',
                        "Dragon Claw of Legend":"claw",
                        "poniard of glory":"poniard",
                        "pair of sai":"sai",
                        'eel skin whip': 'whip',
                        'knobby club': 'club',
                        "brunhilde's spear": "spear",
                        "osprey talon":"talon"
                        
        }
        self.color = "white"
        self.ROD = ROD
        self.pickle = pickle
        self.name = user.capitalize()
        self.time = time
        self.sys = sys
        self.random = random
        self.restart = False
        self.clericon = False
        self.stop = False
        self.ready = False
        self.eqdam = True
        self.support = None
        self.master = None

        self.user_input = None
        self.take_input_bool = take_input_bool
        self.debug = 0
        self.container = container
        self.status = "continue"
        self.disarm = False

        self.goingback = False
        
        try:
            self.alt_info = pickle.load(open("alts/info_%s.pckle"%user,'r'))
        except:
            self.alt_info = {}
        
        
        if True:
            self.rod = Telnet("realmsofdespair.com",4000)


            #create character if does not exist
            self.rod.write("%s\n"%user)
            self.time.sleep(2)
            self.buf = self.read()
            print "\n%s: %s"%(self.name,self.buf)
            
            if "That character is already connected - try again in a few minutes." in self.buf:
                self.quit()
            else:
                self.rod.write("%s\n\n \n \nconfig -ansi\nconfig +autosac\nconfig -autoloot\nwake\nconfig +gag\n"%(pw))

            self.whereami()
            ntries = 5
            if len(self.loc_dic) == 1:
                tries = 0
                while tries < ntries:
                    tries += 1
                    self.rod.write("search\n")
                    while True:
                        r = self.read()
                        time.sleep(1)
                        if r.strip() != "":
                            print r, tries
                        if "You find nothing." in r:
                            break
                        elif "Your search reveals" in r:
                            self.rod.write("get all\nput arrow basket\n")
                            tries = ntries
                            break
                self.rod.write("e\nn\nne\ne\n")
                tries = 0
                while tries < ntries:
                    tries += 1
                    self.rod.write("search\n")
                    while True:
                        r = self.read()
                        time.sleep(1)
                        if r.strip() != "":
                            print r, tries
                        if "You find nothing." in r:
                            break
                        elif "Your search reveals" in r:
                            self.rod.write("get all\nput arrow basket\n")
                            tries = ntries
                            break
                
                self.rod.write("w\nsw\ns\ne\n")
                tries = 0
                while tries < ntries:
                    tries += 1
                    self.rod.write("search\n")
                    while True:
                        r = self.read()
                        time.sleep(1)
                        if r.strip() != "":
                            print r, tries
                        if "You find nothing." in r:
                            break
                        elif "Your search reveals" in r:
                            self.rod.write("get all\nput arrow basket\n")
                            tries = ntries
                            break
                self.rod.write("w\nw\n")
                self.waitcmd("exa basket",p=True)
            self.quit()

            


    def take_input(self):
        while True:
            self.user_input = raw_input('--\n')
            time.sleep(0.2)
    

    def fight(self):        
        r = self.read()

    def waitcmd(self,cmd, p = False):
        self.time.sleep(0.1)
        r = self.read()
        #self.printc(self.name+":" +cmd,'blue')
        if p:
            self.sys.stdout.write(r)

        self.rod.write("%s\nver\n"%cmd)
        self.time.sleep(0.1)
        r = ''
        start = self.time.time()
        while  True:
            r += self.read()
            if "SMAUG 2.6" in r:
                break
            t = time.time()-start
            if t > 20:
                break
            self.time.sleep(0.5)
        
        rflush = self.read()
        #self.printc(self.name+" did " +cmd.replace("\n",";") + " in %f seconds, read %d chars."%(t,len(rflush)),'blue')
        
        if p:
            self.printc(r)
        return r

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
            try: self.check_affect_main(p)
            except:
                N += 1
                print "ERROR IN check_affect"
            else:
                return

    def check_affect_main(self, p = False):
        
        aff = {}
        r = self.waitcmd("score", p)
            
        bsplt = r.split('\n')
        scan = False
        spells = []
        for i in range(len(bsplt)):
            self.check_disarm(bsplt[i])
            if "SMAUG 2.6" in bsplt: continue

            if "Class: " in bsplt[i]:
                self.charclass = bsplt[i].split("Class: ")[-1].split()[0]

            if "LEVEL: " in bsplt[i]:
                self.level = int(bsplt[i].split("LEVEL: ")[-1].split()[0])
            if "Gold :" in bsplt[i]:
                try: self.gold = int(bsplt[i].split("Gold : ")[-1].split()[0].replace(",",""))
                except: self.gold = 500000
            if "Hitpoints:" in bsplt[i]:
                tmpHP, tmpMHP = bsplt[i].split("Hitpoints:")[-1].split("of")
                self.HP = int(tmpHP.strip())
                self.MAXHP = int(tmpMHP.strip().split()[0])
                        
            if "Move:" in bsplt[i]:
                tmpMV, tmpMMV = bsplt[i].split("Move:")[-1].split("of")
                self.MV = int(tmpMV.strip())
                        
            for stat in ["STR", "CON", "WIS", "INT"]:
                if "[" not in bsplt[i] and stat in bsplt[i] and ":":
                    #print "DEBUG:", bsplt[i]
                    try: self.stats[stat] = int(bsplt[i].split("(")[0].split(":")[1].strip())
                    except:
                        pass
                    

            if "AFFECT DATA:" in bsplt[i]:
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
                    print spellname.strip()+ " not in spells"
                    self.check_affect_main(p)
                    continue
                    
        self.aff = aff
        self.printc("%s %s level %d"%(self.name, self.charclass, self.level)+'\n'
                    +" ".join(["%s:%d"%(x,self.stats[x]) for x in self.stats if x in ['STR', "CON", "WIS"]]) +'\n'
                    +" ".join(["%s (%d)"%(x,self.aff[x]) for x in self.aff if x in ['sanctuary','fly','trollish vi']]),'gold')
        
        


    def check_cont(self, container, p = False):
        
        r = self.waitcmd("examine my.%s"%container, p)

        if "You do not see that here." in r:
            self.containers[container] = []
            return
        else:
            bsplt = r.split('\n')
            scan = False
            cont = {}
            for i in range(len(bsplt)):
                if "contains" in bsplt[i]:
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
                    print "ERROR CHAR", bsplt[i] 
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



    def main_loop(self):
        try:
            self.main_loop2()
        except EOFError:
            self.sys.stdout.write("\n\n********CONNECTION CLOSED FOR %s*********\n\n"%self.name)
            self.quit()
        except IndexError:
            self.sys.stdout.write("Index error, restarting %s"%self.name)
            self.quit()
            self.status = "restart"
        #except:
        #    self.quit()
        #    self.status = "restart"

        #except error:
        #    print("Unexpected error:", sys.exc_info()[0], self.name)
        #    self.status = "restart"
        #    self.stop = True
        #except:                                                                                                                       
        #    print("Unexpected error:", sys.exc_info()[0], self.name)
        #    if self.name == "Kaeval":
        #         del self
        #    else:
        #        self.clericon = False
        #        self.status = "restart"
        
        pickle.dump(self.alt_info, open("alts/info_%s.pckle"%self.name,'w'))
            
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
                #if t < 2:
                #    self.sys.stdout.write(self.bufln)
                for ln in self.bufln.split("\n"):
                    if ln.strip() == "": continue
                    if self.fight:
                        self.printc(ln.strip())
                    #print "***", [ln.strip()], self.fight
                    if "PROMPT:" in ln:
                        try: 
                            self.HP, self.MAXHP = ln.split()[1][:-2].split("/")
                            self.MP, self.MAXMP = ln.split()[2][:-2].split("/")
                            self.MV = int(ln.split("MV")[0].split()[-1])
                            self.XP = int(ln.split("xp")[0].split()[-1].replace(",",''))
                        except:
                            self.printc("Error reading prompt...")

                        if self.MV < 100:
                            if self.clericon:
                                self.cleric.rod.write("c 'refresh' %s"%self.name)


                        self.cleric_heal()

                        if self.lastXP == None:
                            try: self.lastXP = self.XP
                            except: self.lastXP = 0

                        if "FPROMPT:" in ln:
                            self.fight = True
                        else:
                            if int(self.MP) < int(self.MAXMP)*0.7:
                                if 'chest' in self.containers:
                                    if "a glowing blue potion" in self.containers['chest']:
                                        self.rod.write("q blue chest\n")
                            self.fight = False
                            cspring = False
                            makespring = False
                    if "You wish that your wounds would stop BLEEDING so much!" in ln:
                        self.rod.write("flee\nquit\n")
                        self.status = "restart"
                        
                    if "Your opponent is not wielding a weapon" in ln:
                        self.disarm = False
                    if "Your stomach cannot contain any more." in ln:
                        # try to drink and/or make spring
                        self.rod.write("drink\n")
                        if int(self.HP) < int(self.MAXHP)*0.4:
                            self.rod.write("flee\nquit\n")
                            #self.status = "restart"
                        if cspring == False:
                            makespring = True
                        else:
                            makespring = False

                    if "Drink what?" in ln and makespring:
                        self.printc("Try to create spring...\n")
                        if self.clericon:
                            self.cleric.rod.write("cast 'create spring'\ntrance\n")
                            
                        if self.charclass != "Barbarian":
                            cspring = True
                            print("get icicle chest\nremove %s\nwear icicle\nbrandish\nremove icicle\nput icicle chest\nwear %s\ndr\n"%(self.weaponkey, self.weaponkey))
                            self.rod.write("get icicle chest\nremove %s\nwear icicle\nbrandish\nremove icicle\nput icicle chest\nwear %s\ndr\n"%(self.weaponkey,self.weaponkey))
                    
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
                    self.func = self.funcdic[nextfunc]
                ####
                
                self.bufln = ''
                self.start = time.time()
            elif t > 1.2*60:
                self.printc("Long time without action (%s, %s)... stopping"%(self.name, str(t)))
                self.quit()
                self.status = "restart"
            
            if self.user_input != None:
                self.rod.write(self.user_input+'\n')
                self.user_input = None

            time.sleep(.2)

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

        if not self.fight:
            r = self.waitcmd(direction, p)
        else:
            r = self.waitcmd("strike",p)

        for l in r.split("\n"):
            self.check_disarm(l)
            self.check_hunger(l)
            
        if "Alas, you cannot go that way." in r:
            return -1
        elif "Exits: " in r:
            self.location = None
            self.exits = []
            return 1
        elif "No way!  You are still fighting!" in r or self.fight:
            if self.random.random() < 0.1:
                self.check_affect(p=False)
                self.sys.stdout.write("Fighting... \n *** AFF ***" + str(self.aff))
                self.check_spells()

            for l in r.split("\n"):
                self.check_disarm(l)
                if "PROMPT:" in l:
                    self.HP, self.MAXHP = l.strip().split()[1][:-2].split("/")
                    self.MP, self.MAXMP = l.strip().split()[2][:-2].split("/")
                    self.sys.stdout.write(r)

                    self.cleric_heal()

                    if int(self.HP) < int(self.MAXHP)*0.4:
                        self.rod.write("flee\nquit\n")
                        self.status = "restart"
                    elif int(self.HP) < int(self.MAXHP)*0.7:
                        self.rod.write("quaff purple %s\n"%self.container)
                    
                if "Your stomach cannot contain any more." in l:
                    self.rod.write('drink\n')

                if "Drink what?" in l:
                    if self.clericon:
                        self.cleric.rod.write("cast 'create spring' %s\ntrance\n"%self.name)
                
                if int(self.HP) < int(self.MAXHP)*0.4:
                    self.rod.write("flee\nquit\n")
                    self.status = "restart"
            self.start = time.time()
            return 2
        elif "look" in direction or "open" in direction or "enter" in direction:
            return 1
        elif "is closed." in r:
            self.rod.write("get key\nunlock %s\ndrop key\nopen %s\nver\n"%(direction, direction))
            r = ''
            while True:
                ln = self.read()
                r += ln
                self.check_disarm(ln)
                if "SMAUG" in r:
                    sys.stdout.write(r)
                    if "You unlock" in r:
                        return 0
                    else:
                        return -1
        elif "You'd need a boat to go there." in r or "You'd need to fly to go there." in r:
            return -2
        
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
        directions = self.parsedir(directions)
        sys.stdout.write("\nMoving %s\n"%(";".join(directions)))
        i = 0
        Nloop = 0
        L = len(directions)
        while len(directions) > i and Nloop < L+10:
            Nloop += 1

            if Nloop % 10 == 0:
                self.get_loc()
                if self.clericon:
                    self.cleric.get_loc()

            direct = directions[i]

            if self.fight:
                pass

            if self.support != None:
                if self.support.fight and not self.fight:
                    self.time.sleep(1)
                    continue
            if i == len(directions)-1:
                movestatus = self.move(direct, True)
            else:
                movestatus = self.move(direct, p)
            
            if movestatus == 1:
                # success                                                           
                i += 1
            elif movestatus == 0:
                pass
            elif movestatus == -1:
                self.printc("\n%s: Cannot move that way (%s)...\n"%(self.name, direct))
                if force:
                    i += 1
                else:
                    return
            elif movestatus == -2:
                return
            elif movestatus == 2: #fighting
                Nloop -= 1
                pass
            self.time.sleep(0.1)
        return

    def func(self):
        return

    def func_none(self):
        return
    
    def check_disarm(self,ln):
        
        if "DISARMS" in ln:
            print "DISARMED!", ln
            weapon = ln.split("DISARMS your ")[-1].split("!")[0]
            if weapon in self.weapons:
                weaponname = self.weapons[weapon]
                self.rod.write("get %s\nwear %s\n"%(weaponname,weaponname))
            else:
                sys.stdout.write("Could not pick up %s!!\n"%weapon)

        elif "you." in ln or "you!" in ln:
            for k in self.flee:
                if k in ln:
                    self.rod.write("flee\nquit\n")
                        
    def check_hunger(self,ln):
        if ("You are STARVING!" in ln
            or "You are hungry." in ln
            or "You are a mite peckish." in ln
            or "You are a mite peckish." in ln
            or "You are famished." in ln):
            
            self.rod.write("eat turkey %s\n"%self.container)
    
        return

    def cleric_heal(self):

        if not self.clericon:
            return
        
        #if self.cleric.location != self.location:
        #    if int(self.HP) < int(self.MAXHP)*0.7:
        #        self.cleric.rod.write("cast 'uplift' %s\ntrance\n"%self.name)
        #    return

        if int(self.HP) < int(self.MAXHP)*0.5:
            if self.clericon:
                self.cleric.rod.write("cast 'heal' %s\ntrance\n"%self.name)
            if self.master != None:
                if self.master.clericon:
                    self.master.cleric.rod.write("cast 'heal' %s\ntrance\n"%self.name)
        elif int(self.HP) < int(self.MAXHP)*0.7:
            self.cleric.rod.write("cast 'cure critical' %s\ntrance\n"%self.name)


        elif int(self.HP) < int(self.MAXHP)*0.8 and int(self.cleric.MP) > 500:
            
            if self.cleric.location== "The Foothills":
                self.cleric.rod.write("cast 'uplift' %s\ntrance\n"%self.name)
            else:
                self.cleric.rod.write("cast 'cure critical' %s\ntrance\n"%self.name)
        elif int(self.HP) < int(self.MAXHP)*0.9 and int(self.cleric.MP) > 900:
            if self.cleric.location== "The Foothills":
                self.cleric.rod.write("cast 'uplift' %s\ntrance\n"%self.name)
            else:
                self.cleric.rod.write("cast 'cure critical' %s\ntrance\n"%self.name)
        
                
        if int(self.MV) < 100:
             self.cleric.rod.write("cast 'refresh' %s\ntrance\n"%self.name)

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

    def func_fight(self):
        
        if self.lag == 0:
            if self.random.random() < 0.3:
                self.check_spells()

            if int(self.HP) <  int(self.MAXHP)*0.4:
                self.rod.write("flee\nquit\n")

            self.cleric_heal()

            if int(self.HP) < int(self.MAXHP)*0.8:
                if self.level <= 7:
                    self.pot = "maroon"
                else:
                    self.pot = "purple"
                self.rod.write("quaff %s %s\n"%(self.pot, self.container))
                self.lag = 1
            else:
                if self.disarm:
                    self.rod.write("disarm\n")
                else:
                    spell = self.find_attack()
                
                    if self.charclass == "Cleric" and "celestial might" not in self.aff and self.attack == 'surestrike' and int(self.MP) > 16:
                        self.rod.write("cast 'celestial might'\n")

                    if int(self.MP) > 30 or ( int(self.MP) > 8 and self.charclass == "Vampire"):
                        if spell != None:
                            self.printc(spell)
                            self.rod.write(spell+'\n')
                        else:
                            self.rod.write("%s\n"%self.attack)
                            self.printc(self.attack)
                    else:
                        
                        if spell != None and self.charclass in ['Mage',"Augurer", "Nephandi", "Cleric","Fathomer"]:
                            if self.charclass == "Fathomer":
                               if self.random.random() < 0.3: 
                                   self.rod.write("q blue chest\n")
                            else:
                                if self.random.random() < 0.7:
                                   self.rod.write("q blue chest\n")

                        

                        self.printc(self.attack)
                        self.rod.write("%s\n"%self.attack)
                self.lag = 1
                
        self.rod.write("ver\n")
        return



    def find_attack(self):
        try: 
            return self.find_attack_main()
        except:
            self.printc("%s: Find_attack has a problem..."%self.name)
            return None

    def find_attack_main(self):
        ''' finds attack based on slist '''
        mage = ["black hand",
               "galvanic whip",
               "colour spray",
               "spectral furor",
               "sulfurous spray",
               "caustic fount",      # Priority spell - best damage for leveling
               "sonic resonance",
               "black fist",
               "ethereal fist",
               "magnetic thrust",
               "acetum primus"]

        augurer = ["shocking grasp",'scorching surge','spiral blast']
        thief = ["circle"]
        warrior = ["smash"]
        vampire = ['chill touch', 
                   'shocking grasp',
                   ]
        cleric = ['necromantic touch']

        fathomer = ['water spout','diminue geysir','isfundere']

        spells = []
        if self.charclass == "Mage":
            for x in self.slist:
                if x[0] in mage and x[1] != '0':
                    spells.append(x[0])
            if len(spells) >= 2:
                spell = spells[-2]
            elif len(spells) == 1:
                spell = spells[0]
            else:
                return None
            return "cast '%s'"%spell
        elif self.charclass == "Fathomer":
            for x in self.slist:
                if x[0] in fathomer and x[1] != '0':
                    spells.append(x[0])
            if len(spells) > 0:
                spell = spells[-1]
            else:
                return None
            return "cast '%s'"%spell
        elif self.charclass == "Cleric":
            for x in self.slist:
                if x[0] in cleric and x[1] != '0':
                    spells.append(x[0])
            if len(spells) > 0:
                spell = spells[-1]
            else:
                return None
            return "cast '%s'"%spell
        elif self.charclass == "Vampire":
            for x in self.slist:
                if x[0] in vampire and x[1] != '0':
                    spells.append(x[0])
            if len(spells) >= 1:
                spell = spells[-1]
            elif len(spells) == 1:
                spell = spells[0]
            else:
                return None
            return "cast '%s'"%spell

        elif self.charclass == "Augurer":
            for x in self.slist:
                if x[0] in augurer and x[1] != '0':
                    spells.append(x[0])
            
            if len(spells) > 0:
                spell = spells[-1]
            else:
                return None
            return "cast '%s'"%spell

        elif self.charclass == "Thief":
            for x in self.slist:
                if x[0] in thief and x[1] != '0':
                    spells.append(x[0])
            #print "SLIST LEN", self.slist
            use = spells[-1]
            if use in ['circle'] and self.target != None:
                return spells[-1]+ " "+self.target


        elif self.charclass == "Warrior":
            for x in self.slist:
                if x[0] in warrior and x[1] != '0':
                    spells.append(x[0])
            use = spells[-1]
        return None

    def godh(self, loc = "dhsquare"):

        if self.goingback:
            return 
        else:
            self.goingback = True

        if self.fight:
            self.printc("Fighting: %s can't go back to DH %s\n"%(self.name, loc))
            return

        if self.clericon:
            if self.cleric.fight:
                self.printc("Cleric fighting: %s can't go back to DH %s\n"%(self.name, loc))
                return

        if self.support != None:
            if self.support.fight:
                self.printc("Support fighting: %s can't go back to DH %s\n"%(self.name, loc))
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
                if self.charclass == "Barbarian":
                    self.rod.write("inv\nshatter recall\nget recall my.chest\n")
                    self.time.sleep(2)
                    self.go("w;n;n;nw;w;n;nw;n;w")
                    self.time.sleep(2.5)
                    self.rod.write("buy recall\nput recall my.chest\ne\nn\nn\nsay I wish to visit the city dwellers\ns\ndr\n")
                    self.time.sleep(2.5)
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
                        self.rod.write("recite scroll\nget recall my.chest\ns\ndr\n")
                    self.time.sleep(2.5)
        elif loc == "recall":
            if self.location == "Thoth's Rune on Vertic Avenue":
                pass
            elif  self.location == "Darkhaven Square":
                self.go("n")
            else:
                if self.charclass == "Barbarian":
                    self.rod.write("inv\nshatter recall\nget recall my.chest\n")
                    self.time.sleep(1.5)
                    self.go("w;n;n;nw;w;n;nw;n;w")
                    self.time.sleep(2)
                    self.rod.write("buy recall\nput recall my.chest\ne\nn\nn\nsay I wish to visit the city dwellers\n")
                    self.time.sleep(2)
                else:
                    self.rod.write("recite scroll\nget recall my.chest\n")
                    if self.name in ["Kaeval", "Lemaitre"]:
                        self.rod.write("c word\n")
                    else:
                        self.time.sleep(2.5)

        self.goingback = False

    def read(self):
        '''' read everywhere goes here '''
        r = self.rod.read_very_eager()
        #if self.name == "Kaeval":
        #    if len(r.strip()) > 0:
        #        self.printc(r,'blue')
        rln = r.split('\n')

        if len(rln) >= 1:
            if rln[0].strip() != "":
                #print rln[0]
                self.start = time.time()
                self.N = 0

        for i in range(len(rln)):            


            if "starved" in rln[i] or "You are mite peckish" in rln[i] or "You are STARVING!" in rln[i]:
                self.rod.write("eat turkey chest\n")

            if "..Everything begins to fade to black." in rln[i]:
                # I died
                self.quit()
                self.status = "quit"
            if "You come out of your trance." in rln[i]:
                self.trancing = False
            if "You enter a peaceful trance, collecting mana from the cosmos." in rln[i]:
                self.trancing = True

            if "You follow" in rln[i]:
                self.trancing = False
                self.location = None
                self.following = True

            if "You now follow" in rln[i]:
                self.following = True

            if "They aren't here." in rln[i] or "You can't circle" in rln[i]:
                self.target = None

            if "gets damaged" in rln[i]:
                self.eqdam = True

            if "tells you '" in rln[i]:
                self.printc(rln[i])
                if "Destre" in rln[i]:
                    self.time.sleep(1000000)
                if  rln[i].strip().split()[0] not in ["Sigvald", "Anihprom", "Adnai","The", "A"]:
                    self.emergency_quit()
                    self.status = "restart"

            if "yells '" in rln[i]:
                if "The Royal Herald yells" in rln[i]:
                    pass
                else:
                    self.time.sleep(20)
                    self.godh()
                    if self.clericon:
                        self.cleric.godh()

            if ("The corpse of" in rln[i] and "holds" in rln[i]):
                thismob = rln[i].split("The corpse of ")[-1].split(" holds")[0]

                #print self.alt_info['kills']


            if "Your gain is:" in rln[i]:
                self.logfile.write(rln[i]+'\n')
                self.logfile.flush()

            if "is DEAD!!" in rln[i] and i < len(rln) -1:
                self.status_msg = "Waiting for kill to register"
                #self.check_spells()

                thismob = rln[i].split('is')[0].strip()
                if self.lastXP != None:
                    XPgain = self.lastXP-self.XP
                    if XPgain < 0:
                        XPgain = self.lastXP
                    self.printc("%s: Mob %s gave me total %.2fK XP"%(self.name,thismob,XPgain/1000.0),'gold')
                    self.logfile.write("%s: %s %s %s %s %.2fK/%.2fK XP\n"%(time.ctime(),self.name,self.charclass,self.level,thismob,XPgain/1000.0, self.XP/1000.0))
                    self.logfile.flush()

                if "kills" not in self.alt_info:
                    self.alt_info["kills"] = {}
                if thismob in self.alt_info['kills']:
                    self.alt_info['kills'][thismob] = self.alt_info['kills'][thismob] + 1
                else:
                    self.alt_info['kills'][thismob] = 1
                self.printc("%s: Killing blow %s (%d)"%(self.name, thismob, self.alt_info['kills'][thismob]),'gold')

                self.pickle.dump(self.alt_info, open("alts/info_%s.pckle"%self.name,'w'))
                print self.alt_info['kills']

                self.lastmob = thismob
                try: self.lastXP = self.XP
                except: continue

        return r



    def buyblue(self):
        tmp = self.ROD("Salamon","Elijah","chest",'none')
        if self.charclass == "Fathomer":
            self.waitcmd("give 200k coin salamon\nvis")

            r = tmp.waitcmd("buy 20 blue\ngive bag %s"%self.name)
            self.printc(r,"red")
            try: tmp.rod.write("give %d coin %s\n"%(tmp.gold, self.name))
            except: pass
            self.waitcmd("empty bag chest\ndrop bag\n")

            tmp.quit()
        else:
            r = ''
            self.waitcmd("give 500k coin salamon\nvis")
        
            r = tmp.waitcmd("buy 50 blue\ngive bag %s"%self.name)
            self.printc(r,"red")
            try: tmp.rod.write("give %d coin %s\n"%(tmp.gold, self.name))
            except: pass
            self.waitcmd("empty bag chest\ndrop bag\n")
        
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


    def check_cleric(self):
        try:
            self.cleric.get_loc()
        except:
            return False
        else:
            return self.cleric.location

    def log_cleric(self):
        if self.master != None:
            return 
        
        #self.cleric = self.ROD("Kaeval","1q2w3e4r","basket", "cleric")
        self.cleric = self.ROD(sys.argv[2],"1q2w3e4r","basket", "cleric")
        self.clericon = True
        if self.support!= None:
            self.support.cleric = self.cleric
            self.support.clericon = True
        return

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

    def cleric_follow(self):
        if self.master != None:
            return True
        Ntries = 0
        self.cleric.get_loc()
        if self.cleric.location != "Darkhaven Square":
            self.cleric.godh()
        
        while not self.cleric.following:
            self.printc("Try to follow... %d"%Ntries,'gold')
            Ntries += 1
            self.get_loc()
            self.cleric.get_loc()
            self.time.sleep(2)
            print self.location, self.cleric.location
            if self.location == "Darkhaven Square" and self.cleric.location == "Darkhaven Square":
                r = self.cleric.waitcmd("follow %s"%self.name)
                self.printc("Following try: %d"%Ntries,'gold')
                self.printc(r,'gold')
                if "You now follow" in r:
                    self.cleric.following = True
                    return True
            elif self.cleric.location != "Darkhaven Square":
                self.cleric.godh()
            elif self.location != "Darkhaven Square":
                self.godh()
            self.time.sleep(1)
            if Ntries >= 4:
                return False
        return True

    def quit(self, action = 'quit'):
        try:
            self.rod.write("%s\n"%action)
        except:
            self.printc("%s quit -- write failed"%self.name)
        try:
            self.stop =True
        except:
            self.printc("%s quit -- stop failed"%self.name)

        if self.clericon:
            try:
                self.cleric.stop =True
            except:
                self.printc("%s quit -- stop for cleric failed"%self.name)

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREY = '\033[91m'
    WHITE = '\033[97m'
    GREEN = '\033[92m'
    RED = '\033[31;42m'
    CYAN = '\u001b[36m'
    MAGENTA = '\033[35m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    PINK = '\033[38;5;206m'
    
def printc(text, color = None):
    if color == "gold":
        color = bcolors.WARNING
    elif color == None:
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
    else:
        color = ""
    sys.stdout.write(color + text + bcolors.ENDC+'\n')

if __name__ == "__main__":
    support = None
    import sys
    maxtime = 60*24 #24 hours
    maxtime = 60*5
    target_level = 60
    user, pw, container = "Kaerim", "1q2w3e4r", "chest"
    user, pw, container = "lasonas", "yaoyao2020", "chest"
    
    import time
    import pickle
    

    start = time.time()
    month,date =time.ctime().split()[1:3]
    year = time.ctime().split()[-1]

    
    status, N = "restart", 0
    last_status = None
    while True:
        try:
            rod = ROD(user,pw,container,'dhaven')
        except EOFError:
            pass
        N = 90
        for i in range(N):
            print "sleeping (%d/%d minutes)"%(i,N)
            time.sleep(60)
        
    exit()


