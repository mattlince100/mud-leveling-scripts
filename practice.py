import telnetlib, time
import sys
import random



if True:
    user = "Delfys"
    pw = "1q2w3e4r"
    manaspell = "meditate"
elif True:
    user = sys.argv[1]
    pw = "1q2w3e4r"
    manaspell = "trance"

print manaspell

toprac = ['weaken', 'elven beauty', 'mystical vision', 'rapture','faerie fire', 'invis', 'float', 'refresh', 'adamant', 'create fire', 'infravision', 'trollish vigor', 'brawn', 'fly', 'ogre might', 'blindness', 'acumen', 'adroitness', 'dragon wit', 'slink', 'create spring', 'faerie fog', 'sagacity', 'sapience', 'shield', 'valiance', 'scry', 'dragonskin', 'antimagic shell', 'ethereal web', 'pass door', 'razorbait','demonskin', 'iceshield', 'swordbait','inner warmth', 'winter mist', 'blazeward', 'aqua breath', 'blazebane', 'eldritch sphere', 'fireshield', 'ethereal shield', 'true sight', 'ethereal funnel', 'shockshield', 'shadowform',"prismatic shield", "elemental supremacy","confidence","immobilize"]


toprac += ['prophetic aura','ritual blessing','fireshield',"greater sanctuary","divine power", "defense against devout"]


toprac += ['armor', 'cure light', 'burden defense', 'detect magic', 'refresh', 'cure blindness', 'detect evil', 'bless', 'blindness','create symbol', 'cure serious', 'detect invis', 'detect poison', 'know alignment', 'protection', 'detect hidden', 'float',  'cure critical', 'cure poison', 'minor invocation', 'create spring', 'identify', 'curse', 'fly', 'lethargy', 'remove curse', 'remove hex', 'sanctuary', 'ameliorate', 'heal', 'fortify', 'dispel magic', 'mass invis', 'major invocation', 'benediction', 'scry', 'create fire', 'aqua breath', 'alertness', 'dream', 'divine agility', 'feast of champions', 'indignation', 'grounding', 'fireshield', 'restoration', 'acidward', 'expunge', 'unravel defense', 'shockshield', 'uplift', 'true sight', 'ill fortune', 'resilience', 'cascading heal', 'antimagic shell', 'divinity', 'holy sanctity', 'salvation', 'nimbus of light', 'ethereal funnel','indurate']


toprac += ['create fire', 'execrate', 'detect poison', 'disruption', 'fade', 'mind fortress', 'lingering decay', 'wine invocation', 'mystic awareness', 'gremlin', 'demonic aura', 'flesh armor', 'remove hex', 'might of the Fiend', 'demonskin', 'detect hidden', 'rid toxins', 'pentagram', 'plague', 'seduction', 'occular explosium', 'reveal', 'quickening',   'identify', 'dehydrate', 'sleep', 'chains of agony', 'nightmare', 'levitate', 'kleshas', 'fatigue', 'pass door', 'blasphemy', 'locate object',  'enervate', 'shadow walk', 'fireshield', 'feebleness', 'mark of pactolus',  'famish', 'know alignment', 'denigrate', 'aggravate wounds',  'hellskin', 'desecrate', 'mental anguish', 'infuscate', 'zidros wrath', 'petrification', 'sands of Hades', 'shadowform', 'nefarious pact', 'possess', 'pestilence']


toprac += [ 'dall loisg', 'ioc beag', 'ioc dall', 'oaken consecration', 'create fire', 'float', 'infravision', 'refresh',  'ioc puinsean', 'control weather', 'fly', 'puinsean', 'wisteria', 'ciall', 'create spring', 'invis', 'dion', 'ioc abhbhal', 'nadur ciall', 'faic puinsean',  'identify', 'locate object', 'dispel magic', 'nuadhaich', 'remove invis',  'weaken', 'ceangail nadur', 'sylvan shell', 'asgaidh nadur', 'dream', 'aqua breath', 'slainte', 'luths nadur', 'mass invis', 'word of recall', 'ceoban', 'iceshield', 'nadur dion', 'organic infusion', 'depuinsean', 'sgorr craiceann', 'sleep', 'fireshield', 'abrar beathach', 'shockshield', 'dance of vines', 'firinn faic', 'sylvan mist', 'boannaich nadur']

