GGcomsDef = """
@name       =  "GGCommsDefinition"
@version    =  "1.0-0"
@doc_title  =  "Greatguide Communications Protocol Definition"
@doc_header =  "BXB definition documen"
@doc_intro  =  '''This is the definiton of the message protocol
                  used between the seat unts and the master streamer'''

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

/* A list of all the commands. Note that all commands are send to a spesific 
   address except the broadcast command. Most command have an acknowladge
   except for he debug command.
*/
enum cmd_t { 
    CMD_BROADCAST      = 0x0A;  // Broadcast 
    CMD_BROADCAST_ACK  = 0x03;  // An acknowladge if the broadcast command was sucessfull 
    CMD_READ           = 0x15;
    CMD_READ_ACK       = 0x16;
    CMD_WRITE          = 0x29;
    CMD_WRITE_ACK      = 0x30;  // Acknowladge send on a write
    CMD_WR_SLAVE       = 0x3D;  // Not used: Reserved to be used to write to a single seat unit.
    CMD_DEBUG          = 0x1A;  // Debug command only and should be ignored otherwise.
    CMD_NACK           = 0x04;  // A negative ackowladge used if any command failed  
    CMD_ACK_HEADER     = 0x05;  // An acknowladge used if the header was recieved withhout error.  
    }


/* 
 This is the common header for all messages. 
*/
struct MsgHeader
{
    /* This is a magic number that indicates the start of the message. */
    uint32  magic = 0xEFBE0D90;   // This is the same as 0x900DBEEF in bigendian format
    /*
       The destination address is where the message should be send to.
       Devices are allocated a fixed address. The address for the master streamer 
       is always 0. Seat units are each configured with ther own addresses.
       Messages can be either directed to a single device or broadcasted 
       depending on the command. If it is a broadcast command the destination
       will still be for a spesific address and that address should send CMD_BROADCAST_ACK
       acknowladges or a CMD_ACK_HEADER on sucess or a CMD_NACK on an error. 
       When broadcasted the broadcast address 
    */
    uint8       destAddr;   
    uint8       sourceAddr;         // The source address.
    enum8 cmd_t    cmd    = CMD_ID; // This is the message identifier. 
    
}  

/*
  The read command reads information from the seat units, normally statistics 
  and state changes. The seat unit should respond with a CMD_READ_ACK or 
  CMD_NAC on failure.
*/
struct ReadMsg headedby MsgHeader
@DD=55  @FF=44
<CMD_ID = 2> <xx = CMD_READ>
{
      
    enum8 read_t   subCmd;         // 
    uint16         len    = 0;     // no data send with this message
    /*
      A sequence number assosiated with this message and returned 
      by the CMD_READ_ACK
    */
    uint16         seqNr;       
    CRC16          crc16[destAddr:seqNr]; // crc use for integrity checking
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
struct SetProfile headedby MsgHeader 
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

from genBase import (parseBxbDefStr,MarkdownGenerator)

def mainTest():
    pp = parseBxbDefStr(GGcomsDef)
    docgen = MarkdownGenerator() 
    s = docgen.genAll()
    print(s)

    # pygen = OOpythonGenerator()
    # pygen.pprint()
    # s = pygen.genAll()
    # print(s)
    # print("\n------------------------------\n\n")
    # oogen = OOcodeGenerator()
    # #oogen.pprint()
    # s = oogen.genAll("test.hpp","test.cpp")
    # print(s)

if __name__ == "__main__":
    # execute only if run as a script
    mainTest()