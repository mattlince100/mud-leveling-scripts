

from telnetlib_compat import Telnet

class Helper:


    def log_alt(self, name):

        self.alt = Telnet("realmsofdespair.com",4000)
        
        # Monkey patch for Python 3 compatibility
        original_write = self.alt.write
        def write_with_encoding(text):
            if isinstance(text, str):
                original_write(text.encode('ascii'))
            else:
                original_write(text)
        self.alt.write = write_with_encoding
           
        self.alt.write("%s\n"%name)
        self.time.sleep(2)
        buf = self.alt.read_very_eager()
        if isinstance(buf, bytes):
            buf = buf.decode('ascii', errors='replace')
        print("\n%s: %s"%(name,buf))

        if name in ["Xixili", "Lasonas"]:
            pw = "yaoyao2020"
        elif name in ["Dresden", "Lore", "Daltin"]:
            pw = "Elijah"
        else:
            pw = "1q2w3e4r"

        
        if "That character is already connected - try again in a few minutes." in buf:
            return False
        else:
            self.alt.write("%s\n\n \n \nconfig -ansi\nconfig -autosac\nconfig -autoloot\n"%pw)
            self.alt.write("wake\nconfig +gag\nwimpy 0\n\n")

        return True


    def log(self):

        self.rod = Telnet("realmsofdespair.com",4000)
        
        # Monkey patch for Python 3 compatibility
        original_write = self.rod.write
        def write_with_encoding(text):
            if isinstance(text, str):
                original_write(text.encode('ascii'))
            else:
                original_write(text)
        self.rod.write = write_with_encoding
                        
        self.rod.write("%s\n"%self.name)
        self.time.sleep(2)
        self.buf = self.read()
        print("\n%s: %s"%(self.name,self.buf))

        if self.name in ["Xixili", "Lasonas"]:
            pw = "yaoyao2020"
        elif self.name in ["Dresden", "Lore", "Daltin"]:
            pw = "Elijah"
        else:
            pw = "1q2w3e4r"

        
        if "That character is already connected - try again in a few minutes." in self.buf:
            self.quit()
        else:
            # Send password with extra newlines to get through MOTD
            self.rod.write("%s\n\n \n \n"%pw)
            self.time.sleep(3)
            self.rod.write("config -ansi\nconfig -autosac\nconfig -autoloot\n")
            self.rod.write("wake\nconfig +gag\nwimpy 0\n\nfollow %s\n"%self.leader)

        # Find potions/container

        self.time.sleep(.5)
        
        self.charclass = None

        if True:
            self.check_affect()
        if False:
            self.whereami()


        if self.charclass in ["Dread", "Vampire"]:
            self.rod.write("prompt ("+self.name.lower()+") &w&Y%h/%Hhp &C%b/%Bmn &G%v/%Vmv&w &Y%gg &r&w%aa &p%i%\n")
            self.rod.write("fprompt ("+self.name.lower()+")F &w&Y%h/%Hhp &C%b/%Bmn &G%v/%Vmv&w [%n] &r&w%aa &p%i%a &w(&R%c&w) .:%L:.\n")
        else:
            self.rod.write("prompt ("+self.name.lower()+") &w&Y%h/%Hhp &C%m/%Mmn &G%v/%Vmv&w &Y%gg &r&w%aa &p%i%\n")
            self.rod.write("fprompt ("+self.name.lower()+")F &w&Y%h/%Hhp &C%m/%Mmn &G%v/%Vmv&w [%n] &r&w%aa &p%i%a &w(&R%c&w) .:%L:.\n")

        self.time.sleep(2.5)
        
        self.loadvars()

        if self.charclass == "Barbarian":
            self.recallname = "a Barbarian stone of recall"
        else:
            self.recallname = "a recall scroll"

        if self.charclass in ["Cleric", "Mage", "Nephandi"]:
            self.nextfunc = "cleric"
            self.func = self.func_cleric
        else:
            self.func = self.func_wait


        self.initrun()

        self.main_loop()
    
    def quit(self, action = 'quit'):
        self.quitflag = True
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
        self.time.sleep(1)
        if "Your surroundings begin to fade" not in self.read():
            self.quit()       

    def waitcmd(self,cmd, p = False):
        self.time.sleep(0.1)
        r = self.read()
        self.printc(self.name+":" +cmd,'blue')
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
            t = self.time.time()-start
            if t > 20:
                break
            self.time.sleep(0.5)
        
        #rflush = self.read()
        #self.printc(self.name+" did " +cmd.replace("\n",";") + " in %f seconds, read %d chars."%(t,len(rflush)),'blue')
        
        if p:
            self.printc(r)
        return r


    def loadvars(self):
        try: self.vars = pickle.load(open("chars/vars_%s.pck"%self.name))
        except: self.vars = {}

        if "recall" not in self.vars:
            self.check_prac()
            if "word of recall" in self.slist:
                self.vars["recall"] = ("spell", None)
            else:
                loc = self.find_item("a recall scroll")
                self.vars['recall'] = ("scroll", loc)
                if self.charclass == "Barbarian":
                    loc = self.find_item("a Barbarian stone of recall")
                    self.vars['recall'] = ("stone", loc)

        print("vars", self.vars)
        self.pickle.dump(self.vars, open("chars/vars_%s.pck"%self.name,'wb'))

    def cmdandwait(self,cmd, string):
        # perform a command and wait till you get a string match

        p = self.waitcmd(cmd)
        print(p)
        if string in p:
            return True
        else:
            return False


    def waitcmd2(self,cmd, p = False):
        ''' sometimes using waitcmd does not work well and should alternate '''
        self.time.sleep(0.1)
        r = self.read()
        #self.printc(self.name+":" +cmd,'blue')
        if p:
            self.sys.stdout.write(r)

        self.rod.write("%s\nbeck\n"%cmd)
        self.time.sleep(0.1)
        r = ''
        start = self.time.time()
        while  True:
            r += self.read()
            if "Who do you wish to beckon?" in r:
                break
            t = self.time.time()-start
            if t > 20:
                break
            self.time.sleep(0.5)

        rflush = self.read()

        if p:
            self.printc(r)
        return r


    def read(self):
        ''' read everywhere goes here
        This now includes fighting as well and HP checks '''

        r = self.rod.read_very_eager()
        if isinstance(r, bytes):
            r = r.decode('ascii', errors='replace')
        
        rln = [x for x in r.split('\n\r') if r != '']
        #print "read", rln

        for i in range(len(rln)):      

            #HP CHECKS and FIGHT CHECKS
            ln = rln[i]
      
            self.triggers(ln)
            self.check_disarm(ln)

            if "(%s)"%self.name.lower() in ln:
                if "&" in ln: continue
                try:
                    self.HP, self.MAXHP = ln.strip().replace("hp","").split()[1].split("/")
                    self.MP, self.MAXMP = ln.strip().replace("mn","").split()[2].split("/")
                    self.MV, self.MAXMV = ln.strip().replace("mv","").split()[3].split("/")
                    self.HP, self.MAXHP = int(self.HP), int(self.MAXHP)
                    self.MP, self.MAXMP = int(self.MP), int(self.MAXMP)
                    self.align = ln.strip().split("mv ")[-1].split("a ")[0].split()[-1].strip('a')
                    self.align = int(self.align)
                except:
                    pass
                
                if "(%s)F "%self.name.lower() in ln:
                    self.fight = True
                    # gets mob words
                    self.fighting = ln.split('[')[-1].split(']')[0]
                    self.kw = None
                    if self.fighting in self.autotargetdic:
                        self.kw = self.autotargetdic[self.fighting]
                else:
                    #self.manaup
                
                    self.fight = False
                    cspring = False
                    makespring = False
                            
            if "Your opponent is not wielding a weapon" in ln:
                self.disarm = False

            if "Your stomach if getting full" in ln:
                self.gettingfull = True

            if "Your stomach cannot contain any more." in ln:
                # try to drink and/or make spring
                self.full = True
                self.rod.write("drink\n")

            if "You drink from" in ln or "You drink deeply from" in ln:
                self.full = False
                self.gettingfull = True

            if "exclaims 'fol!'" in rln[i]:
                char = rln[i].split()[0]
                if char in self.trusted:
                    self.waitcmd("follow %s"%char)

            elif "tells you '" in rln[i]:
                char = rln[i].split()[0]
                if char in self.trusted:
                    cmd = rln[i].split("you '")[-1].split("'")[0]
                    if cmd == "recall":
                        self.nextfunc = 'dhaven'
                        self.godh("recall")
                    else:
                        self.waitcmd(cmd)                

            elif "is DEAD!!" in rln[i]:
                k = rln[i].split(" is")[0]
                self.printc("%s: %s is dead"%(self.name, k),'red')
                self.fight = False
                print(self.fighting, k)
            
                self.fighting = ''
            elif "tells the group 'stat'" in rln[i]:
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
                

            if "says '" in rln[i]:
                char = rln[i].split()[0]
                if char in self.trusted:
                    action = rln[i].split("says '")[-1].split("'")[0]
                    self.waitcmd(action)
            


            if "tells the group 'handgold'" in rln[i]:
                char = rln[i].split()[0]
                if char in self.trusted:
                    self.check_affect(p=True)
                    give = self.gold-1e6
                    if give > 0:
                        self.waitcmd("give %d coin %s"%(give, char))

            if "tells the group 'do " in rln[i]:
                char = rln[i].split()[0]
                if char in self.trusted:
                    action = rln[i].split("'do ")[-1].split("'")[0]
                    self.waitcmd(action)

            if "tells the group 'restock" in rln[i]:
                char = rln[i].split()[0]
                if char in self.trusted:
                    self.godh('recall')
                    self.resotck()

            if "You slowly float to the ground." in rln[i]:
                self.waitcmd("say let me fly!")
                self.waitcmd("sit broom")

            if "..Everything begins to fade to black." in rln[i]:
                # I died
                self.quit()
                self.status = "quit"

            if "You come out of your trance." in rln[i]:
                self.trancing = False

            if "You enter a peaceful trance, collecting mana from the cosmos." in rln[i]:
                self.trancing = True

            if "Exits: " in rln[i]:
                self.movement += 1
            if "You follow" in rln[i]:
                self.trancing = False
                self.location = None
                self.following = True

            if "They aren't here." in rln[i] or "You can't circle" in rln[i]:
                self.target = None
                self.forcetarget = None

            if "gets damaged" in rln[i]:
                self.eqdam = True
        return r