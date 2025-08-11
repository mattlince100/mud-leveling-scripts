import telnetlib, time
import sys
import threading
from threading import Thread
import random
import os
from level import dhaven
from level import Starting
from level import Cleric
from level import Support
from tom import Tom
from tol import Tree
from winterlight import Winter
from canyon import Canyon
from gnome import Gnome
from coral import Coral
from artgallery import Art
from sunless import Sunless
from mith import Mithril
from toz import Toz
from king import King
from shire import Shire

class ROD(dhaven, Gnome, Sunless, Starting, Cleric, Coral, Art, Toz, Mithril, Support, Tom, Canyon, Winter, Tree, King, Shire):
    
    def write_to_telnet(self, connection, text):
        """Helper to write text to telnet connection with proper encoding"""
        if isinstance(text, str):
            connection.write(text.encode('ascii'))
        else:
            connection.write(text)
        
    def __init__(self, user, pw, container, function, support = None,  take_input_bool = False):


        # weapons and their keywords for disarm checks
        
        self.weapons = {
            
                        "Nasr, Claymore of Sovereignty":"Nasr",
                        "Dragon Claw of Legend":"claw",
                        "oar":"oar",
                        "chipped hammer": "chipped",
                        "pair of sai":"sai",
                        "crude wooden club":"club",
                        "Black Dragonskull Ax":"ax",
                        "crocodile claw":"claw",
                        "Soulslayer": "soul",
                        "Black Dragonskull Ax":"ax",
                        "bone blade":"blade",
                        "fishing pole cut from thick reed":"pole",
                        "poniard of glory":"poniard",
                        "bat claw":"claw",
                        "leatherworker's awl":"awl",
                        "amazon spear":"spear",
                        "katana":"katana",
                        "Shock Whip":"whip",
                        
        }

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
        self.funcdic = {"dhaven":self.func_dhaven, 
                        "gnome": self.func_gnome, 
                        "exit": exit, 
                        "sunless":self.func_sunless, 
                        "starting": self.func_starting, 
                        "cleric": self.func_cleric,
                        "coral":self.func_coral,
                        "art":self.func_art,
                        "toz":self.func_toz,
                        "mith":self.func_mith,
                        "support": self.func_support,
                        "tom": self.func_tom,
                        "canyon":self.func_canyon,
                        "winter":self.func_winter,
                        "none":self.func_none,
                        "tree":self.func_tree,
                        "king":self.func_king,
                        "shire":self.func_shire,
                        }

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
            self.alt_info = pickle.load(open("alts/info_%s.pckle"%self.name,'rb'))
        except:
            self.alt_info = {}
        
        
        if True:
            self.rod = telnetlib.Telnet("realmsofdespair.com",4000)
            
            # Monkey patch the write method to handle string encoding
            original_write = self.rod.write
            def write_with_encoding(text):
                if isinstance(text, str):
                    original_write(text.encode('ascii'))
                else:
                    original_write(text)
            self.rod.write = write_with_encoding


            #create character if does not exist
            self.rod.write("%s\n"%user)
            self.time.sleep(2)
            self.buf = self.read()
            print("\n%s: %s"%(self.name,self.buf))
            if "No such player exists." in self.buf:
                #create alt
                self.rod.write("new\n%s\ny\n%s\n%s\nn\nbarb\nhalf-orc\nfemale\nn\n\n\nhelp start\n"%(user,pw,pw))
                function = "sunless"
            elif "That character is already connected - try again in a few minutes." in self.buf:
                self.quit()
            else:
                self.rod.write("%s\n\n \n \nconfig -ansi\nconfig +autosac\nconfig -autoloot\nwake\nconfig +gag\n"%(pw))


            
            self.mudtime = None

            self.phase = 0
            self.switch = 0

            self.color = "white"

            # locations
            self.location = None
            self.exits = []
            self.area = []
            self.roomitems = []
            self.loc_dic = {}
            
            ##

            self.HP = 0
            self.MAXHP = 0
            self.MP = 0
            self.MAXMP = 0
            self.MV = 0
            
            # fight
        
            self.fight = False
            self.attack = "strike"
            self.usespell = True
            self.lag = 0
            self.flee = []
            self.weapon = "Unknown"
            self.target = None
            self.trancing = False
            self.nofeed = False
            ##

            # misc
            self.aff = {}
            self.affby = []
            self.stats = {}
            self.inv = {}
            self.containers = {}
            self.gold = None
            self.eq = {}
            self.sect_member = False  # Track sect membership status
            self.level = 0
            self.prestige = False
            
            # Check if previously joined sect
            try:
                self.alt_info = self.pickle.load(open("alts/info_%s.pckle"%self.name,'r'))
                if "sect_member" in self.alt_info:
                    self.sect_member = self.alt_info["sect_member"]
            except:
                pass

            # log
            self.lastmob = None
            self.lastXP = None
            self.kills = {}
            self.kill_xp = {}
            
            self.status_msg = "login"

            self.func = self.funcdic[function]
            self.buf = ''
            self.bufln = ''
            
            self.charclass = None
            self.sys.stdout.write('\n'+"*"*30+" [STARTING UP %s"%self.name+"] "+"*"*30+'\n')
            
            # Give time for login to complete
            self.time.sleep(3)
            self.whereami()
            
            self.check_affect()
            self.check_prac()
            self.check_eq()
            self.time.sleep(2)
            
            if self.charclass == "Vampire":
                self.rod.write("prompt PROMPT: %h/%HHP &C%b/%BMP &G%vMV&w &p%Xxp %gg%l\n")
                self.rod.write("fprompt FPROMPT: %h/%HHP &C%b/%BMP &G%vMV&w &p%Xxp %c%l\n")
                self.attack = "feed"
                
            else:
                self.rod.write("prompt PROMPT: %h/%HHP &C%m/%MMP &G%vMV&w &p%Xxp %gg%l\n")
                self.rod.write("fprompt FPROMPT: %h/%HHP &C%m/%MMP &G%vMV&w &p%Xxp %c%l\n")
                if self.charclass == "Mage" and self.level > 20:
                    self.container = 'my.extrad'  # Use extradimensional portal for weight reduction

            

            self.weaponkey = "?"

            for weap in self.weapons:
                if weap in self.weapon[0]:
                    self.weaponkey = self.weapons[weap] 
            self.printc("Gold: %d\nWeapon: %s (%s)\n"%(self.gold,self.weapon, self.weaponkey))

            self.check_prac()
            
            for skill, v in self.slist:
                if skill in ["kick","surestrike","spurn","cuff","pummel","lunge",'shieldbash']:
                    self.attack = skill

            self.printc("Attack: %s\n"%self.attack)
            
            self.check_time()

            self.t1 = Thread(target = self.main_loop)
            if self.take_input_bool:
                self.t2 = Thread(target = self.take_input)
                self.t2.start()
            self.t1.start()

            if support != None:
                supportname, supportpw, supportcontainer = support
                self.support = self.ROD(supportname,supportpw,supportcontainer,'dhaven')
                self.support.master = self
                print((self.support.master.name))
                self.support.color = "red"
            
            if self.name in ["Kaeval","Lemaitre"]:
                self.color = "grey"

            year = self.time.ctime().split()[-1]

            self.logfile = open("logs/log_%s_%s.txt"%(self.name,year),'a')


    def take_input(self):
        while True:
            self.user_input = input('--\n')
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
                print("ERROR IN check_affect")
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
                    print(spellname.strip()+ " not in spells")
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
                    self.printc("%s is at %s"%(self.name,self.location),'blue')
                    return
                else:
                    self.location = None

                        
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
        
        self.pickle.dump(self.alt_info, open("alts/info_%s.pckle"%self.name,'wb'))
            
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
                                self.cleric.rod.write("cast \"refresh\" %s"%self.name)


                        self.cleric_heal()

                        if self.lastXP == None:
                            try: self.lastXP = self.XP
                            except: self.lastXP = 0

                        if "FPROMPT:" in ln:
                            self.fight = True
                        else:
                            self.nofeed = False
                            if int(self.MP) < int(self.MAXMP)*0.7:
                                if self.container in self.containers:
                                    if "a glowing blue potion" in self.containers[self.container]:
                                        self.rod.write("q blue %s\n"%self.container)
                            self.fight = False
                            self.usespell = True
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
                            self.cleric.rod.write("cast \"create spring\"\ntrance\n")
                            
                        if self.charclass != "Barbarian":
                            cspring = True
                            print(("get icicle chest\nremove %s\nwear icicle\nbrandish\nremove icicle\nput icicle chest\nwear %s\ndr\n"%(self.weaponkey, self.weaponkey)))
                            self.rod.write("get icicle %s\nremove %s\nwear icicle\nbrandish\nremove icicle\nput icicle %s\nwear %s\nwear guide\ndr\n"%(self.container,self.weaponkey,self.container,self.weaponkey))
                    
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
                        self.cleric.rod.write("cast \"create spring\" %s\ntrance\n"%self.name)
                
                if int(self.HP) < int(self.MAXHP)*0.4:
                    self.rod.write("flee\nquit\n")
                    self.status = "restart"
                else:
                    self.waitcmd(self.attack)
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
            print("DISARMED!", ln)
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
                self.cleric.rod.write("\ncast \"heal\" %s\ntrance\n"%self.name)
            if self.master != None:
                if self.master.clericon:
                    self.master.cleric.rod.write("\ncast \"heal\" %s\ntrance\n"%self.name)
        elif int(self.HP) < int(self.MAXHP)*0.7:
            self.cleric.rod.write("\ncast \"cure critical\" %s\ntrance\n"%self.name)


        elif int(self.HP) < int(self.MAXHP)*0.8 and int(self.cleric.MP) > 500:
            
            if self.cleric.location== "The Foothills":
                self.cleric.rod.write("cast \"uplift\" %s\ntrance\n"%self.name)
            else:
                self.cleric.rod.write("cast \"cure critical\" %s\ntrance\n"%self.name)
        elif int(self.HP) < int(self.MAXHP)*0.9 and int(self.cleric.MP) > 900:
            if self.cleric.location== "The Foothills":
                self.cleric.rod.write("cast \"uplift\" %s\ntrance\n"%self.name)
            else:
                self.cleric.rod.write("cast \"cure critical\" %s\ntrance\n"%self.name)
        
                
        if int(self.MV) < 100:
             self.cleric.rod.write("cast \"refresh\" %s\ntrance\n"%self.name)

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
                self.cleric.rod.write("cast \"remove curse\" %s\ntrance\n"%self.name)
            if "poison" in self.aff:
                self.cleric.rod.write("cast \"cure poison\" %s\ntrance\n"%self.name)
            if "blindness" in self.aff:
                self.cleric.rod.write("cast \"cure blindness\" %s\ntrance\n"%self.name)

        if self.master != None:
            if self.master.clericon:
                if "sanctuary" not in self.aff:
                    self.master.cleric.rod.write("cast sanc %s\ntrance\n"%self.name)
                    if "fly" not in self.aff:
                        self.master.cleric.rod.write("cast fly %s\ntrance\n"%self.name)
                if "curse" in self.aff:
                    self.cleric.rod.write("cast \"remove curse\" %s\ntrance\n"%self.name)

    def func_fight(self):
        
        if self.lag == 0:
            if self.random.random() < 0.3:
                self.check_spells()

            if int(self.HP) <  int(self.MAXHP)*0.4:
                self.rod.write("flee\nquit\n")

            self.cleric_heal()

            if int(self.HP) < int(self.MAXHP)*0.8:
                
                self.pot = "purple"
                self.rod.write("quaff %s %s\n"%(self.pot, self.container))
                self.lag = 1
            else:
                if self.disarm:
                    self.rod.write("disarm\n")
                else:
                    spell = self.find_attack()
                
                    if self.charclass == "Cleric" and "celestial might" not in self.aff and self.attack == 'surestrike' and int(self.MP) > 16:
                        self.rod.write("cast \"celestial might\"\n")

                    if int(self.MP) > 30 or ( int(self.MP) > 8 and self.charclass == "Vampire"):
                        if spell != None and self.usespell:
                            self.printc(spell)
                            self.rod.write(spell+'\n')
                        else:
                            if self.nofeed:
                                self.rod.write("strike\n")
                            else:
                                self.rod.write("%s\n"%self.attack)
                                self.printc(self.attack)
                    else:
                        
                        if spell != None and self.charclass in ['Mage',"Augurer", "Nephandi", "Cleric","Fathomer"]:
                            if self.charclass == "Fathomer":
                               if self.random.random() < 0.3: 
                                   self.rod.write("q blue %s\n"%self.container)
                            else:
                                if self.random.random() < 0.7:
                                   self.rod.write("q blue %s\n"%self.container)

                        

                        self.printc(self.attack)
                        self.rod.write("%s\n"%self.attack)
                self.lag = 1
                
        self.rod.write("ver\n")
        return


    def healup(self):
        heal = "lament"
        printc("Heals: %d Purples: %d"%(self.heals, 0), 'gold')
        self.rod.write("quaff %s %s\n"%(heal, self.container))
        self.heals -= 1

    def manaup(self):
        printc("Mana: %d Nips: %d"%(self.manas, self.nips), 'gold')
        if self.pipelit:
            self.rod.write("smoke pipe\n")
        elif self.pipeempty and self.nips > 0:
            self.rod.write("empty pipe\nget nip %s\nfill pipe nip\nlight pipe\nsmoke pipe\nput nip %s\n"%(self.container,self.container))
            self.nips -= 1
            self.pipelit = True
            self.pipeempty = False
        elif self.nips > 0 and not self.pipelit:
            self.rod.write("light pipe\nsmoke pipe\n")
            self.pipelit = True
        if self.nips > 0:
            self.rod.write("smoke pipe\n")
            self.pipelit = True
        elif self.manas > 0:
            self.rod.write("quaff mana %s\n"%self.container)
            self.manas -= 1

    

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
                #"sulfurous spray",
               "sonic resonance",
               "black fist",
               "ethereal fist",
                "caustic fount",
               "magnetic thrust"]

        augurer = ["shocking grasp",'scorching surge','spiral blast']
        thief = ["circle"]
        warrior = ["smash"]
        vampire = ['chill touch', 
                   'shocking grasp',
                   ]
        cleric = ['necromantic touch']

        fathomer = ['water spout']
        nephandi = ['nihil']
        spells = []
        print([self.charclass])
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
            return "cast \"%s\""%spell
        elif self.charclass == "Nephandi":
            for x in self.slist:
                if x[0] in nephandi and x[1] != '0':
                    spells.append(x[0])
            if len(spells) == 1:
                spell = spells[-1]
            elif len(spells) >= 2:
                spell = spells[-2]
            else:
                return None
            return "cast \"%s\""%spell
        elif self.charclass == "Fathomer":
            for x in self.slist:
                if x[0] in fathomer and x[1] != '0':
                    spells.append(x[0])
            if len(spells) > 0:
                spell = spells[-1]
            else:
                return None
            return "cast \"%s\""%spell
        elif self.charclass == "Cleric":
            for x in self.slist:
                if x[0] in cleric and x[1] != '0':
                    spells.append(x[0])
            if len(spells) > 0:
                spell = spells[-1]
            else:
                return None
            return "cast \"%s\""%spell
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
            return "cast \"%s\""%spell

        elif self.charclass == "Augurer":
            for x in self.slist:
                if x[0] in augurer and x[1] != '0':
                    spells.append(x[0])
            
            if len(spells) > 0:
                spell = spells[-1]
            else:
                return None
            return "cast \"%s\""%spell

        elif self.charclass == "Thief":
            for x in self.slist:
                if x[0] in thief and x[1] != '0':
                    spells.append(x[0])
            #print "SLIST LEN", self.slist
            if len(spells) >0:
                use = spells[-1]
                if use in ['circle'] and self.target != None:
                    return spells[-1]+ " "+self.target

        elif self.charclass == "Warrior":
            for x in self.slist:
                if x[0] in warrior and x[1] != '0':
                    spells.append(x[0])
            if len(spells) >0:
                use = spells[-1]
                return use
        return None

    def godh(self, loc = "dhsquare"):

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

        self.location = None
        self.get_loc()
        
        self.printc("%s is going back to DH %s from %s\n"%(self.name, loc, self.location),'gold')
        if self.location == None:
            self.printc("%s: could not determine location\n"%(self.name))
            return
        self.trancing = False

        if loc == "dhsquare":
            if self.location == "Thoth's Rune on Vertic Avenue":
                self.go("s")
            elif self.location == "Darkhaven Square":
                pass
            else:
                # Debug: Print current location for Kaeval
                if self.name in ["Kaeval", "Lemaitre"]:
                    self.printc("KAEVAL RECALL DEBUG: Currently at '%s'" % self.location, 'red')
                if self.charclass == "Barbarian":
                    self.rod.write("inv\nshatter recall\nget recall my.chest\n")
                    self.time.sleep(2)
                    self.go("w;n;n;nw;w;n;nw;n;w")
                    self.time.sleep(2.5)
                    self.rod.write("buy recall\nput recall my.chest\ne\nn\nn\nsay I wish to visit the city dwellers\ns\ndr\n")
                    self.time.sleep(2.5)
                elif self.name in ["Kaeval","Lemaitre"]:
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
                    if self.charclass == "Cleric" and self.level == 50:
                        printc("RECALLING CLERIC %s located %s"%(self.name,self.location))
                        self.rod.write("c word\n")
                        self.time.sleep(2)
                        self.go("w;w;s;s;e;se")
                        
                    else:
                        self.rod.write("recite scroll\nget recall %s\ns\ndr\n"%self.container)
                    self.get_loc()

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
                    if self.charclass == "Cleric" and self.level == 50:
                        self.rod.write("c word\n")
                    else:
                        self.rod.write("recite scroll\nget recall %s\n"%self.container)
                    self.get_loc()
        self.goingback = False

    def read(self):

        '''' read everywhere goes here '''
        r = self.rod.read_very_eager()
        if isinstance(r, bytes):
            r = r.decode('ascii', errors='replace')
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
            if "You disarm" in rln[i]:
                self.disarm = False

            if "Your target does not have any blood to feed upon." in rln[i]:
                self.nofeed = True

            if "You cannot cast that here." in rln[i]:
                self.usespell = False
            
            # Check for sanctuary fade message
            if "The luminous aura about your body fades away." in rln[i]:
                if self.level >= 10 and self.sect_member:
                    # Check if we have sanctuary potions
                    sanctpotname = "a sanctuary potion"
                    if sanctpotname in self.containers.get(self.container, {}):
                        if self.containers[self.container][sanctpotname] > 0:
                            self.rod.write("quaff sanctuary-potion %s\n" % self.container)
                            self.printc("Sanctuary faded! Quaffing sanctuary potion...", 'gold')
                        else:
                            self.printc("Sanctuary faded and no potions available!", 'red')
                            if self.fight:
                                self.rod.write("flee\n")
                
            if "starved" in rln[i] or "You are mite peckish" in rln[i] or "You are STARVING!" in rln[i]:
                self.rod.write("eat turkey %s\n"%self.container)

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
                    #self.time.sleep(60*30)
                    self.status = "quit"

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


            

                if "clearbuffer" not in self.alt_info or "kills" not in self.alt_info:
                    try: self.alt_info = pickle.load(open("alts/info_%s.pckle"%self.name,'rb'))
                    except: pass

                    if "clearbuffer" not in self.alt_info:
                        self.alt_info['clearbuffer'] = False
                        self.alt_info['buffer'] = set()
                    
                    if "kills" not in self.alt_info:
                        self.alt_info["kills"] = {}

                if not self.alt_info["clearbuffer"]:
                    if thismob in self.alt_info['kills']:
                        self.alt_info['kills'][thismob] = self.alt_info['kills'][thismob] + 1
                    else:
                        self.alt_info['kills'][thismob] = 1
                    self.printc("%s: Killing blow %s (%d)"%(self.name, thismob, self.alt_info['kills'][thismob]),'gold')
                    
                else:
                    self.alt_info["buffer"].add(thismob)
                    printc("Clearing buffer: %d mobs"%len(self.alt_info["buffer"]),'gold')
                    

                

                self.pickle.dump(self.alt_info, open("alts/info_%s.pckle"%self.name,'wb'))
                print("Kills", self.alt_info['kills'], "Buffer", self.alt_info['buffer'])

                self.lastmob = thismob
                try: self.lastXP = self.XP
                except: continue

        return r

    def buypurple(self):
        tmp = self.ROD("Salamon","Elijah","chest",'none')
        self.waitcmd("give 50k coin salamon\nvis")
        r = tmp.waitcmd("buy 20 purple\ngive bag %s"%self.name)
        self.printc(r,"red")
        self.waitcmd("empty bag %s\ndrop bag\n"%self.container)
        tmp.quit()

    def buyblue(self):
        tmp = self.ROD("Salamon","Elijah","chest",'none')
        if self.charclass == "Fathomer":
            self.waitcmd("give 200k coin salamon\nvis")

            r = tmp.waitcmd("buy 20 blue\ngive bag %s"%self.name)
            self.printc(r,"red")
            tmp.rod.write("eat tur chest\ndr dra\n")
            try: tmp.rod.write("give 500k coin %s\n"%(self.name))
            except: pass
            
            self.waitcmd("empty bag %s\ndrop bag\n"%self.container)

            tmp.quit()
        elif self.charclass in ["Mage","Nephandi"]:
            r = ''
            self.waitcmd("give 500k coin salamon\nvis")
            self.waitcmd("give 500k coin salamon\nvis")

            tmp.rod.write("eat tur chest\ndr dra\n")
            try: tmp.rod.write("give 500k coin %s\n"%(self.name))
            except: pass

            r = tmp.waitcmd("buy 50 blue\ngive bag %s"%self.name)
            self.printc(r,"red")
            self.waitcmd("empty bag %s\ndrop bag\n"%self.container)

            r = tmp.waitcmd("buy 50 blue\ngive bag %s"%self.name)
            self.printc(r,"red")
            self.waitcmd("empty bag %s\ndrop bag\n"%self.container)

            tmp.quit()
        else:
            r = ''
            self.waitcmd("give 500k coin salamon\nvis")
        
            r = tmp.waitcmd("buy 50 blue\ngive bag %s"%self.name)
            self.printc(r,"red")
            tmp.rod.write("eat tur chest\ndr dra\n")
            try: tmp.rod.write("give 500k coin %s\n"%(self.name))
            except: pass

            self.waitcmd("empty bag %s\ndrop bag\n"%self.container)
        
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

    def handle_sect_invitation(self):
        """Handle the sect invitation process for level 10+ characters"""
        if self.level >= 10 and not self.sect_member:
            self.printc("Initiating sect invitation process...", 'gold')
            
            # Character goes to Darkhaven Square and waits
            self.printc("Going to Darkhaven Square for sect invitation...", 'gold')
            self.godh()
            self.time.sleep(3)
            
            # Verify character is at Darkhaven Square
            self.get_loc()
            if self.location != "Darkhaven Square":
                self.printc("Failed to reach Darkhaven Square, halting...", 'red')
                self.quit()
                self.status = "quit"
                return False
            
            self.printc("Character ready at Darkhaven Square, logging in Kaan...", 'gold')
            
            # Now log in Kaan
            kaan = self.ROD("Kaan", "Elijah", "chest", "none")
            self.time.sleep(5)
            
            # Kaan goes to sect house (which is at Darkhaven Square)
            kaan.rod.write("secthome\n")
            self.time.sleep(2)
            kaan.rod.write("jig\n")
            self.time.sleep(3)
            
            self.printc("Both characters should now be at Darkhaven Square", 'gold')
            
            # Kaan invites the character
            self.printc("Kaan sending sectinvite to %s..." % self.name, 'gold')
            kaan.rod.write("sectinvite %s invite\n" % self.name.lower())
            self.time.sleep(2)
            
            # Read Kaan's response
            kaan_response = kaan.read()
            self.printc("Kaan response: %s" % kaan_response.strip(), 'cyan')
            
            # Character accepts invitation
            self.printc("Character accepting sect invitation...", 'gold')
            self.rod.write("sectinvite seraphim accept\n")
            self.time.sleep(3)
            
            # Check if invitation was successful
            r = self.read()
            self.printc("Character response: %s" % r.strip(), 'cyan')
            
            if ("You are now a member of" in r or "Seraphim" in r or "accept" in r.lower() or 
                "You have sworn allegiance to" in r):
                self.sect_member = True
                self.printc("Successfully joined sect Seraphim!", 'green')
                
                # Save sect membership status
                self.alt_info["sect_member"] = True
                self.pickle.dump(self.alt_info, open("alts/info_%s.pckle"%self.name,'wb'))
                
                # Immediately go to sect house now that we're a member
                self.printc("Going to sect house for the first time...", 'gold')
                self.rod.write("secthome\n")
                self.time.sleep(2)
                self.rod.write("jig\n")
                self.time.sleep(2)
            else:
                self.printc("DEBUG: Looking for success patterns in response:", 'red')
                self.printc("  'You are now a member of' found: %s" % ("You are now a member of" in r), 'red')
                self.printc("  'You have sworn allegiance to' found: %s" % ("You have sworn allegiance to" in r), 'red')
                self.printc("  'Seraphim' found: %s" % ("Seraphim" in r), 'red')
                self.printc("  'accept' found: %s" % ("accept" in r.lower()), 'red')
                self.printc("Sect invitation may have failed, halting...", 'red')
                kaan.quit()
                self.quit()
                self.status = "quit"
                return False
            
            # Kaan returns to sect house and logs out
            kaan.rod.write("secthome\n")
            self.time.sleep(2)
            kaan.quit()
            
            return True
        return True

    def log_cleric(self):
        if self.master != None:
            return 
        
        #self.cleric = self.ROD("Kaeval","1q2w3e4r","basket", "cleric")
        try:
            if sys.argv[2] != "None":
                self.cleric = self.ROD(sys.argv[2],"1q2w3e4r","basket", "cleric")
                self.clericon = True
                if self.support!= None:
                    self.support.cleric = self.cleric
                    self.support.clericon = True
        except IndexError:
            # No cleric specified, run solo
            pass
        else:
            self.clericon = False
        return

    def emergency_quit(self):
        self.printc("EMERGENCY QUIT")
        self.time.sleep(6)
        msg = self.random.choice(["hi, brb", "brb", "hey","hello","sup?","brb, got to run","yo!"])
        
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
                try: sname, svalue = bsplt[i].split("%: ")
                except:
                    print(bsplt[i])
                    continue
                sname = sname.split(":")[-1].strip()
                svalue = svalue.split()[0]
                slist.append((sname, svalue))
        self.slist = slist
        
        

    def cleric_follow(self):
        global clericfol
        if self.master != None or not self.clericon or clericfol != "follow":
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
            print(self.location, self.cleric.location)
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
    CYAN = '\\u001b[36m'
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
    maxtime = 60*1
    # Get user first
    user,  container =  sys.argv[1], "chest"
    
    try: targetlvl = int(sys.argv[3])
    except: targetlvl = 50
    try: maxtime = int(sys.argv[4])
    except: maxtime = 525600  # Default to 1 year (essentially infinite)
    try: pw = sys.argv[5]
    except: 
        # Check for known character passwords
        if user in ["Xixili", "Lasonas"]:
            pw = "yaoyao2020"
        elif user in ["Dresden", "Lore", "Daltin"]:
            pw = "Elijah"
        else:
            pw = "1q2w3e4r"
    #user, pw, container = "Mordok", "1q2w3e4r", "chest"  
    #user, pw, container = "Zordok", "1q2w3e4r", "chest"
    #user, pw, container = "Fardok", "1q2w3e4r", "chest"
    #user, pw, container =  "Lynnok", "1q2w3e4r", "chest" # low level  
    
    try: container = sys.argv[6]
    except: container = "chest"

    try: clericfol = sys.argv[7]
    except: clericfol = "follow"

    print(user, pw, "target",targetlvl, "cleric:", clericfol)


    
    #user, pw, container = "Marijoie", "1q2w3e4r", "chest"
    #support, supportpw, supportcontainer =  "Zordok", "1q2w3e4r", "chest"
    import time
    import pickle
    

    start = time.time()
    month,date =time.ctime().split()[1:3]
    year = time.ctime().split()[-1]

    
    status, N = "restart", 0
    last_status = None
    while True:
        try:
            while True:
                if status == "restart":
                    status = "continue"
                    if N == 0:
                        if support != None:
                            rod = ROD(user,pw,container,'dhaven', (support,supportpw,supportcontainer))
                        else:
                            rod = ROD(user,pw,container,'dhaven')
                    else:
                        try: del rod
                        except: pass
                        if support != None:
                            rod = ROD(user,pw,container,'dhaven', (support,supportpw,supportcontainer))
                        else:
                            rod = ROD(user,pw,container,'dhaven')
                    rod.N = 0
                    time.sleep(10)
                status = rod.status
                
                if rod.support == None:
                    printc("%s\nStatus: %s\n%s \t Phase (%d)\n%s\nAction: %s\nReached level %d of target level %d.\n"%(rod.name,status, "%s | %s"%(rod.area,rod.location), rod.phase, "Stalled: %d"%N, rod.status_msg, rod.level, targetlvl),'gold')
                    printc("Alive for:%.2f minutes (max: %.2f)\n"%(float(time.time()-start)/60, maxtime),'gold')

                else:
                    printc("%s\nStatus: %s\n%s \t Phase (%d)\n%s\nAction: %s | %s\nReached level %d of target level %d.\n"%(rod.name,status, "%s | %s"%(rod.area,rod.location), rod.phase, "Stalled: %d"%N, rod.status_msg,rod.support.status_msg, rod.level, targetlvl),'gold')

                    printc("Alive for:%.2f minutes (max: %.2f)\n"%(float(time.time()-start)/60, maxtime),'gold')

                threads = threading.enumerate()
                if len(threads) >= 2:
                    printc("Threads:" +" ".join([str(t.is_alive()) for t in threads[1:]]),'green')
                    #for t in threads[1:]:
                    #    t.stop()


                # Time limit check disabled for indefinite leveling
                # if float(time.time()-start)/60 > maxtime and not rod.fight:
                #     printc("Reached time limit\n")
                #     rod.quit()
                #     break
                if targetlvl == rod.level and not rod.fight:
                    printc("Reached target level\n")
                    rod.quit()
                    break
                cstatus = (rod.name, rod.phase, rod.location)
                if last_status != cstatus:
                    last_status = cstatus
                    rod.N = 0
                else:
                    rod.N += 1


                if rod.status_msg == "Waiting for kill to register":
                    rod.status_msg = "Just killed something..."
                    rod.N = 0
                if rod.N > 5 and not rod.fight and "Wait" not in rod.status_msg:
                    status = "restart"
                    rod.quit()
                    continue
                elif N > 70:
                    status = "restart"
                    rod.quit()
                    continue

                time.sleep(15)
                
                if status == "continue":
                    continue
                elif status == "restart":
                    if rod.clericon:
                        rod.cleric.quit()
                    rod.quit()
                elif status == "quit":
                    rod.quit()
                    break
                else:
                    rod.quit()
                    status = "restart"

        except KeyboardInterrupt:
            rod.rod.write("quit\n")
            rod.stop = True
            time.sleep(2)
            exit()
        except EOFError:
            if 'rod' in locals():
                rod.stop = True
            status = "restart"
        except:
            if 'rod' in locals():
                rod.stop = True
            status = "restart"
        if 'rod' in locals() and rod.stop:
            rod.stop = True
            break
        #except: #error: [Errno 60] Operation timed out
        #    print("Unexpected error:", sys.exc_info()[0])
        #    del rod
        #    break
        #    status = "restart"
        #    continue
        #else:
        #    break
        
    exit()


