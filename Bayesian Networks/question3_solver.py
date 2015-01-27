import string
     

class Question3_Solver:
    def __init__(self, cpt):
        self.cpt = cpt;
        self.prob = {};

    #####################################
    # ADD YOUR CODE HERE
    # Pr(x|y) = self.cpt.conditional_prob(x, y);
    # A word begins with "`" and ends with "`".
    # For example, the probability of word "ab":
    # Pr("ab") = \
    #    self.cpt.conditional_prob("a", "`") * \
    #    self.cpt.conditional_prob("b", "a") * \
    #    self.cpt.conditional_prob("`", "b");
    # query example:
    #    query: "qu--_--n";
    #    return "t";
    '''
    Generate domain table for each of the factor
    This is only used for initializing the probability table of each factor
    '''
    def getPossibleValues(self,var1,var2,memz):
       if memz==1:
         xVar=var1
         yVar=var2
         if '-' in var1:
           xVar='-'
         if '-' in var2:
           yVar='-'
         if (xVar,yVar) in self.prob:
          return self.prob[xVar,yVar]
       possibleProb={}
       if var1=='_' or var1=='-' :
        alphabet1 = list(string.ascii_lowercase)
       else:
        alphabet1 = list(var1)
       if var2=='_' or var2=='-' :
        alphabet2 = list(string.ascii_lowercase)
       else:
        alphabet2 = list(var2)
       for i in alphabet1:
         for j in alphabet2:
            possibleProb[i,j]=self.cpt.conditional_prob(i,j)
       if memz == 1:
         self.prob[xVar,yVar]= possibleProb
       return possibleProb
    '''
      This step involves pair wise product & summation both in same step
      Memoization is used
    '''
    def removeHiddenVariable(self,var1,var2,val1,val2,memz):
      if memz==1:
         xVar=var1
         yVar=var2
         if '-' in var1:
           xVar='-'
         if '-' in var2:
           yVar='-'
         if (xVar,yVar) in self.prob:
          return self.prob[xVar,yVar]
      possibleProb={}
      newVar=(var2[0],var1[1])
      if var2[0]=='_' or '-' in var2[0] :
        alphabet1 = list(string.ascii_lowercase)
      else:
        alphabet1 = list(var2[0])
      if var1[1]=='_' or '-' in var1[1] :
        alphabet2 = list(string.ascii_lowercase)
      else:
        alphabet2 = list(var1[1])
      #alphabet1 holds the domain for xyar
      #alphabet2 holds the domain for yvar
      alphabet = list(string.ascii_lowercase)
      for i in alphabet1:
        for j in alphabet2:
          possibleProb[i,j]=0.0
          for k in alphabet:
            possibleProb[i,j]= possibleProb[i,j]+ val1[k,j]*val2[i,k]
      if memz == 1:
         self.prob[xVar,yVar]= possibleProb
      return possibleProb
    def solve(self, query):
        tempQuery="`"
        tempQuery+=query
        tempQuery+="`"
        #hidden variable name
        hidden=1
        variablesVal=[]
        probVal=[]
        for i in range(len(tempQuery)):
            if tempQuery[i]=='_' :
              if tempQuery[i-1]=='-':
                variablesVal.append((tempQuery[i],str(hidden-1)+'-'))
              else:
                variablesVal.append((tempQuery[i],tempQuery[i-1]))
              probVal.append(self.getPossibleValues(tempQuery[i],tempQuery[i-1],1))
            elif tempQuery[i]=='-' :
              if tempQuery[i-1]=='-':
                variablesVal.append((str(hidden)+'-',str(hidden-1)+'-'))
              else:
                variablesVal.append((str(hidden)+'-',tempQuery[i-1]))
              hidden=hidden+1
              probVal.append(self.getPossibleValues(tempQuery[i],tempQuery[i-1],1))
            else :
               if tempQuery[i-1]=='-':
                 variablesVal.append((tempQuery[i],str(hidden-1)+'-'))
                 probVal.append(self.getPossibleValues(tempQuery[i],tempQuery[i-1],1))
               elif tempQuery[i-1]=='_':
                 variablesVal.append((tempQuery[i],tempQuery[i-1]))
                 probVal.append(self.getPossibleValues(tempQuery[i],tempQuery[i-1],1))
        #Variablevar from above step contains various factors..where each hidden variable has been given a
        #unique name
        SinglehiddenRemovedVar=[]
        SinglehiddenRemovedProbVal=[]
        i=0
        while i < len(variablesVal):
          cur=variablesVal[i]
          curprobVal=probVal[i]
          if '-' in cur[0]:
              next=variablesVal[i+1]
              nextprobVal=probVal[i+1]
              if cur[0]==next[1]:
                curprobVal=self.removeHiddenVariable(cur, next, curprobVal, nextprobVal,1)
                cur=(next[0],cur[1])
                i=i+1
                if i+1==len(variablesVal):
                  SinglehiddenRemovedVar.append(cur)
                  SinglehiddenRemovedProbVal.append(curprobVal)
                  break
          i=i+1
          SinglehiddenRemovedVar.append(cur)
          SinglehiddenRemovedProbVal.append(curprobVal)
        #In above we've applied one-level hidden variable deletion using memoization  
        hiddenRemovedVar=[]
        hiddenRemovedProbVal=[]
        i=0
        while i < len(SinglehiddenRemovedVar):
           #if hidden Variable is present in this,and next
           cur=SinglehiddenRemovedVar[i]
           curprobVal=SinglehiddenRemovedProbVal[i]
           if i+1==len(SinglehiddenRemovedVar):
                hiddenRemovedVar.append(cur)
                hiddenRemovedProbVal.append(curprobVal)
                break
           next=SinglehiddenRemovedVar[i+1]
           nextprobVal=SinglehiddenRemovedProbVal[i+1]
           #Remove hidden variables
           if cur[0]==next[1] and '-' in cur[0]:
              curprobVal=self.removeHiddenVariable(cur, next, curprobVal, nextprobVal,0)
              cur=(next[0],cur[1])
              #checking for continuous hidden variables
              i=i+1
              if i+1==len(SinglehiddenRemovedProbVal):
                hiddenRemovedVar.append(cur)
                hiddenRemovedProbVal.append(curprobVal)
                break
           i=i+1
           hiddenRemovedVar.append(cur)
           hiddenRemovedProbVal.append(curprobVal)
        #Now hiddenRemovedVar contains no hidden variable, but just two factors corresponding to 
        #missing variable
        #Substitute various values of missing variable in probability table and return the highest letter
        alphabet = list(string.ascii_lowercase)
        try:
          cleanVar1=hiddenRemovedVar[0]
          cleanVar2=hiddenRemovedVar[1]
          cleanProb1=hiddenRemovedProbVal[0]
          cleanProb2=hiddenRemovedProbVal[1]
          finalProb={}
        
          for k in alphabet:
            pr=1.0
            if cleanVar1[0]=='_':
              pr=pr*cleanProb1[k,cleanVar1[1]]
            elif cleanVar1[1]=='_':
              pr=pr*cleanProb1[cleanVar1[0],k]
            if cleanVar2[0]=='_':
              pr=pr*cleanProb2[k,cleanVar2[1]]
            elif cleanVar2[1]=='_':
              pr=pr*cleanProb2[cleanVar2[0],k]
            finalProb[k]=pr
        except:
           print 'Exception in solve'
        #print max(finalProb, key=finalProb.get)
        return max(finalProb, key=finalProb.get);

