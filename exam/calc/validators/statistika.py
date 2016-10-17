from exam.calc import models as calc
from exam.calc.models import Dataset, Section, Task, Answer, Question, CalculatedAnswer
import validator_core
import stats
from django.contrib.auth.models import User
import math
from pprint import pprint
import statistics

from scipy.stats import t

def test():
    uid = '21030101'
   
    var1 = variabla(uid, 'var1')
    var2 = variabla(uid, 'var2')
    year1 = variabla(uid, 'var1.year')
    year2 = variabla(uid, 'var2.year')

    r =  aritmeticna(var2, year1)
    print var1, var2
    i = '-2.664'

    a1 = aritmeticna(var1, year1)
    '''
    print 'a2', aritmeticna(var2, year1)
    print 'st1', std_odklon(var1, year1)
    print 'std', std_odklon(var2, year1)
    print 'q1',kvartil(var1, year1, 0.25)
    print 'q2',kvartil(var1, year1, 0.5)
    print 'q3',kvartil(var1, year1, 0.75)

    print vzorcna_aritmeticna(var1, year1)
    print vzorcna_varianca(var1, year1)

    print zaupanje_aritmeticna(var1, year1)
    print zaupanje_varianca(var1, year1)

    print seznam_vzorec(var1, year1), '\n\n'
    print seznam_vzorec(var1, year1, 'new'), '\n\n'
    print seznam_vzorec(var1, year1, 'old'), '\n\n'

    print eu_vzorcna_varianca(var1, year1, 'new')
    print eu_vzorcna_varianca(var1, year1, 'old')
    foo = eu_skupni_std_odklon(var1, year1)
    print foo
    print primerjaj('15.317', foo[0]) 
    print eu_std_razlika_vzorcnih_arit_sred(var1, year1)
    '''

    print 'kontingencna:', kontingencna(var1, year1)
    print 'hikvadrat', hikvadrat(var1, year1)
    print alpha(var1, year1)
    print nal_32b(var1, year1, var2, year2)
    print 'kontingencni', kontingencni(var1, year1)
    print 'regex', cregr(var1, year1, var2, year2, 'y=12.2+0.000103x')

    print "Rang:", rang(var1, year1, 7)

    print primerjaj('0.00006',kontingencni(var1, year1)[0])

def nal_32b(var1, year1, var2, year2):
    v1 = seznam_vzorec(var1, year1)[1]
    v2 = seznam(var2, year2)[1]
    
    for i in v2.copy():
      if not v1.has_key(i):
        del(v2[i])

    # iz drugega seznama je treba zbrisat tiste vnose, ki jih ni v prvem
    temp = dict(v1)
    for i in temp:
        try:
            v2[i]
        except KeyError:
            v1.__delitem__(i)
    temp = dict(v2)
    for i in temp:
        try:
            v1[i]
        except KeyError:
            v2.__delitem__(i)
    n = len(v2)
    
    sez1 = []
    for i in range(1,29):
        try:
            sez1.append(v1['c'+str(i)])
        except KeyError:
            pass
    sez2 = []
    for i in range(1,29):
        try:
            sez2.append(v2['c'+str(i)])
        except KeyError:
            pass
    
    as1 = stats.lmean(sez1)
    as2 = stats.lmean(sez2)

    c = 0
    d = 0
    e = 0
    for i in range(0, n):

        c = c + (sez1[i] - as1)*(sez2[i] - as2)
        d = d + (sez1[i] - as1)**2
        e = e + (sez2[i] - as2)**2

        # print sez1[i], sez2[i], c, d, e
    rxy = round(c / math.sqrt(d*e),4)

    texp = (rxy*math.sqrt(n-2)) / math.sqrt(1 - rxy**2) 

    s = math.sqrt( d / (n - 1))
    mm1 = c / d
    mm2 = c / e


    X = as2
    Y = as1
   
    regr1a = Y + mm2*((-1)*X)
    regr1b = mm2
    
    regr2a = X + mm1*((-1)*Y)
    regr2b = mm1

    R = rxy**2

    o = s * math.sqrt(1 - R)

    return as1, as2, rxy, texp, (regr1a, regr1b), (regr2a, regr2b), R, o

def cregr_ab(var1, year1, var2, year2):
    reg = nal_32b(var1, year1, var2, year2)
    a = reg[4][0]
    b = reg[4][1]
    
    return a,b
    
