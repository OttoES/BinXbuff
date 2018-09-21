
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

