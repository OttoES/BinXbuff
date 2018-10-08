
#include <stdio.h>
#include "comms.h"

void testfun(void)
{
   dosomething();
} // end test

typedef enum cmd_t {
  CMD_BROADCAST             = 0x0A ,    //  Broadcast 
  CMD_BROADCAST_ACK         = 0x03 ,    //  An acknowladge if the broadcast command was sucessfull 
  CMD_READ                  = 0x15 ,
  CMD_READ_REPLY            = 0x16 ,
  CMD_WRITE                 = 0x29 ,
  CMD_WRITE_ACK             = 0x30 ,    //  Acknowladge send on a write
  CMD_WR_SLAVE              = 0x3D ,    //  Not used: Reserved to be used to write to a single seat unit.
  CMD_DEBUG                 = 0x1A ,    //  DevOnly: Debug command only and should be ignored otherwise.
  CMD_NACK                  = 0x04 ,    //  A negative ackowladge used if any command failed  
  CMD_ACK_HEADER            = 0x05 ,    //  An acknowladge used if the header was recieved withhout error.  
} cmd_t_t;

typedef enum SubCmdRead {
  DINFO_STATUS              = 1    ,    //  DevOnly
  DINFO_VERSION             = 2    ,    //  DevOnly
  DINFO_NETSTATS            = 4    ,
  DINFO_VERSION             = 5    ,
  DINFO_LANG_STATS          = 6    ,
  DINFO_HOPONOFF_STATS      = 7    ,
  DINFO_EVENT_LOG           = 8    ,
  DINFO_EVENT_LOG_WITH_DEL  = 9    ,
  DINFO_DEBUG               = 100  ,    //  DevOnly
} SubCmdRead_t;

typedef enum Gender {
  UNKNOWN                   = 0    ,
  MALE                      = 1    ,    //  set as male
  FEMLE                     = 0x2  ,    //  set as female
  OTHER                     = 0x3  ,    //  if a person identifies with a different gender 
} Gender_t;

typedef enum ename {
  x1                        = 1    ,
  x2                        = 2    ,
  a1                        = 3    ,
} ename_t;

int  packMsg(uint8_t  buff[],int  pos, uint8_t destAddr,uint8_t sourceAddr,uint8_t subCmd,uint16_t seqNr,CRC16_t crc16)
{
    static const int  MSG_BASE = (int ) (TRUE);
    const int  buffLen = 4+1+1+1+1+2+2+2;
    if (buffLen > bufSize) return 0;   // buffer to small
    // this is a fixed assigned field
    static const uint32 magic = (uint32) (0xEFBE0D90);
    // it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)magic;
    buff[pos++] = (uint8_t)(magic>>8);
    buff[pos++] = (uint8_t)(magic>>16);
    buff[pos++] = (uint8_t)(magic>>24);
    buff[pos++] = (uint8_t)destAddr;
    buff[pos++] = (uint8_t)sourceAddr;
    // this is a fixed assigned field
    static const enum8 cmd = (enum8) (CMD_ID);
    buff[pos++] = (uint8_t)cmd;
    buff[pos++] = (uint8_t)subCmd;
    // this is a fixed assigned field
    static const uint16 len = (uint16) (MSG_LEN);
    buff[pos++] = (uint8_t)len;
    buff[pos++] = (uint8_t)(len>>8);
    buff[pos++] = (uint8_t)seqNr;
    buff[pos++] = (uint8_t)(seqNr>>8);
    int16_t   crc16 += CalcCRC16crc16(buff, 4,4+1+1+1+1+2+2);
    buff[pos++] = (uint8_t)crc16;
    buff[pos++] = (uint8_t)(crc16>>8);
    return  pos;

} // end

