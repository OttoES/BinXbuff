from enum import Enum

class comnd(IntEnum):
  CMD_NONE             = 0x0     #  Not a valid command 
  CMD_BROADCAST        = 0x0A    #  Broadcast 
  CMD_BROADCAST_ACK    = 0x03    #  An acknowladge if the broadcast command was sucessfull 
  CMD_READ             = 0x15
  CMD_READ_REPLY       = 0x16
  CMD_WRITE            = 0x29
  CMD_WRITE_ACK        = 0x30    #  Acknowladge send on a write
  CMD_WR_SLAVE         = 0x3D    #  Not used: Reserved to be used to write to a single seat unit.
  CMD_DEBUG            = 0x1A    #  DevOnly: Debug command only and should be ignored otherwise.
  CMD_NACK             = 0x04    #  A negative ackowladge used if any command failed  
  CMD_ACK_HEADER       = 0x0     #  An acknowladge used if the header was recieved withhout error.  



class subRead(IntEnum):
  a                    = 1   
  b                    = 2   



class SubCmdRead(IntEnum):
  DINFO_STATUS         = 1       #  DevOnly
  DINFO_VERSION        = 2       #  DevOnly
  DINFO_NETSTATS       = 4   
  DINFO_STATS_REP      = 5   
  DINFO_LANG_STATS     = 6   
  DINFO_HOPONOFF_STATS = 7   
  DINFO_EVENT_LOG      = 8   
  DINFO_EVENT_LOG_WITH_DEL = 9   
  DINFO_DEBUG          = 100     #  DevOnly



class Gender(IntEnum):
  UNKNOWN              = 0   
  MALE                 = 1       #  set as male
  FEMLE                = 0x2     #  set as female
  OTHER                = 0x3     #  if a person identifies with a different gender 



class ename(IntEnum):
  x1                   = 1   
  x2                   = 2   
  a1                   = 3   



# =======================================
# Class MsgHeader implementation
# ---------------------------------------

''' 
    :param buff[]:    buffer into which data should be packed 
    :param pos:       start position in buffer 
    :return if > 0:   position in array of last extracted data
    :return if < 0:   error in data stream 
 '''
int MSG_HEADER_MsgHeader::pack(uint8_t  buff[],int bufSize,  destAddr, sourceAddr, subCmd, seqNr, xxxxx)
{
    const int MSG_ID = (const int) (CMD_NONE);
    const int MLEN = (const int) (5);
    const int buffLen = 4+1+1+1+1+2+2+2+2;
          int pos    = 0;
    if (buffLen > bufSize) return ERR_BUFF_OUT_OF_DATA;   # buffer to small
    #  this is a fixed assigned field
    const uint32_t __magic = (const uint32_t) (0xEFBE0D90 );
    #  it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)__magic;
    buff[pos++] = (uint8_t)(__magic>>8);
    buff[pos++] = (uint8_t)(__magic>>16);
    buff[pos++] = (uint8_t)(__magic>>24);
    buff[pos++] = (uint8_t)(destAddr);
    buff[pos++] = (uint8_t)(sourceAddr);
    #  this is a fixed assigned field
    const enum comnd msg_id = (const enum comnd) (MSG_ID);
    buff[pos++] = (uint8_t)(msg_id);
    buff[pos++] = (uint8_t)(subCmd);
    #  this is a fixed assigned field
    const uint16_t mlen = (const uint16_t) (MLEN);
    buff[pos++] = (uint8_t)(mlen);
    buff[pos++] = (uint8_t)(mlen>>8);
    buff[pos++] = (uint8_t)(seqNr);
    buff[pos++] = (uint8_t)(seqNr>>8);
    buff[pos++] = (uint8_t)(xxxxx);
    buff[pos++] = (uint8_t)(xxxxx>>8);
    # call user function with &destAddr and xxxxx&
    const uint16_t __crc2 = (const uint16_t) (crc16(buff,4,14));
    buff[pos++] = (uint8_t)(__crc2);
    buff[pos++] = (uint8_t)(__crc2>>8);
    return  pos;

} // end

''' 
    :param buff[]    buffer with data to be unpacked 
    :param buflen    number of bytes in buff, must be at long enough for complete struct 
    :return if > 0 : position in array of last extracted data
    :return if < 0 : error in data stream (-4: too short, -23: CRC error
 '''
