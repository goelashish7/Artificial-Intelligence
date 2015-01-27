import string
class Question5_Solver:
    def __init__(self, cpt2):
        self.cpt2 = cpt2;
        return;

    #####################################
    # ADD YOUR CODE HERE
    #         _________
    #        |         v
    # Given  z -> y -> x
    # Pr(x|z,y) = self.cpt2.conditional_prob(x, z, y);
    #
    # A word begins with "``" and ends with "``".
    # For example, the probability of word "ab":
    # Pr("ab") = \
    #    self.cpt2.conditional_prob("a", "`", "`") * \
    #    self.cpt2.conditional_prob("b", "`", "a") * \
    #    self.cpt2.conditional_prob("`", "a", "b") * \
    #    self.cpt2.conditional_prob("`", "b", "`");
    # query example:
    #    query: "ques_ion";
    #    return "t";
    def solve(self, query):
        tempQuery ="`"+"`"+query+"`"+"`"
        x = tempQuery.index('_');
        j = len(tempQuery);
        pr = [];
        alphabet = list(string.ascii_lowercase)
        for i in range(len(alphabet)):
            pr.append(1);
              
        for l in alphabet:
            query1 = tempQuery.replace(tempQuery[x],l);
            pr[alphabet.index(l)] *= self.cpt2.conditional_prob(query1[x], query1[x-2], query1[x-1])*self.cpt2.conditional_prob(query1[x+1], query1[x-1], query1[x])*self.cpt2.conditional_prob(query1[x+2], query1[x], query1[x+1]);
        t = alphabet[pr.index(max(pr))]
        return t;
    

