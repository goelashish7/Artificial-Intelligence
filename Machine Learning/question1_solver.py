import math
class Question1_Solver:
    attributes=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    output=['democrat','republican']
    attributesVal=['y','n','?']
    count=0
    classificationAttr=0
    def __init__(self):
        self.learn('train.data');
        self.count=0
        return;
    #Returns which of the classification class has higher number
    def majority(self, data):
   
      valFreq = {}
      for entry in data:
        if (valFreq.has_key(entry[self.classificationAttr])):
          valFreq[entry[self.classificationAttr]] += 1
        else:
          valFreq[entry[self.classificationAttr]] = 1
      maxi = 0
      major = ""
      for key in valFreq.keys():
        if valFreq[key]>maxi:
          maxi = valFreq[key]
          major = key
      return major
    #Returns the entropy on the given dataset
    def entropy(self, data):
      valFreq = {}
      dataEntropy = 0.0
      for entry in data:
        if (valFreq.has_key(entry[self.classificationAttr])):
          valFreq[entry[self.classificationAttr]] += 1.0
        else:
          valFreq[entry[self.classificationAttr]] = 1.0
          
      for freq in valFreq.values():
          dataEntropy += (-freq/len(data)) * math.log(freq/len(data), 2)
      return dataEntropy
    #Returns the gain for the corresponding attribute
    def gain(self,data, targetAttr):
        valFreq = {}
        subsetEntropy = 0.0
        for entry in data:
          if (valFreq.has_key(entry[targetAttr])):
            valFreq[entry[targetAttr]] += 1.0
          else:
            valFreq[entry[targetAttr]] = 1.0
        for val in valFreq.keys():
          valProb = valFreq[val] / sum(valFreq.values())
          dataSubset = [entry for entry in data if entry[targetAttr] == val]
          subsetEntropy += valProb * self.entropy( dataSubset)
        return (self.entropy(data) - subsetEntropy)
    #choose best attibute
    def chooseAttr(self,data, attributes):
        best = attributes[0]
        maxGain = 0;
        for attr in attributes:
          newGain = self.gain(data,attr)
          if newGain>maxGain:
            maxGain = newGain
            best = attr
        return best  
    def getAttrRemainingValues(self,data, attribute):
      values = []
      for entry in data:
        if entry[attribute] not in values:
          values.append(entry[attribute])
      return values
    # If all the records in the dataset have the same classification,
      # return that classification.
    def checkSameClassification(self,data,output):
       for entry in data:
          if entry[self.classificationAttr]!=output:
            return False
       return True
    def ID3(self,data, attributes):
      
      data = data[:]
      default =self.majority(data)
      # If the dataset is empty or the attributes list is empty, return the
      # default value. 
      if not data or (len(attributes)) <= 0:
        return default
      elif self.checkSameClassification(data, default):
        return default
      else:
        # Choose the next best attribute 
        bestAttr = self.chooseAttr(data, attributes)
        # Create a new decision tree/node with the best attribute 
        tree = {bestAttr:{},'default':{}}
      # Create a new decision tree/sub-node for each of the values in the
      #bestAttr found above
        for val in self.getAttrRemainingValues(data, bestAttr):
          
          subsetdata=[]
          for entry in data:
            if(entry[bestAttr]==val):
              subsetdata.append(entry)
          newAttr = attributes[:]
          newAttr.remove(bestAttr)
          subtree = self.ID3(subsetdata, newAttr)
          tree[bestAttr][val] = subtree
      tree['default']=default
      return tree

    # Add your code here.
    # Read training data and build your decision tree
    # Store the decision tree in this class
    # This function runs only once when initializing
    # Please read and only read train_data: 'train.data'
    def learn(self, train_data):
        f=open(train_data,'r')
        ''''
        self.data={'democrat':[[],[],[]],'republican':'[[],[]]'}
        
        '''
        self.data = []
        #count=0
        '''
        Read all the data in self.data
        '''
        for row in f.readlines():
          Data = row.split()
          rowClass=Data[0]
          rowAttrData=Data[1].split(',')
          tempList=[]
          tempList.append(rowClass)
          tempList.extend(rowAttrData)
          self.data.append(tempList)
     #   self.entropy=self.findEntropy(countDemocrat, countRepublican)
        attributes= self.attributes[:]
        self.root=self.ID3(self.data,attributes)
        f = open('decision_tree.txt', 'w')
        f.write(str(self.root))
        f.close()
        
        return;
    
    # Add your code here.
    # Use the learned decision tree to predict
    # query example: 'n,y,n,y,y,y,n,n,n,y,?,y,y,y,n,y'
    # return 'republican' or 'republican'
    def solve(self, query):
        self.count=self.count+1
        listQuery=query.split(",")
        currentNode=self.root
        while 1:
          if isinstance(currentNode, str):
            return currentNode
          for key in currentNode.keys():
             if(key=='default'):
              continue
             else:
               break 
             
         # splittingAttribute=currentNode['attribute']
          chosenVote=listQuery[key-1]
          subTrees=currentNode[key]
          if chosenVote in subTrees.keys():
            currentNode=subTrees[chosenVote]
          else:
            return currentNode['default']
       

