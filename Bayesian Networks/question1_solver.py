import string
class Question1_Solver:
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
    #    query: "ques_ion";
    #    return "t";
    
    def solve(self, query):
        tempQuery ="`"+query+"`"
        x = tempQuery.index('_');
        len_query = len(tempQuery);
        alphabet = list(string.ascii_lowercase)
        prob_alpha = []
        for i in range(len(alphabet)):
            prob_alpha.append(1);
        for l in alphabet:
            new_query = tempQuery.replace(tempQuery[x],l)
            prob_alpha[alphabet.index(l)]*= self.cpt.conditional_prob(new_query[x], new_query[x-1])*self.cpt.conditional_prob(new_query[x+1], new_query[x])
        t = alphabet[prob_alpha.index(max(prob_alpha))]
        return t;    

