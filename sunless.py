

class Sunless:
    
    def func_sunless(self):

        self.whereami()
        self.check_affect()

        print("Sunless", self.phase)
        if self.location == "The Sunless Sea":
            self.rod.write("n\nn\nget torch\nwear torch\nu\nw\nn\nsw\nw\nn\nopen box\nget all box\nwear all\n")
            while True:
                r = self.rod.read_very_eager()
                self.sys.stdout.write(r)
                if "GET SHIELD." in r:
                    break
                self.time.sleep(1)
            self.rod.write("get shield\nwear all\nne\nw\nn\nw\nnw\ne\nget all bed\nwear all\nw\nn\nw\nw\nw\nsw\nw\nw\nw\nnw\n")
            self.time.sleep(5)
            self.rod.write("train STR 3\ntrain DEX 6\ntrain CON 4\ntrain LCK 3\nhelp start\n")
            self.phase = 2
        elif self.phase == 2:
            # waiting of name auth
            self.rod.write("pull cord\n")
            self.sys.stdout.write("pull cord\n")
            self.time.sleep(60)
        elif self.location == "The Future Awaits":
            self.rod.write("train STR 3\ntrain DEX 6\ntrain CON 4\ntrain LCK 3\nhelp start\n")
            self.rod.write("pull cord\n")
            self.sys.stdout.write("pull cord\n")
            self.time.sleep(60)

        if self.location == "Rejoining the Ancient Clan Spirits":
            return "starting"
        if self.level >= 2:
            return 'dhaven'
        return "sunless"