def cregr(var1, year1, var2, year2, input):
    if input == 'uporabizapreverjane':
        reg = nal_32b(var1, year1, var2, year2)
        s1 = 'x: ' + str(round(reg[5][0],5)) + ' ' + str(round(reg[5][1],5))
        s2 = 'y: ' + str(round(reg[4][0],5)) + ' ' + str(round(reg[4][1],5))
        s = s1 + ';' + s2
        return s

    import re

    rawstr = r"""([xX|yY])+[\=]+([\+|\-]?[0-9+[.|,]+?]*)([\+|\-][0-9+[.|,]+]*)([xX|yY])"""
    embedded_rawstr = r"""(?i)([xX|yY])+[\=]+([\+|\-]?[0-9+[.|,]+?]*)([\+|\-][0-9+[.|,]+]*)([xX|yYY])"""
    matchstr = ""+input+""
    compile_obj = re.compile(rawstr)
    match_obj = compile_obj.search(matchstr)

    if match_obj == None:
        return False

    all_groups = match_obj.groups()
    
    group_1 = match_obj.group(1)
    group_2 = match_obj.group(2)
    group_3 = match_obj.group(3)
    group_4 = match_obj.group(4)

    reg = nal_32b(var1, year1, var2, year2)

    if group_1.lower() == 'x':
        a1 = primerjaj(group_2, reg[5][0], solve=False)
        a2 = primerjaj(group_3, reg[5][1], solve=False)
    elif group_1.lower() == 'y':
        a1 = primerjaj(group_2, reg[4][0], solve=False)
        a2 = primerjaj(group_3, reg[4][1], solve=False)
    else:
        return False

    if a1 and a2:
        return True
    else:
        return False

def kontingencni(var, year):
    hi = hikvadrat(var, year)[0]
    n = kontingencna(var, year)[4]
    
    c = math.sqrt(hi / (hi + n))
    #WTF?
    #cmax = math.sqrt( (2-1)/2)
    k = 2.0
    cmax = math.sqrt( (k - 1.0) / k)
    cpop = c/cmax

    return c, cmax, cpop

def alpha(var, year):
    hi = hikvadrat(var, year)[0]
    n = kontingencna(var, year)[4]
    k = 2

    a = math.sqrt(hi / float(n * (k - 1)))

    return a

def hikvadrat(var, year):
    t11, t21, t12, t22, n = kontingencna(var, year)
    
    f11 = ((t11+t21) / float(n)) * ((t11 + t12) / float(n)) * n
    f21 = ((t11+t21) / float(n)) * ((t21 + t22) / float(n)) * n
    f12 = ((t12+t22) / float(n)) * ((t11 + t12) / float(n)) * n
    f22 = ((t12+t22) / float(n)) * ((t21 + t22) / float(n)) * n
    
    
    if f11 == 0:
      a = 0
    else:
      a = (((t11 - f11)**2)/f11)
      
    if f21 == 0:
      b = 0
    else:
      b = (((t21 - f21)**2)/f21)
      
    if f12 == 0:
      c = 0
    else:
      c = (((t12 - f12)**2)/f12)
      
    if f22 == 0:
      d = 0
    else:
      d = (((t22 - f22)**2)/f22)
      
    hi2 = a + b + c + d

    return hi2, f11, f21, f12, f22
        
def strukturni_odstotki(var, year):
    t11, t21, t12, t22, n = kontingencna(var, year)
  
    # print t11, t21, t12, t22
  
    o11 = t11 / float(t11+t12) * 100
    o12 = t12 / float(t11+t12) * 100
    o21 = t21 / float(t21+t22) * 100
    o22 = t22 / float(t21+t22) * 100
    
    # print o11, o12, o21, o22
    
    return o11, o12, o21, o22

def kontingencna(var, year):
    stare = seznam_vzorec(var, year, 'old', sez=True)[0]
    stare.sort()

    # Removes 0 from sample values
    # while True:
    #     try:
    #         stare.remove(0)
    #     except ValueError:
    #         break

    nove  = seznam_vzorec(var, year, 'new', sez=True)[0]
    nove.sort()

    # Removes 0 from sample values
    # while True:
    #     try:
    #         nove.remove(0)
    #     except ValueError:
    #         break

    #med = kvartili(var, year)[1]
    sez = seznam(var, year)[0]
    sez.sort()

    med = mediana(sez)
    ms = med
    mn = med
    
    #print "mediana je", med

    t11 = 0
    t21 = 0
    t12 = 0
    t22 = 0
    for i in stare:
        if i <= ms:
            t11 = t11 + 1
        else:
            t12 = t12 + 1
    for i in nove:
        if i <= mn:
            t21 = t21 + 1
        else:
            t22 = t22 + 1
    
    n = t11 + t21 + t12 + t22
    
    return t11, t21, t12, t22, n
    