if user == 'marijoie':
    toprac = ['enervate', 'fatigue', 'fireshield','denigrate','plague', 'quickening','chains of agony']
#toprac = ['inviola magicka']

#toprac = ['gremlin']

def waitcmd(rod,cmd, p = False):
    time.sleep(0.1)
    r = rod.read_very_eager()
        
    if p:
        sys.stdout.write(r)

    rod.write("%s\nver\n"%cmd)
    time.sleep(0.1)
    r = ''
    start = time.time()
    while  True:
        r += rod.read_very_eager()
        if "SMAUG 2.6" in r:
            break
        t = time.time()-start
        if t > 20:
            break
        time.sleep(0.5)
        
    rflush = rod.read_very_eager()
    return r

def check_prac(rod,p = True):
    r = waitcmd(rod,"slist", p)
    
    bsplt = r.split('\n')
    slist = []
    print r
    for i in range(len(bsplt)):
        if "Spell:" in bsplt[i]:
            sname, svalue = bsplt[i].split("%: ")
            smax = bsplt[i].split("Max: ")[-1].split()[0]
            sname = sname.split(":")[-1].strip()
            svalue = svalue.split()[0]
            slist.append((sname, int(svalue),int(smax)))
    print [x[0] for x in slist]
    return slist


def tranceup(rod):
    buf = ''
    rod.write("%s\n"%manaspell)
    
    while int(MP) < int(maxMP)-100:
        time.sleep(16)
        buf += rod.read_very_eager()
        if "\r\n" in buf:
            get_hpmp(buf)
            rod.write("%s\n"%manaspell)
        buf = ''
    print("Done trancing")

def get_hpmp(buf):
    global MP, HP, maxHP, maxMP, gold
    for ln in buf.split('\n'):
        ln = ln.strip()
        if user.capitalize() in ln or "(Standard)" in ln or user.lower() in ln: # prompt
            
            #print [ln]
            #print ln.split("Hp ")[0].split("m")[-1]
            print ln
            try: 
                HP,maxHP = tuple(ln.split("hp ")[0].split("(")[-1].split("/"))
                try: MP, maxMP = tuple(ln.split("m ")[0].split(" ")[-1].split("/"))
                except:
                    MP, maxMP = tuple(ln.split("mn ")[0].split(" ")[-1].split("/"))
                gold = int(ln.split()[-1].strip().strip(")").replace(',',""))
                HP, maxHP = int(HP), int(maxHP)
                MP, maxMP = int(MP), int(maxMP)
            except:
                continue
            else:
                MP, maxMP = int(MP), int(maxMP)


rod = telnetlib.Telnet("realmsofdespair.com",4000)
rod.write("%s\n"%user)
rod.write("%s\n\n \n \nconfig -ansi\n"%(pw))
waitcmd(rod,"cast 'dispel magic' self", p = True)


#slist = [(x[0],x[1],x[2]) for x in check_prac(rod, p = False) if x[1] > 0 and x[1]<x[2]]
#print str([x[0] for x in slist])
slist = [(x[0],x[1],x[2]) for x in check_prac(rod, p = False) if x[1] > 0 and x[1]<x[2] and x[0] in toprac]+[('dispel magic',0,0)]

print str([x[0] for x in slist])
stop = False

start = time.time()
r = ''
i = 0
while len(slist) > 0:
    # read until newline and add to buf
 
    rod.write("look\n")
    time.sleep(2)
    r += rod.read_very_eager()
    if "\n" in r:
        
        get_hpmp(r)
        
        if int(MP) < 100:
            slist = [(x[0],x[1],x[2]) for x in check_prac(rod, p = False) if x[1] > 0 and x[1]<x[2] and x[0] in toprac]+[('dispel magic',0,0)]
            waitcmd(rod,"cast 'dispel magic' self", p = True)
            tranceup(rod)
        else:
            i += 1
            print ("cast '%s' self (%d%%/%d%%)"%slist[i%len(slist)])
            waitcmd(rod,"cast '%s' self"%slist[i%len(slist)][0], p = True)
        print MP, maxMP
        r = ''
    rod.write("look\n")
    time.sleep(.5)
        
