import telnetlib, time
import sys
import threading
from threading import Thread
import random
import os


class dhaven:
    ''' class for activities in dhaven '''
    wait = 0
    trancing = 0
    def func_dhaven(self):
        # step 1 check supplies and spells
        # step 2 check cleric is with us
        # step 3 check eq
        self.godh("recall")
        self.printc("Dhaven: %s %s %s"%(self.name, self.phase, self.location))

        self.status_msg = "dhaven -- start"
        self.ready = False
        self.rod.write("wake\n")
        self.check_eq()
        self.check_prac()

        if self.fight:
            return
            
        if self.phase == 0:
            self.godh()
            
            self.rod.write("follow self\n")
            self.following = False
        # check everything
            self.phase = 1
            self.whereami()
            self.check_inv()
            self.check_affect() 
            self.check_prac()
            self.survey()
            self.time.sleep(2)
            if len([x for x in self.eqdam if x != "superb"]) > 0:
                self.go("s;s;e;s")
                self.rod.write("rem all\nrepair all\nwear all\nrem shield\n")
                self.time.sleep(3)
                self.go("n;w;n;n")
            self.whereami()

            if self.charclass == "Cleric":
                potreq = 50
            else:
                potreq = 100
            #    return "cleric"

            self.check_cont("basket")
            
            self.potname = "a glowing purple potion"
            
            
            getrecall = False
            if self.recallname in self.containers["basket"]:
                if self.containers["basket"][self.recallname] < 5:
                    # need recall
                    getrecall = True
            else:
                getrecall = True
                
            if getrecall:
                self.status_msg = "Getting recall scrolls"
                if self.charclass == "Barbarian":
                    self.rod.write("get recall basket\nshatter recall\n")
                    time.sleep(2)
                    self.go("w;n;n;nw;w;n;nw;n;w")
                    self.rod.write("buy 10 recall\nempty bag basket\ndrop bag\ne\nn\nn\nsay I wish to visit the city dwellers\ns\n")
                    self.phase = 0

            getpotion = False
            if self.potname in self.containers["basket"]:
                if self.containers["basket"][self.potname] < potreq:
                    getpotion = True
            else:
                getpotion = True
            print "get potion", getpotion
            if getpotion:
                sys.stdout.write("GETTING potions...\n")
                self.status_msg = "Getting potions"
                self.godh()
                self.go("s;s;w;w;n")
                    
                
                if getpotion:
                    if potreq > 20:
                        for i in range(max([potreq/20-1,0])):
                            self.rod.write("buy %s %s\nempty bag basket\ndrop bag\n"%(20, self.potname.split()[2]))
                    else:
                        self.rod.write("buy %s %s\nempty bag basket\ndrop bag\n"%(20, self.potname.split()[2]))

                self.go("s;e;e;n;n")
                self.time.sleep(4)
            self.godh("recall")
        if self.charclass == "Cleric":
            return "cleric"
        self.nextfunc = 'wait'
        return "wait"

    def func_wait(self):

        self.time.sleep(.2)
        #self.get_loc()
        #self.printc("%s at %s"%(self.name,self.location),'gold')
        

        self.check_affect()
        while "sanctuary" not in self.aff:
            self.waitcmd("say xsanc")
            self.time.sleep(3)
            self.check_affect()

        while "elemental supremacy" not in self.aff:
            self.waitcmd("say elem")
            self.time.sleep(5)
            self.check_affect()


        if int(self.HP) < 1100:
            self.waitcmd("report")
            self.waitcmd("say heal")
            raise Exception("DONE")

        self.waitcmd("beam")
        self.waitcmd("n\nchoke justice")
        while True:                                                                                                                                                                                                        
            r = self.waitcmd("flee\nflee\nflee")                                                                                                                                                                            
            if "You flee head over heels from combat!" in r:                                                                                                                                                                
                break                                                                                                                                                                                                       
            self.time.sleep(1) 

        print self.HP, self.MAXHP

        healN = 1200-int(self.HP)
        for i in range(healN/600+1):
            self.waitcmd("say heal")
        
        #while True:
        #    r = self.waitcmd("flee")
        #    if "You flee head over heels from combat!" in r:
        #        break
        #    self.time.sleep(1)
        

        

        raise Exception("DONE")
        

    def func_cleric(self):
        if self.wait %3 == 0: 
            self.printc("Trancing: %s Location: %s"%(self.trancing,self.location))
            if not self.fight:
                self.check_inv()
                if True not in ["a symbol of faith" in x for x in self.inv]:
                    self.waitcmd("cast 'create symbol'")

            print self.MP, self.MAXMP
            group = self.check_group()
            toheal = []
            for name, v in group.items():
                hp,maxhp,perc = v
                if perc < 0.95:
                    toheal.append(name)

            self.printc("To heal: %s"%(" ".join(toheal)), 'gold')
            if len(toheal) >= 2:
                self.waitcmd("cast 'fortify'")
            elif len(toheal) == 1:
                self.waitcmd("cast 'heal' %s"%toheal[0])
        elif self.wait %2 == 0:
            self.check_cont('chest')
            print self.containers['chest']
            
            
            #for it in self.midas:
                
            #    self.printc("Midas %s..."%self.midas[0])
            #    if self.domidas(self.midas[0]):
            #        done.append(it)
            

            #if len(damaged) >= 2 and self.MP > 800:
            #    self.waitcmd("cast 'fortify'")

        if not self.trancing:
            self.rod.write("trance\n")
            self.trancing = True

        if self.wait >= 20:
            self.whereami()
            self.phase += 1
            if float(self.HP) < float(self.MAXHP) *0.9:
                self.rod.write("c heal\n")
                self.trancing = False
        
            self.check_affect(p=False)
            if "fly" not in self.aff:
                self.check_affectby()
                self.printc("Cleric: %s %s"%(str(self.aff), str(self.affby)))
                if "flying" not in self.affby:
                    self.rod.write("cast fly\n")
                    self.trancing = False
            #if "sanctuary" not in self.aff:
            #    self.rod.write("cast sanc\n")
            #    self.trancing = False
            self.wait = 0
        
        if self.following:
            self.phase += 1
        self.wait += 1
        self.time.sleep(1)
        return False



