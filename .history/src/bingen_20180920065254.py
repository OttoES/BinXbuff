# protobuf_parser.py
#
#  simple parser for parsing protobuf .proto files
#
#  Copyright 2010, Paul McGuire
#  Modified  2018,  otto    
#
from pprint import pprint

from pyparsing import (Word, alphas, alphanums, Regex, Suppress, Forward,
    Group, oneOf, ZeroOrMore, Optional, delimitedList, Keyword, cStyleComment, cppStyleComment,
    restOfLine, quotedString,QuotedString, Dict)


enumList     = []
structList   = []
structDict   = {}
headerList   = {}
annotateDict = {}

def addStructToList(structt):
    sdict = structt.asDict()
    structList.append(sdict)
    structDict[sdict["name"]] = sdict
 

def addEnumToList(enumm):
    #print("\n==========")
    #print(enumm.asDict())
    enumList.append(enumm.asDict())

def addToHeaderDict(headerName,structt):
    headerList[headerName] = structt.asDict()

def addToAnnotationDict(annotateName,annotate):
    s = annotate[1]
    # first remove the quotes
    if s.startswith("'''"):  s = s[3:-3]
    if s.startswith('"'):  s = s[1:-1]
    annotateDict[annotate['name']] = s


comment       = '## ' + restOfLine
#comment       = '#' + restOfLine
CMNT          = Optional(cStyleComment("comment"))
CMNT2         = Optional( (Suppress('//') + restOfLine("comment2")) )  #Optional(cppStyleComment("comment2"))
STRQ3         = QuotedString("'''", multiline=True)
ANNOTSTR      = ( QuotedString("'''", multiline=True) | quotedString )
#IDENTIFIER = Regex(r'[a-zA-Z_][a-zA-Z_0-9]*')
#INTEGER    = Regex(r'([+-]?(([1-9][0-9]*)|0+))')
#IDENTIFIER       = Word(alphas+"_", alphas+nums+"_" )
INT_DECI   = Regex('([+-]?(([1-9][0-9]*)|0+))')
INT_OCT    = Regex('(0[0-7]*)')
INT_HEX    = Regex('(0[xX][0-9a-fA-F]*)')
INT        = INT_HEX | INT_OCT | INT_DECI
FLOAT      = Regex('[+-]?(((\d+\.\d*)|(\d*\.\d+))([eE][-+]?\d+)?)|(\d*[eE][+-]?\d+)')
SIZE       = INT
#VARNAME    = IDENTIFIER
##ident = Word(alphas+"_",alphanums+"_").setName("identifier")
IDENT      = Word(alphas+"_",alphanums+"_")("name")
xxINT        = Regex(r"[+-]?\d+")

EXPR = Word(alphanums+"_",alphanums+"_"+"+"+"-"+"/"+"*")("expr")

LBRACE,RBRACE,LBRACK,RBRACK,LPAR,RPAR,EQ,SEMI,COLON,AT,STOP,LESS,LARGER = map(Suppress,"{}[]()=;:@.<>")

#kwds = """message required optional repeated enum extensions extends extend 
#          to package service rpc returns true false option import"""

kwds = """struct enum headedby 
          extensions extends extend 
          required optional array
          true false option import"""

for kw in kwds.split():
    exec("{}_ = Keyword('{}')".format(kw.upper(), kw))

structtBody         = Forward()

#structDefn          = Optional(CMNT("comment")) + STRUCT_ - ident("structName") + LBRACE + structtBody("body") + RBRACE
##structDefn          = CMNT + STRUCT_ - ident("structName") + LBRACE + structtBody("body") + RBRACE
###structDefn          = CMNT + STRUCT_ - ident + Optional(EXTENDS_ + ident)("baseName") + LBRACE + structtBody("body") + RBRACE
####structDefn          = (CMNT + STRUCT_ - ident + Optional(EXTENDS_ + ident("baseName")) + LBRACE + structtBody("body") + RBRACE).setParseAction(addStructToList)
#####structDefn          = (CMNT + STRUCT_ - IDENT + Optional(HEADEDBY_ + IDENT("parentName").setParseAction(addToHeaderDict)) + Optional(EXTENDS_ + IDENT("baseName")) +Optional(AT+IDENT + EQ + ANNOTSTR("anno")) + LBRACE + structtBody("body") + RBRACE).setParseAction(addStructToList)
structDecl          = CMNT + STRUCT_ - IDENT + Optional(HEADEDBY_ + IDENT("parentName").setParseAction(addToHeaderDict))  
#structAnnotations   = ZeroOrMore(AT+IDENT("annoName") + EQ + INT("annoValue")) +  ZeroOrMore(LESS+IDENT("defName") + EQ + INT("defValue") + LARGER)
structAnno          = Group(ZeroOrMore(AT+IDENT("annoName") + EQ + INT("annoValue")))("anno")
structLocals        = ZeroOrMore(LESS+IDENT("defName") + EQ + INT("defValue") + LARGER)("localConst")
structAnnotations   = structAnno + structLocals
structDefn          = (structDecl + structAnnotations + LBRACE + structtBody("body") + RBRACE).setParseAction(addStructToList)
#######structDefn          = (CMNT + STRUCT_ - IDENT + Optional(HEADEDBY_ + IDENT("parentName").setParseAction(addToHeaderDict))  + Optional(AT+IDENT("annoName") + EQ + INT("annoValue")) +  Optional(LESS+IDENT("defName") + EQ + INT("defValue") + LARGER) + LBRACE + structtBody("body") + RBRACE).setParseAction(addStructToList)

