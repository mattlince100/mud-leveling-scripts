import time
import sys
import random


class Starting:

    def func_starting(self):
        self.rod.write("config -autosac\n")
        
        print [self.location, self.exits, self.area], self.phase


        self.whereami()
        self.check_affect()

        if self.level > 2:
            return 'dhaven'
        
        if self.location == "Rejoining the Ancient Clan Spirits" and self.phase == 0:
            # right after pulling the rod
            self.rod.write("config -autoloot\nconfig -shields\nconfig +brief\nconfig +gag\n")
            self.go("n;e;n;ne;n") #kobold phase 1
            self.phase = 1
            self.time.sleep(20)
        elif self.phase == 0:
            return 'dhaven'
        if self.buf.count("a long black cloak" ) == 1 and "gloves of striking" in self.buf and self.phase == 1:
            self.buf = ''
            self.rod.write("get all corpse\nget all 2.corpse\nwear all\n")
            self.go("s;e;n")
            self.phase = 2
            self.time.sleep(15)
        elif self.phase == 1:
            self.rod.write("get all corpse\nget all 2.corpse\nwear all\n")
            self.go("s;e;n")
            self.phase = 2
            self.time.sleep(15)
        if self.buf.count("a studded leather bracer") == 2 and "a war belt" in self.buf and self.phase == 2:
            self.buf = ''
            self.rod.write("get all corpse\nget all 2.corpse\nwear all\n")
            self.go("s;se;s;e")
            self.phase = 3
            self.time.sleep(20)
        elif self.phase == 2:
            self.rod.write("get all corpse\nget all 2.corpse\nwear all\n")
            self.go("s;se;s;e")
            self.phase = 3
            self.time.sleep(20)

        if "a fur skin cap" in self.buf and self.buf.count("a leather neckband") == 2 and self.phase == 3:
            self.buf = ''
            self.rod.write("get all corpse\nget all 2.corpse\nwear all\n")
            self.go("w;s;sw;s")
            self.time.sleep(2)
            self.rod.write("kill drake\n")
            time.sleep(5)
            self.rod.write("kill drake\n")
            self.phase = 4
        elif self.phase == 3:
            self.rod.write("get all corpse\nget all 2.corpse\nwear all\n")
            self.go("w;s;sw;s")
            self.time.sleep(2)
            self.rod.write("kill drake\n")
            time.sleep(5)
            self.rod.write("kill drake\n")
            self.phase = 4
            self.time.sleep(20)

        if "bone plate leggings" in self.buf and "a pair of fur lined boots" in self.buf and self.phase == 4:
            self.rod.write("get all corpse\nget all 2.corpse\nwear all\n")
            self.rod.write("n\nw\nopen sw\nsw\n")
            self.phase = 5
            self.buf = ''
            self.time.sleep(15)
        elif self.phase == 4:
            self.rod.write("get all corpse\nget all 2.corpse\nwear all\n")
            self.rod.write("n\nw\nopen sw\nsw\n")
            self.phase = 5
            self.buf = ''
            self.time.sleep(15)
            
        if "a pair of leather armguards" in self.buf and self.phase == 5:
            self.buf = ''
            self.rod.write("get all corpse\nwear all\n")
            self.go("ne;n;n;n")
            self.phase = 6
            self.time.sleep(5)
            self.whereami()
        elif self.phase == 5:
            self.rod.write("get all corpse\nwear all\n")
            self.go("ne;n;n;n")
            self.phase = 6
            self.time.sleep(5)
            self.whereami()

        if self.location == "Under a Large Hole in the Cavern" and self.phase == 6:
            self.buf = ''
            # ready to go do DH
            self.go("#4 w;#2 nw;n;w;#4 n;nw;w;n;nw;n;w")
            self.rod.write("buy recall\nbuy recall\n")
            self.go("e;n;n")
            self.rod.write("say I wish to visit the city dwellers\n")
            self.time.sleep(15)
            return 'dhaven'
        