int MSG_HEADER_MsgHeader::unpack(uint8_t  buff[],int buflen )
{
    int pos = 0;
    uint32_t  __magic = (uint32_t)(buff[pos] + (buff[pos+1]<<8) + (((uint32_t)buff[pos+2])<<16) + (((uint32_t)buff[pos+3])<<24)) ;
    pos +=4;
    #  check the field value is equal to the expected value
    if (__magic != 0xEFBE0D90 ) return ERR_VALUE_NOT_EQUAL;
    uint8_t  destAddr = (uint8_t)buff[pos++] ;
    uint8_t  sourceAddr = (uint8_t)buff[pos++] ;
    enum comnd  msg_id = (enum comnd)buff[pos++] ;
    #  this is an assigned value but not verified here
    uint8_t  subCmd = (uint8_t)buff[pos++] ;
    uint16_t  mlen = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
    pos +=2;
    #  this is an assigned value but not verified here
    uint16_t  seqNr = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
    pos +=2;
    uint16_t  xxxxx = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
    pos +=2;
    uint16_t  __crc2 = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
    pos +=2;
    #  check the field value is equal to the returned function value
    # call user function with &destAddr and xxxxx&
    const uint16_t ret___crc2 = (const uint16_t) (crc16(buff,4,14));
    if (ret___crc2 != __crc2) return ERR_VALUE_NOT_EQUAL;
    if ( pos > buflen) return ERR_BUFF_OUT_OF_DATA;
    // no call after unpack
    return  pos;
} // end

# =======================================
# Class ReadMsg implementation
# ---------------------------------------

''' 
    :param buff[]:    buffer into which data should be packed 
    :param pos:       start position in buffer 
    :return if > 0:   position in array of last extracted data
    :return if < 0:   error in data stream 
 '''
int READ_MSG_ReadMsg::pack(uint8_t  buff[],int bufSize,  destAddr, sourceAddr, subCmd, seqNr, xxxxx,enum subRead subCmd2, seqNr2)
{
    const int MSG_ID = (const int) (CMD_READ);
    const int MSG_LEN = (const int) (0);
    const int IS_MSG = (const int) (0x55);
    const int buffLen = 4+1+1+1+1+2+2+2+2+ 1+2+2;
          int pos    = 0;
    if (buffLen > bufSize) return ERR_BUFF_OUT_OF_DATA;   # buffer to small
    #  this is a fixed assigned field
    const uint32_t __magic = (const uint32_t) (0xEFBE0D90 );
    #  it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)__magic;
    buff[pos++] = (uint8_t)(__magic>>8);
    buff[pos++] = (uint8_t)(__magic>>16);
    buff[pos++] = (uint8_t)(__magic>>24);
    buff[pos++] = (uint8_t)(destAddr);
    buff[pos++] = (uint8_t)(sourceAddr);
    #  this is a fixed assigned field
    const enum comnd msg_id = (const enum comnd) (MSG_ID);
    buff[pos++] = (uint8_t)(msg_id);
    buff[pos++] = (uint8_t)(subCmd);
    #  this is a fixed assigned field
    const uint16_t mlen = (const uint16_t) (MLEN);
    buff[pos++] = (uint8_t)(mlen);
    buff[pos++] = (uint8_t)(mlen>>8);
    buff[pos++] = (uint8_t)(seqNr);
    buff[pos++] = (uint8_t)(seqNr>>8);
    buff[pos++] = (uint8_t)(xxxxx);
    buff[pos++] = (uint8_t)(xxxxx>>8);
    # call user function with &destAddr and xxxxx&
    const uint16_t __crc2 = (const uint16_t) (crc16(buff,4,14));
    buff[pos++] = (uint8_t)(__crc2);
    buff[pos++] = (uint8_t)(__crc2>>8);
    buff[pos++] = (uint8_t)(subCmd2);
    #  this is a fixed assigned field
    const uint16_t rlen = (const uint16_t) (0);
    buff[pos++] = (uint8_t)(rlen);
    buff[pos++] = (uint8_t)(rlen>>8);
    buff[pos++] = (uint8_t)(seqNr2);
    buff[pos++] = (uint8_t)(seqNr2>>8);
    return  pos;

} // end

''' 
    :param buff[]    buffer with data to be unpacked 
    :param buflen    number of bytes in buff, must be at long enough for complete struct 
    :return if > 0 : position in array of last extracted data
    :return if < 0 : error in data stream (-4: too short, -23: CRC error
 '''