def mediana(seznam):
    while True:
        try:
            seznam.remove(0)
        except ValueError:
            break

    n = len(seznam)
   
    if n % 2 != 0:        
        mm = ((n -1) / 2) + 1
        # REMOVE one because lists begin with 0
        Me = seznam[mm-1]
    else:
        m = n/2
        xm = seznam[m-1]
        xm1 = seznam[m]
        Me = (xm + xm1) / 2
    return Me

def sorted(x):
    x.sort()
    return x

def kvartil(var, year, p):
    i, m = seznam(var, year)

    r = ( p * len(i) ) + 0.5
    i.sort()

    r0 = int(r)
    r1 = int(r) + 1

    x0 = i[r0 - 1]
    x1 = i[r1 - 1]
    
    kvart = x0 + (x1 - x0) * ( (r - r0) / (r1 - r0))
    return kvart

def rang(var, year, r):
    def _countrysort(x, y):
      compare1 = cmp(x[0], y[0])
      
      if not compare1:
        x1 = int(x[1][1:])
        y1 = int(y[1][1:])
        
        return cmp(x1, y1)
      else:
        return compare1
      
    i, m = seznam(var, year)

    s = []
    items = [(v, k) for k, v in m.items()]
    
    items.sort(lambda x,y: _countrysort(x,y))
    items = [(k, v) for v, k in items]

    s = items

    counter = 1
    for j in s:
        if j[0] == 'c25':
            slovenija = counter
        counter = counter + 1

    #print slovenija

    return slovenija

def variabla(uid, polje):
    user = User.objects.get(username=uid)
    r = eval('user.get_profile().'+polje)
    return r

def seznam_vzorec(var, year, eu=None, sez=None):
    #a = uset.datasets.get_object(varname__exact=var, year__exact=year).sel.split(', ')
    #exam.calc.DataSet.objects.get(varname__exact=var, year__exact=year).get_selected_countries
    a = Dataset.objects.get(varname__exact=var, year__exact=year).sel.split(', ')[0:18]

    if not sez:
        sez = []
        for t in a:
            sez.append(int(t))
        sez.sort()
    else:
        sez = range(1,29)

    old_member = [1,2,6,8,9,10,12,13,16,19,20,22,26,27,28]
    new_member = [3,4,5,7,11,14,15,17,18,21,23,24,25]

    #i = uset.datasets.get_object(varname__exact=var, year__exact=year).__dict__
    i = Dataset.objects.get(varname__exact=var, year__exact=year).__dict__
    x = []
    y = {}
    for m in range(1,29):
        if m in sez:
            if   eu == None:
                     ok = True
            elif eu == 'new':
                 if m in new_member:
                     ok = True
                 else:
                     ok = False
            elif eu == 'old':
                 if m in old_member:
                     ok = True
                 else:
                     ok = False
            else:
                ok = True
            if ok:
                if i['c'+str(m)] != None:
                  x.append(i['c'+str(m)])
                  y.__setitem__('c'+str(m), i['c'+str(m)])
                ok = False
    return  x,y

def seznam(var, year):
    #i = uset.datasets.get_object(varname__exact=var, year__exact=year).__dict__
    #print Dataset.objects.get(varname__exact=var, year__exact=year).id
    i = Dataset.objects.get(varname__exact=var, year__exact=year).__dict__
    x = []
    y = {}
    for m in range(1,29):
        # if i['c'+str(m)] == 0:
        if i['c'+str(m)] == None:
            pass
        else:
            value = float(str(i['c'+str(m)]))
            x.append(value)
            y.__setitem__('c'+str(m), value)
    return x, y

