#subnetting python script, does subnetting for networking and security
#built for funzies 11/17/22
import math

path = "subOutput.txt" #where do you want to save the subOutput.txt
testMode = True #True uses static data, anything else will get user inputs.

##cdir : decimal mask
dec = {
    32 : "255.255.255.255",
    31 : "255.255.255.254",
    30 : "255.255.255.252",
    29 : "255.255.255.248",
    28 : "255.255.255.240",
    27 : "255.255.255.224",
    26 : "255.255.255.192",
    25 : "255.255.255.128",
    24 : "255.255.255.0",
    23 : "255.255.254.0",
    22 : "255.255.252.0",
    21 : "255.255.248.0"
}

## cdir : binary mask
bin = {
    32 : "11111111.11111111.11111111.11111111",
    31 : "11111111.11111111.11111111.11111110",
    30 : "11111111.11111111.11111111.11111100",
    29 : "11111111.11111111.11111111.11111000",
    28 : "11111111.11111111.11111111.11110000",
    27 : "11111111.11111111.11111111.11100000",
    26 : "11111111.11111111.11111111.11000000",
    25 : "11111111.11111111.11111111.10000000",
    24 : "11111111.11111111.11111111.00000000",
    23 : "11111111.11111111.11111110.00000000",
    22 : "11111111.11111111.11111100.00000000",
    21 : "11111111.11111111.11111000.00000000"
}

## cdir size : cell size
siz = {
    32 : "1", #why did i use string here?
    31 : "1",
    30 : "1",
    29 : "1",
    28 : "1",  ## 1/16 row
    27 : "2",  ## 1/8 row
    26 : "4",  ## 1/4 row
    25 : "8",  ## 1/2 row
    24 : "16", ## 1 row
    23 : "32", ## 2 row
    22 : "64", ## 4 row
    21 : "128"
}

## matrix len : cell IP range
chartThing = {
    0 : [0, 15], ##[start, end] of cell
    1 : [16, 31],
    2 : [32, 47],
    3 : [48, 63],
    4 : [64, 79],
    5 : [80, 95],
    6 : [96, 111],
    7 : [112, 127],
    8 : [128, 143],
    9 : [144, 159],
    10 : [160, 175],
    11 : [176, 191],
    12 : [192, 207],
    13 : [208, 223],
    14 : [224, 239],
    15 : [240, 255]
}

##create obs
class company:
    def __init__(self,nameIn, symbolIn, sizeIn, growthIn):
        self.rank = 0
        self.name = nameIn
        self.symbol = symbolIn
        self.size = sizeIn
        self.growth = growthIn
        self.projected = math.ceil(sizeIn * (1+growthIn))
        self.actual = self.projected+3
        self.power = 0
        self.users = 0
        while self.actual >= self.users:
            self.power = self.power + 1
            self.users = math.pow(2, self.power)
        cidr = 32-self.power
        self.binary = bin[cidr]
        self.decim = dec[cidr]
        self.chunkSize = siz[cidr]
        self.waste = int(self.users - self.actual)
        self.rowStart = -1
        self.rowEnd = -1
        self.colStart = -1
        self.colEnd = -1

    def setRowStart(self, rowStartIn):
        self.rowStart = rowStartIn
    def setRowEnd(self, rowEndIn):
        self.rowEnd = rowEndIn
    def setColStart(self, colStartIn):
        self.colStart = colStartIn
    def setColEnd(self, colEndIn):
        self.colEnd = colEndIn
        
def createCompanyObs(): #get user inputs - need to account for errors
    container = []
    x = 1
    
    if testMode == True:
        container.append(company('Adjecta', 'A', 50, .25))
        container.append(company('Spambot', 'S', 45, .25))
        container.append(company('Myspacebook', 'M', 480, .25))
        container.append(company('AbraCadab', 'B', 27, .25))
        container.append(company('Cougar Town', 'C', 120, .25))
        container.append(company('2 to the 8th', '2', 256, .25))
        container.append(company('TinyCo', 'T', 3, .25))
        container.append(company('Nothin', 'N', 200, .25))
        container.append(company('GoMommy', 'G', 12, .25))
        container.append(company('Japaneiros', 'J', 5, .25))
    else: #force valid/desired inputs
        count = int(input("How many companies to subnet?"))
        while x <= count:
            name = input("Enter the name of company #{}: ".format(x))
            z = 0
            while z == 0:
                symbol = input("Enter the symbol of {}: ".format(name))
                if len(symbol) == 1:
                    z = 9000
                else:
                    print("Max symbol size = 1 char")
            z = 0
            while z == 0:
                try:
                    size = int(input("Enter size requirement of {}: ".format(name)))
                    z = 9000
                except:
                    print("You tried to insert something that wasn't an INTEGER!")
            z = 0
            while z == 0:
                try:
                    growth = float(input("Enter expected growth of {} in decimal form: ".format(name)))
                    z = 9000
                    print("\n")
                except:
                    print("You tried to insert something that wasn't an INTEGER!")
            container.append(company(name, symbol, size, growth))
            x = x + 1

    return container

