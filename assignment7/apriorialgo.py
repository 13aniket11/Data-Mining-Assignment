import numpy as np
import pandas as pd
from itertools import combinations

# Reading Excel file 
def aa_helper(op,transaction,bread):
    # bread = pd.read_csv(filename)

    # bread = bread.drop_duplicates()

    # bread = bread.drop('DateTime', axis=1)
    # print(len(set(bread['Items'])))
    # print(bread.head)

    # transaction = pd.crosstab(index= bread['TransactionNo'], columns= bread['Items'])
    # print(transaction)


    def APRIORI_MY(data, min_support=0.04,  max_length = 4):
        # Collecting Required Library
        
        # Step 1:
        # Creating a dictionary to stored support of an itemset.
        support = {} 
        L = list(data.columns)
        
        # Step 2: 
        #generating combination of items with len i in ith iteration
        for i in range(1, max_length+1):
            c = set(combinations(L,i))
            
        # Reset "L" for next ith iteration
            L =set()     
        # Step 3: 
            #iterate through each item in "c"
            for j in list(c):
                #print(j)
                sup = data.loc[:,j].product(axis=1).sum()/len(data.index)
                if sup > min_support:
                    #print(sup, j)
                    support[j] = sup
                    
                    # Appending frequent itemset in list "L", already reset list "L" 
                    L = list(set(L) | set(j))
            
        # Step 4: data frame with cols "items", 'support'
        result = pd.DataFrame(list(support.items()), columns = ["Items", "Support"])
        return(result)

    ## finding frequent itemset with min support = 4%
    if(op == "1"):
        print(op)
        my_freq_itemset = APRIORI_MY(transaction, 0.04, 3)
        my_freq_itemset.sort_values(by = 'Support', ascending = False)
        return my_freq_itemset

    # print(my_freq_itemset)

    def ASSOCIATION_RULE_MY(df, min_threshold=0.5):
        import pandas as pd
        from itertools import permutations
        
        # STEP 1:
        #creating required varaible
        support = pd.Series(df.Support.values, index=df.Items).to_dict()
        data = []
        L= df.Items.values
        
        # Step 2:
        #generating rule using permutation
        p = list(permutations(L, 2))
        
        # Iterating through each rule
        for i in p:
            
            # If LHS(Antecedent) of rule is subset of RHS then valid rule.
            if set(i[0]).issubset(i[1]):
                conf = support[i[1]]/support[i[0]]
                #print(i, conf)
                if conf > min_threshold:
                    #print(i, conf)
                    j = i[1][not i[1].index(i[0][0])]
                    lift = support[i[1]]/(support[i[0]]* support[(j,)])
                    leverage = support[i[1]] - (support[i[0]]* support[(j,)])
                    convection = (1 - support[(j,)])/(1- conf)
                    data.append([i[0], (j,), support[i[0]], support[(j,)], support[i[1]], conf, lift, leverage, convection])

            
        # STEP 3:
        result = pd.DataFrame(data, columns = ["antecedents", "consequents", "antecedent support", "consequent support",
                                            "support", "confidence", "Lift", "Leverage", "Convection"])
        return(result)

    ## Rule with minimun confidence = 50%
    if(op == "2"):
        print(op)
        my_freq_itemset = APRIORI_MY(transaction, 0.04, 3)
        my_freq_itemset.sort_values(by = 'Support', ascending = False)
        my_rule = ASSOCIATION_RULE_MY(my_freq_itemset, 0.5)
        return my_rule
        print(my_rule)












# import pandas as pd


# def app(dataset):
#     # st.header("Assignment 7")

#     url = 'https://raw.githubusercontent.com/Udayraj2806/dataset/main/house-votes-84.data.csv'
#     df = pd.read_csv(url)

#     # st.write(df[:5])
#     d = pd.DataFrame(df)
#     data = d
#     d.head()

#     df_rows = d.to_numpy().tolist()

#     cols = []
#     for i in data.columns:
#         cols.append(i)
#     # st.write(cols)
#     print(cols)
#     col_len = len(cols)
#     # st.write("At Max Rules to be Generated: ",
#     #          ((3**col_len)-(2**(col_len+1)))+1)
#     # st.write("Attributes:", len(cols))
#     # st.write(cols)
#     newDataSet = []
#     # st.write(len(df_rows))
#     i, cnt = 0, 0
#     for row in df_rows:
#         i += 1
#         if '?' in row:
#             continue
#         else:
#             lst = []
#             cnt += 1
#             for k in range(1, len(row)):
#                 if row[k] == 'y':
#                     lst.append(cols[k])
#             newDataSet.append(lst)
#     # st.write(newDataSet)

