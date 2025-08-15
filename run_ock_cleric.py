from telnetlib_compat import Telnet
import sys
import time

user, pw, container = "Marrill", "1q2w3e4r", "chest"


month,date =time.ctime().split()[1:3]
year = time.ctime().split()[-1]

logW = open("logs/log_oakwater_%s_%s_%s.txt"%(year,date,month),'a')

safechars = ["Kaerim", "Kaetas", "Keamval", "Grotok"]
midascontainer = "chest"
returnchar = None
HP,maxHP = 100, 100
MP,maxMP = 100, 100
gold = None
cgold = None


def get_hpmp(buf):
    global MP, HP, maxHP, maxMP, gold
    for ln in buf.split('\n'):
        ln = ln.strip()
        if user.capitalize() in ln or user.lower() in ln or "Standard" in ln: # prompt
            #print [ln]
            
            #print [ln]
            #print ln.split("Hp ")[0].split("m")[-1]
            #print ln
            try: 
                HP,maxHP = tuple(ln.split("hp ")[0].split(")")[-1].split("/"))
                MP, maxMP = tuple(ln.split("mn ")[0].split(" ")[-1].split("/"))
                HP, maxHP = int(HP), int(maxHP)
                MP, maxMP = int(MP), int(maxMP)
            except:
                continue

            #print ("You have %d out of %d manapoint.."%(MP, maxMP))
            #print ("You have %d gold coins"%(gold))
    
def tranceup(rod):
    buf = ''
    rod.write("trance\n")

    N = 0
    while MP < maxMP-50:
        time.sleep(4)
        print("trancing...(%d/%d) %d"%(MP,maxMP, N))
        buf += read(rod)
        if "\r\n" in buf:
            get_hpmp(buf)
        buf = ''
        N += 1
        if N > 4:
            N = 0
            rod.write("where\nver\n")
            r = ''
            while True:
                r += read(rod)
                if "SMAUG" in r:
                    print r
                    rod.write("trance\n")
                    if not isalone(r):
                        rquit(rod)
                    break

    print("Done trancing")


def isalone(buf):

    buf = buf.split('\n')
    for i in range(len(buf)):
        if "Players near you in" in buf[i].strip():
            printT = True
            break
    if printT:
        if len(buf[i+2].strip()) == 0 or "|" not in buf[i+2]:
            return True
        else:
            return False
    

