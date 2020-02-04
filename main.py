import pandas as pd
import math
df = pd.read_csv('data.csv')
df_ = df.drop(['Class'], axis = 1) 

# print(df)

def I_pn(p, n ):
    if(p == 0):
        return - (n / (p + n))* (math.log2(n / (p + n)))
    elif(n == 0):
        return  -(p / (p + n)) * (math.log2(p / (p + n)))
    else:
        return -(p / (p + n)) * (math.log2(p / (p + n))) - (n / (p + n))* (math.log2(n / (p + n)))

def Entropy(plist, nlist, ilist, p , n):
    result = 0
    for i in range(len(plist)):
        result += (plist[i] + nlist[i])/ (p + n) * ilist[i]
    return result



# Calculating I(p,n) for entire table
p = df['Class'].value_counts()[1]
n = df['Class'].value_counts()[0]
I_pn_total = I_pn(p,n)

print("I_pn of entire data = {0:.2f}".format(I_pn_total))

# Calculating Entropy and Gain of Entire data
columns = df_.columns
Entropy_attr,Gain_attr = [], []
for attribute in columns:
    set_ = set(df_[attribute])
    p_temp,n_temp = 0,0
    pi,ni,I_pi_ni = [],[],[]
    for attr_val in set_:
        if (df[df[attribute] == attr_val].Class.value_counts(sort = False).shape == (2,)):
            p_temp = df[df[attribute] == attr_val].Class.value_counts(sort = False).loc['Yes']
            n_temp = df[df[attribute] == attr_val].Class.value_counts(sort = False).loc['No']
        elif(df[df[attribute] == attr_val].Class.value_counts(sort = False).index[0] == 'Yes'):
            p_temp = df[df[attribute] == attr_val].Class.value_counts(sort = False).loc['Yes']
            n_temp = 0
        else:
            p_temp = 0
            n_temp = df[df[attribute] == attr_val].Class.value_counts(sort = False).loc['No']
        pi.append(p_temp)
        ni.append(n_temp)
        I_pi_ni_value = I_pn(p_temp,n_temp)
#         print("I_pi_ni_value = ", I_pi_ni_value)
        I_pi_ni.append(I_pi_ni_value)
#     print("I_pi_ni=",I_pi_ni)
    Entropy_attr_val = Entropy(pi, ni, I_pi_ni,3, 5)
    Entropy_attr.append(Entropy_attr_val)
    Gain_attr_value = I_pn(3,5) - Entropy_attr_val
    Gain_attr.append(Gain_attr_value)

print("The Root Of the Decision Tree Is:", df.columns[Gain_attr.index(max(Gain_attr))])