def primerjaj(input, rezultat, solve, const=0.001, absolute=False, return_const=False):
    # print input, rezultat, solve, const, absolute, return_const
    if return_const:
      return const
      
    if absolute and type(rezultat) != list:
      rezultat = abs(rezultat)
  
    if type(rezultat) == list:
        pass
    elif rezultat == 0 or (round(rezultat, 10) == 0.0):
        i1 = rezultat - const
        i2 = rezultat + const
    else:
        i1 = rezultat * (1 - const)
        i2 = rezultat * (1 + const)

        # print i1, i2

    if solve:
      if type(rezultat) == list:
        return rezultat[0]
      else:
        return rezultat

    input = input.replace(',','.')
    try:
        x = float(input)
    except:
        return False
                
    if absolute:
        x = abs(x)
    
    if type(rezultat) == list:
      if x in rezultat:
        r = True
      else:
        r = False
    elif const == 0:
      if rezultat == x:
        r = True
      else:
        r = False      
    elif x < 0:
        #negativna
        if (i1 > x) and (i2 < x):
            r = True
        else:
            r = False
    else:
        #pozitivna
        #print i1, i2, x
        if (i1 < x) and (i2 > x):
            r = True
        elif (i1 == 0) and (i2 == 0):
            r = True
        elif (i1 == i2):
            r = True
        else:
            r = False

    print "Primerjam %s in %s pri %s in je %s [%s, %s]" % (input, rezultat, const, r, i1, i2)
    
    return r

def aritmeticna(var, year):
    s = seznam(var, year)
    arit = stats.lmean(s[0])
    
    return arit

def zaupanje_aritmeticna(var, year):
    s,f = seznam_vzorec(var, year)
    n = len(s)
    asredina = stats.lmean(s)
    #z = 2.093
    
    # print n, "artimeticna", var, year
    probability = 0.10
    
    z = round(statistics.tinv(probability, n-1), 2)
    # print "z is", z
           
    std = math.sqrt(vzorcna_varianca(var, year)[0])

    interval1 = asredina - (z * (std / math.sqrt(n)) )
    interval2 = asredina + (z * (std / math.sqrt(n)) )

    return interval1, interval2

def zaupanje_varianca(var, year):
    s,f = seznam_vzorec(var, year)
    n = len(s)
    #z1 = 32.9
    #z2 = 8.91
    
    if n == 25:
     z1 = 39.36
     z2 = 12.4
    elif n == 24:
     z1 = 38.08
     z2 = 11.69
    elif n == 23:
     z1 = 36.78
     z2 = 10.98
    elif n == 22:
     z1 = 35.48
     z2 = 10.28
    elif n == 21:
     z1 = 34.17
     z2 = 9.59
    elif n == 20:
     z1 = 32.85
     z2 = 8.91
    elif n == 19:
     z1 = 31.53
     z2 = 8.23
    elif n == 18:
     z1 = 30.19
     z2 = 7.56
    elif n == 17:
     z1 = 28.85
     z2 = 6.91
    elif n == 16:
     z1 = 27.49
     z2 = 6.26
    elif n == 15:
     z1 = 26.12
     z2 = 5.63
    elif n == 14:
     z1 = 24.74
     z2 = 5.01
    elif n == 13:
     z1 = 23.34
     z2 = 4.4
    elif n == 12:
     z1 = 21.92
     z2 = 3.82
    elif n == 11:
     z1 = 20.48
     z2 = 3.25
    elif n == 10:
     z1 = 19.02
     z2 = 2.7
    elif n == 9:
     z1 = 17.53
     z2 = 2.18
    elif n == 8:
     z1 = 16.01
     z2 = 1.69
    elif n == 7:
     z1 = 14.45
     z2 = 1.24
    elif n == 6:
     z1 = 12.83
     z2 = 0.83
    elif n == 5:
     z1 = 11.14
     z2 = 0.48
    elif n == 4:
     z1 = 9.35
     z2 = 0.22
    elif n == 3:
     z1 = 7.38
     z2 = 0.05
    
    s2 = vzorcna_varianca(var, year)[0]

    interval1 = ((n -1) * s2) / z1
    interval2 = ((n -1) * s2) / z2

    return interval1, interval2, math.sqrt(interval1), math.sqrt(interval2)

def vzorcna_aritmeticna(var, year, eu=None):
    s = seznam_vzorec(var, year, eu)
    arit = stats.lmean(s[0])
    
    return arit

def vzorcna_varianca(var, year):
    s,f = seznam_vzorec(var, year)
    n = len(s) - 1
    asredina = stats.lmean(s)
    
    x = 0
    for i in s:
        x = x + (i - asredina)*(i - asredina)

    vv = x / float(n)

    return vv, math.sqrt(vv)

def eu_arit_sred(var, year, eu):
    s,f = seznam_vzorec(var, year, eu)
    asredina = stats.lmean(s)

    return asredina

def eu_vzorcna_varianca(var, year, eu):
    s,f = seznam_vzorec(var, year, eu)
    asredina = stats.lmean(s)
    n = len(s)

    m = 0
    for i in s:
        m = m + ((i - asredina) * (i - asredina))
    s2 = m / (n - 1)
    vso = math.sqrt(s2)

    return vso, s2

