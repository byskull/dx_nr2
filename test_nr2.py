#-*- coding: utf-8 -*-

import os
import codecs
import math
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getKeyWord( dirname, keylist) :
 flist = os.listdir(dirname)
 for f in flist:
  next = os.path.join(dirname,f)
  if os.path.isdir(next) == False:
   fname = os.path.split(next)[-1].split(".")[-2]
   keylist.append(fname.split("_")[0] + "_"+ fname.split("_")[1])

def getSubDir( dirname, sublist) :
 flist = os.listdir(dirname)
 for f in flist:
  next = os.path.join(dirname,f)
  if os.path.isdir(next) :
   sublist.append(os.path.split(next)[-1])

def search(dirname, a, b, sm) :
 flist = os.listdir(dirname)
 for f in flist:
  next = os.path.join(dirname,f)
  if os.path.isdir(next) :
   search(next,a,b,sm)
  else :
   doFileWork(next,a,b,sm)

def searchlist(dirname, fnlist, a, b, sm) :
 flist = os.listdir(dirname)
 for f in flist:
  next = os.path.join(dirname,f)
  fname = os.path.split(next)[-1].split(".")[-2]
  for fn in fnlist :
   comp_size = len(fn)
   if fname[0:comp_size] == fn :
    doFileWork(next,a,b,sm)

def searchlistvec(dirname, fn, veca, vecb, sm) :

 flist = os.listdir(dirname)
 for f in flist:
  next = os.path.join(dirname,f)
  fname = os.path.split(next)[-1].split(".")[-2]
  comp_size = len(fn)
  if fname[0:comp_size] == fn :
   CheckDrNr(next,veca,vecb,sm)

def doFileWork(filename,a,b,sm) :
 ext = os.path.split(filename)[-1].split(".")[-1]
 #print( ext)

 if ext == "txt" :
  CheckDr(filename,a,b,sm)

def CheckDr(filename, a, b,sm) :

 fn = codecs.open( filename , "r", 'utf-8')

 ss =  unicode( fn.read()[1:] )

 for i in range(len(ss) ) :
  if ss[i] not in a :
   a.append(ss[i])
   b.append(1)
  else :
   b[ a.index(ss[i])] += 1

  sm[0] += 1

def CheckDrNr( filename, vecta, vectb, sm) :
 fn = codecs.open( filename , "r", 'utf-8')

 ss =  unicode( fn.read()[1:] )

 for i in range(len(ss) ) :
  if ss[i] in vecta :
   vectb[vecta.index(ss[i])] += 1
  sm[0] += 1

def GetVec ( vecta, vectb, vecsmb ) :
 xa = 0
 xb = 0
 xc = 0

 for i in range(len(vecta)) :
  #print vecta[i], vectb[i]
  xa +=  vectb[i] * vecsmb[i]
  xb +=  vectb[i] * vectb[i]
  xc +=  vecsmb[i] * vecsmb[i]

 if xb * xc == 0 :
  return 0.0
 else :
  return (xa) / math.sqrt( xb) / math.sqrt( xc)

def GetVecNM ( dirname, fname, vecta, vectb ) :

 # GetVec ( "C:\\Users\\knr\\Desktop\\dx\\OCR-RESULT", fname, vecta, vectb )
 vecsmb = []

 for i in range(len(vecta)) :
  vecsmb.append(0)

 smsm = [0]

 searchlistvec ( dirname, fname, vecta, vecsmb, smsm)
 return GetVec( vecta, vectb, vecsmb )

dirloc = "C:\\Users\\knr\\Desktop\\dx\\OCR-RESULT"  # 샘플 들 리스트
dirval = u"C:\\Users\\knr\\Desktop\\dx\\value\\개념" # 개념의 위치
dirvalc = u"C:\\Users\\knr\\Desktop\\dx\\value\\"


sublist = []
getSubDir(dirvalc, sublist)

alla = []
allb = []
sama = []
samb = []

allsm = [0.0]
samsm = [0.0]

flist = []
'''
flist.append( "133996_26144800" )
flist.append( "133995_26144758" )
flist.append( "133994_26144757" )
'''

getKeyWord(dirval, flist)

flist = list(set(flist))

searchlist ( dirloc, flist, sama, samb, samsm)

search ( dirloc, alla, allb, allsm)

print len(sama) , samsm[0]
print len(alla) , allsm[0]

vecta = []
vectb = []

for i in range(len(sama)) :
 if ( samb[i] / samsm[0] > 0 + allb[alla.index(sama[i])] / allsm[0] ) :
  if ( sama[i] not in (' \t\n') ) and ord( sama[i] ) not in range(9312,9316+1)  :
   try  :
    if int(sama[i]) >= 0 :
     print sama[i]
  #print samb[i] / samsm[0] , allb[alla.index(sama[i])] / allsm[0]
   except :
    vecta.append( sama[i])
    vectb.append( samb[i])

err = 0

print len(vecta)
'''
for i in range(len(vecta)) :
 try :
  print "[" , vecta[i].decode('utf-8', "ignore") , "]", vectb[i]
 except :
  err += 1
'''
'''

fname = "133992_26144754"
print GetVecNM ( dirloc, fname, vecta, vectb )

fname = "137835_26140703"
print GetVecNM ( dirloc, fname, vecta, vectb )
'''

value = []

for fn in flist :
 value.append( GetVecNM ( dirloc, fn , vecta, vectb ) )

print value

keylist = []
getKeyWord(dirloc, keylist)

keylist = list( set (keylist))

for key in keylist :
 cosval = GetVecNM ( dirloc, key , vecta, vectb )
 if ( max(value) >= cosval and min(value) <= cosval ) :
  print key,  cosval