#typespec = oneOf("""double float int32 int64 uint32 uint64 sint32 sint64 
#                    fixed32 fixed64 sfixed32 sfixed64 bool string bytes""") | ident
typespec            = oneOf("""int8 uint8 int16 uint16 int32 int64 uint32 uint64 bool char wchar string zstring bytes enum8 enum16 enum32 TAG8 TAG16 """) | IDENT
##typespec            = oneOf("""int8 uint8 int16 uint16 int32 int64 uint32 uint64 bool char string zstring bytes enum8 enum16 enum32 """)

typeint             = oneOf("""int8 uint8 int16 uint16 int32 int64 uint32 uint64 bool char wchar byte""")
typestr             = oneOf("""string zstring ustring zustring""")
typeenum            = oneOf("""enum8 enum16 enum32""")
typetag             = oneOf("""TAG8 TAG16 TAG32 MSGID8 MSGID16""")
typeres             = oneOf("""STRUCTLEN8 STRUCTLEN16 CRC8 CRC16 CRC32""")


#typespec            =  typestd | typetag | typeres | ident

fieldtag            = typetag("type")  + IDENT + Optional(EQ + INT("value"))
fieldint            = typeint("type")  + Optional(LBRACK + EXPR("arrLen") + RBRACK)  + IDENT + Optional(EQ + EXPR("value"))
fieldstr            = typestr("type")  + IDENT + Optional(EQ + quotedString("value"))
#fieldenumInline     = (typeenum("type") + IDENT("enumName") + IDENT + LBRACE + Dict( ZeroOrMore( Group(IDENT + EQ + INT("value") + SEMI + CMNT2 ) ))('values') + RBRACE).setParseAction(addEnumToList)
fieldenumInline     = (typeenum("type") + IDENT("enumName") + IDENT + LBRACE + ( ZeroOrMore( Group(IDENT + EQ + INT("value") + SEMI + CMNT2 ) ))('values') + RBRACE).setParseAction(addEnumToList)
fieldenum           = typeenum("type") + IDENT("enumName") + IDENT + Optional(EQ + IDENT("value"))
fieldres            = typeres("type")  + IDENT + LBRACK + IDENT("rangeStart")+COLON+ IDENT("rangeEnd")+RBRACK
#fieldres            = typeres("type")  + IDENT + LPAR + IDENT("rangeStart")+".."+ IDENT("rangeEnd")+RPAR

fieldstruct         = IDENT("stype")   + IDENT

rvalue              = INT | TRUE_ | FALSE_ | IDENT
fieldDirective      = LBRACK + Group(IDENT("fid") + EQ + rvalue("fidval")) + RBRACK
##fieldDefn           = (( REQUIRED_ | OPTIONAL_ | ARRAY_ )("fieldQualifier") - 
##                      typespec("typespec") + ident("ident") + EQ + integer("value") + ZeroOrMore(fieldDirective) + SEMI) + Optional(CMNT2("comment2"))
###fieldDefn           = typespec("type") + ident + EQ + integer("value") + ZeroOrMore(fieldDirective) + SEMI + Optional(CMNT2("comment2"))
field               = fieldint | fieldstr | fieldenumInline | fieldenum | fieldtag | fieldres | fieldstruct 
fieldDefn           = CMNT + field  + SEMI + Optional(CMNT2)

# enumDefn        ::= 'enum' ident '{' { ident '=' integer ';' }* '}'
##enumDefn            = CMNT + ENUM_("typespec") - ident('name') +  LBRACE + Dict( ZeroOrMore( Group(ident("name") + EQ + integer("value") + SEMI + CMNT2 ) ))('values') + RBRACE
#enumInline          = (LBRACE + Dict( ZeroOrMore( Group(IDENT + EQ + INT("value") + SEMI + CMNT2 ) ))('values') + RBRACE).setParseAction(addEnumToList)
##enumDefn            = (CMNT + ENUM_("type") - IDENT +  LBRACE + Dict( ZeroOrMore( Group(IDENT + EQ + INT("value") + SEMI + CMNT2 ) ))('values') + RBRACE).setParseAction(addEnumToList)
###enumDefn            = (CMNT + ENUM_("type") + IDENT +  LBRACE + Dict( ZeroOrMore( Group(IDENT + EQ + INT("value") + SEMI + CMNT2 ) ))('values') + RBRACE).setParseAction(addEnumToList)
enumDefn            = (CMNT + ENUM_("type") + IDENT("enumName") +  LBRACE + ( ZeroOrMore( Group(IDENT + EQ + INT("value") + SEMI + CMNT2 ) ))('values') + RBRACE).setParseAction(addEnumToList)

# extensionsDefn ::= 'extensions' integer 'to' integer ';'
##extensionsDefn = EXTENSIONS_ - integer + TO_ + integer + SEMI

# structExtension ::= 'extend' ident '{' messageBody '}'
####structExtension     = Optional(CMNT("comment")) + EXTEND_ - ident + LBRACE + structtBody + RBRACE
###structExtension     = CMNT + ident + EXTEND_ + ident("baseName") + LBRACE + structtBody + RBRACE