#     # st.write(row)
#     # st.write("--------------")
#     # st.write(cnt)
#     # st.write(newDataSet)
#     # newDataSet.drop()

#     data = []

#     for i in range(len(newDataSet)):
#         # data[i] = newDataSet[i]
#         data.append([i, newDataSet[i]])

#     # st.write(data)

#     # extract distinct items

#     init = []
#     for i in data:
#         for q in i[1]:
#             if (q not in init):
#                 init.append(q)
#     init = sorted(init)

#     # st.write("Init:", len(init))

#     # st.write(init)

#     sp = 0.4
#     s = int(sp*len(init))
#     s

#     from collections import Counter
#     c = Counter()
#     for i in init:
#         for d in data:
#             if (i in d[1]):
#                 c[i] += 1
#     # st.write("C1:")
#     for i in c:
#         pass
#         # st.write(str([i])+": "+str(c[i]))
#     # st.write()
#     l = Counter()
#     for i in c:
#         if (c[i] >= s):
#             l[frozenset([i])] += c[i]
#     # st.write("L1:")
#     for i in l:
#         pass
#         # st.write(str(list(i))+": "+str(l[i]))
#     # st.write()
#     pl = l
#     pos = 1
#     for count in range(2, 1000):
#         nc = set()
#         temp = list(l)
#         for i in range(0, len(temp)):
#             for j in range(i+1, len(temp)):
#                 t = temp[i].union(temp[j])
#                 if (len(t) == count):
#                     nc.add(temp[i].union(temp[j]))
#         nc = list(nc)
#         c = Counter()
#         for i in nc:
#             c[i] = 0
#             for q in data:
#                 temp = set(q[1])
#                 if (i.issubset(temp)):
#                     c[i] += 1
#         # st.write("C"+str(count)+":")
#         for i in c:
#             pass
#             # st.write(str(list(i))+": "+str(c[i]))
#         # st.write()
#         l = Counter()
#         for i in c:
#             if (c[i] >= s):
#                 l[i] += c[i]
#         # st.write("L"+str(count)+":")
#         for i in l:
#             pass
#             # st.write(str(list(i))+": "+str(l[i]))
#         # st.write()
#         if (len(l) == 0):
#             break
#         pl = l
#         pos = count
#     # st.write("Result: ")
#     # st.write("L"+str(pos)+":")

#     for i in pl:
#         print(str(list(i))+": "+str(pl[i]))
#     #     st.write(str(list(i))+": "+str(pl[i]))

#     # st.subheader("Rules Generation")
#     for l in pl:
#         print(l)
#     #     st.write(l)
#     #     break
#     from itertools import combinations
#     for l in pl:
#         cnt = 0
#         c = [frozenset(q) for q in combinations(l, len(l)-1)]
#         mmax = 0
#         for a in c:
#             b = l-a
#             ab = l
#             sab = 0
#             sa = 0
#             sb = 0
#             for q in data:
#                 temp = set(q[1])
#                 if (a.issubset(temp)):
#                     sa += 1
#                 if (b.issubset(temp)):
#                     sb += 1
#                 if (ab.issubset(temp)):
#                     sab += 1
#             temp = sab/sa*100
#             if (temp > mmax):
#                 mmax = temp
#             temp = sab/sb*100
#             if (temp > mmax):
#                 mmax = temp
#             cnt += 1
#             # st.write(str(cnt) + str(list(a))+" -> " +
#             #          str(list(b))+" = "+str(sab/sa*100)+"%")
#             cnt += 1
#             # st.write(str(cnt) + str(list(b))+" -> " +
#             #          str(list(a))+" = "+str(sab/sb*100)+"%")
#         # mmax = st.number_input('Select value of alpha', step=5, min_value=5)
#         mmax = int(mmax)
#         curr = 1
#         # st.write("choosing:", end=' ')

#         for a in c:
#             b = l-a
#             ab = l
#             sab = 0
#             sa = 0
#             sb = 0
#             for q in data:
#                 temp = set(q[1])
#                 if (a.issubset(temp)):
#                     sa += 1
#                 if (b.issubset(temp)):
#                     sb += 1
#                 if (ab.issubset(temp)):
#                     sab += 1
#             temp = sab/sa*100
#             # if (temp >= mmax):
#             #     st.write(curr, end=' ')
#             curr += 1
#             temp = sab/sb*100
#             # if (temp >= mmax):
#             #     st.write(curr, end=' ')
#             curr += 1
#             # break
#         # st.write()
#         # st.write()
#         break

# app("")