def eu_skupni_std_odklon(var, year):
    s2n = eu_vzorcna_varianca(var, year, 'new')[1]
    s2s = eu_vzorcna_varianca(var, year, 'old')[1]

    s,f = seznam_vzorec(var, year, 'new')
    nn = len(s)
    s,f = seznam_vzorec(var, year, 'old')
    ns = len(s)

    s2 = (((nn - 1) * s2n) + ((ns - 1) * s2s)) / (nn + ns - 2)
    s = math.sqrt(s2)

    return s,s2

def eu_std_razlika_vzorcnih_arit_sred(var, year):
    s,f = seznam_vzorec(var, year, 'new')
    as_n = stats.lmean(s)
    nn = len(s)
    s,f = seznam_vzorec(var, year, 'old')
    as_s = stats.lmean(s)
    ns = len(s)

    s = eu_skupni_std_odklon(var, year)[0]

    h = float((ns + nn) /( float(ns) * float(nn)))
    te = (as_s - as_n) / (s * math.sqrt(h) ) 

    return te

def eu_testna_statistika(var, year):
    #return 1.734
    s,f = seznam_vzorec(var, year)
    n = len(s)
    
    probability = 0.10
    #TODO figure out why n-2 and not n-1
    t = statistics.tinv(probability, n-2)
    
    return t

def tdist(var, year, x, eu=None):
    s,f = seznam_vzorec(var, year, eu=eu)
    n = len(s)
    x = abs(x)

    # print "=TDIST(%s, %s, 2)" % (x, n-2)
    result = ( 1-t.cdf(x, n-2) ) * 2
    return result

def std_odklon(var, year):
    s, m = seznam(var, year)
    std = stats.lsamplestdev(s)
    
    return std

def kvartili(var, year):
    s = seznam(var, year)[0]
    q1 = stats.lscoreatpercentile(s, 25)
    q2 = stats.lscoreatpercentile(s, 50)
    q3 = stats.lscoreatpercentile(s, 75)
    q4 = stats.lscoreatpercentile(s, 100)

    return round(q1,2), round(q2,2), round(q3,2), round(q4,2)

def t_vrednost(var, year):
    n = len(seznam_vzorec(var, year)[0])
    
    probability = 0.10
    t = statistics.tinv(probability, n-1)
    t_array = [round(t, 2),
               round(t, 3),
               round(t, 3)]
      
    return t_array

def hi2_sp_varianca(var, year):
    n = len(seznam_vzorec(var, year)[0])
    
    if n == 25:
      hi2_array = [39.36, 39.364, 39.3641]
    elif n == 24:
      hi2_array = [38.07, 38.075, 38.0756]
    elif n == 23:
      hi2_array = [36.78, 36.780, 36.7807]
    elif n == 22:
      hi2_array = [35.48, 35.479, 35.4789]
    elif n == 21:
      hi2_array = [34.16, 34.169, 34.1696]
    elif n == 20:
      hi2_array = [32.85, 32.852, 32.8523]
    elif n == 19:
      hi2_array = [31.53, 31.526, 31.5264]
    elif n == 18:
      hi2_array = [30.19, 30.191, 30.1910]
    elif n == 17:
      hi2_array = [28.85, 28.845, 28.8454]
    elif n == 16:
      hi2_array = [27.49, 27.488, 27.4884]
    elif n == 15:
      hi2_array = [26.12, 26.119, 26.1189]
    elif n == 14:
      hi2_array = [24.73, 24.736, 24.7356]
    elif n == 13:
      hi2_array = [23.33, 23.336, 23.3367]
    elif n == 12:
      hi2_array = [21.92, 21.920, 21.9200]
    elif n == 11:
      hi2_array = [20.48, 20.483, 20.4832]
    elif n == 10:
      hi2_array = [19.0, 19.02, 19.023, 19.0228, 19.02277]
    elif n == 9:
      hi2_array = [17.53, 17.534, 17.5345]
    elif n == 8:
      hi2_array = [16.01, 16.013, 16.0128]
    elif n == 7:
      hi2_array = [14.45, 14.449, 14.4494]
    elif n == 6:
      hi2_array = [12.83, 12.832, 12.8325]
    elif n == 5:
      hi2_array = [11.14, 11.143, 11.1433]
    elif n == 4:
      hi2_array = [9.35, 9.348, 9.3484]
    elif n == 3:
      hi2_array = [7.38, 7.378, 7.3778]
      
    return hi2_array
    