# messageBody     ::= { fieldDefn | enumDefn | structDefn | extensionsDefn | structExtension }*
##messageBody << Group(ZeroOrMore( Group(fieldDefn | enumDefn | structDefn | extensionsDefn | structExtension) ))
###structtBody << Group(ZeroOrMore( Group(fieldDefn | enumDefn | structDefn | structExtension) ))
structtBody << Group(ZeroOrMore( Group(fieldDefn | enumDefn | structDefn ) ))

# methodDefn ::= 'rpc' ident '(' [ ident ] ')' 'returns' '(' [ ident ] ')' ';'
# methodDefn = (RPC_ - ident("methodName") + 
#               LPAR + Optional(ident("methodParam")) + RPAR + 
#               RETURNS_ + LPAR + Optional(ident("methodReturn")) + RPAR)

# serviceDefn ::= 'service' ident '{' methodDefn* '}'
##serviceDefn = SERVICE_ - ident("serviceName") + LBRACE + ZeroOrMore(Group(methodDefn)) + RBRACE

# packageDirective ::= 'package' ident [ '.' ident]* ';'
##packageDirective = Group(PACKAGE_ - delimitedList(ident, '.', combine=True) + SEMI)



importDirective = IMPORT_ - quotedString("importFileSpec") + SEMI

optionDirective = OPTION_ - IDENT("optionName") + EQ + quotedString("optionValue") + SEMI


#annotateDef     = AT + (IDENT + EQ + (quotedString | STRQ3)).setParseAction(addToAnnotationDict)
annotateDef     = AT + (IDENT + EQ + ANNOTSTR).setParseAction(addToAnnotationDict)

#topLevelStatement = Group(structDefn | structExtension | enumDefn | serviceDefn | importDirective | optionDirective)
##topLevelStatement = Group(structDefn | structExtension | enumDefn | importDirective | optionDirective)
topLevelStatement = Group(annotateDef | structDefn  | enumDefn | importDirective | optionDirective)

##parser = Optional(packageDirective) + ZeroOrMore(topLevelStatement)
#parser = Group(CMNT) + ZeroOrMore(topLevelStatement)
parser = ZeroOrMore(topLevelStatement)

parser.ignore(comment)


test1 = """
@name       =  "Test BBX"
@version    =  "0.1-4"
@doc_title  =  "BBX document"
@doc_header =  "BBX document heading generation Testing"
@doc_intro  =  '''This is the definiton of the message protocol
                  used for bla-bla-bla'''

@c_includes =  '''
#include <stdio.h>
#include "comms.h"
'''

@c_code = '''
void testfun(void)
{
   dosomething();
} // end test
'''

/* 
 This is the common header for everybody.
*/
struct GGheader
{
    /* This is to test a very long comment line. 
       The destination is where the message should be send to.
       Each device should be allocated a fixed address.
    */
  uint8     dest;   // Alt dest comment
  MSGID16   mM; // This is to test a very long comment line. Abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
  uint16    msg_id = MSG_ID; // This is to test a very long comment line. Abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
  CRC16     CalcCrc16[dest:msgid];  //  CRC16     CalcCrc16(dest..msgid); 
}  

enum Gender {
    UNKNOWN = 0;    
    MALE    = 1;   // set as male
    FEMLE   = 0x2;   // set as female
    OTHER   = 0x3;   // if a person identifies with a different gender 
}

/*
  This is the message to set the user profile.
  Line 2 of comment
*/
struct SetProfile headedby GGheader 
@CC=56
@CV=542
<MSG_ID = 0x1155>  <ARRLEN = 10>
{ 
  int32 id = 1;      // the user identificatin number
  char[20]  surname; // the user surname
  enum8     ename  fieldvarname {  x1=1; x2=2; a1 = 3;  };

  enum8  Gender gender;
  int8     dlen;
  CRC16     hdrCrc2[dest:dlen]; // a message calculated crc
  char[dlen]    addit;
  zstring email = "eeeeee"; 
}"""

test2 = """

  enum Gender {
    UNKNOWN = 0;    
    MALE = 1;  // mmmjhjjj   j h hjjjj
    FEMLE = 2;   // sdfds d d sdfdsfdssf 
  }
## package tutorial;

struct Person {
  string name = "gg";
  int32 id = 2;     // not defined
  string email = "emailll";
  enum8 Gender gen;
  /* enum comment */
  enum PhoneType {
    MOBILE = 0;
    HOME = 1;  // xxx cccccccffffffffff nn
    WORK = 2;
  }

  struct PhoneNumber {
    string number = "3656354";
    enum8  PhoneType ptype ; ## [default = HOME];
  }

  PhoneNumber phone;
}
/* 
 My comment
*/
struct AddressBook {
  Person person;
}

struct Student extends Person {
  int16   SN  = 1234;
  int8    ghg = 23;
  int16   nn    = 323;
  zstring us = "hfhdhfdh"; 
}

"""



def cleanstr(s):
    if s.startswith("'''"):  s = s[3:-3]
    if s.startswith('/*'):  s = s[2:-2]
    if s.startswith('"'):  s = s[1:-1]
    #if s.endswith('*/'):  s = s[2:]
    return s.replace("\n", " ")