int  packMsg(uint8_t  buff[],int  pos, uint8_t destAddr,uint8_t sourceAddr,uint8_t subCmd,uint16_t seqNr,CRC16_t crc16,uint8_t subCmd,uint16_t seqNr,CRC16_t crc16)
{
    static const int  MSG_ID = (int ) (CMD_READ);
    static const int  MSG_LEN = (int ) (0);
    static const int  IS_MSG = (int ) (0x55);
    const int  buffLen = 4+1+1+1+1+2+2+2+ 1+2+2+2;
    if (buffLen > bufSize) return 0;   // buffer to small
    // this is a fixed assigned field
    static const uint32 magic = (uint32) (0xEFBE0D90);
    // it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)magic;
    buff[pos++] = (uint8_t)(magic>>8);
    buff[pos++] = (uint8_t)(magic>>16);
    buff[pos++] = (uint8_t)(magic>>24);
    buff[pos++] = (uint8_t)destAddr;
    buff[pos++] = (uint8_t)sourceAddr;
    // this is a fixed assigned field
    static const enum8 cmd = (enum8) (CMD_ID);
    buff[pos++] = (uint8_t)cmd;
    buff[pos++] = (uint8_t)subCmd;
    // this is a fixed assigned field
    static const uint16 len = (uint16) (MSG_LEN);
    buff[pos++] = (uint8_t)len;
    buff[pos++] = (uint8_t)(len>>8);
    buff[pos++] = (uint8_t)seqNr;
    buff[pos++] = (uint8_t)(seqNr>>8);
    int16_t   crc16 += CalcCRC16crc16(buff, 4,4+1+1+1+1+2+2);
    buff[pos++] = (uint8_t)crc16;
    buff[pos++] = (uint8_t)(crc16>>8);
    buff[pos++] = (uint8_t)subCmd;
    // this is a fixed assigned field
    static const uint16 len = (uint16) (0);
    buff[pos++] = (uint8_t)len;
    buff[pos++] = (uint8_t)(len>>8);
    buff[pos++] = (uint8_t)seqNr;
    buff[pos++] = (uint8_t)(seqNr>>8);
    int16_t   crc16 += CalcCRC16crc16(buff, 4,4+1+1+1+1+2+2);
    buff[pos++] = (uint8_t)crc16;
    buff[pos++] = (uint8_t)(crc16>>8);
    return  pos;

} // end

int  packMsg(uint8_t  buff[],int  pos, uint8_t destAddr,uint8_t sourceAddr,uint8_t subCmd,uint16_t seqNr,CRC16_t crc16,infoLog_t log[],CRC16_t crc16)
{
    static const int  CASE = (int ) (44);
    static const int  MSG_ID = (int ) (CMD_READ_REPLY);
    static const int  MSG_COND = (int ) ((subCmd == DINFO_EVENT_LOG)  );
    const int  buffLen = 4+1+1+1+1+2+2+2+  (10)*-100000+2;
    if (buffLen > bufSize) return 0;   // buffer to small
    // this is a fixed assigned field
    static const uint32 magic = (uint32) (0xEFBE0D90);
    // it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)magic;
    buff[pos++] = (uint8_t)(magic>>8);
    buff[pos++] = (uint8_t)(magic>>16);
    buff[pos++] = (uint8_t)(magic>>24);
    buff[pos++] = (uint8_t)destAddr;
    buff[pos++] = (uint8_t)sourceAddr;
    // this is a fixed assigned field
    static const enum8 cmd = (enum8) (CMD_ID);
    buff[pos++] = (uint8_t)cmd;
    buff[pos++] = (uint8_t)subCmd;
    // this is a fixed assigned field
    static const uint16 len = (uint16) (MSG_LEN);
    buff[pos++] = (uint8_t)len;
    buff[pos++] = (uint8_t)(len>>8);
    buff[pos++] = (uint8_t)seqNr;
    buff[pos++] = (uint8_t)(seqNr>>8);
    int16_t   crc16 += CalcCRC16crc16(buff, 4,4+1+1+1+1+2+2);
    buff[pos++] = (uint8_t)crc16;
    buff[pos++] = (uint8_t)(crc16>>8);
    memcpy(buff,log,-100000*10);
    int16_t   crc16 += CalcCRC16crc16(buff, 4+1+1+1+1+2+2+2+,4+1+1+1+1+2+2+2+  (10)*-100000);
    buff[pos++] = (uint8_t)crc16;
    buff[pos++] = (uint8_t)(crc16>>8);
    return  pos;

} // end

