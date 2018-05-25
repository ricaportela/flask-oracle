#
# Python script to demonstrate basics of best practice with Oracle 
# 
# Guy Harrison Jan 2010:  www.guyharrison.net
#

import cx_Oracle
import sys, traceback, time

def setup():
    my_csr=conn.cursor()
    my_csr.execute(" alter session set events '10046 trace name context forever, level 12' ")

    my_csr.execute(" ALTER SESSION SET tracefile_identifier = PythonDemo ")
    my_csr.execute("alter session set session_cached_cursors=0")
    try:
        my_csr.execute(" DROP table PythonDemo ");
    except cx_Oracle.Error, e:
        print e[0] + "when DROPPING PythonDemo"
    finally:
        my_csr.execute("CREATE TABLE PythonDemo( " +\
           " x varchar2(12) primary key, y number)")
        print "PythonDemo table created"
        
def arrayInsert(rowCount):

    arrayValues=[]
    for i in range(0,rowCount) : 
        xvalue=i
        yvalue=i+1
        arrayValues.append((xvalue,yvalue))
    print "rowCount=%d" % rowCount
    startTime = time.clock()
    ins_csr=conn.cursor()
    ins_csr.prepare(" INSERT /* array */ INTO PythonDemo (x, y) " +\
          " VALUES (:1, :2)")
    ins_csr.executemany(None,arrayValues)

    conn.commit()
    elapsedTime = time.clock()- startTime 
    print "%d rows affected %f s " % (ins_csr.rowcount, elapsedTime)

def singleRowInsert(rowCount):

    startTime=time.clock()
    ins_csr=conn.cursor()
    ins_csr.prepare(" INSERT /* no array */ INTO PythonDemo (x, y) " +\
          " VALUES (:1, :2)")  

    for i in range(0,rowCount) : 
        xvalue=i
        yvalue=i+1
        ins_csr.execute(None,(xvalue,yvalue)) 
        
    print "%d rows inserted (one at a time)" % rowCount
    conn.commit()
    elapsedTime = time.clock()- startTime 
    print "%d rows affected %f s " % (ins_csr.rowcount, elapsedTime)
  

def gatherStats():
    my_csr=conn.cursor()
    my_csr.execute( "begin sys.dbms_stats.gather_table_stats" +\
           "(ownname=>user,tabname=>'PythonDemo'); end; "  )
    
def flushDb():
    my_csr=conn.cursor()
    my_csr.execute( "ALTER SYSTEM FLUSH SHARED_POOL")   
    my_csr.execute( "ALTER SYSTEM FLUSH BUFFER_CACHE")    

def simpleFetch(arraySize):
 
    print "Simple fetch example : " 
    startTime=time.clock()
    sel_csr=conn.cursor()
    print "default arraysize=%d" % sel_csr.arraysize
    
    sel_csr.arraysize=arraySize  
    sel_csr.execute("SELECT /* fetchone*/ x,y FROM PythonDemo")
    rowcount=0 
    while (1):
        row = sel_csr.fetchone ()   
        if row == None:
            break
        rowcount+=1 
 
    elapsedTime = time.clock()- startTime 
    print  "%d rows (array=%d) returned %f s " % (rowcount,sel_csr.arraysize, elapsedTime)
    sel_csr.close()
  
def arrayFetchMany(arraySize):
 
    print "fetchmany example : " 
    startTime=time.clock()
    sel_csr=conn.cursor()
    sel_csr.arraysize = arraySize
    sel_csr.execute("SELECT /* fetchmany */ x,y FROM PythonDemo")
    done = False
    rowcount=0
    batchCount=0
    while not done:
        rows = sel_csr.fetchmany()       
        if rows == []:
            done = True
            break
        batchCount+=1
        for row in rows:
            rowcount+=1
    elapsedTime = time.clock()- startTime 
    print  "%d rows returned in %d batches: %f s " % (rowcount,batchCount, elapsedTime)
  
def arrayFetchAll(arraySize):
 
    print "ArrayFetchAllexample: " 
    startTime=time.clock()
    sel_csr=conn.cursor()
    sel_csr.arraysize = arraySize
    sel_csr.execute("SELECT /* fetchall */ x,y FROM PythonDemo")
    rowcount=0
    for row in sel_csr.fetchall():
        rowcount+=1
    sel_csr.close()
    elapsedTime = time.clock()- startTime 
    print  "%d rows returned %f s " % (rowcount, elapsedTime)
    
def bindSelect(rowFetches):

    print "Select with binds: " 
    startTime=time.clock()
    sumOfY = 0;
    sel_csr=conn.cursor()

    for i in range(0,rowFetches):
       sel_csr.execute("SELECT /*bind1*/ y FROM PythonDemo WHERE x=:x_value",
                       x_value=i)
       for row in sel_csr.fetchall():
           sumOfY+=row[0]
    sel_csr.close()
    elapsedTime = time.clock()- startTime 
    print  "sumOfY=%d rows returned %f s " % (sumOfY, elapsedTime)
   

def noBindSelect(rowFetches):

    print "Select without binds: " 
    startTime=time.clock()
    sumOfY = 0;
    sel_csr=conn.cursor()
    for i in range(0,rowFetches):
       sel_csr.execute("SELECT /*nobind*/ y FROM PythonDemo WHERE x=%d" % i)
       for row in sel_csr.fetchall():
           sumOfY+=row[0]
    sel_csr.close()
    
    elapsedTime = time.clock()- startTime 
    print  "sumOfY=%d rows returned %f s " % (sumOfY, elapsedTime)
           
try:    
    rowCount=500000
    arraySize=100
    conn = cx_Oracle.connect (sys.argv[1]) 
    setup()
    arrayInsert(rowCount)
    setup()
    singleRowInsert(rowCount)     
    gatherStats()
    flushDb()
    simpleFetch(1)
    flushDb()
    simpleFetch(100)
    flushDb()
    arrayFetchAll(100)
    flushDb()
    arrayFetchMany(100)
    flushDb()
    bindSelect(10000)
    flushDb()
    noBindSelect(10000)
    print "done"

except cx_Oracle.Error, e:
        print e[0]
        traceback.print_exc(file=sys.stdout)       
        sys.exit(1)