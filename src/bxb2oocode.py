from genBase import *

class OOcodeGenerator(CcodeGenerator):
    typeTable1      = {"bool":"bool","enum8":"uint8_t","char":"char","string":"String"}
    def __init__(self):
        # set the language
        self.LANG = BaseCodeGenerator.LANG_CPP
    def genClassDeclBegin(self,structname,parentstruct= None):
        s = "class "+structname+" "
        if parentstruct is not None: 
            s += ": public " + parentstruct + "\n"
        s += "{\n public:\n"
        return s
    def genClassDeclEnd(self,structname):
        s = "}; // end class "+structname+ "\n\n"
        return s

    def genClassDef(self,struct):
        parent = struct.get("parentName",None)
        s  = self.genClassDeclBegin(struct["name"],parent) 
        #  for each field, add a declaration
        s += self.genStructFieldDecls(struct)
        # for f in struct["body"]:
        #     if 'value' in f:
        #       vv = f["value"]
        #     else:
        #       vv = None
        #     s += "  "+self.genVarDecl(f, termstr = ";\n")
        #     #s += "  "+self.genVarDecl(f["type"],f["name"],vv, termstr = ";\n")
        # generate the serialze and deserialize functions for the struct
        s1 = self.genCreateFunDecl(struct)
        s += "  "+addIndent(s1) + ";\n"
        s1 = self.genCreateFromBuffFunDecl(struct)
        s += "  "+addIndent(s1) + ";\n"
        s1 = self.genPackFunDecl(struct)
        s += "  "+addIndent(s1) + ";\n"
        s1 = self.genUnpackFunDecl(struct)
        s += "  "+addIndent(s1) + ";\n"
        s += self.genClassDeclEnd(struct["name"])
        return s
    def genClassImplementation(self,struct):
        parent = struct.get("parentName",None)
        s  = self.makeLineCommentDivider2()
        s += self.makeLineComment( "Class "+struct["name"] + " implementation")
        s += self.makeLineCommentDivider()
        # generate the serialze and deserialize functions for the struct
        s += self.genPackFun(struct,namePrefix = struct['name']+"::")
        s += self.genUnpackFun(struct,namePrefix = struct['name']+"::",callParentUnpack=True)
        #s += "  "+addIndent(s1) + "\n"
        return s
    def genAll(self,hFileName,cFileName):
        # generate h file -------
        s  = self.genFileHeader(hFileName)
        s += "\n"
        s += '#include "inttypes.h"\n'
        #s += annotateDict.get('copyrigh',"")
        s += annotateDict.get('h_includes',"")
        s += self.genAllEnumDefs()
        s += self.genAuxDef()
        for st in structList:
            s += self.genClassDef( st) +"\n"

        # generate cpp file -------
        ss  = self.genFileHeader(cFileName)
        ss += "\n"
        ss += '#include "' + hFileName + "\n"
        ss += annotateDict.get('c_includes',"")
        ss += annotateDict.get('c_code',"")
        for st in structList:
            ss += self.genClassImplementation( st) +"\n"
        return s,ss