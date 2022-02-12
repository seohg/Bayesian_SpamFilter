import re

def loadtrainFile(): 
    global spamMailList, hamMailList
    
    sf = open('D:/한동대/4학기/이산수학/HW/spamMail.txt', 'r')
    hf = open('D:/한동대/4학기/이산수학/HW/hamMail.txt', 'r')

    spamMailList =[]
    for sline in sf:
        spamMailList.append(sline)

    hamMailList =[]
    for hline in hf:
        hamMailList.append(hline)

    sf.close()
    hf.close()

def loadtestFile():
    global testSpamMaliList, testhamMaliList
    
    tsf = open("D:/한동대/4학기/이산수학/HW/testSpamMail.txt", 'r')
    thf = open("D:/한동대/4학기/이산수학/HW/testHamMail.txt", 'r')
    
    testSpamMaliList =[]
    for tsline in tsf:
        testSpamMaliList.append(tsline)

    testhamMaliList =[]
    for thline in thf:
        testhamMaliList.append(thline)

    tsf.close()
    thf.close()

def saveWord(listStr,newdict): #한 문자 안에 있는 단어 dict에 저장
    parseListStr = listStr.split() #parsing
    parseListStr = list(set(parseListStr)) #중복 제거
    for word in parseListStr:
        if word in list(newdict.keys()):
            newdict[word] = int(newdict[word])+1
        else :
            newdict[word] = 1
    return newdict

def list2sortword():
    global spamlist, hamlist
    
    global spamDict
    spamDict={}
    
    global hamDict
    hamDict={}
    
    for slist in spamMailList:
        slist = slist.lower()
        slist = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', ' ', slist)
        spamDict = saveWord(slist,spamDict)
    spamlist = sorted(spamDict.items(), key=lambda spamDict: spamDict[1], reverse=True)
    
    for hlist in hamMailList:
        hlist = hlist.lower()
        hlist = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', ' ', hlist)
        hamDict = saveWord(hlist,hamDict)
    hamlist = sorted(hamDict.items(), key=lambda hamDict: hamDict[1], reverse=True)
    
    
def bayesian(mail):
    global spamMailList, hamMailList
    global spamDict, hamDict
    spamNum = float(len(spamMailList))
    hamNum = float(len(hamMailList))
    wcount = 0
    a = 1
    b = 1
    #print(testCaseWord)
    for i in testCaseWord:
        if i in mail:
            spamDicNum = float(spamDict[i])
            if i in list(hamDict.keys()):
                hamDicNum = float(hamDict[i])
            else:   
                hamDicNum = 0
            a = float(a) * ( spamDicNum / spamNum )
            b = float(b) * (hamDicNum / hamNum )

    pWord = a / (a+b)
    
    if pWord >0.9:
        return True
    else:
        return False
    
def trainSpamfilter():
    global spamMailList, hamMailList
    global spamDict, hamDict
    global spamlist, hamlist
    global spamWordList
    global testCaseWord
    spamWordList = []
    testCaseWord = []
    
    spamNum = float(len(spamMailList))
    hamNum = float(len(hamMailList))

    
    for i in range(len(spamlist)):
        temp = spamlist[i]
        sDicNum = float(temp[1])
        if temp[0] in hamlist:
            hDicNum = float(hamDict[temp[0]])
        else:   
            hDicNum = 0
        ss =  sDicNum / spamNum 
        hh =  hDicNum / hamNum
        result1 = ss / (ss+hh)
        if result1 >0.9 and temp[1]>7:             
            testCaseWord.append(temp[0])

def testSpamfilter():
    global spamResult
    global testSpamMaliList, testhamMaliList
    correct = 0
    
    spamResult = []
    testSMailList = []
    testHMailList = []
    
    for i in range(len(testSpamMaliList)):
        testSMailList.append( testSpamMaliList[i].lower())
        testSMailList[i] = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', ' ', testSMailList[i])
        tf1 = bayesian(testSMailList[i])
        
        if tf1 == False:
            spamResult.append(("incorrect","spam",testSpamMaliList[i]))
        else:
            spamResult.append(("correct","spam",testSpamMaliList[i]))
            correct = correct+1

    for i in range(len(testhamMaliList)):
        testHMailList.append( testhamMaliList[i].lower())
        testHMailList[i] = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', ' ', testHMailList[i])
        tf2 = bayesian(testHMailList[i])
        

        if tf2 ==False:
            spamResult.append(("correct","ham",testhamMaliList[i]))
            correct = correct+1
        else:
            spamResult.append(("incorrect","ham",testhamMaliList[i]))
           
    return float(correct) / float(len(testSpamMaliList)+len(testhamMaliList)) * 100

#main함수 ====================================================================================
while True:
    mode = input("\nchoose mode 1.train 2.test 3.quit\n")
    
    if mode == '1': #train mode
        loadtrainFile()
        list2sortword()
        trainSpamfilter()
       
        
    elif mode == '2': #test mode
        loadtestFile()
        try:
            accuracy = testSpamfilter()
            for i in spamResult:
                print(i)
            print("\naccuracy: ",accuracy,"%\n")
        except:
            print("\ntrain first\n")
                    
    elif mode =='3': #quit
        input("press enter to quit")
        break
        
    else: #wrong input
        continue
