
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

/* These are the main commands.
*/
enum8 cmd_t { 
    CMD_BROADCAST      = 0x0A;  // Broadcast 
    CMD_BROADCAST_ACK  = 0x03;  // An ackowladge if the broadcast command was sucessfull 
    CMD_READ           = 0x15;
    CMD_READ_ACK       = 0x16;
    CMD_WRITE          = 0x29;
    CMD_WRITE_ACK      = 0x30;  // Acknowladge send on a write
    CMD_WR_SLAVE       = 0x3D;  // Not used: Reserved to be used to write to a single seat unit.
    CMD_DEBUG          = 0x1A;  // Debug command only and should be ignored otherwise.
    CMD_NACK           = 0x04;  // A negative ackowladge used if any command failed  
    CMD_ACK_HEADER     = 0x05;  // An ackowladge used if the header was recieved withhout error.  
    }


/* 
 This is the common header for all messages. 
*/
struct MsgHeader
{
    /* This is a magic number that indicates the start of the message */
    uint32  magic = 0x900DBEEF;
    /*
       The destination address is where the message should be send to.
       Devices are allocated a fixed address. The address for the master streamer 
       is always 0. Seatuinits are each configured with ther own addresses.
    */
    uint8       destAddr;   
    uint8       sourceAddr;  // The source address.
    
}  

struct ReadMsg headedby MsgHeader
{
    enum8 cmd_t    cmd = CMD_READ;   
    enum8 read_t   subCmd;     // 
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
