// C code 
#include "xx.h

#include <stdio.h>
#include "comms.h"

void testfun(void)
{
   dosomething();
} // end test

/* 
 @param buff[]     buffer into which data should be packed 
 @param pos        start position in buffer 
 @return if > 0    position in array of last extracted data
 @return if < 0    error in data stream 
 */
int  MSGHEADER_packMsg(uint8_t destAddr,uint8_t sourceAddr,uint8_t subCmd,uint16_t seqNr)
{
    static const int  MSG_BASE = (int ) (TRUE);
    const int  buffLen = 4+1+1+1+1+2+2+2;
          int  pos    = 0;
    uint8_t   buff[buffLen];
    //  this is a fixed assigned field
    static const uint32 __magic = (uint32) (0xEFBE0D90);
    //  it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)__magic;
    buff[pos++] = (uint8_t)(__magic>>8);
    buff[pos++] = (uint8_t)(__magic>>16);
    buff[pos++] = (uint8_t)(__magic>>24);
    buff[pos++] = (uint8_t)destAddr;
    buff[pos++] = (uint8_t)sourceAddr;
    //  this is a fixed assigned field
    static const enum8 cmd = (enum8) (CMD_ID);
    buff[pos++] = (uint8_t)cmd;
    buff[pos++] = (uint8_t)subCmd;
    //  this is a fixed assigned field
    static const uint16 len = (uint16) (MSG_LEN);
    buff[pos++] = (uint8_t)len;
    buff[pos++] = (uint8_t)(len>>8);
    buff[pos++] = (uint8_t)seqNr;
    buff[pos++] = (uint8_t)(seqNr>>8);
    int16_t   __crc16 += CalcCRC16__crc16(buff, 4,4+1+1+1+1+2+2);
    buff[pos++] = (uint8_t)__crc16;
    buff[pos++] = (uint8_t)(__crc16>>8);
    return  CallStoreSendBuffer(buff, pos);

} // end

int  MSGHEADER_unpackMsg(uint8_t  buff[],int  len )
{
    int  pos = 0;
    //  this is a fixed assigned field
    static const uint32 __magic = (uint32) (0xEFBE0D90);
    __magic = (uint32_t)(buff[pos] + (buff[pos+1]<<8) + (((uint32_t)buff[pos+2])<<16) + (((uint32_t)buff[pos+3])<<24)) );
pos +=4;
    destAddr = (uint8)buff[pos++] ;
    sourceAddr = (uint8)buff[pos++] ;
    //  this is a fixed assigned field
    static const enum8 cmd = (enum8) (CMD_ID);
    cmd = (enum8)buff[pos++] ;
    subCmd = (uint8)buff[pos++] ;
    //  this is a fixed assigned field
    static const uint16 len = (uint16) (MSG_LEN);
    len = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    seqNr = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    ??int16_t   __crc16 += CalcCRC16__crc16(buff, 4,4+1+1+1+1+2+2);
    __crc16 = (CRC16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;

} // end


/* 
 @param buff[]     buffer into which data should be packed 
 @param pos        start position in buffer 
 @return if > 0    position in array of last extracted data
 @return if < 0    error in data stream 
 */
