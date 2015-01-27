import random
class Question2_Solver:
    classifier=['democrat','republican']
    attributes=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    values=['y','n','?']
    def __init__(self):
        self.learn('train.data');
        return;

    # Add your code here.
    # Read training data and build your naive bayes classifier
    # Store the classifier in this class
    # This function runs only once when initializing
    # Please read and only read train_data: 'train.data'
    def learn(self, train_data):
        f=open(train_data,'r')
        self.data = []
        for row in f.readlines():
          Data = row.split()
          rowClass=Data[0]
          rowAttrData=Data[1].split(',')
          tempList=[]
          tempList.append(rowClass)
          tempList.extend(rowAttrData)
          self.data.append(tempList)
        
        self.classifierProb={}
        self.classifierCount={}
        totalClassifierCount=0.0
        self.FeatureProb={}
        for val in self.classifier:
          self.classifierCount[val]=0.0
          self.FeatureProb[val]=[]
          for row in self.data:
            if val==row[0]:
              self.classifierCount[val]=self.classifierCount[val]+1
          totalClassifierCount=totalClassifierCount+self.classifierCount[val]
        #Update feature prob vector/class Prob vector
        for classVal in self.classifier:
          self.classifierProb[classVal]=self.classifierCount[classVal]/totalClassifierCount
          for feature in self.attributes:
            self.FeatureProb[classVal].append({val:0 for val in self.values})
        
        
       # k=random.uniform(0, 0.0018)
        k=0.000634514758844
    #    print 'k=%',k
        for feature in self.attributes:
         for val in self.values:
            for classVal in self.classifier:
              count=0.0
              for entry in self.data:
                if entry[0]==classVal and entry[feature]==val:
                  count=count+1
              #Smoothing happens here k/3k factor
              probFeature=(count+k)/(self.classifierCount[classVal]+3*k)
              self.FeatureProb[classVal][feature-1][val]=probFeature
     #   print 'hell'
      #  f=open('test','w')
       # f.write(str(self.FeatureProb))
        return;

    # Add your code here.
    # Use the learned naive bayes classifier to predict
    # query example: 'n,y,n,y,y,y,n,n,n,y,?,y,y,y,n,y'
    # return 'republican' or 'republican'
    def solve(self, query):
        listQuery=query.split(",")
        probClassification={}
        for classVal in self.classifier:
          prob=self.classifierProb[classVal]
          for l in range(len(listQuery)):
            vote=listQuery[l]
            featureProb=self.FeatureProb[classVal][l][vote]
          #  if featureProb==0:
           #   featureProb=1
            prob=prob*featureProb
          probClassification[classVal]=prob
        max=-1
        maxKey=""
        for classVal in self.classifier:  
          if probClassification[classVal]>max:
            max=probClassification[classVal]
            maxKey=classVal
#        if(probClassification['democrat']==probClassification['republican']):
 #        return 'republican'
        return maxKey