class dhaven:
    ''' class for activities in dhaven '''
               
    switch_runs = 0 # keep track of runs
    
    def __init__(self, user, pw, container):
        # just returned to Harakiem
        self.phase = 0 
        self.level = 0
        self.func = self.func_dhaven
    

    def func_dhaven(self):
        # step 1 check supplies and spells
        # step 2 check cleric is with us
        # step 3 check eq
        self.printc("Dhaven: %s %s %s"%(self.name, self.phase, self.location))
        

        self.printc("Time since last ready: %d seconds...\n"%(self.time.time()-self.timesinceready),'gold')
        if (self.time.time()-self.timesinceready) > 10*60:
            self.status = "quit"
            self.quit()
            return "quit"

        if self.level == 50:
            self.godh()
            self.time.sleep(10)
            return 'dhaven'

        self.status_msg = "dhaven -- start"
        self.ready = False
        self.rod.write("wake\n")

        if self.fight:
            return
            
        if self.phase == 0:

            self.godh()

            if not self.clericon:
                self.log_cleric()
                self.cleric_follow()

            self.rod.write("follow self\n")
            self.following = False
            # check everything
            self.phase = 1
            self.whereami()
            self.check_inv()
            self.check_affect() # add check golda soft black wolf hide
            self.check_prac()
            self.time.sleep(2)

            print "\nINITIAL CHECKUP", self.location, self.inv, self.aff,"\n", "STATS", self.stats


        

            if "curse" in self.aff and self.charclass != "Barbarian":
                if self.clericon:
                    self.cleric.rod.write("c 'remove curse' %s\n"%self.name)
                else:

                    if not self.clericon:
                        self.log_cleric()

                    try: self.cleric.rod.write("c 'remove curse' %s\n"%self.name)
                    except: pass
                    self.time.sleep(5)
                    self.check_affect()
                    if "curse" in self.aff:
                        self.whereami()
                        if self.area != "New Darkhaven":
                            self.rod.write("supplicate recall\n")
                        if self.clericon:
                            self.cleric.rod.write("c 'remove curse' %s\n"%self.name)
                        
                        self.time.sleep(5)
                        self.check_affect()
                        if "curse" in self.aff:
                            self.rod.write("sleep\n")
                            self.printc("Waiting curse to wear off... it'll be a while\n")
                            self.status_msg = "Waiting curse to wear off"
                            self.time.sleep(self.aff['curse']*3.1)
                            self.rod.write("wake\n")                    

            print "LOCATION:",self.location
            if self.location in ["A watery tangle of caves",'The bottom of the vortex', 'A Dark passage','Surrounded in dark water','An escape??','A dark cave']:
                return "coral"
                   
        

            self.godh()

            #if len(self.inv) > 3:
            #    self.rod.write("wear oar\nwear oar\nwear hammer\nwear hammer\nwear all\ndrop all\nget %s\nget recall\n"%self.container)
            #    self.time.sleep(2)


            
            if self.level >= 18 and self.eqdam:
                self.go("s;s;e;s")
                #self.rod.write("rem all\nrepair all\nwear all\nrem chest\nwear oar\nwear hammer\n")
                self.rod.write("rem all\nrepair all\nwear death\nwear %s\nwear %s\nwear all\nrem %s\n"%(self.weaponkey,self.weaponkey,self.container))
                self.time.sleep(3)
                self.go("n;w;n;n")
                self.whereami()
                self.eqdam = False



            if self.gold != None and self.gold < 5e5:
                # need gold on this char
                self.sys.stdout.write("NEED GOLD....\n")
                self.godh("recall")
                self.status_msg = "Getting gold..."
                # wait till someone gives me gold
                if not self.clericon:
                    self.log_cleric()
                if self.master != None:
                    if self.master.clericon:
                        self.cleric = self.master.cleric

                if self.clericon:
                    self.cleric.godh("recall")
                    
                if self.clericon:
                    while True:
                        self.time.sleep(5)
                        amount = 1e6-self.gold
                        self.cleric.rod.write("give %d coin %s\n"%(amount, self.name))
                        self.time.sleep(5)
                        ln = self.rod.read_very_eager()
                        self.bufln += ln
                        if "gives you" in ln:
                            break
                
                self.phase = 0                
            
            toprac = []
            
            for skill, perc in self.slist:
                if perc == '0':
                    toprac.append(skill)

            if (self.container == "chest" and "a small birch chest" not in self.inv) and self.phase == 1:
                # go get a birch chest
                self.rod.write("rem chest\nwear hammer\nwear oar\n")
                self.check_inv()
                if "a small birch chest" not in self.inv:
                    self.status_msg = "Getting birch chest"
                    self.godh()
                    self.go("#6 n;#3 nw;w;n;e;e;e;n;n;n;w")
                    self.rod.write("buy chest\nempty 2.chest chest\nput all chest\nget recall my.chest\n")
                    time.sleep(2)
                    self.godh()
                    self.phase = 0
                    
            if len(toprac) > 0 and self.phase == 1:
                topracbool = False
                if "prac" in self.alt_info:
                    if self.level in self.alt_info["prac"]:
                        pass
                    else:
                        self.alt_info["prac"].append(self.level)
                        topracbool = True
                else:
                    self.alt_info["prac"] = [self.level]
                    topracbool = True

                if topracbool:
                    self.status_msg = "Practicing skills & Spells"
                    if self.charclass == "Barbarian":
                        self.rod.write("shatter recall\nget recall my.chest\n")
                        time.sleep(1)
                        self.go("w;s;s;e;s;se;se;e;e;n")
                        for skill in toprac:
                            self.rod.write("prac '%s'\n"%skill)
                            self.printc("practiced '%s'"%skill)
                        time.sleep(2)
                        self.go("s;w;w;nw;nw;n;w;n;n;n;n;nw;w;n;nw;n;n;n")
                        self.rod.write("say I wish to visit the city dwellers\ns\n")
                        self.phase = 0
                    else:
                        self.godh()
                        self.go("e;e;e;s;d;n;e")
                        for skill in toprac:
                            self.rod.write("prac '%s'\n"%skill)
                            self.printc("practiced '%s'"%skill)
                        time.sleep(2)
                        self.go("w;s;u;n;w;w;w")
                        self.phase = 0

            # check eq: level 5, 9

            # log in cleric to check eq
            upgear = False
            print self.alt_info
            if self.level in []: #[5,9,21,26,33,40,45]:
                if "upgrade_gear" in self.alt_info:
                    if self.level in self.alt_info["upgrade_gear"]:
                        pass
                    else:
                        upgear = True
                        self.alt_info['upgrade_gear'].append(self.level)
                else:
                    self.alt_info['upgrade_gear'] = [self.level]
                    
                    upgear = True

            if upgear and self.phase == 1:
                self.status_msg = "Upgrading EQ"
                self.check_eq()
                available_eq = [x for x in self.toequip if self.toequip[x] <= self.level]
                replace = {}
                for x in available_eq:
                    for y in self.upequip[x][1]:
                        replace[y] = x
                
                canreplace = []
                for wearloc, eq in self.eq.items():
                    for e in eq:
                        if e in replace:
                            E, R = e, replace[e]
                        elif (wearloc+":"+e) in replace:
                            E, R = wearloc+":"+e, replace[(wearloc+":"+e)]
                        else:
                            continue
                        canreplace.append((E,R))
                        break
                    
                if len(canreplace) > 0:
                    for e,r in canreplace:
                        self.sys.stdout.write("Replacing %s with %s...\n"%(e,r))        
                else:
                    self.sys.stdout.write("Nothing to replace at level %d...\n"%self.level)
                
                
                storage = "Kaeval"

                if not self.clericon:
                    self.log_cleric()
                
                self.godh("recall")
            
                if self.level == 21 and self.charclass == "Barbarian":
                    self.rod.write("rem guide\nrem shield\ngive bullette %s\n"%(storage))
                    self.time.sleep(5)
                    if self.clericon:
                        self.cleric.rod.write("get oar basket\ngive oar %s\nput shield basket\n"%(self.name))
                        self.time.sleep(5)
                        self.rod.write("wear oar\n")

                

                # if level 5 then go devote too
                #if True:
                #    self.time.sleep(10)
                #    self.rod.write("get recall chest\nshatter recall\n")
                #    self.time.sleep(2)
                #    self.go("w;n;n;nw;w;n;nw;n;w")
                #    self.time.sleep(6)
                #    self.rod.write("e\nn\nn\nn\ndevote tempus\ns\nsay I wish to visit the city dwellers\n")
                #    self.time.sleep(2)
                    

                self.phase = 0

        if self.phase == 1:
            self.status_msg = "Checking spells and wares"
            self.phase = 2
            self.whereami()
            self.check_cont(self.container)
            self.check_affect()
            time.sleep(2)
            # check and get restock

            # need at least 20 recalls in the chest:
            if self.charclass == "Barbarian":
                recallname = "a Barbarian stone of recall"
            else:
                recallname = "a recall scroll"

            getthoric = False
            if self.level < 15 and self.phase == 2:
                if 'blessing of' in self.aff:
                    if self.aff['blessing of'] < 40:
                        getthoric = True
                        self.status_msg= "Waiting blessing of thoric to wear off"
                        sys.stdout.write("sleeping %d...\n"%(self.aff['blessing of']*3))
                        time.sleep(self.aff['blessing of']*3)
                elif 'blessing of thoric' in self.aff:
                    if self.aff['blessing of thoric'] < 40:
                        getthoric = True
                        self.status_msg = "Waiting blessing of thoric to wear off"
                        sys.stdout.write("sleeping %d...\n"%(self.aff['blessing of thoric']*3))
                        time.sleep(self.aff['blessing of thoric']*3)
                else:
                    getthoric = True
                            
                if getthoric and self.phase == 2:
                    sys.stdout.write("GETTING THORIC...\n")
                    self.status_msg = "Getting thoric's blessing"
                    self.godh()
                    self.go("e;e;e;s;d;u;n;w;w;w")
                    self.phase = 1



            getlvl = False
            if "trollish vi" in self.aff:
                if self.aff['trollish vi'] < 30:
                    self.sys.stdout.write("Waiting trollish vigor to run out...\n")
                    self.status_msg = "Waiting for lvl spells to wear out..."
                    time.sleep(self.aff['trollish vi']*3.2)
                    getlvl = True
            else:
                getlvl = True
            #if self.stats['CON'] == 20 and (self.charclass != "Barbarian" or self.stats['CON'] == 22):
            #    getlvl = False
            #getlvl = False
            if getlvl and self.phase == 2:
                sys.stdout.write("GETTING LVL...\n")
                self.status_msg  = "Getting leveling spells"
                self.godh()

                if True:
                    self.go("nw;w;w;w")
                #self.rod.write("say refresh\nsay level\nsay shields\nsay fly\n")
                    #self.rod.write("say mspells\nsay cspells\n")
                    self.rod.write("say buffs!\nsay shields!\n")
                    sys.stdout.write("Waiting for level spells 30s...\n")
                    time.sleep(40)
                    self.check_affect()
                    self.go("e;e;e;se")
                #self.phase = 1  
                else:
                    self.go("nw;w;w;w")
                    self.rod.write("say buffs!\nsay shields!\n")
                    sys.stdout.write("Waiting for level spells 30s...\n")
                    time.sleep(40)
                    self.check_affect()
                    self.go("e;e;e;se")

            getrecall = False
            if recallname in self.containers[self.container]:
                if self.containers[self.container][recallname] < 2:
                    # need recall
                    getrecall = True
            else:
                getrecall = True
                
            if getrecall:
                self.status_msg = "Getting recall scrolls"
                if self.charclass == "Barbarian":
                    self.rod.write("get recall chest\nshatter recall\n")
                    time.sleep(2)
                    self.go("w;n;n;nw;w;n;nw;n;w")
                    self.rod.write("buy 10 recall\nempty bag chest\ndrop bag\ne\nn\nn\nsay I wish to visit the city dwellers\ns\n")
                    self.phase = 1
                else:
                    self.godh()
                    self.go("s;s;w;w;w;n")
                    self.rod.write("buy 12 recall\nempty bag %s\ndrop bag\n"%self.container)
                    time.sleep(1)
                    self.go("s;e;e;e;n;n")
        
            spring = "an icicle staff"
            getspring = False
            if spring in self.containers[self.container]:
                if self.containers[self.container][spring] <= 2:
                    getspring = True
            else:
                getspring = True        

            if self.charclass == "Barbarian":
                getspring = False
            
            if getspring and self.phase == 2 and self.level >= 6:
                sys.stdout.write("GETTING spring...\n")
            
                self.godh()
                self.go("e;s;s;w")
                self.rod.write("buy 2 icicle\nempty bag %s\ndrop bag\n"%self.container)
                self.time.sleep(1)
                self.go("e;n;n;w")
                self.phase = 1


            getfood = False
            food = 'a cooked turkey'
            if food in self.containers[self.container]:
                if self.containers[self.container][food] < 3:
                    getfood = True
            else:
                getfood = True

            getfood = False
            if getfood and self.phase == 2:
                sys.stdout.write("GETTING FOOD...\n")
                self.status_msg = "Getting food"
                self.godh()
                self.go("s;s;e;n")
                self.rod.write("buy 10 turkey\nempty bag %s\ndrop bag\n"%self.container)
                time.sleep(2)
                self.go("s;w;n;n")
                self.phase = 1
                

            getsanc = False
            if "sanctuary" in self.aff:
                tleft = self.aff['sanctuary'] 
                
                if tleft < 5:
                    self.status_msg = "Waiting sanc to run out..."
                    sys.stdout.write("waiting for sanc to run out...(%d)\n"%self.aff['sanctuary'])
                    self.time.sleep(tleft*3.2)
                    getsanc = True
                
            else:
                getsanc = True
            
            if self.master != None:
                getsanc = False

            
            
            if "sanctuary" not in self.aff or getsanc and self.master == None:

                if not self.clericon:
                    self.log_cleric()
                if self.clericon:
                    self.cleric.godh()
                    self.godh()
                    self.cleric.rod.write("cast sanctuary %s\ntrance\n"%self.name)
                    self.time.sleep(3)
                else:
                    self.godh()
                    self.go("nw;w;w;w")
                    self.rod.write("say #sanc\n")
                    time.sleep(10) 
                    self.go("e;e;e;se")
                self.phase = 1
            
            self.check_affect()
            
            getheal = False
            if int(self.HP) < int(self.MAXHP)*0.9:
                getheal = True
                print self.HP, self.MAXHP
            
            if getheal and self.phase == 2:
                self.status_msg= "Waiting for heals"
                self.godh()
                self.go("nw;w;w;w")
                self.rod.write("say heal\n")
                self.sys.stdout.write("waiting for heal...\n")
                time.sleep(5)
                self.go("e;e;e;se")

            getfly = False
            
            if "fly" in self.aff:
                if self.aff['fly'] < 30:
                    sys.stdout.write("waiting for fly to run out...\n")
                    self.status_msg = "Waiting fly to run out..."
                    time.sleep(self.aff['fly']*3.1)
                    getfly = True
            elif "float" not in self.aff:
                getfly = True

            if self.MV < 105:
                getfly = True
            elif getfly:
                self.check_affectby()
                if "flying" in self.affby:
                    getfly = False

            #if getfly and self.phase == 2:
            #    sys.stdout.write("GETTING FLY...\n")
            #    self.status_msg = "Getting fly spell"
            #    self.godh()
            #    self.go("ne")
            #    self.rod.write("say fly\nsay refresh\nsay refresh\n")
            #    sys.stdout.write("waiting for fly/refresh spells 20s...\n")
            #    time.sleep(20)
            #    self.go("sw")

            if "fly" not in self.aff:
                self.check_affectby()
                if "flying" not in self.affby:
                    self.status_msg= "Waiting for fly spells"
                    
                    if not self.clericon:                        
                        self.log_cleric()
                    if self.clericon:
                        self.cleric.godh()
                        self.godh()
                        self.time.sleep(5)
                        self.cleric.rod.write("cast fly %s\ncast refresh %s\ncast refresh %s\n"%(self.name,self.name,self.name))
                        self.time.sleep(5)
                        self.godh()
                    else:
                        self.godh()
                        self.go("nw;w;w;w")
                        self.rod.write("say #fly\n")
                        self.time.sleep(5)
                        self.go("e;e;e;se")
                    
                
                    self.phase = 1

            self.buf = ''
    
        
        if self.phase >= 2:

            self.timesinceready = self.time.time()
            self.get_loc()
            self.switch_runs = 0
            self.status_msg = "Getting ready to leave..."
            # cast on self before start
            if self.phase == 2 and self.level >= 18 and self.charclass == "Barbarian":
                self.rod.write("bear\neye\n")
            elif self.phase == 2 and self.level >= 18 and self.charclass == "Vampire":
                self.rod.write("occulutus\n")

            if "hide" in self.slist:
                self.rod.write("hide\n")

            self.time.sleep(1)

            # if has support (leech alt) then make sure to get parity
            print "SUPPORT-MASTER?", self.support, self.master
            

            if self.master == None and self.phase == 2:
                if "kills" not in self.alt_info:
                    self.alt_info['kills'] = {}

                if "buffer" not in self.alt_info:
                    try: self.alt_info = pickle.load(open("alts/info_%s.pckle"%self.name,'r'))
                    except: pass
                    if 'buffer' not in self.alt_info:
                        self.alt_info['buffer'] = set()
                        self.alt_info["clearbuffer"] = False

                allkills = self.alt_info['kills']
                if len(allkills) > 0:
                    for x in allkills.items():
                        self.printc("Killed %s %d times"%(x[0],x[1]))
                        if ((x[1] >= 12 and self.level >= 10 and x[0] != "A twisted bronze statue" and x[0] != 'A tw' and x[0] != 'The crab guard') or 
                            (x[1] >= 8 and self.level >= 24 and x[0] != "A twisted bronze statue" and x[0] != 'A tw' and x[0] != 'The crab guard') or
                            (x[1] >= 7 and self.level >= 38 and x[0] != "A twisted bronze statue" and x[0] != 'A tw' and x[0] != 'The crab guard') or
                            (x[1] >= 5 and self.level >= 45 and x[0] != "A twisted bronze statue" and x[0] != "A tw" and x[0] != 'The crab guard')):

                            self.alt_info["clearbuffer"] = True
                            self.alt_info['buffer'] = set()
                            self.alt_info['kills'] = {}

                if len(self.alt_info['buffer']) >= 23:
                    self.alt_info["clearbuffer"] = False
                    self.alt_info['buffer'] = set()
                    self.alt_info['kills'] = {}

                self.pickle.dump(self.alt_info, open("alts/info_%s.pckle"%self.name,'w'))

                if self.alt_info["clearbuffer"]:
                    self.printc("Going to clear buffer")
                    if not ("A small elemental" in self.alt_info['buffer'] or "An elemental puddle" in self.alt_info['buffer']):
                        return "canyon"
                    elif not ("A Halfling villager" in self.alt_info['buffer']):
                        return "shire"
                    else:
                        return "coral"
                self.printc("Good to go for now...")


                if self.level < 6:
                    return "gnome"
                elif self.level <= 10:
                    self.switch += 1
                    if self.switch % 2 == 0:
                        return "gnome"
                    else:
                        return "coral"
                elif self.level <= 13:
                    self.switch += 1
                    if self.switch % 2 == 0:
                        return "coral"
                    else:
                        return "art"
                elif self.level <= 22:
                    self.switch += 1
                    if self.switch % 3 == 0:
                        return "coral"
                    elif self.switch % 3 == 2:
                        return "toz"
                    else:
                        return "art"

                elif self.level <= 26:
                    self.switch += 1
                    if self.switch % 3 == 2:
                        return "coral"
                    else:
                        if self.switch % 3 == 0:
                            return "mith"
                        else:
                            return "art"

                elif self.level <= 50:
                    self.switch += 1

                    if self.random.random() < 0.08:
                        return "coral"
                    
                    if self.level >= 28:
                        if self.random.random() < 0.5:
                            self.check_time()
                            hour, am = self.mudtime
                            if (am == "am" and int(hour) == 12) or  (am == "am" and int(hour) <= 4) or (am == "pm" and int(hour) >= 6 and int(hour) != 12):
                                return "tom"

                    self.printc("SWITCH %d"%self.switch)
                    if self.level <= 35:
                        if self.switch % 4 == 0:
                            return "mith"
                        else:
                            return "art"
                    elif self.level <= 38:
                        if self.switch % 3 == 0:
                            return "mith"
                        else:
                            return "art"
                    elif self.level <= 41:
                        
                        if self.switch % 4 == 0:
                            return "winter"
                        elif self.switch % 4 ==2:
                            return "mith"
                        else:
                            return "art"
                    else:
                        #if self.switch % 4 == 0:
                        #    return "king"
                        #elif self.switch % 4 == 2:
                        #    return "canyon"
                        #else:
                        #    return "king"


                        
                        if self.switch % 2 == 0:
                            return "king"
                        elif self.switch % 2 == 1:
                            return "art"
                        
                        
                else:
                    return "exitexit"
        return False
        
    def check_prac_defunct(self):

        self.rod.write("slist 1 %d\nver\n"%self.level)
        self.buf = ''
        slist = None
        r = ''
        while slist == None:
            rl = self.rod.read_very_eager()
            r += rl
            if "SMAUG 2.6" in r:
                bsplt = r.split('\n')
                scan = False
                slist = []
                for i in range(len(bsplt)):
                    if "Skill:" in bsplt[i] or "Weapon:" in bsplt[i]:
                        sname, svalue = bsplt[i].split("%: ")
                        sname = sname.split(":")[-1].strip()
                        svalue = svalue.split()[0]
                        slist.append((sname, svalue))
        self.slist = slist
        

    def update_gear(self):
        # go to DH and barb donation to check for stuff
        #if self.charclass == "Barbarian": # check barb donation
        #    self.rod.write("get recall chest\nshatter recall\n")
        #    self.go("w;n;n;nw;w;n;nw;n;n;w")
        #    
        #    self.rod.write("\nsay I wish to visit the city dwellers\ns\ndr\nne\n")
        return