int  READMSG_packMsg(uint8_t destAddr,uint8_t sourceAddr,uint8_t subCmd,uint16_t seqNr,uint8_t subCmd,uint16_t seqNr)
{
    static const int  MSG_ID = (int ) (CMD_READ);
    static const int  MSG_LEN = (int ) (0);
    static const int  IS_MSG = (int ) (0x55);
    const int  buffLen = 4+1+1+1+1+2+2+2+ 1+2+2+2;
          int  pos    = 0;
    uint8_t   buff[buffLen];
    //  this is a fixed assigned field
    static const uint32 __magic = (uint32) (0xEFBE0D90);
    //  it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)__magic;
    buff[pos++] = (uint8_t)(__magic>>8);
    buff[pos++] = (uint8_t)(__magic>>16);
    buff[pos++] = (uint8_t)(__magic>>24);
    buff[pos++] = (uint8_t)destAddr;
    buff[pos++] = (uint8_t)sourceAddr;
    //  this is a fixed assigned field
    static const enum8 cmd = (enum8) (CMD_ID);
    buff[pos++] = (uint8_t)cmd;
    buff[pos++] = (uint8_t)subCmd;
    //  this is a fixed assigned field
    static const uint16 len = (uint16) (MSG_LEN);
    buff[pos++] = (uint8_t)len;
    buff[pos++] = (uint8_t)(len>>8);
    buff[pos++] = (uint8_t)seqNr;
    buff[pos++] = (uint8_t)(seqNr>>8);
    int16_t   __crc16 += CalcCRC16__crc16(buff, 4,4+1+1+1+1+2+2);
    buff[pos++] = (uint8_t)__crc16;
    buff[pos++] = (uint8_t)(__crc16>>8);
    buff[pos++] = (uint8_t)subCmd;
    //  this is a fixed assigned field
    static const uint16 len = (uint16) (0);
    buff[pos++] = (uint8_t)len;
    buff[pos++] = (uint8_t)(len>>8);
    buff[pos++] = (uint8_t)seqNr;
    buff[pos++] = (uint8_t)(seqNr>>8);
    int16_t   __crc16 += CalcCRC16__crc16(buff, 4,4+1+1+1+1+2+2);
    buff[pos++] = (uint8_t)__crc16;
    buff[pos++] = (uint8_t)(__crc16>>8);
    return  CallStoreSendBuffer(buff, pos);

} // end

int  READMSG_unpackMsg(uint8_t  buff[],int  len )
{
    int  pos = 0;
    //  this is a fixed assigned field
    static const uint32 __magic = (uint32) (0xEFBE0D90);
    __magic = (uint32_t)(buff[pos] + (buff[pos+1]<<8) + (((uint32_t)buff[pos+2])<<16) + (((uint32_t)buff[pos+3])<<24)) );
