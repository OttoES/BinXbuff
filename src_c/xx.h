/* --Autogenerated code--
File name : xx.h
Name      : GGCommsDefinition
Version   : 1.0.dev1
Copyright : Copyright OttoES (2018)
 */
#ifndef __XX_H__
#define __XX_H__

#include <stdio.h>
#include "inttypes.h"
//  Constant return values defined
#define ERR_BUFF_OUT_OF_BOUNDS -2
#define ERR_BUFF_OUT_OF_DATA -4
#define ERR_TAG_UNKNOWN -6
#define ERR_CRC_FAIL    -23
#define ERR_VALUE_NOT_EQUAL -41

// ---------------------------------------

typedef enum comnd {
  CMD_NONE             = 0x0 ,    //  Not a valid command 
  CMD_BROADCAST        = 0x0A,    //  Broadcast 
  CMD_BROADCAST_ACK    = 0x03,    //  An acknowladge if the broadcast command was sucessfull 
  CMD_READ             = 0x15,
  CMD_READ_REPLY       = 0x16,
  CMD_WRITE            = 0x29,
  CMD_WRITE_ACK        = 0x30,    //  Acknowladge send on a write
  CMD_WR_SLAVE         = 0x3D,    //  Not used: Reserved to be used to write to a single seat unit.
  CMD_DEBUG            = 0x1A,    //  DevOnly: Debug command only and should be ignored otherwise.
  CMD_NACK             = 0x04,    //  A negative ackowladge used if any command failed  
  CMD_ACK_HEADER       = 0x05     //  An acknowladge used if the header was recieved withhout error.  
} comnd_t;


typedef enum subRead {
  a                    = 1   ,
  b                    = 2    
} subRead_t;


typedef enum SubCmdRead {
  DINFO_STATUS         = 1   ,    //  DevOnly
  DINFO_VERSION        = 2   ,    //  DevOnly
  DINFO_NETSTATS       = 4   ,
  DINFO_STATS_REP      = 5   ,
  DINFO_LANG_STATS     = 6   ,
  DINFO_HOPONOFF_STATS = 7   ,
  DINFO_EVENT_LOG      = 8   ,
  DINFO_EVENT_LOG_WITH_DEL = 9   ,
  DINFO_DEBUG          = 100      //  DevOnly
} SubCmdRead_t;


typedef enum Gender {
  UNKNOWN              = 0   ,
  MALE                 = 1   ,    //  set as male
  FEMLE                = 0x2 ,    //  set as female
  OTHER                = 0x3      //  if a person identifies with a different gender 
} Gender_t;


typedef enum ename {
  x1                   = 1   ,
  x2                   = 2   ,
  a1                   = 3    
} ename_t;


// ---------------------------------------
// Function declarations
// ---------------------------------------


/* 
 @param buff[]    buffer with data to be unpacked 
 @param buflen    number of bytes in buff, must be at long enough for complete struct 
 @return if > 0 : position in array of last extracted data
 @return if < 0 : error in data stream (-4: too short, -23: CRC error
 */
int MSG_HEADER_unpack(uint8_t  buff[],int buflen );

/* 
 @param buff[]     buffer into which data should be packed 
 @param pos        start position in buffer 
 @return if > 0    position in array of last extracted data
 @return if < 0    error in data stream 
 */
int MSG_HEADER_pack(uint8_t  buff[],int bufSize, uint8_t destAddr,uint8_t sourceAddr,uint8_t subCmd,uint16_t seqNr,uint16_t xxxxx);

//============== base =================



/* 
 @param buff[]    buffer with data to be unpacked 
 @param buflen    number of bytes in buff, must be at long enough for complete struct 
 @return if > 0 : position in array of last extracted data
 @return if < 0 : error in data stream (-4: too short, -23: CRC error
 */
int READ_MSG_unpack(uint8_t  buff[],int buflen );

/* 
 @param buff[]     buffer into which data should be packed 
 @param pos        start position in buffer 
 @return if > 0    position in array of last extracted data
 @return if < 0    error in data stream 
 */
int READ_MSG_pack(uint8_t  buff[],int bufSize, uint8_t destAddr,uint8_t sourceAddr,uint8_t subCmd,uint16_t seqNr,uint16_t xxxxx,enum subRead subCmd2,uint16_t seqNr2);

