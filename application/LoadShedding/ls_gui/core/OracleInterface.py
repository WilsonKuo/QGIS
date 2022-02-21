#!/usr/bin/python3.6
# coding=utf-8
"""
:Copyright: © 2020 Advanced Control Systems, Inc. All Rights Reserved.
"""

__author__ = 'Terry Lin'

import os
import cx_Oracle
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8' 

class OracleInterface:
    
    def __init__(self, usrn, pswd, tnsn, arrsz=100):
        self._Username = None
        self.Username = usrn
        self._Password = None
        self.Password = pswd
        self._TNSName = None
        self.TNSName = tnsn
        self._ArraySize = None
        self.ArraySize = arrsz
        
        self.__connstr = self.Username + '/' + self.Password + '@' + self.TNSName
    
    @property
    def Username(self):
        """get Connection Username"""
        return self._Username

    @Username.setter
    def Username(self, value):
        """set Connection Username"""
        self._Username=value
    
    @property
    def Password(self):
        """get Connection Password"""
        return self._Password


    @Password.setter
    def Password(self, value):
        """set Connection Password"""
        self._Password=value
    
    @property
    def TNSName(self):
        """get Connection TNS name"""
        return self._TNSName

    @TNSName.setter
    def TNSName(self, value):
        """set Connection TNS name"""
        self._TNSName=value
    
    @property
    def ArraySize(self):
        """get Cursor Array Size"""
        return self._ArraySize

    @ArraySize.setter
    def ArraySize(self, value):
        """set Cursor Array Size"""
        self._ArraySize=value
    
    def ConnectTest(self):
        """execute the SQL"""
        try:
            print ('Connecting to ' + self.Username + '@' + self.TNSName + '...')
#           self.__connstr=self.Username + '/' + self.Password + '@' + self.TNSName
            self.conn=cx_Oracle.connect(self.__connstr)
            print ('Connected.')
            print ('Oracle Server version: ' + self.conn.version)
            self.conn.close()
            return True
        except cx_Oracle.DatabaseError as err:
            print (err)
            return False
    
    def ExecNonQuery(self, sql, bindVar=[]):
        """execute the SQL"""
        try:
            self.conn=cx_Oracle.connect(self.__connstr)
            cur=self.conn.cursor()
            cur.prepare(sql)
            cur.execute(None, bindVar)
            self.conn.commit()
            cur.close()
            self.conn.close()
            # return True
        except cx_Oracle.DatabaseError as err:
            print (err)
            raise
            # return False

    def ExecQuery(self, sql, bindVar=[]):
        """execute the SQL and return result"""
        res=[]
        try:
            self.conn=cx_Oracle.connect(self.__connstr)
            cur=self.conn.cursor()
            cur.arraysize=self.ArraySize
            cur.prepare(sql)
            cur.execute(None, bindVar)
            res=cur.fetchall()
            cur.close()
            self.conn.close()
            return res
        except cx_Oracle.DatabaseError as err:
            print (err)
            raise

    def ExecQuery2(self, sql, bindVar=[]):
        """execute the SQL and return DBMS_Output"""
        try:
            self.conn=cx_Oracle.connect(self.__connstr)
            cur=self.conn.cursor()
            cur.callproc("dbms_output.enable")
            cur.arraysize=self.ArraySize
            cur.prepare(sql)
            cur.execute(None, bindVar)
            statusVar = cur.var(cx_Oracle.NUMBER)
            lineVar = cur.var(cx_Oracle.STRING)
            while True:
                cur.callproc("dbms_output.get_line", (lineVar, statusVar))
                if statusVar.getvalue() != 0:
                  break
                return lineVar.getvalue()
            cur.close()
            self.conn.close()
        except cx_Oracle.DatabaseError as err:
            print (err)
            raise
    
    def ExecReader(self, sql, bindVar=[]):
        """execute the SQL and return cursor"""
        try:
            self.conn=cx_Oracle.connect(self.__connstr)
            cur=self.conn.cursor()
            cur.arraysize=self.ArraySize
            cur.prepare(sql)
            cur.execute(None, bindVar)
            return cur
        except cx_Oracle.DatabaseError as err:
            print (err)
            raise

    def GetCursor(self):
        """execute the SQL and return cursor"""
        try:
            self.conn=cx_Oracle.connect(self.__connstr)
            cur=self.conn.cursor()
            cur.arraysize=self.ArraySize
            return cur
        except cx_Oracle.DatabaseError as err:
            print (err)
            raise
    
    def InsertArray(self, sql, bindArray=[]):
        """execute many with an array"""
        try:
            self.conn=cx_Oracle.connect(self.__connstr)
            cur=self.conn.cursor()
            cur.arraysize=self.ArraySize
            cur.prepare(sql)
            cur.executemany(None, bindArray)
            self.conn.commit()
            cur.close()
            self.conn.close()
        except cx_Oracle.DatabaseError as err:
            print (err)
    
    def CheckTableExist(self, tableName):
        """check table is existed and return true/false"""
        try:
            sql='select count(*) from USER_TABLES where TABLE_NAME=:vn'
            res = self.ExecQuery(sql, [tableName.upper()])[0][0]
            #print ('table '+tableName + ' is ' + str(res))
            if res==0:
                return False
            else:
                return True
        except cx_Oracle.DatabaseError as err:
            print (err)
            return None
    
    def CheckViewExist(self, viewName):
        """check view is existed and return true/false"""
        try:
            sql='select count(*) from user_views where view_name=:vn'
            res = self.ExecQuery(sql, [viewName.upper()])[0][0]
            #print ('table '+tableName + ' is ' + str(res))
            if res==0:
                return False
            else:
                return True
        except cx_Oracle.DatabaseError as err:
            print (err)
            return None

    def CheckIndexExist(self, indexName):
        """check view is existed and return true/false"""
        try:
            sql='select count(*) from USER_INDEXES where INDEX_NAME=:xn'
            res = self.ExecQuery(sql, [indexName.upper()])[0][0]
            #print ('index '+indexName + ' is ' + str(res))
            if res==0:
                return False
            else:
                return True
        except cx_Oracle.DatabaseError as err:
            print (err)
            return None
    
    def CreateDictTable(self, tableName, dictDef):
        cols=[]
        for colname in dictDef:
            if dictDef[colname]==True:
                cols.append(colname + ' varchar2(255)')
            else:
                cols.append(colname + ' number')
        colstr=','.join("%s" % c for c in cols)
        sql='create table %s (%s)' % (tableName, colstr)
        self.ExecNonQuery(sql)
    
    def DropTable(self, tableName):
        isExists = self.CheckTableExist(tableName)
        if isExists is True:
            try:
                query="drop table {0}".format(tableName)
                # print (query)
                self.ExecNonQuery(query)
            except cx_Oracle.DatabaseError as err:
                print (err)

                

if __name__ == "__main__":
    print ("*** Execute OracleInterface.py ***")

    # """Self testing"""
    PRISMdb=OracleInterface('acs_qa', 'acs_qa', 'ems')
    PRISMdb.ConnectTest()
    