pos +=4;
    destAddr = (uint8)buff[pos++] ;
    sourceAddr = (uint8)buff[pos++] ;
    //  this is a fixed assigned field
    static const enum8 cmd = (enum8) (CMD_ID);
    cmd = (enum8)buff[pos++] ;
    subCmd = (uint8)buff[pos++] ;
    //  this is a fixed assigned field
    static const uint16 len = (uint16) (MSG_LEN);
    len = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    seqNr = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    ??int16_t   __crc16 += CalcCRC16__crc16(buff, 4,4+1+1+1+1+2+2);
    __crc16 = (CRC16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    subCmd = (enum8)buff[pos++] ;
    //  this is a fixed assigned field
    static const uint16 len = (uint16) (0);
    len = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    seqNr = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    ??int16_t   __crc16 += CalcCRC16__crc16(buff, 4,4+1+1+1+1+2+2);
    __crc16 = (CRC16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;

} // end


/* 
 @param buff[]     buffer into which data should be packed 
 @param pos        start position in buffer 
 @return if > 0    position in array of last extracted data
 @return if < 0    error in data stream 
 */
int  READMSGREPLY_packMsg(uint8_t destAddr,uint8_t sourceAddr,uint8_t subCmd,uint16_t seqNr,infoLog_t log[])
{
    static const int  CASE = (int ) (44);
    static const int  MSG_ID = (int ) (CMD_READ_REPLY);
    static const int  MSG_COND = (int ) ((subCmd == DINFO_EVENT_LOG)  );
    const int  buffLen = 4+1+1+1+1+2+2+2+  (10)*-100000+2;
          int  pos    = 0;
    uint8_t   buff[buffLen];
    //  this is a fixed assigned field
    static const uint32 __magic = (uint32) (0xEFBE0D90);
    //  it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)__magic;
    buff[pos++] = (uint8_t)(__magic>>8);
    buff[pos++] = (uint8_t)(__magic>>16);
    buff[pos++] = (uint8_t)(__magic>>24);
    buff[pos++] = (uint8_t)destAddr;
    buff[pos++] = (uint8_t)sourceAddr;
    //  this is a fixed assigned field
    static const enum8 cmd = (enum8) (CMD_ID);
    buff[pos++] = (uint8_t)cmd;
    buff[pos++] = (uint8_t)subCmd;
    //  this is a fixed assigned field
    static const uint16 len = (uint16) (MSG_LEN);
    buff[pos++] = (uint8_t)len;
    buff[pos++] = (uint8_t)(len>>8);
    buff[pos++] = (uint8_t)seqNr;
    buff[pos++] = (uint8_t)(seqNr>>8);
    int16_t   __crc16 += CalcCRC16__crc16(buff, 4,4+1+1+1+1+2+2);
    buff[pos++] = (uint8_t)__crc16;
    buff[pos++] = (uint8_t)(__crc16>>8);
    memcpy(buff,log,-100000*10);
    int16_t   __crc16 += CalcCRC16__crc16(buff, 4+1+1+1+1+2+2+2+,4+1+1+1+1+2+2+2+  (10)*-100000);
    buff[pos++] = (uint8_t)__crc16;
    buff[pos++] = (uint8_t)(__crc16>>8);
    return  CallStoreSendBuffer(buff, pos);

} // end

int  READMSGREPLY_unpackMsg(uint8_t  buff[],int  len )
{
    int  pos = 0;
    //  this is a fixed assigned field
    static const uint32 __magic = (uint32) (0xEFBE0D90);
    __magic = (uint32_t)(buff[pos] + (buff[pos+1]<<8) + (((uint32_t)buff[pos+2])<<16) + (((uint32_t)buff[pos+3])<<24)) );
pos +=4;
    destAddr = (uint8)buff[pos++] ;
    sourceAddr = (uint8)buff[pos++] ;
    //  this is a fixed assigned field
    static const enum8 cmd = (enum8) (CMD_ID);
    cmd = (enum8)buff[pos++] ;
    subCmd = (uint8)buff[pos++] ;
    //  this is a fixed assigned field
    static const uint16 len = (uint16) (MSG_LEN);
    len = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    seqNr = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    ??int16_t   __crc16 += CalcCRC16__crc16(buff, 4,4+1+1+1+1+2+2);
    __crc16 = (CRC16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    memcpy(log,buff,-100000*10);
    ??int16_t   __crc16 += CalcCRC16__crc16(buff, 4+1+1+1+1+2+2+2+,4+1+1+1+1+2+2+2+  (10)*-100000);
    __crc16 = (CRC16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;

} // end


/* 
 @param buff[]     buffer into which data should be packed 
 @param pos        start position in buffer 
 @return if > 0    position in array of last extracted data
 @return if < 0    error in data stream 
 */
int  INFOLOG_packMsg(uint8_t etype,uint8_t seatNr,uint8_t seatLeftAux1,uint8_t seatRightAux1,uint32_t res)
{
    const int  buffLen = 1+1+1+1+4;
          int  pos    = 0;
    uint8_t   buff[buffLen];
    buff[pos++] = (uint8_t)etype;
    buff[pos++] = (uint8_t)seatNr;
    buff[pos++] = (uint8_t)seatLeftAux1;
    buff[pos++] = (uint8_t)seatRightAux1;
    //  it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)res;
    buff[pos++] = (uint8_t)(res>>8);
    buff[pos++] = (uint8_t)(res>>16);
    buff[pos++] = (uint8_t)(res>>24);
    return  CallStoreSendBuffer(buff, pos);

} // end

int  INFOLOG_unpackMsg(uint8_t  buff[],int  len )
{
    int  pos = 0;
    etype = (enum8)buff[pos++] ;
    seatNr = (uint8)buff[pos++] ;
    seatLeftAux1 = (uint8)buff[pos++] ;
    seatRightAux1 = (uint8)buff[pos++] ;
    res = (uint32_t)(buff[pos] + (buff[pos+1]<<8) + (((uint32_t)buff[pos+2])<<16) + (((uint32_t)buff[pos+3])<<24)) );
pos +=4;

} // end


/* 
 @param buff[]     buffer into which data should be packed 
 @param pos        start position in buffer 
 @return if > 0    position in array of last extracted data
 @return if < 0    error in data stream 
 */
int  SETPROFILE_packMsg(uint8_t destAddr,uint8_t sourceAddr,uint8_t subCmd,uint16_t seqNr,char surname[],uint8_t fieldvarname,uint8_t gender,int8_t dlen,CRC16_t hdrCrc2,char addit[])
{
    static const int  MSG_ID = (int ) (0x1155);
    static const int  ARRLEN = (int ) (10);
    const int  buffLen = 4+1+1+1+1+2+2+2+ 4+ (20)*1+1+1+1+2+ (dlen)*1+-100000;
          int  pos    = 0;
    uint8_t   buff[buffLen];
    //  this is a fixed assigned field
    static const uint32 __magic = (uint32) (0xEFBE0D90);
    //  it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)__magic;
    buff[pos++] = (uint8_t)(__magic>>8);
    buff[pos++] = (uint8_t)(__magic>>16);
    buff[pos++] = (uint8_t)(__magic>>24);
    buff[pos++] = (uint8_t)destAddr;
    buff[pos++] = (uint8_t)sourceAddr;
    //  this is a fixed assigned field
    static const enum8 cmd = (enum8) (CMD_ID);
    buff[pos++] = (uint8_t)cmd;
    buff[pos++] = (uint8_t)subCmd;
    //  this is a fixed assigned field
    static const uint16 len = (uint16) (MSG_LEN);
    buff[pos++] = (uint8_t)len;
    buff[pos++] = (uint8_t)(len>>8);
    buff[pos++] = (uint8_t)seqNr;
    buff[pos++] = (uint8_t)(seqNr>>8);
    int16_t   __crc16 += CalcCRC16__crc16(buff, 4,4+1+1+1+1+2+2);
    buff[pos++] = (uint8_t)__crc16;
    buff[pos++] = (uint8_t)(__crc16>>8);
    //  this is a fixed assigned field
    static const int32 id = (int32) (1);
    //  it is faster to copy byte by byte than calling memcpy()
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
    //  this is a fixed assigned field
    static const zstring __email = (zstring) ("eeeeee");
    pos    += BIN_callZstring(buff, pos,__email);
    return  CallStoreSendBuffer(buff, pos);

} // end

int  SETPROFILE_unpackMsg(uint8_t  buff[],int  len )
{
    int  pos = 0;
    //  this is a fixed assigned field
    static const uint32 __magic = (uint32) (0xEFBE0D90);
    __magic = (uint32_t)(buff[pos] + (buff[pos+1]<<8) + (((uint32_t)buff[pos+2])<<16) + (((uint32_t)buff[pos+3])<<24)) );
pos +=4;
    destAddr = (uint8)buff[pos++] ;
    sourceAddr = (uint8)buff[pos++] ;
    //  this is a fixed assigned field
    static const enum8 cmd = (enum8) (CMD_ID);
    cmd = (enum8)buff[pos++] ;
    subCmd = (uint8)buff[pos++] ;
    //  this is a fixed assigned field
    static const uint16 len = (uint16) (MSG_LEN);
    len = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    seqNr = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    ??int16_t   __crc16 += CalcCRC16__crc16(buff, 4,4+1+1+1+1+2+2);
    __crc16 = (CRC16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    //  this is a fixed assigned field
    static const int32 id = (int32) (1);
    id = (int32_t)(buff[pos] + (buff[pos+1]<<8) + (((uint32_t)buff[pos+2])<<16) + (((uint32_t)buff[pos+3])<<24)) );
pos +=4;
    memcpy(surname,buff,1*20);
    fieldvarname = (enum8)buff[pos++] ;
    gender = (enum8)buff[pos++] ;
    dlen = (int8)buff[pos++] ;
    ??int16_t   hdrCrc2 += CalcCRC16hdrCrc2(buff, 4+1+1+1+1+2+2+2+ 4+ (20)*1+1+1+1+2+ (dlen)*1+-100000,4+1+1+1+1+2+2+2+ 4+ (20)*1+1+1+1);
    hdrCrc2 = (CRC16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    memcpy(addit,buff,1*dlen);
    //  this is a fixed assigned field
    static const zstring __email = (zstring) ("eeeeee");
    pos    += BIN_callZstring(buff, pos,__email);

} // end


/* 
 @param buff[]     buffer into which data should be packed 
 @param pos        start position in buffer 
 @return if > 0    position in array of last extracted data
 @return if < 0    error in data stream 
 */
int  DEMOINTLFUNCCALL_packMsg(uint16_t vxx1,uint32_t vxx2)
{
    const int  buffLen = 2+4;
          int  pos    = 0;
    uint8_t   buff[buffLen];
    buff[pos++] = (uint8_t)vxx1;
    buff[pos++] = (uint8_t)(vxx1>>8);
    //  it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)vxx2;
    buff[pos++] = (uint8_t)(vxx2>>8);
    buff[pos++] = (uint8_t)(vxx2>>16);
    buff[pos++] = (uint8_t)(vxx2>>24);
    return  CallStoreSendBuffer(buff, pos);

} // end

int  DEMOINTLFUNCCALL_unpackMsg(uint8_t  buff[],int  len )
{
    int  pos = 0;
    vxx1 = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
pos +=2;
    vxx2 = (uint32_t)(buff[pos] + (buff[pos+1]<<8) + (((uint32_t)buff[pos+2])<<16) + (((uint32_t)buff[pos+3])<<24)) );
pos +=4;

} // end