def hi2_zg_varianca(var, year):
    n = len(seznam_vzorec(var, year)[0])
    
    if n == 25:
          hi2_array = [12.4, 12.401, 12.4012]
    elif n == 24:
          hi2_array = [11.69, 11.689, 11.6886]
    elif n == 23:
          hi2_array = [10.98, 10.982, 10.9823]
    elif n == 22:
          hi2_array = [10.28, 10.283, 10.2829]
    elif n == 21:
          hi2_array = [9.59, 9.591, 9.5908]
    elif n == 20:
          hi2_array = [8.91, 8.907, 8.9065]
    elif n == 19:
          hi2_array = [8.23, 8.231, 8.2307]
    elif n == 18:
          hi2_array = [7.56, 7.564, 7.5642]
    elif n == 17:
          hi2_array = [6.91, 6.908, 6.9077]
    elif n == 16:
          hi2_array = [6.26, 6.262, 6.2621]
    elif n == 15:
          hi2_array = [5.63, 5.629, 5.6287]
    elif n == 14:
          hi2_array = [5.01, 5.009, 5.0088]
    elif n == 13:
          hi2_array = [4.4, 4.404, 4.4038]
    elif n == 12:
          hi2_array = [3.82, 3.816, 3.8157]
    elif n == 11:
          hi2_array = [3.25, 3.247, 3.247]
    elif n == 10:
          hi2_array = [2.7, 2.7, 2.7004]
    elif n == 9:
          hi2_array = [2.18, 2.18, 2.1797]
    elif n == 8:
          hi2_array = [1.69, 1.69, 1.6899]
    elif n == 7:
          hi2_array = [1.24, 1.237, 1.2373]
    elif n == 6:
          hi2_array = [0.83, 0.831, 0.8312]
    elif n == 5:
          hi2_array = [0.48, 0.484, 0.4844]
    elif n == 4:
          hi2_array = [0.22, 0.216, 0.2158]
    elif n == 3:
          hi2_array = [0.05, 0.051, 0.0506]

    
    return hi2_array
    
def nal1_b(uid, q, input, extra, solve=False, return_const=False):
        var1 = variabla(uid, 'var1')
        var2 = variabla(uid, 'var2')
        year1 = variabla(uid, 'var1.year')
        year2 = variabla(uid, 'var2.year')

        if extra == 'a1':
            rezultat = aritmeticna(var1, year1)
        elif extra == 'a2':
            rezultat = aritmeticna(var2, year2)
        elif extra == 's1':
            rezultat = std_odklon(var1, year1)
        elif extra == 's2':
            rezultat = std_odklon(var2, year2)
            
        return primerjaj(input, rezultat, solve, return_const=return_const)
          
validator_core.register_validator('nal1_b', nal1_b)

def nal1_c(uid, q, input, extra, solve=False, return_const=False):
    var1 = variabla(uid, 'var1')
    year1 = variabla(uid, 'var1.year')
   
    const = None
    absolute = False
   
    if extra == "rang1":
        rezultat = rang(var1, year1, 25)
        const = 0
        
        # print rezultat, const

    if const != None:
      return primerjaj(input, rezultat, solve, const, absolute=absolute, return_const=return_const)
    else:
      return primerjaj(input, rezultat, solve, absolute=absolute, return_const=return_const)
    
validator_core.register_validator('nal1_c', nal1_c)

def nal1_e(uid, q, input, extra, solve=False, return_const=False):
    var1 = variabla(uid, 'var1')
    year1 = variabla(uid, 'var1.year')

    var2 = variabla(uid, 'var2')

    user = User.objects.get(username=uid)
    if user.get_profile().is_special:
        rezultat = CalculatedAnswer.objects.get(var1=var1, var2=var2, question=q).value

    if not locals().get('rezultat'):
        if extra == 'kvartil1':
            rezultat = kvartil(var1, year1, 0.25)
        elif extra == 'kvartil2':
            rezultat = kvartil(var1, year1, 0.5)
        elif extra == 'kvartil3':
            rezultat = kvartil(var1, year1, 0.75)

    inp = input.replace(',','.')
    return primerjaj(inp, rezultat, solve, return_const=return_const)

validator_core.register_validator('nal1_e', nal1_e)

