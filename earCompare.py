from math import exp as e

def compareEar(ear1, ear2, a=0.5):
    '''
        accuracy = 100 - Σ (e^a(fv₁[i]-fv₂[i]) - 1)
        a : senstivity of comparison function
    '''
    diff = 0
    for i in range(len(ear1[0])):
        diff+= abs(ear1[0][i] - ear2[0][i])
    for i in range(len(ear1[1])):
        diff+= abs(ear1[1][i] - ear2[1][i])
    accuracy = 100 - (e(diff*a) - 1)
    if accuracy<0:
        accuracy=0.00
    return round(accuracy,2)

def compareEar2(ear1, ear2, a=0.5):
    '''
        accuracy = 100 - Σ (e^a(fv₁[i]-fv₂[i]) - 1)
        a : senstivity of comparison function
    '''
    accuracy = 100
    for i in range(len(ear1[0])):
        accuracy-= (e(abs(ear1[0][i] - ear2[0][i])*a)-1)
    for i in range(len(ear1[1])):
        accuracy-= (e(abs(ear1[1][i] - ear2[1][i])*a)-1)
    if(accuracy<0):
        accuracy = 0.00
    return round(accuracy,2)
    