int READ_MSG_ReadMsg::unpack(uint8_t  buff[],int buflen )
{
    int pos = 0;
    pos +=  READ_MSG_MsgHeader::unpack(buff,pos);
    enum subRead  subCmd2 = (enum subRead)buff[pos++] ;
    uint16_t  rlen = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
    pos +=2;
    #  this is an assigned value but not verified here
    uint16_t  seqNr2 = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
    pos +=2;
    if ( pos > buflen) return ERR_BUFF_OUT_OF_DATA;
    // no call after unpack
    return  pos;
} // end

# =======================================
# Class infoLog implementation
# ---------------------------------------

''' 
    :param buff[]:    buffer into which data should be packed 
    :param pos:       start position in buffer 
    :return if > 0:   position in array of last extracted data
    :return if < 0:   error in data stream 
 '''
int INFO_LOG_infoLog::pack(uint8_t  buff[],int bufSize, enum SubCmdRead etype, seatNr, seatLeftAux1, seatRightAux1, res)
{
    const int buffLen = 1+1+1+1+4;
          int pos    = 0;
    if (buffLen > bufSize) return ERR_BUFF_OUT_OF_DATA;   # buffer to small
    buff[pos++] = (uint8_t)(etype);
    buff[pos++] = (uint8_t)(seatNr);
    buff[pos++] = (uint8_t)(seatLeftAux1);
    buff[pos++] = (uint8_t)(seatRightAux1);
    #  it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)res;
    buff[pos++] = (uint8_t)(res>>8);
    buff[pos++] = (uint8_t)(res>>16);
    buff[pos++] = (uint8_t)(res>>24);
    return  pos;

} // end

''' 
    :param buff[]    buffer with data to be unpacked 
    :param buflen    number of bytes in buff, must be at long enough for complete struct 
    :return if > 0 : position in array of last extracted data
    :return if < 0 : error in data stream (-4: too short, -23: CRC error
 '''
int INFO_LOG_infoLog::unpack(infoLog_t* this,uint8_t  buff[],int buflen )
{
    int pos = 0;
    this->etype = (enum SubCmdRead)buff[pos++] ;
    this->seatNr = (uint8_t)buff[pos++] ;
    this->seatLeftAux1 = (uint8_t)buff[pos++] ;
    this->seatRightAux1 = (uint8_t)buff[pos++] ;
    this->res = (uint32_t)(buff[pos] + (buff[pos+1]<<8) + (((uint32_t)buff[pos+2])<<16) + (((uint32_t)buff[pos+3])<<24)) ;
    pos +=4;
    if ( pos > buflen) return ERR_BUFF_OUT_OF_DATA;
    return  pos;
} // end

# =======================================
# Class ReadMsgReply implementation
# ---------------------------------------

''' 
    :param buff[]:    buffer into which data should be packed 
    :param pos:       start position in buffer 
    :return if > 0:   position in array of last extracted data
    :return if < 0:   error in data stream 
 '''
int READ_MSG_REPLY_ReadMsgReply::pack(uint8_t  buff[],int bufSize,  destAddr, sourceAddr, subCmd, seqNr, xxxxx, log[])
{
    const int CASE = (const int) (44);
    const int MSG_ID = (const int) (CMD_READ_REPLY);
    const int MSG_COND = (const int) ((subCmd == DINFO_EVENT_LOG)  );
    const int buffLen = 4+1+1+1+1+2+2+2+2+  (10)*-100000;
          int pos    = 0;
    if (buffLen > bufSize) return ERR_BUFF_OUT_OF_DATA;   # buffer to small
    #  this is a fixed assigned field
    const uint32_t __magic = (const uint32_t) (0xEFBE0D90 );
    #  it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)__magic;
    buff[pos++] = (uint8_t)(__magic>>8);
    buff[pos++] = (uint8_t)(__magic>>16);
    buff[pos++] = (uint8_t)(__magic>>24);
    buff[pos++] = (uint8_t)(destAddr);
    buff[pos++] = (uint8_t)(sourceAddr);
    #  this is a fixed assigned field
    const enum comnd msg_id = (const enum comnd) (MSG_ID);
    buff[pos++] = (uint8_t)(msg_id);
    buff[pos++] = (uint8_t)(subCmd);
    #  this is a fixed assigned field
    const uint16_t mlen = (const uint16_t) (MLEN);
    buff[pos++] = (uint8_t)(mlen);
    buff[pos++] = (uint8_t)(mlen>>8);
    buff[pos++] = (uint8_t)(seqNr);
    buff[pos++] = (uint8_t)(seqNr>>8);
    buff[pos++] = (uint8_t)(xxxxx);
    buff[pos++] = (uint8_t)(xxxxx>>8);
    # call user function with &destAddr and xxxxx&
    const uint16_t __crc2 = (const uint16_t) (crc16(buff,4,14));
    buff[pos++] = (uint8_t)(__crc2);
    buff[pos++] = (uint8_t)(__crc2>>8);
    int ii;
    for (ii = 0; ii < 10 ;ii++) {
      int ret =  INFO_LOG_packIntoBuffer(&log[ii],&buff[pos],bufSize-pos);
      if (ret<0) return ret;
      pos += ret;
    } // for ii
    return  pos;

} // end

