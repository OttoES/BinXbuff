# binXbuff_parser.py
#
#  simple parser for parsing binXbuff files
#
#  Based on protobuf parser by Paul McGuire
#  Copyright 2018  OttoES    
#


from pyparsing import (Word, alphas, alphanums, Regex, Suppress, Forward,
    Group, oneOf, ZeroOrMore, Optional, delimitedList, Keyword, cStyleComment, cppStyleComment,
    restOfLine, quotedString,QuotedString, Dict)


enumList     = []
structList   = []
structDict   = {}
msgList   = []
msgDict   = {}
headerList   = {}
annotateDict = {}

def addStructToList(structt):
    sdict = structt.asDict()
    structList.append(sdict)
    structDict[sdict["name"]] = sdict
 
# def addMessageToList(structt):
#     sdict = structt.asDict()
#     msgList.append(sdict)
#     msgDict[sdict["name"]] = sdict
 

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
#xxINT        = Regex(r"[+-]?\d+")

EXPR = Word(alphanums+"_"+"(",alphanums+"_"+"+"+"-"+"/"+"*"+"("+")"+ " "+"=")("expr")

LBRACE,RBRACE,LBRACK,RBRACK,LPAR,RPAR,EQ,SEMI,COLON,AT,STOP,LESS,LARGER = map(Suppress,"{}[]()=;:@.<>")

#kwds = """message required optional repeated enum extensions extends extend 
#          to package service rpc returns true false option import"""

kwds = """struct message enum headedby 
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
#messageDecl         = CMNT + STRUCT_ - IDENT + Optional(HEADEDBY_ + IDENT("parentName").setParseAction(addToHeaderDict))  

valvarAssign        = (INT("value") | EXPR | quotedString("string"))
#structAnnotations   = ZeroOrMore(AT+IDENT("annoName") + EQ + INT("annoValue")) +  ZeroOrMore(LESS+IDENT("defName") + EQ + INT("defValue") + LARGER)
#structAnno          = ZeroOrMore(AT+Group(IDENT("annoName") + EQ + INT("annoValue")))
##structAnno          = ZeroOrMore(AT+Group(IDENT("annoName") + EQ + (INT("annoValue") | IDENT("annoVar") | quotedString("annoStr"))  ))
###structAnno          = ZeroOrMore(AT+Group(IDENT + EQ + (INT("annoValue") | IDENT("annoVar") | quotedString("annoStr"))  ))
structAnno          = ZeroOrMore(AT+Group(IDENT + EQ + valvarAssign  ))

#structLocals        = Group(ZeroOrMore(LESS+IDENT("defName") + EQ + INT("defValue") + LARGER))("localConst")
#structLocals        = ZeroOrMore(LESS+Group(IDENT + EQ + INT("value")) + LARGER)
structLocals        = ZeroOrMore(LESS+Group(IDENT + EQ + (INT("value") | EXPR  ) ) + LARGER)
structAdds          = structAnno("anno") + structLocals("localConst")
structDefn          = (structDecl + structAdds + LBRACE + structtBody("body") + RBRACE).setParseAction(addStructToList)
#######structDefn          = (CMNT + STRUCT_ - IDENT + Optional(HEADEDBY_ + IDENT("parentName").setParseAction(addToHeaderDict))  + Optional(AT+IDENT("annoName") + EQ + INT("annoValue")) +  Optional(LESS+IDENT("defName") + EQ + INT("defValue") + LARGER) + LBRACE + structtBody("body") + RBRACE).setParseAction(addStructToList)
#messageDefn         = (messageDecl + structAdds + LBRACE + structtBody("body") + RBRACE).setParseAction(addMessageToList)

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
arrDec              = Optional(LBRACK + EXPR("arrLen") + RBRACK)

fieldtag            = typetag("type")  + IDENT + Optional(EQ + INT("value"))
#fieldint            = typeint("type")  + Optional(LBRACK + EXPR("arrLen") + RBRACK)  + IDENT + Optional(EQ + EXPR("value"))
fieldint            = typeint("type")  + arrDec  + IDENT + Optional(EQ + EXPR("value"))
fieldstr            = typestr("type")  + IDENT + Optional(EQ + quotedString("value"))
#fieldenumInline     = (typeenum("type") + IDENT("enumName") + IDENT + LBRACE + Dict( ZeroOrMore( Group(IDENT + EQ + INT("value") + SEMI + CMNT2 ) ))('values') + RBRACE).setParseAction(addEnumToList)
fieldenumInline     = (typeenum("type") + IDENT("enumName") + IDENT + LBRACE + ( ZeroOrMore( Group(IDENT + EQ + INT("value") + SEMI + CMNT2 ) ))('values') + RBRACE).setParseAction(addEnumToList)
fieldenum           = typeenum("type") + IDENT("enumName") + IDENT + Optional(EQ + IDENT("value"))
fieldres            = typeres("type")  + IDENT + LBRACK + IDENT("rangeStart")+COLON+ IDENT("rangeEnd")+RBRACK
#fieldres            = typeres("type")  + IDENT + LPAR + IDENT("rangeStart")+".."+ IDENT("rangeEnd")+RPAR

fieldstruct         = IDENT("type") + arrDec   + IDENT

rvalue              = INT | TRUE_ | FALSE_ | IDENT
fieldDirective      = LBRACK + Group(IDENT("fid") + EQ + rvalue("fidval")) + RBRACK
##fieldDefn           = (( REQUIRED_ | OPTIONAL_ | ARRAY_ )("fieldQualifier") - 
##                      typespec("typespec") + ident("ident") + EQ + integer("value") + ZeroOrMore(fieldDirective) + SEMI) + Optional(CMNT2("comment2"))
###fieldDefn           = typespec("type") + ident + EQ + integer("value") + ZeroOrMore(fieldDirective) + SEMI + Optional(CMNT2("comment2"))
field               = fieldint | fieldstr | fieldenumInline | fieldenum | fieldtag | fieldres | fieldstruct 
####fieldDefn           = CMNT + field  + SEMI + Optional(CMNT2)
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
###topLevelStatement = Group(annotateDef | structDefn  | messageDefn  | enumDefn | importDirective | optionDirective)
topLevelStatement = Group(annotateDef | structDefn  |  enumDefn | importDirective | optionDirective)

##parser = Optional(packageDirective) + ZeroOrMore(topLevelStatement)
#parser = Group(CMNT) + ZeroOrMore(topLevelStatement)
parser = ZeroOrMore(topLevelStatement)

parser.ignore(comment)

