
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

/* 
 This is the common header definition for all messages. 
*/
struct GGheader
{
    /* This is a magic number that indicates the start of the message */
    uint32  magic = 0x900DBEEF;
    /*
       The destination is where the message should be send to.
       Devices are allocated a fixed address. The address for the master streamer 
       is always 0. Seatuinits are each configured with ther own addresses.
    */
    uint8     dest;   
    uint8     source; 
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