class Cleric:
    ''' class for activities in dhaven '''

    following = False
    trancing = False
    wait = 0
    def func_cleric(self):
        if self.wait %5 == 0: 
            self.printc("Trancing: %s Location: %s"%(self.trancing,self.location))
        
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
            if "sanctuary" not in self.aff:
                self.rod.write("cast sanc\n")
                self.trancing = False
            self.wait = 0
        
        if self.following:
            self.phase += 1
        self.wait += 1
        self.time.sleep(1)
        return False

    def quit(self,delay):
        self.time.sleep(delay)
        self.rod.write("quit\n")
        
    def check_lvlgear(self):
        self.check_cont("basket")
        return self.containers['basket']


class Support:
    ''' class for support leechers '''
    
    goDH = False
    goPlace = "dhaven"

    def func_support(self):
        
        # mostly checks that they are still following the lead character
        
        #if self.master.location != self.location:
        #    self.sys.stdout.write("Not at the same place as lead\n")
        #    self.rod.write("follow self\n")
        #    return "dhaven"
        
        # class specific actions
        if self.goDH:
            self.goDH = False
            return self.goPlace

        return False

    def gofunc(self,func):
        self.goDH = True
        self.goPlace = func

    def quit(self,delay):
        self.time.sleep(delay)
        self.rod.write("quit\n")


        
if __name__ == "__main__":
    import sys
    import time
    

    #r = starting_sequence(name,pw, cont, True)
    
    r = dhaven(name,pw, cont, False)
    

    print r.level, r.containers, r.location
    
    #r = gnome(name,pw,cont,False)