def addIndent(s):
    return s.replace("\n", "\n   ")



class BaseCodeGenerator:
    codeHeader          = " Auto generated code"
    codeCommentStart    = "/* "
    codeCommentEnd      = " */"
    typePostfix         = "_t"
    funcNamePrefix      = "BIN_"
    funcPackCallPrefix  = "BIN_call"
    funcPackBaseName    = "packMsg"
    funcProcessBuffName = "CallStoreSendBuffer"
    funcUnpackNamePrefix= "BIN_unpack"
    noTypeName          = "void"
    intTypeName         = "int "
    typeTable1          = {"bool":"bool","enum8":"uint8_t","char":"char"}
    typeTable2          = {"string":"char","zstring":"char","ustring":"wchar","uzstring":"wchar"}
    # these types are internally generated andnot passed in by the user  
    typeTableLoc        = {"CRC8":"uint8","CRC16":"uint16","CRC32":"uin32","MSG_ID16":"uint16"}
    typeSizeTable       = {"char":1,"bool":1,"wchar":2,"byte":1}
    packBuffName        = "buff"  
    packBuffType        = "char"  
    def __init__(self,bbxDef= None):
        if bbxDef is not None:
            pp = parser.parseString(bbxDef)
    def pprint(self):
        pprint(enumList)
        pprint(structList)
    def lookupType(self,vartype):  
        if vartype in self.typeTable2: return  self.typeTable2[vartype]
        if vartype in self.typeTable1: return  self.typeTable1[vartype]
        return vartype+self.typePostfix          
    def lookupTypeSize(self,vartype):  
        # handel all the non standard cases that is in the table
        if vartype in self.typeSizeTable: return  self.typeSizeTable[vartype]
        # do the standard cases where the bit isze is embedded in the type name
        if vartype.find("8") >0 : return 1
        if vartype.find("16")>0 : return 2
        if vartype.find("32")>0 : return 4
        if vartype.find("64")>0 : return 8
        return -100000  # this is an n error
    def getParent(self,structt):
        if not "parentName" in structt: return None 
        parnt = structt["parentName"]
        return structDict[parnt]  
    def genVarOnlyDecl(self,varType,varName,arrayLen = None):
        ''' Generate variable declaration of the given type.
            If an array size given it will be declared as an 
            array of that size.
            Note that arrayLen of 0 is handeled differently:
            it will be declared as an array argument using "[]"
            as normally used in function arguments.
        '''
        tt = self.lookupType(varType)
        s  = tt + " "+varName
        if arrayLen is not None:
            if arrayLen == 0:
                s += "[]"
            else:
                s += "[" + str(arrayLen) +"]"
        return s
    def genFileHeader(self,fileName):
        s = "Autogenerated code\n"
        s += "File name : "+fileName + "\n"
        if "name" in annotateDict:
            s += "Name      : "+cleanstr(annotateDict["name"]) + "\n"
        if "version" in annotateDict:
            s += "Version   : " + cleanstr(annotateDict["version"]) + "\n"   
        if "copyright" in annotateDict:
            s += "Copyright : " + cleanstr(annotateDict["copyright"]) + "\n"   
        return s
    def genPackVar(self,buff,buffpos,vartype,varname, varval): 
        #if vartype in self.typeTable2: 
        #    return self.funcPackNamePrefix+vartype+"("+buff+", "+buffpos+", "+varname+","+varval+");"
        return self.funcPackCallPrefix+vartype+"("+buff+", "+buffpos+", "+varname+","+varval+");"
    def genArg(self,fields):    
        s = ""
        for f in fields:
            s = s + f["name"] + ","
        return s[:-1] 
    def genTypedArg(self,fields):    
        s = ""
        for f in fields:
            # if the field is in the locked list it is internally 
            # generated and should not be in the argument list so skip it
            if f["type"] in self.typeTableLoc: 
                continue
            if "arrLen" in f:
                # 0 will force it to use [] in declaration
                arrLen = 0   
            else:
                arrLen = None
            #arrLen = f.get("arrLen",None)    
            s += self.genVarOnlyDecl(f["type"] , f["name"],arrLen ) + ","
            #s = s + self.lookupType(f["type"])+ "  "+ f["name"] + ","
        return s[:-1] 
    #####-------------------------------------
    def makeFunName(self,structt,retType,funName,args,isClassFun = True):
        """ Make a valid function declaration

        Arg:
          funName    - the base name (root) of the name. If it is part of a class
                       it should be prefixed wih the class name (or what ever the 
                       programming language require)
          isClassFun -  will declare it as a static (a class function)
        """
        s = ""
        if isClassFun: s+= "static "
        s += retType + " " + funName + "(" + args + ")"
        return s
    def makeDeclFunArgList(self,structt):
        return self.makeFieldListGeneric(structt,True, seperator = "," , inclParent = True , inclConst = False )    
    def makeCallFunArgList(self,structt):
        return self.makeFieldListGeneric(structt,False, seperator = "," , inclParent = True , inclConst = False )
    def makeClassMemberList(self,structt):
        return self.makeFieldListGeneric(structt,True, seperator = ";\n  " , inclParent = False , inclConst = True )
    def makeFieldListGeneric(self,structt,inclTypes, seperator = "," , inclParent = True , inclConst = False ):
        """ Flexible generation of variable/argument list 
        """
        fields    = structt["body"]
        s = ""
        if inclParent and "parentName" in structt:
            parnt = self.getParent(structt)
            s += self.makeFieldListGeneric(parnt,inclTypes, seperator, inclParent , inclConst) + seperator
        for f in fields:
            # if the field is assigned a value 
            # do not include in the argument list 
            # but can be over ridden with  inclConst
            if "value" in f and inclConst == False: 
                continue  
            #if f["type"] in self.typeTableLoc: 
            #    continue
            # if "arrLen" in f:
            #     # 0 will force it to use [] in declaration
            #     arrLen = 0   
            # else:
            #     arrLen = None
            arrLen = f.get("arrLen",None)    
            if inclTypes:
                #s += self.genVarDecl(f["type"] , f["name"],arrLen ) + seperator
                s += self.genVarDecl(f, inclArrLen =False, termstr = seperator ) 
            else: 
                s += self.genVarOnlyDecl(f["type"] , f["name"],arrLen ) + seperator
        return s[:-len(seperator)]         
    def genPackFieldCode(self,f):
        tsize = self.lookupTypeSize(f["type"])
        if "arrLen" in f:  
            lenstr = str(tsize)+"*" + f["arrLen"]
            ## this is only valid if the endianess is the same for multibyte types !!!!
            return "memcpy("+self.packBuffName+","+f["name"] +","+lenstr + ");\n"
        if tsize == 1:
            return self.packBuffName+"[pos++] = (uint8_t)"+ f["name"] + ";\n"
        elif tsize == 2: 
            # this is stored in little endian
            s = self.packBuffName+"[pos++] = (uint8_t)"+ f["name"] + ";\n"
            return s + "    "+ self.packBuffName+"[pos++] = (uint8_t)("+ f["name"] + ">>8);\n"
        elif tsize == 4: 
            # this is stored in little endian
            s  = "// it is faster to copy byte by byte than calling memcpy()\n"
            s += "    "+ self.packBuffName+"[pos++] = (uint8_t)"+ f["name"] + ";\n"
            s += "    "+ self.packBuffName+"[pos++] = (uint8_t)("+ f["name"] + ">>8);\n"
            s += "    "+ self.packBuffName+"[pos++] = (uint8_t)("+ f["name"] + ">>16);\n"
            return s + "    "+ self.packBuffName+"[pos++] = (uint8_t)("+ f["name"] + ">>24);\n"
        s  = "pos    += " + self.funcPackCallPrefix + f["type"].capitalize() 
        s += "(" +self.packBuffName +", pos,"+ f["name"] + ");\n"
        return s
    
    def genPackFields(self,structt):    
        fields    = structt["body"]
        s = ""
        for f in fields:
            if f["type"] == "CRC16":
              p1,fnd1 = self.genPackFieldPosCalc(structt,f['rangeStart'],False)
              p2,fnd2 = self.genPackFieldPosCalc(structt,f['rangeEnd'],True)
              s += "    int16_t   "+f["name"] +" += CalcCRC16"+f["name"]+"("+self.packBuffName+", "+p1 + "," + p2 + ");\n" 

            s += "    " + self.genPackFieldCode(f) 
            #s += "    pos    += " + self.funcPackNamePrefix + f["type"].capitalize() 
            #s += "(" +self.packBuffName +", pos,"+ f["name"] + ");\n"
        return s 
    # includeField inidcate if the field named fieldName shold be included in the position calculations    
    #def genPackFieldPosCalc(self,fields,fieldName,includeField):    
    def genPackFieldPosCalc(self,structt,fieldName,includeField):    
        fields    = structt["body"]
        ##fieldName = structt['name']
        s = ""
        if "parentName" in structt:
            parnt = structt["parentName"]
            parStruct = structDict[parnt]
            s,fieldFound = self.genPackFieldPosCalc(parStruct,fieldName,includeField)
            if fieldFound: return s,True
            if s != "":  s += "+ "
        for f in fields:
            # if the selected field size must be included
            if includeField == False:    
                if f["name"] == fieldName: 
                    if len(s) < 1: return "0",True  # if it is the first element
                    return s[:-1],True
            # if it is an array, multiply with the array length        
            if 'arrLen' in f: 
                s = s +" ("+f['arrLen']+")*"
            # get the size of the element
            s += str(self.lookupTypeSize(f["type"]))+ "+"
            if f["name"] == fieldName: 
                return s[:-1],True
        return s[:-1],False
    def genPackLenCalc(self,structt):    
        # calculate the struct size by finding the last field offset
        lastField = structt["body"][-1]        
        return self.genPackFieldPosCalc(structt,lastField,True)
          
    ## try to simplify the equation if it only contains numbers
    def simplifyEq(self,eqs):    
        if any(c not in '0123456789+*- ' for c in eqs):  
            return eqs,False
        ll = eval(eqs)
        return ll,True
    def xxgenPackFun(self,struct,copyToBuff=True,msgIdArg = False):
        structnme     = struct["name"]
        fields        = struct["body"]
        parentArgs    = ""
        # the parent arguments should also be send 
        if "parentName" in struct:
            prn           = struct["parentName"]
            parentStruct  = structDict[prn]
            parentStruct  = parentStruct["body"]
            parentArgs    = self.genTypedArg(parentStruct) +", "
        # in some cased the dest buffer should also be passed as argument
        if copyToBuff:
            funName   = self.funcPackBaseName + structnme.capitalize()
            s  = self.intTypeName +" "+ funName +"(" + parentArgs
            s += self.genVarOnlyDecl(self.packBuffType,self.packBuffName,0) + ","
            s += self.genVarOnlyDecl(self.intTypeName, "pos") + "," 
        else:
            funName   = self.funcPackCallPrefix + structnme.capitalize()
            s  = self.intTypeName +" "+ funName +"(" + parentArgs
        #s += self.packBuffType+" "+self.packBuffName+","+self.intTypeName +" pos, "
        s += self.genTypedArg(fields) +")\n"
        s += "{\n"
        (structLen,_) = self.genPackLenCalc(struct)
        s += "    const "+self.intTypeName +" "+self.packBuffName+"Len = " + structLen
        #s += "    const int "+self.packBuffName+"Len = " + self.genPackLenCalc(fields)
        s += ";\n"
        if not copyToBuff:
            s += "          "+self.intTypeName +" pos    = 0;\n"
            s += "    uint8_t   "+self.packBuffName+"["+self.packBuffName+"Len];\n"
        #else:
        #    s += "    if ("+self.packBuffName+"Len > bufSize) return 0;   // buffer to small"
        if "parentName" in struct:
            # fill in the inherited data from the parent
            s += "    pos = " +self.funcPackBaseName + struct["parentName"].capitalize() 
            s += "(" + self.packBuffName + ", pos, "+ self.genArg(parentStruct) +");\n"
        s += self.genPackFields(struct)
        if not copyToBuff:
            s += "    return  "+self.funcProcessBuffName+"("+self.packBuffName
            s += ", pos);\n"
        else:
            s += "    return  pos;\n"
        s += "} // end "+ funName + "\n"
        return s

    def genPackFun(self,structt,copyToBuff=True,msgIdArg = False,namePrefix = ""):
        structnme     = structt["name"]
        fields        = structt["body"]
        parentArgs    = ""
        # the parent arguments should also be send 
        # if "parentName" in struct:
        #     prn           = struct["parentName"]
        #     parentStruct  = structDict[prn]
        #     parentStruct  = parentStruct["body"]
        #     parentArgs    = self.genTypedArg(parentStruct) +", "
        # in some cased the dest buffer should also be passed as argument
        if copyToBuff:
            args = "uint8_t  "+self.packBuffName+"[],"+self.intTypeName +" pos, "
            #args = self.makeDeclFunArgList(structt)
            # s    = self.makeFunName(structt,self.intTypeName,self.funcPackBaseName,args)
            # s  = self.intTypeName +" "+ funName +"(" + parentArgs
            # s += self.makeDeclFunArgList(structt)
            #funName   = self.funcPackBaseName + structnme.capitalize()
            # s  = self.intTypeName +" "+ funName +"(" + parentArgs
            # s += self.genVarOnlyDecl(self.packBuffType,self.packBuffName,0) + ","
            # s += self.genVarOnlyDecl(self.intTypeName, "pos") + "," 
        # else:
        #     funName   = self.funcPackCallPrefix + structnme.capitalize()
        #     s  = self.intTypeName +" "+ funName +"(" + parentArgs
        else: args = ""
        args += self.makeDeclFunArgList(structt)
        s     = self.makeFunName(structt,self.intTypeName,namePrefix+self.funcPackBaseName,args)
        #s += self.packBuffType+" "+self.packBuffName+","+self.intTypeName +" pos, "
        #s += self.genTypedArg(fields) +")\n"
        s += "\n{\n"
        (structLen,__) = self.genPackLenCalc(structt)
        s += "    const "+self.intTypeName +" "+self.packBuffName+"Len = " + structLen
        #s += "    const int "+self.packBuffName+"Len = " + self.genPackLenCalc(fields)
        s += ";\n"
        if not copyToBuff:
            s += "          "+self.intTypeName +" pos    = 0;\n"
            s += "    uint8_t   "+self.packBuffName+"["+self.packBuffName+"Len];\n"
    #s += self.makeClassMemberList(structt)
        else:
            s += "    if ("+self.packBuffName+"Len > bufSize) return 0;   // buffer to small\n"
        if "parentName" in structt:
            # fill in the inherited data from the parent
            prn           = structt["parentName"]
            parentStruct  = structDict[prn]
            #parentStruct  = parentStruct["body"]
            s += self.genPackFields(parentStruct)
            #parentArgs    = self.genTypedArg(parentStruct) +", "            s += "    pos = " +self.funcPackBaseName + structt["parentName"].capitalize() 
            #s += "(" + self.packBuffName + ", pos, "+ self.genArg(parentStruct) +");\n"
        s += self.genPackFields(structt)
        if not copyToBuff:
            s += "    return  "+self.funcProcessBuffName+"("+self.packBuffName
            s += ", pos);\n"
        else:
            s += "    return  pos;\n"
        s += "\n} // end\n"
        return s


    def genVarDecl(self,sfield,inclArrLen =False, termstr = ";"):
        if not "type" in sfield:
            return "" 
        vtype = sfield["type"]
        vname = sfield["name"]
        if vtype in self.typeTable2: 
            s = self.lookupType(vtype) +" "+vname+"["+sfield["type"]+"]"
        else:  
            s = self.lookupType(vtype) +" "+vname
        if 'arrLen' in sfield:
            if inclArrLen:  
                s = s +"["+sfield['arrLen']+"]"
            else:
                s = s +"[]"
        if 'value' in sfield:
          s = s + " = " +  sfield["value"]
        s = s + termstr   
        return s
    def genAllEnumDefs(self):    
        s = ""
        
        for enm in enumList:
            s += "\nenum "+enm["enumName"] + " {\n"
            elmlist = enm["values"]
            for vv in elmlist:
                #elms = elmlist[vv]
                #s += " "+vv +" = "+ elms["name"] + "\n"
                #s += " "+vv +" = "+ "FF" + "\n"
                s += " "+vv["name"] +" = "+ vv["value"]+","
                if "comment2" in vv:
                  s += "    // " + vv["comment2"]
                s += "\n"
            s += "}; // end enum\n" 

        return s
    def genHeader(self,pp):
        s = "*Autogenerated code\n"
        if  "comment" in pp:
          s += pp["comment"]
        return s

    def genAll(self):
        s  = ""
        s += annotateDict.get('c_includes',"")
        s += annotateDict.get('c_code',"")
        s += self.genAllEnumDefs()
        for st in structList:
            s += genPackFun( st) +"\n"
        return s


