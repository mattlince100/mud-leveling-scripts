

class Gnome:
    
    def func_gnome(self):

        if int(self.HP) < int(self.MAXHP)-30:
            if self.level <= 7:
                self.pot = "maroon"
            else:
                # Sect members use 'heal' keyword, others use 'purple'
                if hasattr(self, 'sect_member') and self.sect_member and self.level >= 10:
                    self.pot = "heal"
                else:
                    self.pot = "purple"
                
            self.rod.write("quaff %s %s\n"%(self.pot, self.container))
            
        if self.phase == 0:
            self.phasedir = {}
            self.phase = 1
            
            if not self.cleric_follow():
                self.phase = 0
            else:
                self.godh()
                self.go("#9 s;w;#3 s;#4 w")
                self.whereami()
            
        elif self.phase == 1:
            # initialize the circuit
            self.status_msg = "On the way to Shattered Refuge"
            self.phase = 2
            
            if self.support != None:
                try: self.support.whereami()
                except:
                    self.printc("Encountered a problem with support (%s)"%self.support.name)
                    self.support.stop = True
                    return 'dhaven'
                if self.support.location != "A thin trail":
                    return 'dhaven'
                    
            if self.location != "A thin trail":
                # did not get to place
                return 'dhaven'
            elif self.phase == 2:
                self.phasedir = {}
            
                if self.level >= 7:
                    dirs = 'nw;w;w;n;w;w;e;e;e;e;w;w;n;w;w;e;e;n;s;e;e'.split(";")
                elif self.level <= 4:
                    dirs = 'nw;w;s;s;s;e;e;w;s;n;w;s;n;w;e;n;n;n;w'.split(";")
                else:
                    dirs = 'nw;w;s;s;s;e;e;w;s;n;w;s;n;w;e;n;n;n;w;n;w;w;e;e;e;e;w;w;n;w;w;e;e;n;s;e;e'.split(";")

                for i in range(len(dirs)):
                    self.phasedir[i+2] = dirs[i]

                self.cankill = ['A gnome child', 'A gnome woman']
                
                if self.level >= 3:
                    self.cankill.append('A gnome man')
                if self.level >= 5:
                    self.cankill.append('An assistant scientist')
                    self.cankill.remove("A gnome child")
                if self.level >= 6:
                    self.cankill.remove("A gnome woman")
                    self.cankill.append('A scientist wanders')
                if self.level >= 7:
                    self.cankill.append('A particularly mean')
                if self.level >= 8:
                    self.cankill.remove("A gnome man")

                
        elif self.phase >= 2 and not self.fight:
            # now go through shattered refuge one room at the time
            # 1) check no one else is in my room
            # 2) check mobs
            # 3) kill mobs if there
            # 4) move
            self.status_msg = "Killing gnomes -- Shattered Refuge"
            
            if self.phase % 3 == 0:
                # every few rooms check effects                                                                                                                                                                        
                self.check_affect()
                getsanc = False
                if "sanctuary" in self.aff:
                    if self.aff['sanctuary'] < 10:
                        getsanc = True
                else:
                    getsanc = True

                getlvl = False
                if "trollish vi" in self.aff:
                    if self.aff['trollish vi'] < 15:
                        getlvl = True
                else:
                    getlvl = True
                    
                if getsanc or getlvl:
                    self.status_msg = "Going back to DH to get spells..."

                    if self.support != None:
                        self.support.gofunc("dhaven")
                        self.time.sleep(1)
                    return "dhaven"

            
            self.mobs = {"A gnome man":0,
                         "A gnome woman":0,
                         "A gnome child":0,
                         "A scientist wanders": 0,
                         "A particularly mean": 0,
                         "An assistant scientist":0}
            
            self.mobnames = {"A gnome man":'man',
                             "A gnome woman":'woman',
                             "A gnome child":'child',
                             "A scientist wanders": 'scientist',
                             "A particularly mean": 'guard',
                             "An assistant scientist":'assistant'}

            if self.phase in self.phasedir:
                self.whereami()
                
                
                self.printc("\n%s: roomitems: %s\n"%(self.name, ",".join(self.roomitems)),'blue')


                for item in self.roomitems:
                    mob = " ".join(item.split()[:3])
                    if mob in self.mobs:
                        self.mobs[mob] += 1

                # am I alone here?
                alone = True
                if self.clericon:
                    trusted = [self.name.capitalize(), self.cleric.name]
                else:
                    trusted = [self.name.capitalize()]
                if self.support != None:
                    trusted += [self.support.name]
                for character in self.loc_dic:
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
                    for mob in self.mobs:
                        if self.mobs[mob] > 0 and mob in self.cankill:
                            # Check if leveling spells need refreshing before combat
                            self.check_affect()  # Update current spell durations
                            needs_refresh, low_spells = self.check_leveling_spells()
                            if needs_refresh:
                                self.printc("Low critical spells detected before combat: %s" % ", ".join(low_spells), 'red')
                                self.refresh_leveling_spells()
                                self.printc("Spells refreshed, returning to Gnome Village...", 'green')
                                return "continue"  # Stay in this area and re-evaluate
                            
                            self.rod.write("kill %s\n"%(self.mobnames[mob]))
                            self.fight = True
            else:

                self.sys.stdout.write("\nDONE THIS ROUND, WAIT 10s...\n")
                
                self.time.sleep(10)
                return 'dhaven'

            if not self.fight:
                if self.support != None:
                    if self.support.fight:
                        return False
                
                self.go(self.phasedir[self.phase])
                self.phase += 1
                #self.time.sleep(.5)
            
            
        return False