def gokill():
    global switch
    # connect
    rod = Telnet("realmsofdespair.com",4000) 
    rod.write("%s\n%s\n\n \n \n"%(user,pw))
    rod.write("config -ansi\n")
    log = []
    buf = ''
    start = time.time()
    #print "go back"

    
    rod.write("look\nver\n")
    r = ''
    while True:
        l = read(rod)
        r += l
        if len(l) > 0:
            sys.stdout.write(l)
        
        if "SMAUG 2.6" in r:
            if "The Chief's Chamber" not in r:
                go_back(rod)
            break

    #rquit(rod)
    
    read(rod)
    rod.write('where\nver\n')
    r = ''
    while True:

        l = read(rod)
        r += l
        if len(l) > 0:
            sys.stdout.write(l)
        if "SMAUG 2.6" in r:
            get_hpmp(r)

            if int(MP) < 400:
                print MP, maxMP
                tranceup(rod)

            print r
            if not isalone(r):
                rod.write("quit\n")
                v = ''
                while "fades to black" not in v:
                    v += read(rod)
                    if "SMAUG" in v: 
                        print v
                        
                return 60
            break

    
    
    time.sleep(6)

    spells = ["fireshield","resilience","fly", "create spring","sanctuary"][1:]
    while len(spells) > 0:
        # check i) spring, ii) fireshield, iii) demonskin
        print "!",spells
        rod.write("aff\nlook\nver\n")
        while True:
            buf += read(rod)
            if "SMAUG 2.6" in buf:
                print buf
                get_hpmp(buf)
                if MP < 400: tranceup(rod)
                toremove = []
                for ln in buf.split('\n'):
                    for spell in spells:
                        if "Affected:" in ln and spell in ln:
                            if spell not in toremove and spell in spells:
                                toremove.append(spell)
                            print "!",ln.strip()
                    if "A mystical spring flows majestically from a glowing circle of blue." in ln:
                        if 'create spring' not in toremove and 'create spring' in spells:
                            toremove.append("create spring")

                for spell in toremove:
                    print "Has %s..."%spell
                    spells.remove(spell)
                print "Spells to be casted: ", spells
                for spell in spells:
                    rod.write("cast '%s'\n"%spell)
                buf = ''
                break

    buf = ''
    fighting = False
        
    quaffing = False
    while True:
        done = False
        time.sleep(2)
        timer = time.time()-start
        if not fighting:
            rod.write('where\nwhere Garsnagg\n')#"examine %s\ninv\n"%midascontainer) # midas items

        rl = read(rod)
        sys.stdout.write(rl)
        buf += rl
        
        if "\r\n" in buf:
            get_hpmp(buf)
                   
            alone = False
            # get players near you
            if fighting:
                rod.write("c virtue kilgore\nc virtue gar\nc virtue warrior\n")
                time.sleep(3)
            if "Players near you" in buf:
                alone = isalone(buf)

                if not alone:
                    break

            for ln in buf.split('\n'):
               if "The corpse of Garsnagg holds:" in ln:
                   #rod.write("get club gars\nsac co\n")
                   rod.write("c 'create spring'\nget turkey basket\ndrop turkey\ntrance\n")
                   midas(rod)
                   time.sleep(4)
                   rod.write("fill basket turkey\nw\nn\ne\n")
                   fighting = False
                   done = True
                   switch = 0
               if "Garsnagg is currently" in ln and HP > 800 and alone and not fighting:
                   if switch == 1:
                       rod.write("c virtue kilgore\n"*8)
                       time.sleep(15)
                       rod.write("w\ns\ne\nk gars\nc virtue gars\nc virtue\nc virtue\nc virtue\nc virtue\n")
                       time.sleep(5)
                        
                       fighting = True
                   else:
                       switch = 1

                       while True:
                           time.sleep(2)
                           rl = read(rod)
                           sys.stdout.write(rl)
                           buf += rl
                           if "A strange voice says," not in buf:
                               rod.write("w\nn\ne\nexa basket\ngold\nquit\n\n\n")
                           else:
                               return 20
                            
               if "You quaff a glowing" in ln:
                   quaffing = False

            if HP < 800:
                quaffing = True
                rod.write("c heal\nc heal\n")
            
            buf = read(rod)
            if done:
                break

            print ("TIMER: %s"%timer)
            if timer > 30 and not fighting:
                break
            if timer > 100 and fighting:
                fighting = False
        

    rl = read(rod)
    sys.stdout.write(rl)
    tranceup(rod)
    loggedGold, loggedPot = False, False

    while True:
        time.sleep(1)
        rl = read(rod)
        sys.stdout.write(rl)
        buf += rl
        for ln in buf.split('\n'):
            if "gold pieces on hand." in ln and not loggedGold:
                loggedGold = True
                logW.write(time.ctime()+"\t\t"+ln.strip().split(")")[-1]+'\n')
                logW.flush()
            if "a glowing purple potion (" in ln and not loggedPot:
                loggedPot = True
                logW.write(time.ctime()+"\t\t"+ln.strip()+'\n')
                logW.flush()
        if "A strange voice says," not in buf:
            rod.write("w\nn\ne\nexa basket\ngold\nquit\n\n\n")
        else:
            break
    try: print read(rod)
    except:
        pass

    return 8
    #if not done:
    #    # if didn't loot recheck in 5 minutes
    ##    return 5
    ##else:
    #    return 23



def rquit(rod):
    r = ''
    while True:
        rod.write("quit\n")
        time.sleep(2)
        r += read(rod)
        if "A strange voice says," in r:
            print r
            break
    
def go_back(rod):
    print "going back"
    rod.write("c word\nlook\nver\n")

    r = ''
    while True:
        r += read(rod)
        
        if "SMAUG 2.6" in r:
            print r
            if "Thoth's Rune on Vertic" in r:
                pass
            else:
                go_back(rod)
            break
            
    
    
    time.sleep(5)
    go(rod,"#3 s;e;s")
    rod.write("rem all\nrepair all\nwear all\n")

    go(rod,"n;n")
    #rod.write("buy 20 turkey\nempty bag basket\ndrop bag\n")

    time.sleep(1)

    go(rod,"s;#3 w;n")

    
    sys.stdout.write(rod.read_very_lazy())
    time.sleep(10)
    go(rod, "s;e;e;#4 s;ne;#2 s;se;#2 e;s;#2 sw;s;#4 sw;#4 s;#5 se;#2 s;d;s;se;s;#3 sw;u;#3 w;s;sw;d;#3 w;#3 n;#2 w;sw;w;#3 n;#2 ne;nw")
    rod.write("n\ndig d\n")
    r = ''
    
    while True:
        l = read(rod)
        
        r += l
        if len(l) > 0:
            sys.stdout.write(l)
        
        if "Your dig did not" in r:
            rod.write("dig d\n")
            r = ''
        elif "You dig open" in r:
            go(rod,"d;d;nw;nw;nw;u;e;n;n")
            break
            
    rod.write("e\nver\n")
    while True:
        l = read(rod)

        r += l
        if len(l) > 0:
            sys.stdout.write(l)

        if "SMAUG 2.6" in r:
            if "The Chief's Chamber" not in r:
                go_back(rod)
            break