class OOcodeGenerator(BaseCodeGenerator):
    typeTable1      = {"bool":"bool","enum8":"uint8_t","char":"char","string":"String"}
    #typeTable2           = {"string":"","zstring":"char","ustring":"wchar","uzstring":"wchar"}
    #packageName     = "DefaultPackageName"
    # def genClassDecl(self,structt):    
    #     fields    = structt["body"]
    #     ##fieldName = structt['name']
    #     s = ""
    #     s = "class "+structt["name"] 
    #     if "parentName" in structt:
    #         parnt = structt["parentName"]
    #         parStruct = structDict[parnt]
    def genClassDeclBegin(self,structname,parentstruct= None):
        s = "class "+structname+" "
        if parentstruct is not None: 
            s += ": public " + parentstruct + "\n"
        s += "{\n public:\n"
        return s
    def genClassDeclEnd(self,structname):
        s = "}; // end class "+structname+ "\n\n"
        return s

    def genStruct(self,struct):
        parent = struct.get("parentName",None)
        s = self.genClassDeclBegin(struct["name"],parent) 
        # for each field, add a declaration
        for f in struct["body"]:
            if 'value' in f:
              vv = f["value"]
            else:
              vv = None
            s += "  "+self.genVarDecl(f, termstr = ";\n")
            #s += "  "+self.genVarDecl(f["type"],f["name"],vv, termstr = ";\n")
        # generate the serialze and deserialize functions for the struct
        s1 = self.genPackFun(struct)
        s += "  "+addIndent(s1) + "\n"
        s2 = self.genPackFun(struct,False)
        s += "   "+addIndent(s2) + "\n"
        s += self.genClassDeclEnd(struct["name"])
        return s
    def genAll(self,hFileName,cFileNme):
        # generate h file -------
        s  = self.codeCommentStart + "\n" + self.genFileHeader(hFileName)
        s += self.codeCommentEnd + "\n"
        s += annotateDict.get('h_includes',"")
        s += self.genAllEnumDefs()

        # generate cpp file -------
        s += '#include "' + hFileName + "\n"
        s += annotateDict.get('c_includes',"")
        s += annotateDict.get('c_code',"")
        for st in structList:
            s += self.genStruct( st) +"\n"
        return s


