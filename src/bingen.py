# protobuf_parser.py
#
#  simple parser for parsing protobuf .proto files
#
#  Copyright 2010, Paul McGuire
#  Modified  2018,  otto    
#

from pyparsing import (Word, alphas, alphanums, Regex, Suppress, Forward,
    Group, oneOf, ZeroOrMore, Optional, delimitedList, Keyword, cStyleComment, cppStyleComment,
    restOfLine, quotedString, Dict)

enumList     = []
structList   = []
structDict   = {}
headerList   = {}

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



comment       = '## ' + restOfLine
#comment       = '#' + restOfLine
CMNT          = Optional(cStyleComment("comment"))
CMNT2         = Optional( (Suppress('//') + restOfLine("comment2")) )  #Optional(cppStyleComment("comment2"))

##ident = Word(alphas+"_",alphanums+"_").setName("identifier")
ident = Word(alphas+"_",alphanums+"_")("name")
integer = Regex(r"[+-]?\d+")

expr = Word(alphanums+"_",alphanums+"_"+"+"+"-"+"/"+"*")("expr")

LBRACE,RBRACE,LBRACK,RBRACK,LPAR,RPAR,EQ,SEMI,COLON = map(Suppress,"{}[]()=;:")

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
structDefn          = (CMNT + STRUCT_ - ident + Optional(HEADEDBY_ + ident("parentName").setParseAction(addToHeaderDict)) + Optional(EXTENDS_ + ident("baseName")) + LBRACE + structtBody("body") + RBRACE).setParseAction(addStructToList)

#typespec = oneOf("""double float int32 int64 uint32 uint64 sint32 sint64 
#                    fixed32 fixed64 sfixed32 sfixed64 bool string bytes""") | ident
typespec            = oneOf("""int8 uint8 int16 uint16 int32 int64 uint32 uint64 bool char wchar string zstring bytes enum8 enum16 enum32 TAG8 TAG16 """) | ident
##typespec            = oneOf("""int8 uint8 int16 uint16 int32 int64 uint32 uint64 bool char string zstring bytes enum8 enum16 enum32 """)

typeint             = oneOf("""int8 uint8 int16 uint16 int32 int64 uint32 uint64 bool char wchar byte""")
typestr             = oneOf("""string zstring ustring zustring""")
typeenum            = oneOf("""enum8 enum16 enum32""")
typetag             = oneOf("""TAG8 TAG16 TAG32 MSG_ID8 MSG_ID16""")
typeres             = oneOf("""STRUCTLEN8 STRUCTLEN16 CRC8 CRC16 CRC32""")


#typespec            =  typestd | typetag | typeres | ident

fieldtag            = typetag("type")  + ident + Optional(EQ + ident("value"))
fieldint            = typeint("type")  + Optional(LBRACK + expr("arrLen") + RBRACK)  + ident + Optional(EQ + integer("value"))
fieldstr            = typestr("type")  + ident + Optional(EQ + quotedString("value"))
fieldenum           = typeenum("type") + ident("enumName") + ident + Optional(EQ + ident("value"))
fieldres            = typeres("type")  + ident + LBRACK + ident("rangeStart")+COLON+ ident("rangeEnd")+RBRACK

fieldstruct         = ident("stype")   + ident

rvalue              = integer | TRUE_ | FALSE_ | ident
fieldDirective      = LBRACK + Group(ident("fid") + EQ + rvalue("fidval")) + RBRACK
##fieldDefn           = (( REQUIRED_ | OPTIONAL_ | ARRAY_ )("fieldQualifier") - 
##                      typespec("typespec") + ident("ident") + EQ + integer("value") + ZeroOrMore(fieldDirective) + SEMI) + Optional(CMNT2("comment2"))
###fieldDefn           = typespec("type") + ident + EQ + integer("value") + ZeroOrMore(fieldDirective) + SEMI + Optional(CMNT2("comment2"))
field               = fieldint | fieldstr | fieldenum | fieldtag | fieldres | fieldstruct 
fieldDefn           = field  + SEMI + Optional(CMNT2)

