import random
def dummyFeatureVector(size):
    '''
        generate dummy feature vector of given size 
    '''
    size = size // 2
    fv = []
    temp = []
    for i in range(size):
        temp.append(round(random.randint(500,8000)*0.01,2))
    temp.sort(reverse=True)
    for item in temp:
        fv.append(item)
    fv.append(0)
    temp.clear()
    for i in range(size):
        temp.append(round(random.randint(500,8000)*0.01,2))
    temp.sort(reverse=False)
    for item in temp:
        fv.append(item)
    return fv

def getDummyFeatureVector(fv1size=19, fv2size=9):
    '''
        return list of two dummy feature vector fv1 and fv2 of size fv1size and fv2size respectively
    '''
    return [dummyFeatureVector(fv1size),dummyFeatureVector(fv2size)]

if __name__=='__main__':
    print(getDummyFeatureVector())