class MarkdownGenerator(BaseCodeGenerator):
    H1     = "# "
    H2     = "## "
    H3     = "### "
    LIST   = "* "
    BOLT   = "**"
    LINE   = "___\n"
    DLINE  = "___\n___\n"
    NLNL   = "\n"
    BR     = "\n"
    COL    = "|"
    ROW    = "\n|"
    def genInternalLink(m,ltext,linktag=None):
        if linktag is None: linktag= ltext
        #if ltext in enumList:
        #   s ="["+ltext+"](#"+"enum-" + ltext.lower() +")"
        #elif ltext in structList:  
        s ="["+ltext+"](#" + linktag.lower() +")"
        return s
    def genDocEnums(m):
        s  = m.H2 + "Enumerations\n" + m.LINE
        for enm in enumList:
            s += m.H3 + "Enum " + enm["enumName"] +"\n"
            if "comment" in enm:
                s += cleanstr(enm["comment"]) +m.NLNL
            # if "parentName" in st:
            #     s += "Structure inherits all fields from " + m.BOLT
            #     s += st["parentName"] + m.BOLT + " and add these" + m.BR
            #     parentstr = m.ROW + "Parent" + m.COL + m.genInternalLink(st["parentName"]) + m.COL + "" + m.COL + "This data prepend this structure"  + m.COL
            #     #parentstr = m.ROW + "Parent" + m.COL + st["parentName"] + m.COL + "" + m.COL + "This data prepend this structure"  + m.COL
            # else: 
            #     parentstr = ""
            #     s += "Fields in this structure" + m.BR
            s += m.ROW + "Tag" + m.COL + "Value" + m.COL + "Comment"  + m.COL
            s += m.ROW + "------" + m.COL + "-----" + m.COL + "------------------------------"  + m.COL
            for vv in enm["values"]:
                if "comment" in vv: cmt = cleanstr(vv["comment"])
                else: cmt = ""
                if "comment2" in vv: cmt += " " +vv["comment2"]
                s += m.ROW + vv["name"] + m.COL + vv["value"] + m.COL + cmt + m.COL
            s += m.NLNL 
        return s        
    def genDocStructs(m):
        s  = m.H2 + "Structures\n" + m.LINE
        for st in structList:
            #s += m.LINE
            s += m.H3 + st["name"] +"\n"
            if "comment" in st:
                s += cleanstr(st["comment"]) +m.NLNL
            if "parentName" in st:
                s += "Structure inherits all fields from " + m.BOLT
                s += st["parentName"] + m.BOLT + " and add these" + m.BR
                parentstr = m.ROW + "Parent" + m.COL + m.genInternalLink(st["parentName"]) + m.COL + "" + m.COL + "This data prepend this structure"  + m.COL
                #parentstr = m.ROW + "Parent" + m.COL + st["parentName"] + m.COL + "" + m.COL + "This data prepend this structure"  + m.COL
            else: 
                parentstr = ""
                s += "Fields in this structure" + m.BR
            s += m.ROW + "Field" + m.COL + "Type" + m.COL + "Array" + m.COL + "Comment"  + m.COL
            s += m.ROW + "------" + m.COL + "-----" + m.COL +"-----" + m.COL + "------------------------------"  + m.COL
            s += parentstr
            for f in st["body"]:
                if "comment" in f: cmt = cleanstr(f["comment"])
                else: cmt = ""
                if "comment2" in f: cmt += " " +f["comment2"]
                if "arrLen" in f: arrLen = f["arrLen"]
                else: arrLen = "-"
                if f["type"].find("enum")>=0: 
                    etxt  = f["enumName"]
                    vtype = f["type"] + " " + m.genInternalLink(etxt,"enum-"+etxt)
                else: vtype = f["type"]
                s += m.ROW + f["name"] + m.COL + vtype + m.COL + arrLen + m.COL + cmt + m.COL
            slen,ret = m.genPackLenCalc(st)    
            simlen,canSimplify = m.simplifyEq(slen)
            if canSimplify : simlen = str(simlen) 
            else : simlen = "variable"
            s += m.ROW + "Total" + m.COL + " length" + m.COL + simlen + m.COL + slen  + m.COL
            s += m.NLNL 
        return s

    def genDocHeader(m):
        s = ""
        if "doc_header" in annotateDict:
            s += m.H1 +  cleanstr(annotateDict["doc_header"])+ m.NLNL
        else:
            s += m.H1 +  "Title" + m.NLNL
        s += m.H3 
        if "name" in annotateDict:
            s += cleanstr(annotateDict["name"])
        if "version" in annotateDict:
            s += " version " + cleanstr(annotateDict["version"])
        s +=  m.NLNL
        s += m.LINE
        if "doc_intro" in annotateDict:
            s += m.H2 + "Intoduction\n" + cleanstr(annotateDict["doc_intro"]) + m.NLNL
        return s
    def genAll(m):
        s  = m.genDocHeader()      
        s += m.DLINE
        s += m.genDocEnums()
        s += m.DLINE
        s += m.genDocStructs()
        return s