# enumDefn        ::= 'enum' ident '{' { ident '=' integer ';' }* '}'
##enumDefn            = CMNT + ENUM_("typespec") - ident('name') +  LBRACE + Dict( ZeroOrMore( Group(ident("name") + EQ + integer("value") + SEMI + CMNT2 ) ))('values') + RBRACE
enumDefn            = (CMNT + ENUM_("type") - ident +  LBRACE + Dict( ZeroOrMore( Group(ident + EQ + integer("value") + SEMI + CMNT2 ) ))('values') + RBRACE).setParseAction(addEnumToList)

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

optionDirective = OPTION_ - ident("optionName") + EQ + quotedString("optionValue") + SEMI

#topLevelStatement = Group(structDefn | structExtension | enumDefn | serviceDefn | importDirective | optionDirective)
##topLevelStatement = Group(structDefn | structExtension | enumDefn | importDirective | optionDirective)
topLevelStatement = Group(structDefn  | enumDefn | importDirective | optionDirective)

##parser = Optional(packageDirective) + ZeroOrMore(topLevelStatement)
parser =  ZeroOrMore(topLevelStatement)

parser.ignore(comment)


test1 = """
struct GGheader
{
  uint8     dest;
  MSG_ID16  msgid;
  CRC16     hdrCrc[dest:msgid]; 
}
struct SetProfile headedby GGheader 
{ 
  int32 id = 1;    
  char[20]  surname;
  string name;   
  int8     dlen;
  CRC16     hdrCrc2[dest:dlen]; 
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


parser.runTests([test1, test2])
print(enumList)
print(structList)


class BaseCodeGenerator:
    codeHeader          = " Auto generated code"
    codeCommentStart    = "/* "
    codeCommentEnd      = " */"
    typePostfix         = "_t"
    funcNamePrefix      = "BIN_"
    funcPackNamePrefix  = "BIN_pack"
    funcUnpackNamePrefix= "BIN_unpack"
    noTypeName          = "void"
    typeTable1          = {"bool":"bool","enum8":"uint8_t","char":"char"}
    typeTable2          = {"string":"char","zstring":"char","ustring":"wchar","uzstring":"wchar"}
    typeSizeTable       = {"char":1,"bool":1,"wchar":2,"byte":1}
    packBuffName        = "buff"  
    def lookupType(self,vartype):  
        if vartype in self.typeTable2: return  self.typeTable2[vartype]
        if vartype in self.typeTable1: return  self.typeTable1[vartype]
        return vartype+self.typePostfix          
    def lookupTypeSize(self,vartype):  
        # handel all the non standardcases he is in the table
        if vartype in self.typeSizeTable: return  self.typeSizeTable[vartype]
        # do the standard cases where the bit iszeis embedded in the tpye name
        if vartype.find("8") >0 : return 1
        if vartype.find("16")>0 : return 2
        if vartype.find("32")>0 : return 4
        if vartype.find("64")>0 : return 8
        return 0xEEEE
    def genPackVar(self,buff,buffpos,vartype,varname, varval): 
        #if vartype in self.typeTable2: 
        #    return self.funcPackNamePrefix+vartype+"("+buff+", "+buffpos+", "+varname+","+varval+");"
        return self.funcPackNamePrefix+vartype+"("+buff+", "+buffpos+", "+varname+","+varval+");"
    def genArg(self,fields):    
        s = ""
        for f in fields:
            s = s + f["name"] + ","
        return s[:-1] 
    def genTypedArg(self,fields):    
        s = ""
        for f in fields:
            s = s + self.lookupType(f["type"])+ "  "+ f["name"] + ","
        return s[:-1] 
    def genPackFields(self,structt):    
        fields    = structt["body"]
        s = ""
        for f in fields:
            if f["type"] == "CRC16":
              p1,fnd1 = self.genPackFieldPosCalc(structt,f['rangeStart'],False)
              p2,fnd2 = self.genPackFieldPosCalc(structt,f['rangeEnd'],True)
              s += "    int16_t   "+f["name"] +" += CalcCRC16"+f["name"]+"("+self.packBuffName+", "+p1 + "," + p2 + ");\n" 
            s += "    pos    += " + self.funcPackNamePrefix + f["type"]+ "("
            s += self.packBuffName +", int pos,"+ f["name"] + ");\n"
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
            #if s != "":  s += "+ "
        for f in fields:
            # if the selected field size must be included
            if includeField == False:    
                if f["name"] == fieldName: 
                    if len(s) < 1: return "0",True  # if it is the first element
                    return s[:-1]
            # if it is an array, multiply with the array length        
            if 'arrLen' in f: 
                s = s +" ("+f['arrLen']+")*"
            # get the size of the element
            s += str(self.lookupTypeSize(f["type"]))+ "+"
            if f["name"] == fieldName: 
                return s[:-1],True
        return s,False
    def genPackLenCalc(self,structt):    
        # calculate the struct size by finding the last field offset
        lastField = structt["body"][-1]        
        return self.genPackFieldPosCalc(structt,lastField,True)
          
        # fields    = struct["body"]
        # s = ""
        # if "parentName" in struct:
        #     parnt = struct["parentName"]
        #     parStruct = structDict[parnt]
        #     s = self.genPackLenCalc(parStruct) + "+"
        # for f in fields:
        #     if 'arrLen' in f: 
        #         s = s +" ("+f['arrLen']+")*"
        #     s += str(self.lookupTypeSize(f["type"]))+ " +"
        # return s[:-1]
    def genPackFun(self,struct):
        structnme = struct["name"]
        fields    = struct["body"]
        s  = self.noTypeName +" "+ self.funcPackNamePrefix+structnme+"("
        s += self.genTypedArg(fields) +")\n"
        s += "{\n"
        (structLen,_) = self.genPackLenCalc(struct)
        s += "    const int "+self.packBuffName+"Len = " + structLen
        #s += "    const int "+self.packBuffName+"Len = " + self.genPackLenCalc(fields)
        s += ";\n"
        s += "          int pos    = 0;\n"
        s += "    uint8_t   "+self.packBuffName+"["+self.packBuffName+"Len];\n"
        s += self.genPackFields(struct)
        s += "    return  pos;\n"
        s += "} // end "+ self.funcPackNamePrefix+structnme+"\n"
        return s

    def xxgenVarDecl(self,vartype,varname,defval= None, termstr = ";"):
        if vartype in self.typeTable2: 
            s = self.lookupType(vartype) +" "+varname+"[]"
        else:  
            s = self.lookupType(vartype) +" "+varname
        if defval is not None: s = s + " = " + defval
        s = s + termstr   
        return s

    def genVarDecl(self,sfield, termstr = ";"):
        if not "type" in sfield:
            return "" 
        vtype = sfield["type"]
        vname = sfield["name"]
        if vtype in self.typeTable2: 
            s = self.lookupType(vtype) +" "+vname+"["+sfield["type"]+"]"
        else:  
            s = self.lookupType(vtype) +" "+vname
        if 'arrLen' in sfield: 
            s = s +"["+sfield['arrLen']+"]"
        if 'value' in sfield:
          s = s + " = " +  sfield["value"]
        s = s + termstr   
        return s


class OOcodeGenerator(BaseCodeGenerator):
    typeTable1           = {"bool":"bool","enum8":"uint8_t","char":"char","string":"String"}
    #typeTable2           = {"string":"","zstring":"char","ustring":"wchar","uzstring":"wchar"}
    def genStructDeclBegin(self,structname,parentstruct= None):
        s = "class "+structname+" \n{\n"
        if parentstruct is not None: s = s + "  struct " + parentstruct + " par;\n"
        return s
    def genStructDeclEnd(self,structname):
        s = "}    // end class "+structname+ self.typePostfix+"; \n\n"
        return s

    def genStruct(self,struct):
        s = self.genStructDeclBegin(struct["name"],None)  #struct["baseName"]):
        for f in struct["body"]:
            if 'value' in f:
              vv = f["value"]
            else:
              vv = None
            s += "  "+self.genVarDecl(f, termstr = ";\n")
            #s += "  "+self.genVarDecl(f["type"],f["name"],vv, termstr = ";\n")

        s= s +   self.genStructDeclEnd(struct["name"])
        return s


cgen = OOcodeGenerator()
s = cgen.genStruct( structList[0])
print(s)
s = cgen.genPackFun( structList[0])
print(s)
s = cgen.genPackFun( structList[1])
print(s)


