def regulatex(listx):
    #print(listx)
    time = 5
    i = 0
    xbass = listx[0]
    while(i<len(listx)):
        if(listx[i] < xbass):
            xbass = listx[i]
        if(i%time == 4):
            listx[i] = listx[i-1] = listx[i-2] = listx[i-3] = listx[i-4] = xbass

        i = i+1

    return listx