''' 
    :param buff[]    buffer with data to be unpacked 
    :param buflen    number of bytes in buff, must be at long enough for complete struct 
    :return if > 0 : position in array of last extracted data
    :return if < 0 : error in data stream (-4: too short, -23: CRC error
 '''
int READ_MSG_REPLY_ReadMsgReply::unpack(uint8_t  buff[],int buflen )
{
    int pos = 0;
    pos +=  READ_MSG_REPLY_MsgHeader::unpack(buff,pos);
    int ii;
    infoLog_t  log[10];
    for (ii = 0; ii < 10 ;ii++) {
      int ret = INFO_LOG_unpack(&log[ii],&buff[pos],buflen-pos);
      if (ret < 0) return ret;
      pos += ret;
    } // for ii
    if ( pos > buflen) return ERR_BUFF_OUT_OF_DATA;
    // no call after unpack
    return  pos;
} // end

# =======================================
# Class SetProfile implementation
# ---------------------------------------

''' 
    :param buff[]:    buffer into which data should be packed 
    :param pos:       start position in buffer 
    :return if > 0:   position in array of last extracted data
    :return if < 0:   error in data stream 
 '''
int SET_PROFILE_SetProfile::pack(uint8_t  buff[],int bufSize,  destAddr, sourceAddr, subCmd, seqNr, xxxxx, surname[],enum ename fieldvarname,enum Gender gender, dlen, addit[])
{
    const int MSG_ID = (const int) (0x1155);
    const int ARRLEN = (const int) (10);
    const int buffLen = 4+1+1+1+1+2+2+2+2+ 4+ (20)*1+1+1+1+ (dlen)*1;
          int pos    = 0;
    if (buffLen > bufSize) return ERR_BUFF_OUT_OF_DATA;   # buffer to small
    #  this is a fixed assigned field
    const uint32_t __magic = (const uint32_t) (0xEFBE0D90 );
    #  it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)__magic;
    buff[pos++] = (uint8_t)(__magic>>8);
    buff[pos++] = (uint8_t)(__magic>>16);
    buff[pos++] = (uint8_t)(__magic>>24);
    buff[pos++] = (uint8_t)(destAddr);
    buff[pos++] = (uint8_t)(sourceAddr);
    #  this is a fixed assigned field
    const enum comnd msg_id = (const enum comnd) (MSG_ID);
    buff[pos++] = (uint8_t)(msg_id);
    buff[pos++] = (uint8_t)(subCmd);
    #  this is a fixed assigned field
    const uint16_t mlen = (const uint16_t) (MLEN);
    buff[pos++] = (uint8_t)(mlen);
    buff[pos++] = (uint8_t)(mlen>>8);
    buff[pos++] = (uint8_t)(seqNr);
    buff[pos++] = (uint8_t)(seqNr>>8);
    buff[pos++] = (uint8_t)(xxxxx);
    buff[pos++] = (uint8_t)(xxxxx>>8);
    # call user function with &destAddr and xxxxx&
    const uint16_t __crc2 = (const uint16_t) (crc16(buff,4,14));
    buff[pos++] = (uint8_t)(__crc2);
    buff[pos++] = (uint8_t)(__crc2>>8);
    #  this is a fixed assigned field
    const int32_t id = (const int32_t) (1);
    #  it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)id;
    buff[pos++] = (uint8_t)(id>>8);
    buff[pos++] = (uint8_t)(id>>16);
    buff[pos++] = (uint8_t)(id>>24);
    // just copy but no valid if endianess differ
    memcpy(buff+pos,surname,1*20);
    pos += 1*20;
    buff[pos++] = (uint8_t)(fieldvarname);
    buff[pos++] = (uint8_t)(gender);
    buff[pos++] = (uint8_t)(dlen);
    // just copy but no valid if endianess differ
    memcpy(buff+pos,addit,1*dlen);
    pos += 1*dlen;
    return  pos;

} // end