def check_disarm(rod,ln):
    if "DISARMS" in ln:
        rod.write("get thunder\nwear thunder\n")

def move(rod,direction):
    ''' try to move a direction and return whether successful '''
    if len(direction) == "": return 1
    rod.write(direction+'\nver\n')
    r = ''
    while True:
        ln = read(rod)
        r += ln

        if "SMAUG 2.6" in r:
            sys.stdout.write(r)
            check_disarm(rod,ln)
            break
    
    if "Alas, you cannot go that way." in r:
        return -1
    elif "Exits: " in r:
            return 1
    elif "No way!  You are still fighting!" in r:
        for l in r.split("\n"):
            rod.write("c virtue\n")
            time.sleep(3)
        return 2
    elif "look" in direction or "open" in direction or "enter" in direction:
        return 1
    elif "is closed." in r:
        rod.write("get key\nunlock %s\ndrop key\nopen %s\nver\n"%(direction, direction))
        r = ''
        while True:
            ln = self.read(rod)
            r += ln
            
            if "SMAUG" in r:
                sys.stdout.write(r)
                if "You unlock" in r:
                    return 0
                else:
                    return -1
    elif "You'd need a boat to go there." in r or "need fly" in r:
        rod.write("drop carpet\nsay let me fly!\nget carpet\n")
        return 0



def midas(rod):
    rod2 = Telnet("realmsofdespair.com",4000)
    rod2.write("%s\n%s\n\n \n \n"%("Vaylis","1q2w3e4r"))
    r = rod2.read_very_eager()
    time.sleep(5)
    rod2.write("dr\nget turkey\neat tur\ndrop turkey\n")
    rod2.write("get club gar\nc midas club\nver\n")
    r = ''
    while True:
        r += read(rod2)
        r2 = read(rod)
        if len(r) > 0:
            print r

        if "enough mana." in r:
            rod2.write("meditate\n")
            time.sleep(30)
            rod2.write("c midas club\nver\n")
            r = ''

        elif "You transmogrify" in r or "You see nothing like that" in r or 'You are not carrying that.' in r:
            break
        elif "SMAUG 2.6" in r:
            rod2.write("c midas club\nver\n")
            r = ''
        time.sleep(4)
        

    rod2.write("meditate\n")
    time.sleep(30)

    rod2.write("quit\n")

def read(rod):
    ln = rod.read_very_eager()

    if "says '" in ln or "tells you '" in ln:
        rod.write("tell kaetas ding!\n")
        rod.write("tell keamval ding!\n")
        rod.write("tell kaetas %s\n"%ln.strip())
        rod.write("tell keamval %s\n"%ln.strip())

    if "tells you '" in ln:
        time.sleep(5)
        rod.write("reply brb\nquit\n")
        raise ValueError(ln)

    elif ("says '" in ln or "wonders '" in ln) and "Harakiem" not in ln:
        time.sleep(5)
        rod.write("say brb\n")
        time.sleep(2)
        rod.write("quit\n")

        raise ValueError(ln)
    return ln

def parsedir(dirs):
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

def go(rod,directions, force = False):
    directions = parsedir(directions)
    sys.stdout.write("Moving %s\n"%(directions))
    i = 0
    Nloop = 0
    L = len(directions)
    while len(directions) > i and Nloop < L+40:
        Nloop += 1
        #print Nloop, directions
        direct = directions[i]
        movestatus = move(rod,direct)

        if movestatus == 1:
            # success
            i += 1
        elif movestatus == 0:
            pass
        elif movestatus == -1:
            sys.stdout.write("Cannot move that way...\n")
            if force:
                i += 1
            else:
                return
        elif movestatus == -2:
            return
        elif movestatus == 2: #fighting
            Nloop -= 1
    
        time.sleep(0.1)
    return


if __name__ == "__main__":
    import sys
    import time
    nsleep = 15
    switch = 1
    while True:
        try: nsleep = gokill()
        except ValueError as err:
            print(err.args)
            # pause for 6 hours
            sys.stdout.write("******* SOMEONE SENT TELL HUH OH, PAUSING FOR A WHILE *****************\n")
            time.sleep(6*60*60)
        except EOFError:
            nsleep = 60
            print "Sleeping a total of %d minutes"%nsleep
            for i in range(nsleep):
                print "sleeping 60s...(%d of %d)"%(i,nsleep)
                time.sleep(60)
        except:
            time.sleep(120)
        else:
            print "Sleeping a total of %d minutes (%s)"%(nsleep,switch)
            for i in range(nsleep):
                print "sleeping 60s...(%d of %d)"%(i,nsleep)
                time.sleep(60)

    