int  packMsg(uint8_t  buff[],int  pos, uint8_t etype,uint8_t seatNr,uint8_t seatLeftAux1,uint8_t seatRightAux1,uint32_t res)
{
    const int  buffLen = 1+1+1+1+4;
    if (buffLen > bufSize) return 0;   // buffer to small
    buff[pos++] = (uint8_t)etype;
    buff[pos++] = (uint8_t)seatNr;
    buff[pos++] = (uint8_t)seatLeftAux1;
    buff[pos++] = (uint8_t)seatRightAux1;
    // it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)res;
    buff[pos++] = (uint8_t)(res>>8);
    buff[pos++] = (uint8_t)(res>>16);
    buff[pos++] = (uint8_t)(res>>24);
    return  pos;

} // end

int  packMsg(uint8_t  buff[],int  pos, uint8_t destAddr,uint8_t sourceAddr,uint8_t subCmd,uint16_t seqNr,CRC16_t crc16,char surname[],uint8_t fieldvarname,uint8_t gender,int8_t dlen,CRC16_t hdrCrc2,char addit[])
{
    static const int  MSG_ID = (int ) (0x1155);
    static const int  ARRLEN = (int ) (10);
    const int  buffLen = 4+1+1+1+1+2+2+2+ 4+ (20)*1+1+1+1+2+ (dlen)*1+-100000;
    if (buffLen > bufSize) return 0;   // buffer to small
    // this is a fixed assigned field
    static const uint32 magic = (uint32) (0xEFBE0D90);
    // it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)magic;
    buff[pos++] = (uint8_t)(magic>>8);
    buff[pos++] = (uint8_t)(magic>>16);
    buff[pos++] = (uint8_t)(magic>>24);
    buff[pos++] = (uint8_t)destAddr;
    buff[pos++] = (uint8_t)sourceAddr;
    // this is a fixed assigned field
    static const enum8 cmd = (enum8) (CMD_ID);
    buff[pos++] = (uint8_t)cmd;
    buff[pos++] = (uint8_t)subCmd;
    // this is a fixed assigned field
    static const uint16 len = (uint16) (MSG_LEN);
    buff[pos++] = (uint8_t)len;
    buff[pos++] = (uint8_t)(len>>8);
    buff[pos++] = (uint8_t)seqNr;
    buff[pos++] = (uint8_t)(seqNr>>8);
    int16_t   crc16 += CalcCRC16crc16(buff, 4,4+1+1+1+1+2+2);
    buff[pos++] = (uint8_t)crc16;
    buff[pos++] = (uint8_t)(crc16>>8);
    // this is a fixed assigned field
    static const int32 id = (int32) (1);
    // it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)id;
    buff[pos++] = (uint8_t)(id>>8);
    buff[pos++] = (uint8_t)(id>>16);
    buff[pos++] = (uint8_t)(id>>24);
    memcpy(buff,surname,1*20);
    buff[pos++] = (uint8_t)fieldvarname;
    buff[pos++] = (uint8_t)gender;
    buff[pos++] = (uint8_t)dlen;
    int16_t   hdrCrc2 += CalcCRC16hdrCrc2(buff, 4+1+1+1+1+2+2+2+ 4+ (20)*1+1+1+1+2+ (dlen)*1+-100000,4+1+1+1+1+2+2+2+ 4+ (20)*1+1+1+1);
    buff[pos++] = (uint8_t)hdrCrc2;
    buff[pos++] = (uint8_t)(hdrCrc2>>8);
    memcpy(buff,addit,1*dlen);
    // this is a fixed assigned field
    static const zstring email = (zstring) ("eeeeee");
    pos    += BIN_callZstring(buff, pos,email);
    return  pos;

} // end

