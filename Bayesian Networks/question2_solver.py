import string

class Question2_Solver:
    def __init__(self, cpt):
        self.cpt = cpt;
        return;

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
    #    query: "que__ion";
    #    return ["s", "t"];
    def solve(self, query):
        tempQuery="`"+query+"`"
        x = tempQuery.index('_');
        y = x+1;
        alphabet = list(string.ascii_lowercase)
        pr = { (i,j):1 for i in alphabet for j in alphabet } ;
        for l in alphabet:
            query1 = tempQuery.replace(query[x],l,1);
            for k in alphabet:
                query2 = query1.replace(query1[y],k);          
                pr[l,k] = (self.cpt.conditional_prob(query2[x], query2[x-1])*self.cpt.conditional_prob(query2[y], query2[x])*self.cpt.conditional_prob(query2[y+1], query2[y]));
           
        maxx = max(pr.values()) ;
        keys = [(x,z) for (x,z),y in pr.items() if y ==maxx];
    
        return [keys[0][0], keys[0][1]];