class OOpythonGenerator(OOcodeGenerator):
    def __init__(self):
        self.typeTable1           = {"bool":"bool","enum8":"uint8_t","char":"char","string":"String"}
        #typeTable2           = {"string":"","zstring":"char","ustring":"wchar","uzstring":"wchar"}
    def lookupType(self,vartype):  
        return ""
    def genClassDeclBegin(self,structname,parentstruct= None):
        s = "class "+structname
        if parentstruct is not None: 
            s += "(" + parentstruct + ")"
        return s + ":\n"
    def genClassDeclEnd(self,structname):
        return "\n\n"
    def genAll(self):
        s  = ""
        s += annotateDict.get('py_imports',"")
        s += annotateDict.get('py_code',"")
        s += self.genAllEnumDefs()

        for st in structList:
            s += self.genStruct( st) +"\n"
        return s



#parser.runTests([test1, test2])
# pp = parser.parseString(test1)
# print(enumList)
# print(structList)


#cgen = OOcodeGenerator(test1)
# s = cgen.genStruct( structList[0])
# print(s)
# s = cgen.genPackFun( structList[0])
# print(s)
# #s = cgen.genPackFun( structList[1])
# #print(s)

# cgen.pprint()

# s = cgen.genHeader(pp.asDict())
# print(s)
# print(pp.asDict())

# cgen = OOcodeGenerator(test1)
# cgen.pprint()
# s = cgen.genAll()
# print(s)

# print(annotateDict)

# docgen = MarkdownGenerator() 
# s = docgen.genAll()
# print(s)

pp = parser.parseString(test1)
pygen = OOpythonGenerator()
pygen.pprint()
s = pygen.genAll()
print(s)
print("\n------------------------------\n\n")
oogen = OOcodeGenerator()
#oogen.pprint()
s = oogen.genAll("test.hpp","test.cpp")
print(s)
