import itertools

class Apriori:
    #default values
    inFilePath = "input.csv"
    outFilePath = "output.csv"
    support = 0.2
    threshold = 0
    confidence = 0.8
    asscnFlag = 1
    itemsToTransaction = {}
    outFile = None
    numTransactions = 0
    freqItemsets = []
    asscnRules = {}
    numAsscnRules = 0

    def mineFrequentItemSets(self, size):
        Log("mining for size: "+str(size))
        if size == 1:
            self.addItemsets(size)
        flag = self.formNewItemsets(size)

        if flag:
            self.mineFrequentItemSets(size+1)

    def addItemsets(self, size):
        #print "printing itemsets"

        for key in self.itemsToTransaction:
            keySize = len(key.split(','))
            #here threshold can be used
            if keySize == size:
                self.freqItemsets.append(key)

    def printFreqItemsets(self):
        Log("printing frequent itemsets")
        self.outFile.write(str(len(self.freqItemsets))+"\n")

        for items in self.freqItemsets:
            self.outFile.write(items+"\n")

    def formNewItemsets(self, size):
        toAdd = {}
        seen = {}
        flag = 0

        for key1 in self.itemsToTransaction:

            if(len(key1.split(',')) < size):
                continue

            for key2 in self.itemsToTransaction:

                if (len(key2.split(',')) < size):
                    continue

                currKey = key1 + "," + key2
                keySplit = currKey.split(',')
                keySet = set(keySplit)

                if len(keySet) == size+1:
                    trans1 = self.itemsToTransaction[key1]
                    trans2 = self.itemsToTransaction[key2]
                    keyStr = ""
                    sortedKey = sorted(keySet)
                    keyStr = ",".join(sortedKey)

                    if keyStr in seen:
                        continue

                    seen[keyStr] = 1
                    currTrans =  list(set(trans1).intersection(set(trans2)))

                    #threshold check can be removed all itemsets required for assn rules
                    if len(currTrans) >= self.threshold:
                        toAdd[keyStr] = currTrans
                        #new line added
                        self.freqItemsets.append(keyStr)
                        self.mineAssociationRules(keyStr, sortedKey, len(currTrans))
                        flag = 1

        for key in toAdd:
            self.itemsToTransaction[key] = toAdd[key]

        return flag

    def mineAssociationRules(self, keyStr, sortedKey, supp_count_I):
        if self.asscnFlag == 0:
            return

        subset = self.getSubsets(sortedKey)
        #subsetKeys = []

        #for item in subset:
         #   subsetKeys.append(str(item).translate(None, "(')").rstrip(","))

        for key in subset:

            I = set(sortedKey).difference(key.split(','))
            I_key = ",".join(list(I))

            if (key in self.asscnRules and self.asscnRules[key] == I_key):
                continue

            #supp_count_I =  len(self.itemsToTransaction[keyStr])
            supp_count_s = len(self.itemsToTransaction[key])
            confidence = float(supp_count_I)/supp_count_s

            if confidence >= self.confidence:
                if key not in self.asscnRules:
                    self.asscnRules[key] = [I_key]
                else:
                    self.asscnRules[key].append(I_key)
                self.numAsscnRules += 1

    def getSubsets(self, itemset):
        #print "getting subsets"
        subset = []

        for i in range(1, len(itemset)):
            #curr = list(itertools.combinations(itemset, i))
            curr = [','.join(x) for x in itertools.combinations(itemset, i)]
            subset += curr

        return subset

    def printAssociationRules(self):
        Log("printing association rules")
        self.outFile.write(str(self.numAsscnRules)+'\n')

        for key in self.asscnRules:
            mapping = self.asscnRules[key]

            for val in mapping:
                self.outFile.write(key+",=>,"+val+"\n")

def Log(msg):
    print "DEBUG: ",msg