// First determine the struct/message type based on MSG_ID and
// MSG_COND and then unpack

// singleton function
int  MSGHEADER_BIN_unpack(uint8_t buff[],int len)
{
   uint8_t destAddr;
   uint8_t sourceAddr;
   uint8_t subCmd;
   uint16_t seqNr;
   __magic = (uint32_t)(buff[pos] + (buff[pos+1]<<8) + (((uint32_t)buff[pos+2])<<16) + (((uint32_t)buff[pos+3])<<24)) );
   pos +=4;
   destAddr = (uint8)buff[pos++] ;
   sourceAddr = (uint8)buff[pos++] ;
   cmd = (enum8)buff[pos++] ;
   subCmd = (uint8)buff[pos++] ;
   len = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
   pos +=2;
   seqNr = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
   pos +=2;
   __crc16 = (CRC16_t)(buff[pos] + (buff[pos+1]<<8));
   pos +=2;
   
   if (msg_id == CMD_READ) {    // ReadMsg
      // unpack each field into a variable
      uint8_t subCmd;
      uint16_t seqNr;
      subCmd = (enum8)buff[pos++] ;
      len = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
      pos +=2;
      seqNr = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
      pos +=2;
      __crc16 = (CRC16_t)(buff[pos] + (buff[pos+1]<<8));
      pos +=2;
      if (pos > len)    {
        // error
        printf("Message ReadMsg to short");
        return -2;
      }
      // call the (external user) defined function with the unpacked data
      BIN_processReadMsg(destAddr,sourceAddr,cmd,subCmd,len,seqNr,subCmd,len,seqNr);
   } else 
   if ((msg_id == CMD_READ_REPLY) & ((subCmd == DINFO_EVENT_LOG)  )) {
      // unpack each field into a variable
      infoLog_t log[10];
      memcpy(log,buff,-100000*10);
      __crc16 = (CRC16_t)(buff[pos] + (buff[pos+1]<<8));
      pos +=2;
      if (pos > len)    {
        // error
        printf("Message ReadMsgReply to short");
        return -2;
      }
      // call the (external user) defined function with the unpacked data
      BIN_processReadMsgReply(destAddr,sourceAddr,cmd,subCmd,len,seqNr,log);
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
      pos    += BIN_callZstring(buff, pos,__email);
      if (pos > len)    {
        // error
        printf("Message SetProfile to short");
        return -2;
      }
      // call the (external user) defined function with the unpacked data
      BIN_processSetProfile(destAddr,sourceAddr,cmd,subCmd,len,seqNr,id,surname,fieldvarname,gender,dlen,hdrCrc2,addit);
   } else 
   {
      // error
      printf("Unknown message tag");
      return -1;
   }
   return pos;
} // end