class ROD(dhaven):
    
    def __init__(self, user, pw, container, function, support = None,  take_input_bool = False):


        # weapons and their keywords for disarm checks
        self.funcdic = {"dhaven":self.func_dhaven,
                        "wait": self.func_wait,
                        "cleric": self.func_cleric}

        self.weapons = {"Nasr, Claymore of Sovereignty":"nasr",
                        "Dragon Claw of Legend":"claw"
        }

        self.midas = []
        self.cleric = []
        self.pot = "purple"
        self.fighting = ''
        self.forcetarget = None
        self.nextfunc = None
        self.following = False
        self.ready = False
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
        self.fight = False
        self.user_input = None
        #self.take_input_bool = take_input_bool
        self.debug = 0
        self.phase = 0
        self.lag = 0
        self.trancing = 0
        self.container = container
        self.status = "continue"
        self.disarm = False
        self.goingback = False
        self.containers = {}
        self.gold = None
        self.eq = {}
        self.level = 50
        self.target = None
        self.HP, self.MAXHP = 1000,1000

        try:
            self.alt_info = pickle.load(open("alts/info_%s.pckle"%user,'r'))
        except:
            self.alt_info = {}
        
        
        if True:
            self.rod = telnetlib.Telnet("realmsofdespair.com",4000)


            #create character if does not exist
            self.rod.write("%s\n"%user)
            self.time.sleep(2)
            self.buf = self.read()
            print "\n%s: %s"%(self.name,self.buf)
            
            if "That character is already connected - try again in a few minutes." in self.buf:
                self.quit()
            else:
                self.rod.write("%s\n\n \n \nconfig -ansi\nconfig -autosac\nconfig -autoloot\nwake\nconfig +gag\nwimpy 0\n\n"%(pw))
                self.rod.write("prompt ("+self.name.lower()+") &w&Y%h/%Hhp &C%m/%Mmn &G%v/%Vmv&w &Y%gg &r&w%aa &p%i%\n")
                self.rod.write("fprompt ("+self.name.lower()+")F &w&Y%h/%Hhp &C%m/%Mmn &G%v/%Vmv&w [%n] &r&w%aa &p%i%a &w(&R%c&w) .:%L:.\n")
        
        self.charclass = None
        self.check_affect()
        

        if self.charclass == "Barbarian":
            self.recallname = "a Barbarian stone of recall"
        else:
            self.recallname = "a recall scroll"

                
        self.func_wait()

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
                print "ERROR IN check_affect"
            else:
                return

    def check_affect_main(self, p = False):
        
        aff = {}
        r = self.waitcmd("score", p)
            
        bsplt = r.split('\n')
        #print bsplt
        scan = False
        spells = []
        for i in range(len(bsplt)):
            self.check_disarm(bsplt[i])
            if "SMAUG 2.6" in bsplt: continue

            if "Class: " in bsplt[i]:
                self.charclass = bsplt[i].split("Class: ")[-1].split()[0]

            if "Gold :" in bsplt[i]:
                self.gold = int(bsplt[i].split("Gold : ")[-1].split()[0].replace(",",""))

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
        self.printc("%s %s"%(self.name, self.charclass) +'\n'
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

    def survey(self, p = False):
        r = self.waitcmd("survey")
        eqdam = []
        for ln in r.split('\n'):
            ln = ln.strip()
            if len(ln) == 0: continue
            if ln[0] == '<':
                wearloc = ln.split(">")[0][1:].split()[-1]
                item = ln.split(">")[-1].strip().split(") ")[-1]
                if wearloc != "light":
                    dam = ln.split("[")[-1].split("]")[0]
                    eqdam.append(dam)
                
        self.eqdam = eqdam
        print eqdam
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
        #except IndexError:
        #    self.sys.stdout.write("Index error, restarting %s"%self.name)
        #    self.quit()
        #    self.status = "restart"
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
                
                for ln in self.bufln.split("\n"):
                    if ln.strip() == "": continue
                    if self.fight:
                        self.printc(ln.strip())
                    #print "***", [ln.strip()], self.fight
                    
                    if "(%s)"%self.name.lower() in ln:
                        
                        self.HP, self.MAXHP = ln.strip().replace("hp","").split()[1].split("/")
                        self.MP, self.MAXMP = ln.strip().replace("mn","").split()[2].split("/")
                        self.MV, self.MAXMV = ln.strip().replace("mv","").split()[3].split("/")
                        
                        #print [self.name,self.HP, self.MAXHP]
                        #if self.MV < 100:
                        #    if self.clericon:
                        #        self.cleric.rod.write("c 'refresh' %s"%self.name)
                        
                        if "(%s)F "%self.name.lower() in ln:
                            self.fight = True
                            self.fighting = ln.split('[')[-1].split(']')[0]

                            kw = None
                            if self.fighting in autotarget:
                                kw = autotarget[self.fighting]
                            self.printc("%s fighting %s (%s, %s)\n"%(self.name, self.fighting,self.target, kw),'gold')
                        else:
                            if int(self.MP) < int(self.MAXMP)*0.7:
                                if 'basket' in self.containers:
                                    if "a glowing blue potion" in self.containers['basket']:
                                        self.rod.write("q blue basket\n")
                        
                            self.fight = False
                            cspring = False
                            makespring = False
                    #if "You wish that your wounds would stop BLEEDING so much!" in ln:
                    #    self.rod.write("flee\nquit\n")
                    #    self.status = "restart"
                        
                    if "Your opponent is not wielding a weapon" in ln:
                        self.disarm = False
                    if "Your stomach cannot contain any more." in ln:
                        # try to drink and/or make spring
                        self.rod.write("drink\n")

                    
                    if int(self.HP) < int(self.MAXHP)*0.4:
                            #self.rod.write("flee\nquit\n")
                        self.rod.write("gt low hp (%d)!!\n"%int(self.HP))
                        self.waitcmd("quaff %s %s"%(self.pot, self.container))
                    elif int(self.HP) < int(self.MAXHP)*0.7:
                        self.waitcmd("quaff %s %s"%(self.pot, self.container))
                    if "Drink what?" in ln and makespring:
                        self.printc("Try to create spring...\n")
                        
                        random.choice(self.cleric).rod.write("cast 'create spring'\ntrance\n")
                        
                        
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
                    self.printc("function %s\n"%(nextfunc),'gold')
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
                if "(%s)"%self.name.lower() in l:
                    self.HP, self.MAXHP = l.strip().replace("hp","").split()[1].split("/")
                    self.MP, self.MAXMP = l.strip().replace("mn","").split()[2].split("/")
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
                    
                    random.choice(self.cleric).rod.write("cast 'create spring' %s\ntrance\n"%self.name)
                
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

    def cleric_heal(self):

        #if not self.clericon:
        #    return
        
        #if self.cleric.location != self.location:
        #    if int(self.HP) < int(self.MAXHP)*0.7:
        #        self.cleric.rod.write("cast 'uplift' %s\ntrance\n"%self.name)
        #    return

        
        if int(self.HP) < int(self.MAXHP)*0.7:
            random.choice(self.cleric).rod.write("cast 'heal' %s\ntrance\n"%self.name)
                
        if int(self.MV) < 100:
             random.choice(self.cleric).rod.write("cast 'refresh' %s\ntrance\n"%self.name)

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
        
        if True:
            if self.random.random() < 0.3:
                self.check_spells()

            #if int(self.HP) <  int(self.MAXHP)*0.4:
            #    self.rod.write("flee\nquit\n")

            self.printc("%s %d/%dhp"%(self.name,  int(self.HP), int(self.MAXHP)))
            if int(self.HP) < int(self.MAXHP)*0.8:
                self.rod.write("quaff %s %s\n"%(self.pot, self.container))
            else:
                if self.charclass == "Barbarian":
                    if self.forcetarget != None:
                        self.waitcmd("gt rend %s\nrend %s"%(self.forcetarget,self.forcetarget))
                    else:
                        self.autotarget("rend")
                        
                elif self.charclass == "Warrior":
                    self.waitcmd("smash")
                elif self.charclass == "Ranger":
                    self.waitcmd("wasp")
                else:
                    self.autotarget("strike")
                    
        #self.rod.write("ver\n")
        return

    def autotarget(self, attack):
        if self.fighting != "":
            if self.fighting in autotarget:
                tar = autotarget[self.fighting]
            else:
                trytargets = self.fighting.split() 
                if random.random() < 0.5:
                    tar = random.choice([x for x in "abcdefghijklmnopqrstuvwxyz"])
                else:
                    tar = random.choice(trytargets)
                self.printc("No target for %s, trying %s"%(self.fighting,tar),'gold')
            r = self.waitcmd("%s %s"%(attack, tar))
            #print [r]
            if ("They aren't here." in r or "You wouldn't dare..." in r or "You feel too nice to do that!" in r or "The gods frown on such illegal killing" in r) and self.fight:
                if self.fighting in autotarget:
                    self.printc("Target was wrong for %s (%s)"%(self.fighting,tar),'gold')
                    autotarget.pop(self.fighting)
                return
            else:
                self.target = tar
                self.printc("%s %s (%s)"%(attack, self.fighting,tar),'gold')
                if self.fighting not in autotarget:
                    autotarget[self.fighting] = tar
                    pickle.dump(autotarget, open("autotarget.pck",'w'))
                elif tar != autotarget[self.fighting]:
                    autotarget[self.fighting] = tar
                    pickle.dump(autotarget, open("autotarget.pck",'w'))
                return
        self.printc("Could not see who I'm attacking",'gold')
            



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
                    self.rod.write("get recall my.basket\nshatter recall\n")
                    self.time.sleep(2)
                    self.go("w;n;n;nw;w;n;nw;n;w")
                    self.time.sleep(2.5)
                    self.rod.write("buy recall\nput recall my.basket\ne\nn\nn\nsay I wish to visit the city dwellers\ns\ndr\n")
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
                        self.rod.write("recite scroll\nget recall my.basket\ns\ndr\n")
                    self.time.sleep(2.5)
        elif loc == "recall":
            if self.location == "Thoth's Rune on Vertic Avenue":
                pass
            elif  self.location == "Darkhaven Square":
                self.go("n")
            else:
                if self.charclass == "Barbarian":
                    self.rod.write("get recall my.basket\nshatter recall\n")
                    self.time.sleep(1.5)
                    self.go("w;n;n;nw;w;n;nw;n;w")
                    self.time.sleep(2)
                    self.rod.write("buy recall\nput recall my.basket\ne\nn\nn\nsay I wish to visit the city dwellers\n")
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
        rln = r.split('\n')
        if len(rln) >= 1:
            if rln[0].strip() != "":
                #print rln[0]
                self.start = time.time()
                self.N = 0

        for i in range(len(rln)):      


            if "(%s)"%self.name.lower() in rln[i]:

                self.HP, self.MAXHP = rln[i].strip().replace("hp","").split()[1].split("/")
                self.MP, self.MAXMP = rln[i].strip().replace("mn","").split()[2].split("/")
                self.MV, self.MAXMV = rln[i].strip().replace("mv","").split()[3].split("/")

            if "exclaims 'fol!'" in rln[i]:
                char = rln[i].split()[0]
                if char in trusted:
                    self.waitcmd("follow %s"%char)

            if "tells you '" in rln[i]:
                char = rln[i].split()[0]
                if char in trusted:
                    cmd = rln[i].split("you '")[-1].split("'")[0]
                    if cmd == "recall":
                        self.nextfunc = 'dhaven'
                        self.godh("recall")
                    else:
                        self.waitcmd(cmd)
                

            if "is DEAD!!" in rln[i]:
                k = rln[i].split(" is")[0]
                self.printc("%s: %s is dead"%(self.name, k),'red')
                self.fight = False
                print self.fighting, k
            
                self.fighting = ''
                self.loot(k)
                    

            if "tells the group 'stat'" in rln[i]:
                self.check_affect(p=True)
                self.check_cont("basket",p=True)
                purple = 'a glowing purple potion'
                try: pnum = self.containers["basket"][purple]
                except: pnum = 0
                try: sanc = self.affect["sanctuary"]
                except:
                    try: sanc = self.affect["holy sanctity"]
                    except: sanc = 0
                
                self.waitcmd("gt gold (%.2fM) purples (%s) sanc (%s)"%(self.gold/1000000.0, pnum, sanc))

            if "says 'sanc'" in rln[i]:
                char = rln[i].split()[0]
                if char in trusted:
                    self.waitcmd("c holy")
            if "tells the group 'handgold'" in rln[i]:
                char = rln[i].split()[0]
                if char in trusted:
                    self.check_affect(p=True)
                    give = self.gold-1e6
                    if give > 0:
                        self.waitcmd("give %d coin %s"%(give, char))

            if "tells the group 't " in rln[i]:
                char = rln[i].split()[0]
                if char in trusted:
                    self.forcetarget = rln[i].split("'t ")[-1].split("'")[0]
                    self.waitcmd("tell %s targeting %s"%(char, self.target))

            if "tells the group 'do " in rln[i]:
                char = rln[i].split()[0]
                if char in trusted:
                    action = rln[i].split("'do ")[-1].split("'")[0]
                    self.waitcmd(action)

            if "tells the group 'recall" in rln[i]:
                char = rln[i].split()[0]
                if char in trusted:
                    self.godh('recall')
                    self.nextfunc = 'dhaven'

            if "You slowly float to the ground." in rln[i]:
                r = self.waitcmd("say let me fly!")

            if "tells the group 'fleequit" in rln[i]:
                char = rln[i].split()[0]
                if char in trusted:
                    while True:
                        r = self.waitcmd("flee")
                        if "You flee head over heels from combat!" in r:
                            self.quit()
                            break

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
                self.forcetarget = None
            if "gets damaged" in rln[i]:
                self.eqdam = True

        return r



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
        time.sleep(1)
        if "Your surroundings begin to fade" not in self.read():
            self.quit()



    def split_attacks(self,string):
        dmg = "misses|brushes|barely scratches|barely scuffs|scratches|scuffs|grazes|nicks|pelts|cuts|bruises|jolts|hits|strikes|wounds|tears|thrashes|injures|rips|batters|gashes|flogs|jars|lacerates|pummels|hacks|smashes|mauls|decimates|rends|bludgeons|_traumatizes_|_devastates_|_mangles_|_shatters_|_maims_|_demolishes_|_cleaves_|_butchers_|_cripples_|MUTILATES|MASSACRES|DISEMBOWELS|PULVERIZES|DISFIGURES|DESTROYS|GUTS|EVISCERATES|* OBLITERATES *|* SLAUGHTERS *|*** ANNIHILATES ***|**** SMITES ****|miss|brush|barely scratch|barely scuff|scratch|scuff|graze|nick|pelt|cut|bruise|jolt|hit|strike|wound|tear|thrash|injur|rip|batter|gash|flog|jar|lacerate|pummel|hack|smash|maul|decimate|rend|bludgeon|_traumatize_|_devastate_|_mangle_|_shatter_|_maim_|_demolishe_|_cleave_|_butcher_|_cripple_|MUTILATE|MASSACRE|DISEMBOWEL|PULVERIZE|DISFIGURE|DESTROY|GUT|EVISCERATE|* OBLITERATE *|* SLAUGHTER *|*** ANNIHILATE ***|**** SMITE ****".split("|")
        for d in dmg:
            if d in string:
                return string.split(d)[-1]
        return ""


    def loot(self,name):
        if self.charclass == "Cleric":
            return


        cle = random.choice(self.cleric)
        name = name.strip()
        if True:
            if name == "The battlerager":
                self.waitcmd("get all.gutbuster battlerager\nput all.gutbuster %s"%self.container)
            elif name == "Thibbledorf Pwent":
                self.waitcmd("get all.gutbuster thibb\nput all.gutbuster %s"%self.container)
            elif name == "Catti-Brie":
                for it in ['cat','taul','khaz']:
                    self.read()
                    r = self.waitcmd("get %s catti"%it)
                    self.rod.write("give %s %s"%(it, cle.name))
                    cle.waitcmd("put %s chest"%(it))
            elif name == "Bruenor Battlehammer":
                self.read()
                r = self.waitcmd("get shield bruenor")
                self.waitcmd("give battle %s"%cle.name)
                cle.waitcmd("put battle chest")
            elif name == "Wulfgar":
                self.read()
                r = self.waitcmd("get aegis-fang wulfgar")
                self.rod.write("give aegis-fang %s"%cle.name)
                cle.waitcmd("put aegis-fang chest")
                    
            elif name == "Drizzt Do'Urden":                
                for it in ['bracer','bracer','twinkle','scimitar']:
                    self.read()
                    r = self.waitcmd("get %s drizz"%it)
                    self.waitcmd("give %s %s"%(it, cle.name))
                    cle.waitcmd("put %s chest"%(it))
                    
            elif name == "Artemis Entreri":
                for it in ["dagger","sword","cloak"]:
                    self.read()
                    r = self.waitcmd("get %s artemis"%it)
                    print self.name,[r]
                    if "You get" in r:
                        self.waitcmd("give %s %s"%(it, cle.name))
                        cle.waitcmd("put %s chest"%(it))
                    
            elif name == "Regis":
                for it in ["pendant"]:
                    self.read()
                    r = self.waitcmd("get %s regis"%it)
                    self.waitcmd("give %s %s"%(it, cle.name))
                    cle.waitcmd("put %s chest"%(it))
                    
                    

    def domidas(self,name):
        for i in range(5):
            r = self.waitcmd("cast midas %s"%name)
            if "You transmogrify" in r or "You are not carrying that." in r:
                return True
        return False
                

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

    
        
    import time
    import pickle
    
    autotarget = pickle.load(open("autotarget.pck"))
    
    #autotarget = {}

    if False:
        for (mob, key) in autotarget.items():
            print mob, key

    start = time.time()
    month,date =time.ctime().split()[1:3]
    year = time.ctime().split()[-1]


    alts = ['Argnok','Grotok']
    trusted = ["Keamval", "Kaetas","Vanox","Mirzakhani","Kaeval","Azaghal","Fanmal"]+alts
    container = "basket"
    pw = "1q2w3e4r"
    # LOG IN
    users = {}

    active = None
    i = 0
    while True:
        
        if active == None:
            i += 1
            user = alts[i%len(alts)]
            try: active = ROD(user,pw,container,'wait')
            except Exception:
                continue
            else:
                break
        time.sleep(20)
        threads = threading.enumerate()
        

        print "Active... %.2f (%d threads)"% (time.time()-start, len(threads))
        
        if len(threads) == 1:
            break

    #for user in alts[1:]:
    #    users[user].waitcmd("follow %s\n"%(lead))

    #users[lead].waitcmd("group all")
    #users[lead].waitcmd("group",p=True)

    #if users[lead].location == "Outside a Mysterious Inn":
    #    users[lead].portal()
        #users[lead].go("enter;w;s;s;w")

    #for user in users:
    #    print user
    #    users[user].quit()
    #exit()