def rankComp(containerIn):
    ln = len(containerIn) #original length
    cont1 = [] #will hold parallel list to containerIn
    cont2 = [] #will hold the new list
    rank = 1
    for comp in containerIn:
        cont1.append(comp.actual) #creates list of parallel actual needs
    while rank < ln+1:
        i = cont1.index(max(cont1)) #find index of highest
        cont2.append(containerIn[i]) #builds list from greatest to smallest
        containerIn[i].rank = rank
        rank = rank + 1

        #this is required for parallelism
        cont1.remove(cont1[i]) #deletes old list greatest to smallest
        containerIn.remove(containerIn[i]) #deletes old list greatest to smallest
    return(cont2)

def makeChart(containerIn):
    amap = [] #holds the working row
    bmap = [] #holds build rows
    for comp in containerIn:
        chunk = int(comp.chunkSize)
        i = 0 #counts how many cells has been filled
        if comp.rowStart == -1: #-1 because once assigned we don't do it again
            comp.setRowStart(len(bmap)) #start of row for this company
            comp.setColStart(chartThing[i][0]) #start of cells
        while chunk > i:
            if len(amap) == 16: ## if amap hits 16 cells it goes back to 0
                bmap.append(amap) #adds finished row to the built rows
                amap = [] #resets working row
            amap.append(comp.symbol)
            i = i + 1
        comp.setRowEnd(len(bmap)) #end of this company's row
        comp.setColEnd(chartThing[len(amap)-1][1]) #end of this company's cells
    bmap.append(amap)
    return(bmap)

def writeComps(containerIn): #this is just writing to file; if we get above 9 rows the spacing shifts over
    chart = makeChart(containerIn)
    f = open(path , 'w')
    f.write("    0-15 | 16-31 | 31-47 | 48-63 | 64-79 | 80-95 | 96-111|112-127|128-143|144-159|160-175|176-191|192-207|208-223|224-239|240-255")
    z = 0
    space = "    "
    space2 = "   "
    for row in chart:
        f.write("\n" + str(z))
        z = z + 1
        if z == 11: #fixes spacing issue after char col shifts b/c double digit
            space = "   "
            space2= "    "
        for x in row:
            f.write(space + str(x) + space2)
    f.write("\n")
    for comp in containerIn:
        f.write("\nName: {}".format(comp.name))
        f.write("\nChart Symbol: {}".format(comp.symbol))
        f.write("\nRank: {}".format(str(comp.rank)))
        f.write("\nProjected Need: {}".format(str(comp.projected)))
        f.write("\nActual need: {}".format(comp.actual))
        f.write("\nBinary Mask: {}".format(comp.binary))
        f.write("\nDecimal mask: {}".format(comp.decim))
        f.write("\nNetwork ID: x.x.{}.{}".format(str(comp.rowStart), str(comp.colStart)))
        f.write("\nGateway address: x.x.{}.{}".format(str(comp.rowStart), str(comp.colStart + 1)))
        f.write("\nBroadcast address: x.x.{}.{}".format(str(comp.rowEnd), str(comp.colEnd)))
        f.write("\nUseful range x.x.{}.{} to x.x.{}.{}".format(str(comp.rowStart), str(comp.colStart + 2), str(comp.rowEnd), str(comp.colEnd - 1)))
        f.write("\nWaste: {}".format(comp.waste))
        f.write("\nCells assigned: {}\n".format(comp.chunkSize))
    f.close()

def MainGo():
    comps = createCompanyObs() #establishes objects
    comps = rankComp(comps) #ranks objects
    writeComps(comps) #creates chart and write to file

MainGo()