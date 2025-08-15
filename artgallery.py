

class Art:     
    
    
    def func_art(self):
        # Check for healing at the start of each Art Gallery phase
        if hasattr(self, 'HP') and hasattr(self, 'MAXHP') and hasattr(self, 'sect_member'):
            if int(self.HP) < int(self.MAXHP) * 0.8:
                # Debug sect membership detection
                self.printc("DEBUG: SECT CHECK - hasattr:%s sect_member:%s level:%s" % (hasattr(self, 'sect_member'), getattr(self, 'sect_member', 'MISSING'), self.level), 'cyan')
                if self.sect_member and self.level >= 10:
                    self.printc("DEBUG: ART GALLERY HEALING for %s HP:%s/%s" % (self.name, self.HP, self.MAXHP), 'red')
                    self.rod.write("quaff heal %s\n" % self.container)
                    self.time.sleep(1)
                else:
                    self.printc("DEBUG: USING PURPLE HEALING for %s HP:%s/%s" % (self.name, self.HP, self.MAXHP), 'red')
                    self.rod.write("quaff purple %s\n" % self.container)
                    self.time.sleep(1)
        
        mobloc = {'By the "Demons Within" Sculpture':"phunbaba", "Welmar's Left Arm":"hand",
                  "Welmar's Right Arm":"hand", "Welmar's Right Foot":"foot", 
                  "Welmar's Left Foot":"foot",
                  "Black": "evil", "Red": "anger", "Orange": "life", "Indigo":"Confusion", 
                  "White":"innocence", "Violet": "love", "Lair of Aram-Dol": 
                  "aram", "The Arena":"giant",'By the "Metamorphosis" Sculpture':"bronze",
                  "large": "Swans Reflecting Elephants"
                  }

        
        print("*** ART ***", self.phase)
        #if self.clericon:
        #    if self.MV < 100:
        #        self.cleric.rod.write("cast refresh %s\ttrance\n"%self.name)

        if self.phase == 0:
            self.status_msg = "Start -- Art Gallery"
            self.todisarm = False
            self.check_affect()

            self.phasedir = {}
            self.phase = 1

            if not self.cleric_follow():
                self.phase = 0
            else:
                # Check if sect member - need to jig to Darkhaven Square first
                if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
                    self.rod.write("jig\n")
                    self.time.sleep(2)
                self.go("#4 s;w;#2 n")
             
        elif self.phase == 1:
            self.status_msg = "Finding mobs to kill -- Art Gallery"
            # initialize the circuit
            self.phase = 2
            self.whereami()

            
            if self.location != "Standing in the Foyer":
                # did not get to place                                                                                                                                        
                return 'dhaven'
            

            elif self.phase == 2:
                self.rod.write("config -autosac\n")
                self.phasedir = {}
                prestigeclass = ['Harbinger']
                if self.level <= 12: # just welmar's feet
                    dirs = '*n;*n;*w;*nw;*w;*nw;*enter;u;*w;*w;*d;u'.split(";")
                    self.cankill = ["foot"]
                elif self.level <= 17: # welmar's feet and hands
                    self.cankill = ["hand","foot"]
                elif self.level <= 19:
                    self.cankill = ["hand"]
                    
                    if self.level >= 18 and self.charclass in prestigeclass:
                        self.cankill += ["love"]
                elif self.level <= 21:
                    self.cankill = ["love","hand"]
                    if self.level >= 20 and self.charclass in prestigeclass:
                        self.cankill += ['confusion']
                elif self.level <= 23:
                    self.cankill = ["love","confusion","hand"]
                    if self.level >= 20 and self.charclass in prestigeclass:
                        self.cankill +=['life']
                elif self.level <= 29:
                    self.cankill = ["anger","life","love","confusion"]
            
                elif self.level <= 35:
                    if self.random.random() < 0.5:
                        self.cankill = ["anger","life","love","confusion",'bronze']
                    else:
                        self.cankill = ["anger","life","love","confusion"]
                    if self.level >= 34 and self.charclass in prestigeclass:
                        self.cankill = ["evil", "life","love","melancholy","innocence",'large','bronze']
                elif self.level <= 38:
                    
                    self.cankill = ["evil", "life","love","melancholy","innocence",'large','bronze']
                    
                elif self.level <= 40:
                    self.cankill = ["evil", "phunbaba","life","melancholy","innocence",'bronze']
                elif self.level <= 43:
                    self.cankill = ["giant","phunbaba","evil","melancholy",'bronze']
                elif self.level <= 46:
                    self.cankill = ["aram","evil",'bronze']
                else:
                    self.cankill = ["aram","giant","evil"]
                self.cankill += ['twisted']

                if not self.clericon:
                    try: self.cankill.remove("large")
                    except: pass
                    
                if self.charclass in ["Vampire",'Mage',"Nephandi"]:
                    try: self.cankill.remove("phunbaba")
                    except: pass
                    if self.charclass == "Vampire":
                        try: self.cankill.remove("bronze")
                        except: pass
                    
                self.random.shuffle(self.cankill)
                
                tokill = self.check_mobs()
                if tokill != "phunbaba":
                    try: self.cankill.remove("phunbaba")
                    except: pass
                elif tokill != "bronze":
                    try: self.cankill.remove("bronze")
                    except: pass

                self.printc("GOING TO KILL %s..."%tokill)
                if tokill == None:
                    return 'dhaven'
                
                # Check if leveling spells need refreshing before combat
                self.check_affect()  # Update current spell durations
                needs_refresh, low_spells = self.check_leveling_spells()
                if needs_refresh:
                    self.printc("Low spells detected: %s" % ", ".join(low_spells), 'red')
                    # Save current location
                    current_location = self.location
                    # Refresh spells
                    self.refresh_leveling_spells()
                    # Return to Art Gallery
                    self.printc("Returning to Art Gallery after spell refresh...", 'cyan')
                    return 'art'  # Restart the art gallery function with fresh spells

                if tokill in ["hand"]:
                    if self.level < 18:
                        dirs = '*n;*n;*w;*nw;*w;*nw;*enter;u;*w;*w;*d;u;*e;*u;*w;e;*e;w'
                    else:
                        dirs = '*n;*n;*w;*nw;*w;*nw;*enter;*u;*w;*u;*e;w;*w;e'
                elif tokill == "foot":
                    dirs = '*n;*n;*w;*nw;*w;*nw;*enter;u;*w;*w;*d;u'
                elif tokill in ["love","confusion"]:
                    dirs = '*n;*n;*e;*se;*e;*se;*e;*ne;*enter;*config +autoloot;e;e;e;w;*config -autoloot'
                elif tokill in ["life"]:
                    dirs = '*n;*n;*e;*se;*e;*se;*e;*ne;*enter;*config +autoloot;w;w;e;e;e;e;e;w;*config -autoloot'
                elif tokill in ["anger"]:
                    dirs = '*n;*n;*e;*se;*e;*se;*e;*ne;*enter;*config +autoloot;w;w;anger;e;e;e;e;e;e;w;*config -autoloot'
                    if self.level >= 30:
                        dirs = '*n;*n;*n;*ne;*n;*nw;*n;s;*se;*s;*sw;*s;*e;*ne;*e;*se;e;se;*enter;*config +autoloot;w;w;anger;e;e;e;e;e;e;w;*config =autoloot'
                elif tokill in ['evil']: 
                    dirs = '*n;*n;*e;*se;*e;*se;*e;*ne;*enter;*config +autoloot;*d;u;*u;d;w;w;anger;e;e;e;e;e;e;w;*config -autoloot'
                    if self.level >= 30:
                        dirs = '*n;*n;*n;*ne;*n;*nw;*n;s;*se;*s;*sw;*s;*e;*ne;*e;*se;e;se;*enter;*config +autoloot;*d;u;*u;d;w;w;anger;e;e;e;e;e;e;w;*config -autoloot'
                    elif self.level >= 38:
                        dirs = '*n;*n;*n;*ne;*n;*nw;*n;s;*se;*s;*sw;*s;*e;*ne;*e;*se;e;se;*enter;*config +autoloot;*d;u;*u;d'
                elif tokill in ["aram"]:
                    dirs = '*n;*n;*n;*nw;*n;*nw;*n;*ne;*n;*enter;*d;*open wall;*s;*look'
                elif tokill in ['giant']:
                    dirs = '*n;*n;*e;*ne;*e;*ne;*e;*enter;*look'
                elif tokill in ['large']:
                    dirs = '*n;*n;*w;*sw;*w;*sw;*w;*nw;*enter;*look'
                elif tokill in ['bronze']:
                    dirs = '*n;*n;*n;*ne;*n;*nw;*n;s;*se;*s;*sw;*s;*e;*ne;*e;*se;e;se;*enter;*config +autoloot;*d;u;*u;d;*config -autoloot'
                else:
                    dirs = '*n;*n;*n;*ne;*n;*nw;*n;s;*se;*s;*sw;*s;*e;*ne;*e;*se;e;se;*enter;*config +autoloot;*d;u;*u;d;*config -autoloot'
                    
                    #dirs = '*n;*n;*e;*se;*e;*se;*e;*ne;*enter;*config -autosac;*d;u;u*;d;w;w;w;e;e;e;e;e;e;w;*config +autosac'
                dirs += ';*look'
                #elif tokill in ['statue']:
                #    dirs = '*n;*n;*e;*ne;*e;*se;*e;se;*enter;*config -autosac;w;w;w;e;e;e;e;e;e;w;*config +autosac'

                for skill in self.slist:
                    if "disarm" == skill[0] and skill[1] != "0":
                        self.todisarm = True

                print(self.todisarm)
                dirs = dirs.split(';')
                for i in range(len(dirs)):
                    self.phasedir[i+2] = dirs[i]


                self.check_inv()
                # open the door
                if 'the Art Gallery key' in self.inv:
                    self.rod.write("unlock north\nopen north\n")
                elif True in ['A silver key with the initials "D A G"' in x for x in self.roomitems]:
                    self.rod.write("get art\nunlock north\nopen north\ndrop art\n")
                else:
                    self.rod.write("give 5k coin kelly\nunlock north\nopen north\ndrop art\n")

                
                for i in range(len(dirs)):
                    self.phasedir[i+2] = dirs[i]
                
        elif self.phase >= 2 and not self.fight:
            if self.clericon:
                if self.cleric.fight:
                    return False
            self.status_msg = "Killing stuff -- Art Gallery"
            # now go through shattered refuge one room at the time
            # 1) check no one else is in my room
            # 2) check mobs
            # 3) kill mobs if there
            # 4) move
            
            self.disarm = self.todisarm
                
            mobnames = {"The humongous right":'foot',
                        "The monstrous left":'foot',
                        "The gigantic right":'hand',
                        "Welmar's enormous left": 'hand',
                        "A purple cloud": 'love',
                        "A dark blue": 'confusion',
                        "An orange glow": 'life',
                        "A red mist":"anger",
                        "Sadness washes over":"melancholy",
                        "Anger is here,":"anger",
                        "A hideous-looking sculpture":"phunbaba",
                        "A large bronze":"bronze",
                        "A large mass": "evil",
                        "A storm giant": "giant",
                        "A skeletal being": "aram",
                        "A large swan": "large",
                        "A beautiful swan": "swan",
                        "Long trunk extended,":"elephant",
                        "A twisted bronze":"twisted"
                }

            mobs = {}
            for k in mobnames:
                mobs[k] = 0
            
            if self.phase % 5 == 0:
                # every few rooms check effects                                                                                                                                                                       

                self.check_affect()
                getsanc = False
                # Skip sanctuary wait if we have potions or cleric
                has_sanctuary_support = self.clericon
                if self.level >= 10 and self.sect_member:
                    sanctpotname = "a sanctuary potion"
                    if sanctpotname in self.containers.get(self.container, {}):
                        if self.containers[self.container][sanctpotname] > 0:
                            has_sanctuary_support = True
                
                if has_sanctuary_support:
                    # We have sanctuary support, just refresh when needed
                    if "sanctuary" not in self.aff:
                        getsanc = True
                else:
                    # Only wait if no sanctuary support available
                    if "sanctuary" in self.aff:
                        if self.aff['sanctuary'] < 10:
                            self.time.sleep(self.aff['sanctuary']*3.2)
                            getsanc = True
                    else:
                        getsanc = True
                getlvl = False
                if "trollish vi" in self.aff:
                    if self.aff['trollish vi'] < 15:
                        self.time.sleep(self.aff['trollish vi']*3.2)
                        getlvl = True
                else:
                    getlvl = True
                if getsanc and not self.fight:
                    self.check_spells()
                    self.time.sleep(2)
                    self.check_affect()
                    if "sanctuary" not in self.aff:
                        
                        if self.clericon:
                            self.cleric.quit()
                            self.clericon = False

                        return "dhaven"

            if self.phase in self.phasedir:
                self.whereami()
                self.sys.stdout.write("\n%s: roomitems: %s\n"%(self.name, ",".join(self.roomitems)))
                
                for item in self.roomitems:
                    mob = " ".join(item.split()[:3]).strip()
                    if mob in mobs:
                        mobs[mob] += 1

                
                # am I alone here?
                alone = True

                if self.clericon:
                    trusted = [self.name.capitalize(), self.cleric.name]
                else:
                    trusted = [self.name.capitalize()]
                for character in self.loc_dic:
                    if character in trusted:
                        continue
                    if self.support != None:
                        if character ==self.support.name:
                            continue
                    if self.loc_dic[character] == self.location:
                        alone = False
                print(self.loc_dic)
                print("Alone?", alone)
                # should I fight?
                if alone:
                    for mob in mobs:
                        if mobs[mob] > 0 and mobnames[mob] in self.cankill:
                            # Ensure spring exists in THIS room before attacking the mob
                            self.printc("About to fight %s in %s - ensuring spring exists" % (mobnames[mob], self.location), 'gold')
                            self.ensure_spring_exists()
                            
                            # Now attack normally - spring is verified to exist
                            self.rod.write("kill %s\n"%(mobnames[mob]))
                            self.target = mobnames[mob]
                            self.fight = True
                            
                # Check for healing during combat in Art Gallery
                if self.fight and hasattr(self, 'HP') and hasattr(self, 'MAXHP'):
                    if int(self.HP) < int(self.MAXHP) * 0.8:
                        # Debug sect membership detection during combat
                        self.printc("DEBUG: COMBAT SECT CHECK - hasattr:%s sect_member:%s level:%s" % (hasattr(self, 'sect_member'), getattr(self, 'sect_member', 'MISSING'), self.level), 'cyan')
                        if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
                            self.printc("DEBUG: ART GALLERY COMBAT HEALING for %s HP:%s/%s" % (self.name, self.HP, self.MAXHP), 'red')
                            self.rod.write("quaff heal %s\n" % self.container)
                        else:
                            self.printc("DEBUG: USING PURPLE COMBAT HEALING for %s HP:%s/%s" % (self.name, self.HP, self.MAXHP), 'red')
                            self.rod.write("quaff purple %s\n" % self.container)
            else:
                
                self.sys.stdout.write("DONE THIS ROUND...\n")
                if len(self.inv) > 3:
                    self.rod.write("wear oar\nwear oar\nwear hammer\nwear hammer\nwear all\ndrop all\nget %s\nget recall\n"%self.container)
                    self.time.sleep(2)

                #if self.clericon:
                #    self.cleric.godh()

                N = 0
                if "curse" in self.aff:
                    if self.clericon:
                        self.cleric.rod.write("c 'remove curse' %s"%self.name)
                    else:
                        self.rod.write("quaff gut %s\n"%self.container)
                    self.time.sleep(6)
                self.check_affect()
                
                #self.rod.write("quit\n")
            
                self.time.sleep(1)
                rl = self.read()
                self.sys.stdout.write("\n%s: %s\n"%(self.name,rl))
                self.time.sleep(1)


                # if tokill phunbaba, etc, then go on
                tokill = self.check_mobs()
                self.printc("Still left %s"%tokill)
                if tokill != None and tokill != "phunbaba" and self.random.random() < 0.8:
                    self.switch -= 1
                self.rod.write("config +autosac\n")
                if "curse" in self.aff:
                    self.rod.write("supplicate recall\n")
                if self.clericon:                                                                                                                                                                           
                    self.cleric.godh() 
                return 'dhaven'



            movenext = True
            if self.clericon:
                if self.cleric.fight:
                    movenext = False
            if not self.fight and movenext:
                if True:
                    self.check_inv()
                    print(self.inv)
                    for c in ["an onyx whip","an ivory rapier","a blue topaz glove","an amethyst gauche","a ruby sabre","a sapphire scythe","a topaz staff"]:
                        for item in self.inv:
                            if c in item:
                                it = c.split()[-1]
                                if self.clericon:
                                    self.rod.write("give %s %s\ndrop glass\n"%(it, self.cleric.name))
                                    self.time.sleep(1)
                                    self.cleric.rod.write("c midas %s\nc midas %s\ntrance\n"%(it,it))
                                self.time.sleep(1)
                                self.rod.write("drop %s\n"%(it))   
                                
                d = self.phasedir[self.phase]

                movecleric = None
                if d == "statue":
                    if self.clericon:
                        self.cleric.whereami()
                        if self.cleric.location == "Hallway":
                            self.cleric.rod.write("e\nc 'create spring'\nse\n")
                            self.time.sleep(2)
                    d = "*e"
                elif d == "anger":
                    if not self.fight:
                        if self.clericon:
                            self.cleric.rod.write("sit\n")
                            self.time.sleep(5)
                            movecleric = "w"
                        d = "*w"
                    else:
                        d = "*look"
                        
                if "*" in d:
                    self.rod.write(d[1:]+'\n')
                else:
                    self.go(self.phasedir[self.phase])
                    
                if movecleric != None:
                    self.cleric.rod.write("wake\n")
                    self.cleric.rod.write(movecleric+'\n')

                self.phase += 1
                #self.time.sleep(.5)  
        return False
    
    def check_mobs(self, p = True):
        ''' check that some of the mobs to be killed are free and there '''
        locations = {}
        for mob in self.cankill:
            if mob == "twisted": continue
            self.rod.write("where %s\nver\n"%mob)
            rl = ''
            while True:
                rl += self.read()
                if "SMAUG 2.6" in rl:
                    if p: 
                        self.sys.stdout.write("\n%s: %s\n"%(self.name,rl))
                    for ln in rl.split('\n'):
                        if "|" in ln and "at" in ln:
                            locations[ln.split("at ")[-1]] = mob
                    break
        self.whereami()

        for alt, location in list(self.loc_dic.items()):
            if alt in ["Kaeval", "Kaetas"]:
                continue
            if location in locations:
                locations.pop(location)
    
        for mob in self.cankill:
            if mob in list(locations.values()):
                return mob
            
        return None
        
