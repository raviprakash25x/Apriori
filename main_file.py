from apriori import Apriori, Log
import math

def readConfigFile(aprioriObj):
    """reads config.csv file and initializes apriori object"""
    Log("reading config file")
    configFile = open("config.csv")

    for line in configFile:
        lineSplit = line.rstrip().split(',')
        key = lineSplit[0]
        value = lineSplit[1]

        if key == "input":
            aprioriObj.inFilePath = value
        elif lineSplit[0] == "output":
            aprioriObj.outFilePath = value;
            aprioriObj.outFile = open(value, "w")
        elif key == "support":
            aprioriObj.support = float(value)
        elif key == "confidence":
            aprioriObj.confidence = float(value)
        elif key == "flag":
            aprioriObj.asscnFlag = int(value)

    configFile.close()

def readInputFile(aprioriObj):
    """reads input.csv file and stores the transactions
        in a dictionary"""
    Log("reading input file")
    inFile = open(aprioriObj.inFilePath)
    i = 1;

    for line in inFile:

        if line == "\n":
            continue

        transaction = line.rstrip().split(',')
        seen = {}

        for item in transaction:
            item = item.strip()

            if item in seen or len(item) == 0:
                continue

            seen[item] = 1

            if(item in aprioriObj.itemsToTransaction):
                aprioriObj.itemsToTransaction[item].append(i)
            else:
                aprioriObj.itemsToTransaction[item] = [i]

        i += 1

    aprioriObj.numTransactions = i-1

def initPrune(aprioriObj):
    Log("initial pruning")
    aprioriObj.threshold = float(aprioriObj.support * float(aprioriObj.numTransactions))
    Log("threshold:"+ str(aprioriObj.threshold))
    toDelete = []

    for key in aprioriObj.itemsToTransaction:
        transactions = len(aprioriObj.itemsToTransaction[key])

        if transactions < aprioriObj.threshold:
            toDelete.append(key)

    for key in toDelete:
        del(aprioriObj.itemsToTransaction[key])



def main():
    #read config.csv and set flags and paths
    aprioriObj = Apriori()
    readConfigFile(aprioriObj)
    readInputFile(aprioriObj)
    initPrune(aprioriObj)
    aprioriObj.mineFrequentItemSets(1)
    aprioriObj.printFreqItemsets()

    if aprioriObj.asscnFlag == 1:
        aprioriObj.printAssociationRules()

    aprioriObj.outFile.close()

if __name__ == "__main__":
    main()