def nal2_a(uid, q, input, extra, solve=False, return_const=False):
    var = variabla(uid, 'var1')
    var1 = var
    year= variabla(uid, 'var1.year')

    var2 = variabla(uid, 'var2')
    const = None
    absolute = False

    user = User.objects.get(username=uid)
    if user.get_profile().is_special:
        try:
            rezultat = CalculatedAnswer.objects.get(var1=var1, var2=var2, question=q).value
        except CalculatedAnswer.DoesNotExist:
            pass

    if not locals().get('rezultat'):
        if extra == 'vzorcna_aritmeticna':
            rezultat = vzorcna_aritmeticna(var, year)
        elif extra == 'vzorcna_varianca':
            rezultat = vzorcna_varianca(var, year)[0]
        elif extra == 'std_odklon':
            rezultat = vzorcna_varianca(var, year)[1]
        elif extra == 'spodnja_as':
            rezultat = zaupanje_aritmeticna(var, year)[0]
            const = 0.005
        elif extra == 'zgornja_as':
            rezultat = zaupanje_aritmeticna(var, year)[1]
            const = 0.005
        elif extra == 'spodnja_va':
            rezultat = zaupanje_varianca(var, year)[0]
            const = 0.05
        elif extra == 'zgornja_va':
            rezultat = zaupanje_varianca(var, year)[1]
            const = 0.05        
        elif extra == 'spodnja_std':
            rezultat = zaupanje_varianca(var, year)[2]
            const = 0.03
        elif extra == 'zgornja_std':
            rezultat = zaupanje_varianca(var, year)[3]
            const = 0.03
        elif extra == 't_vrednost':
            rezultat = t_vrednost(var, year)
        elif extra == 'hi2_sp_varianca':
            rezultat = hi2_sp_varianca(var, year)
        elif extra == 'hi2_zg_varianca':
            rezultat = hi2_zg_varianca(var, year)

        
    if const:
      return primerjaj(input, rezultat, solve, const, absolute=absolute, return_const=return_const)
    else:
      return primerjaj(input, rezultat, solve, absolute=absolute, return_const=return_const)
validator_core.register_validator('nal2_a', nal2_a)
    
def nal2_e(uid, q, input, extra, solve=False, return_const=False):
    var = variabla(uid, 'var1')
    year = variabla(uid, 'var1.year')

    const = None
    absolute = False
    
    if extra == 'vas_n':
        rezultat = eu_arit_sred(var, year, 'new')
    elif extra == 'vas_s':
        rezultat = eu_arit_sred(var, year, 'old')
    elif extra == 'vso_n':
        rezultat = eu_vzorcna_varianca(var, year, 'new')[0]
    elif extra == 'vso_s':
        rezultat = eu_vzorcna_varianca(var, year, 'old')[0]
    elif extra == 'sso':
        rezultat = eu_skupni_std_odklon(var, year)[0]
        const = 0.005
    elif extra == 'evtst':
        rezultat = eu_std_razlika_vzorcnih_arit_sred(var, year)
        const = 0.005
        absolute = True
    elif extra == 'vtst':
        rezultat = eu_testna_statistika(var, year)
        const = 0.05
        if input < 0:
            input = input * (-1)
    elif extra == 'stopnja_znacilnosti':
        x = eu_std_razlika_vzorcnih_arit_sred(var, year)
        rezultat = tdist(var, year, x)
        const = 0.001
    
    if const:
      return primerjaj(input, rezultat, solve, const, absolute=absolute, return_const=return_const)
    else:
      return primerjaj(input, rezultat, solve, absolute=absolute, return_const=return_const)

validator_core.register_validator('nal_2e', nal2_e)

