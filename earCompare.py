def compareEar(ear1, ear2, alpha=0.5):
    accuracy = 100
    for i in range(len(ear1[0])):
        accuracy-= alpha * abs(ear1[0][i] - ear2[0][i])
    for i in range(len(ear1[1])):
        accuracy-= alpha * abs(ear1[1][i] - ear2[1][i])
    return round(accuracy,2)
    