// First determine the struct/message type based on MSG_ID and
// MSG_COND and then unpack

// singleton function
int  BIN_unpack(uint8_t buff[],int len)
{
   uint8_t destAddr;
   uint8_t sourceAddr;
   uint8_t subCmd;
   uint16_t seqNr;
   CRC16_t crc16;
   magic = (uint32_t)(buff[pos] + (buff[pos+1]<<8) + (((uint32_t)buff[pos+2])<<16) + (((uint32_t)buff[pos+3])<<24)) );
   pos +=4;
   destAddr = (uint8)buff[pos++] ;
   sourceAddr = (uint8)buff[pos++] ;
   cmd = (enum8)buff[pos++] ;
   subCmd = (uint8)buff[pos++] ;
   len = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
   pos +=2;
   seqNr = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
   pos +=2;
   crc16 = (CRC16_t)(buff[pos] + (buff[pos+1]<<8));
   pos +=2;
   
   if (msg_id == CMD_READ) {    // ReadMsg
      // unpack each field into a variable
      uint8_t subCmd;
      uint16_t seqNr;
      CRC16_t crc16;
      subCmd = (enum8)buff[pos++] ;
      len = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
      pos +=2;
      seqNr = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
      pos +=2;
      crc16 = (CRC16_t)(buff[pos] + (buff[pos+1]<<8));
      pos +=2;
      if (pos > len)    {
        // error
        printf("Message ReadMsg to short");
        return -2;
      }
      // call the (external user) defined function with the unpacked data
      BIN_processReadMsg(magic,destAddr,sourceAddr,cmd,subCmd,len,seqNr,crc16,subCmd,len,seqNr,crc16);
   } else 
   if ((msg_id == CMD_READ_REPLY) & ((subCmd == DINFO_EVENT_LOG)  )) {
      // unpack each field into a variable
      infoLog_t log[10];
      CRC16_t crc16;
      memcpy(log,buff,-100000*10);
      crc16 = (CRC16_t)(buff[pos] + (buff[pos+1]<<8));
      pos +=2;
      if (pos > len)    {
        // error
        printf("Message ReadMsgReply to short");
        return -2;
      }
      // call the (external user) defined function with the unpacked data
      BIN_processReadMsgReply(magic,destAddr,sourceAddr,cmd,subCmd,len,seqNr,crc16,log,crc16);
   } else 
   if (msg_id == 0x1155) {    // SetProfile
      // unpack each field into a variable
      char surname[20];
      uint8_t fieldvarname;
      uint8_t gender;
      int8_t dlen;
      CRC16_t hdrCrc2;
      char addit[dlen];
      id = (int32_t)(buff[pos] + (buff[pos+1]<<8) + (((uint32_t)buff[pos+2])<<16) + (((uint32_t)buff[pos+3])<<24)) );
      pos +=4;
      memcpy(surname,buff,1*20);
      fieldvarname = (enum8)buff[pos++] ;
      gender = (enum8)buff[pos++] ;
      dlen = (int8)buff[pos++] ;
      hdrCrc2 = (CRC16_t)(buff[pos] + (buff[pos+1]<<8));
      pos +=2;
      memcpy(addit,buff,1*dlen);
      pos    += BIN_callZstring(buff, pos,email);
      if (pos > len)    {
        // error
        printf("Message SetProfile to short");
        return -2;
      }
      // call the (external user) defined function with the unpacked data
      BIN_processSetProfile(magic,destAddr,sourceAddr,cmd,subCmd,len,seqNr,crc16,id,surname,fieldvarname,gender,dlen,hdrCrc2,addit,email);
   } else 
   {
      // error
      printf("Unknown message tag");
      return -1;
   }
   return pos;
} // end