def nal3_a(uid, q, input, extra, solve=False, return_const=False):
    var1 = variabla(uid, 'var1')
    var2 = variabla(uid, 'var2')
    year = variabla(uid, 'var1.year')

    const = None
    absolute = False

    user = User.objects.get(username=uid)
    if user.get_profile().is_special:
        try:
            rezultat = CalculatedAnswer.objects.get(var1=var1, var2=var2, question=q).value
        except CalculatedAnswer.DoesNotExist:
            pass

    if not locals().get('rezultat', None):
        if extra == 'sdomed':
            rezultat = kontingencna(var1, year)[0]
        elif extra == 'ndomed':
            rezultat = kontingencna(var1, year)[1]
        elif extra == 'snadmed':
            rezultat = kontingencna(var1, year)[2]
        elif extra == 'nnadmed':
            rezultat = kontingencna(var1, year)[3]
        elif extra == 'hsdomed':
            rezultat = hikvadrat(var1, year)[1]
        elif extra == 'hndomed':
            rezultat = hikvadrat(var1, year)[2]
        elif extra == 'hsnadmed':
            rezultat = hikvadrat(var1, year)[3]
        elif extra == 'hnnadmed':
            rezultat = hikvadrat(var1, year)[4]
        elif extra == 'alpha':
            rezultat = alpha(var1, year)
            const = 0.005
        elif extra == 'hikvadrat':
            rezultat = hikvadrat(var1, year)[0]
            const = 0.01
        elif extra == 'kontingencni':
            rezultat = kontingencni(var1, year)[0]
            const = 0.005
        elif extra == 'kontingencnipop':
            rezultat = kontingencni(var1, year)[2]
            const = 0.005
        elif extra == 'as1':
            rezultat = nal_32b(var1, year, var2, year)[0]
        elif extra == 'as2':
            rezultat = nal_32b(var1, year, var2, year)[1]
        elif extra == 'rxy':
            # const = 0.005
            # print 'foo', nal_32b(var1, year, var2, year)[2]
            rezultat = nal_32b(var1, year, var2, year)[2]
        elif extra == 'texp':
            const = 0.01
            rezultat = nal_32b(var1, year, var2, year)[3]
        elif extra == 'cregr':
            return cregr(var1, year, var2, year, input) 
        elif extra == 'cregr_a':
            rezultat = cregr_ab(var1, year, var2, year)[0]
        elif extra == 'cregr_b':
            rezultat = cregr_ab(var1, year, var2, year)[1]
        elif extra == 'detr':
            rezultat = nal_32b(var1, year, var2, year)[6]
            const = 0.005
        elif extra == 'sno':
            rezultat = nal_32b(var1, year, var2, year)[7]
        elif extra == 'sto11':
            rezultat = strukturni_odstotki(var1, year)[0]
            const = 0.01
        elif extra == 'sto12':
            rezultat = strukturni_odstotki(var1, year)[1]
            const = 0.01
        elif extra == 'sto21':
            rezultat = strukturni_odstotki(var1, year)[2]
            const = 0.01
        elif extra == 'sto22':
            rezultat = strukturni_odstotki(var1, year)[3]
            const = 0.01
        elif extra == 'stopnja_znacilnosti':
            x = nal_32b(var1, year, var2, year)[3]
            rezultat = tdist(var1, year, x)
            const = 0.01

    if const:
        return primerjaj(input, rezultat, solve, const, absolute=absolute, return_const=return_const)
    else:
        return primerjaj(input, rezultat, solve, absolute=absolute, return_const=return_const)

validator_core.register_validator('nal3_a', nal3_a)


def check_student_section(user_id, section_id):  
    section = Section.objects.get(pk=section_id)
    
    correct_count = 0
    answer_count = 0
    
    answer_list = Answer.objects.filter(user__id__exact=user_id, question__task__lecture__id__exact=section.id)
    question_list = Question.objects.filter(task__lecture__id__exact=section.id, active__exact=True).select_related()
    for task in section.task_set.filter(active__exact=True):
        answer_count += question_list.filter(task=task).count()
        correct_count += answer_list.filter(question__task__id=task.id, correct__exact=True).count()
    return correct_count, answer_count

def calc_show_correct(question_id, user_id):
    #question = Question.objects.get(user__username__exact=user_id, id__exact=question.)
    question = Question.objects.get(pk=question_id)
    user = User.objects.get(pk=user_id)
    
    if question.answer_set.filter(user__id__exact=user_id).count():
      answer = question.answer_set.filter(user__id__exact=user_id).latest('id')
      ainp = answer.input
    else:
      answer = None
      ainp = ''
    
    i = question.validator.split("://")
    calculated = validator_core.validate[i[0]](user.username, question, ainp, i[1], solve=True)
    
    return (answer, calculated)

def calc_show_const(question_id, user_id):
    question = Question.objects.get(pk=question_id)
    user = User.objects.get(pk=user_id)
  
    if question.answer_set.filter(user__id__exact=user_id).count():
      answer = question.answer_set.get(user__id__exact=user_id)
      ainp = answer.input
    else:
      answer = None
      ainp = ''

    i = question.validator.split("://")
    const = validator_core.validate[i[0]](user.username, question, ainp, i[1], return_const=True)*100

    return const

# some test functions
if __name__ == '__main__':
   #nal1_as_b('61231') 
   #nal1_so_b('42342')
   #nal1_ranz_c('24324')
   #nal1_kvar_e('2432')
   test()