''' 
    :param buff[]    buffer with data to be unpacked 
    :param buflen    number of bytes in buff, must be at long enough for complete struct 
    :return if > 0 : position in array of last extracted data
    :return if < 0 : error in data stream (-4: too short, -23: CRC error
 '''
int SET_PROFILE_SetProfile::unpack(uint8_t  buff[],int buflen )
{
    int pos = 0;
    pos +=  SET_PROFILE_MsgHeader::unpack(buff,pos);
    int32_t  id = (int32_t)(buff[pos] + (buff[pos+1]<<8) + (((uint32_t)buff[pos+2])<<16) + (((uint32_t)buff[pos+3])<<24)) ;
    pos +=4;
    #  this is an assigned value but not verified here
    char  surname[20];
    memcpy(surname,buff+pos,1*20);
    enum ename  fieldvarname = (enum ename)buff[pos++] ;
    enum Gender  gender = (enum Gender)buff[pos++] ;
    int8_t  dlen = (int8_t)buff[pos++] ;
    char  addit[dlen];
    memcpy(addit,buff+pos,1*dlen);
    if ( pos > buflen) return ERR_BUFF_OUT_OF_DATA;
    // no call after unpack
    return  pos;
} // end

# =======================================
# Class DemoIntlFuncCall implementation
# ---------------------------------------

''' 
    :param buff[]:    buffer into which data should be packed 
    :param pos:       start position in buffer 
    :return if > 0:   position in array of last extracted data
    :return if < 0:   error in data stream 
 '''
int DEMO_INTL_FUNC_CALL_DemoIntlFuncCall::pack(uint8_t  buff[],int bufSize,  vxx1, vxx2, infox, infoLen, infoarr[])
{
    const int buffLen = 2+4+-100000+1+ (infoLen)*-100000;
          int pos    = 0;
    if (buffLen > bufSize) return ERR_BUFF_OUT_OF_DATA;   # buffer to small
    buff[pos++] = (uint8_t)(vxx1);
    buff[pos++] = (uint8_t)(vxx1>>8);
    #  it is faster to copy byte by byte than calling memcpy()
    buff[pos++] = (uint8_t)vxx2;
    buff[pos++] = (uint8_t)(vxx2>>8);
    buff[pos++] = (uint8_t)(vxx2>>16);
    buff[pos++] = (uint8_t)(vxx2>>24);
    { // start block
      int ret =  INFO_LOG_packIntoBuffer(&infox,&buff[pos],bufSize-pos);
      if (ret < 0) return ret;
      pos += ret;
    } // end block
    buff[pos++] = (uint8_t)(infoLen);
    int ii;
    for (ii = 0; ii < infoLen ;ii++) {
      int ret =  INFO_LOG_packIntoBuffer(&infoarr[ii],&buff[pos],bufSize-pos);
      if (ret<0) return ret;
      pos += ret;
    } // for ii
    return  pos;

} // end

''' 
    :param buff[]    buffer with data to be unpacked 
    :param buflen    number of bytes in buff, must be at long enough for complete struct 
    :return if > 0 : position in array of last extracted data
    :return if < 0 : error in data stream (-4: too short, -23: CRC error
 '''
int DEMO_INTL_FUNC_CALL_DemoIntlFuncCall::unpack(uint8_t  buff[],int buflen )
{
    int pos = 0;
    uint16_t  vxx1 = (uint16_t)(buff[pos] + (buff[pos+1]<<8));
    pos +=2;
    uint32_t  vxx2 = (uint32_t)(buff[pos] + (buff[pos+1]<<8) + (((uint32_t)buff[pos+2])<<16) + (((uint32_t)buff[pos+3])<<24)) ;
    pos +=4;
    infoLog_t  infox;
    // Read a structured type
    int infox_ret =  INFO_LOG_unpack(&infox,buff,pos);
    if (infox_ret <0) return infox_ret;
    pos += infox_ret;
    uint8_t  infoLen = (uint8_t)buff[pos++] ;
    int ii;
    infoLog_t  infoarr[infoLen];
    for (ii = 0; ii < infoLen ;ii++) {
      int ret = INFO_LOG_unpack(&infoarr[ii],&buff[pos],buflen-pos);
      if (ret < 0) return ret;
      pos += ret;
    } // for ii
    if ( pos > buflen) return ERR_BUFF_OUT_OF_DATA;
    // no call after unpack
    return  pos;
} // end