typedef struct infoLog {
  enum SubCmdRead etype;
  uint8_t seatNr;
  uint8_t seatLeftAux1;
  uint8_t seatRightAux1;
  uint32_t res;
} infoLog_t;


/* 
 @param buff[]    buffer with data to be unpacked 
 @param buflen    number of bytes in buff, must be at long enough for complete struct 
 @return if > 0 : position in array of last extracted data
 @return if < 0 : error in data stream (-4: too short, -23: CRC error
 */
int INFO_LOG_unpack(infoLog_t* this,uint8_t  buff[],int buflen );

/* 
 @param buff[]     buffer into which data should be packed 
 @param pos        start position in buffer 
 @return if > 0    position in array of last extracted data
 @return if < 0    error in data stream 
 */
int INFO_LOG_pack(uint8_t  buff[],int bufSize, enum SubCmdRead etype,uint8_t seatNr,uint8_t seatLeftAux1,uint8_t seatRightAux1,uint32_t res);
static inline int INFO_LOG_packIntoBuffer(infoLog_t* this, uint8_t buff[],int bufLen)
// only for same indianness
{
    int pos = 0;
    buff[pos++] = (uint8_t)(this->etype);
    buff[pos++] = (uint8_t)(this->seatNr);
    buff[pos++] = (uint8_t)(this->seatLeftAux1);
    buff[pos++] = (uint8_t)(this->seatRightAux1);
    //  it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)this->res;
    buff[pos++] = (uint8_t)(this->res>>8);
    buff[pos++] = (uint8_t)(this->res>>16);
    buff[pos++] = (uint8_t)(this->res>>24);
    return 8; 
}


/* 
 @param buff[]    buffer with data to be unpacked 
 @param buflen    number of bytes in buff, must be at long enough for complete struct 
 @return if > 0 : position in array of last extracted data
 @return if < 0 : error in data stream (-4: too short, -23: CRC error
 */
int READ_MSG_REPLY_unpack(uint8_t  buff[],int buflen );

/* 
 @param buff[]     buffer into which data should be packed 
 @param pos        start position in buffer 
 @return if > 0    position in array of last extracted data
 @return if < 0    error in data stream 
 */
int READ_MSG_REPLY_pack(uint8_t  buff[],int bufSize, uint8_t destAddr,uint8_t sourceAddr,uint8_t subCmd,uint16_t seqNr,uint16_t xxxxx,infoLog_t log[]);


/* 
 @param buff[]    buffer with data to be unpacked 
 @param buflen    number of bytes in buff, must be at long enough for complete struct 
 @return if > 0 : position in array of last extracted data
 @return if < 0 : error in data stream (-4: too short, -23: CRC error
 */
int SET_PROFILE_unpack(uint8_t  buff[],int buflen );

/* 
 @param buff[]     buffer into which data should be packed 
 @param pos        start position in buffer 
 @return if > 0    position in array of last extracted data
 @return if < 0    error in data stream 
 */
int SET_PROFILE_pack(uint8_t  buff[],int bufSize, uint8_t destAddr,uint8_t sourceAddr,uint8_t subCmd,uint16_t seqNr,uint16_t xxxxx,char surname[],enum ename fieldvarname,enum Gender gender,int8_t dlen,char addit[]);


/* 
 @param buff[]    buffer with data to be unpacked 
 @param buflen    number of bytes in buff, must be at long enough for complete struct 
 @return if > 0 : position in array of last extracted data
 @return if < 0 : error in data stream (-4: too short, -23: CRC error
 */
int DEMO_INTL_FUNC_CALL_unpack(uint8_t  buff[],int buflen );

/* 
 @param buff[]     buffer into which data should be packed 
 @param pos        start position in buffer 
 @return if > 0    position in array of last extracted data
 @return if < 0    error in data stream 
 */
int DEMO_INTL_FUNC_CALL_pack(uint8_t  buff[],int bufSize, uint16_t vxx1,uint32_t vxx2,infoLog_t infox,uint8_t infoLen,infoLog_t infoarr[]);
#endif  // __XX_H__
