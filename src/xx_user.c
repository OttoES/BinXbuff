
#include "xx_user.h"

void PROCESS_MSG_MsgHeader(uint8_t destAddr,uint8_t sourceAddr,enum comnd msg_id,uint8_t subCmd,uint16_t mlen,uint16_t seqNr,uint16_t xxxxx)
{

}

void PROCESS_MSG_ReadMsg(uint8_t destAddr,uint8_t sourceAddr,enum comnd msg_id,uint8_t subCmd,uint16_t mlen,uint16_t seqNr,uint16_t xxxxx,enum subRead subCmd2,uint16_t rlen,uint16_t seqNr2)
{

}

/* 
 @param buff[]    buffer with data to be unpacked 
 @param buflen    number of bytes in buff, must be at long enough for complete struct 
 @return if > 0 : position in array of last extracted data
 @return if < 0 : error in data stream (-4: too short, -23: CRC error
 */
int INFO_LOG_unpack(infoLog_t* this,uint8_t  buff[],int buflen )
{

}

void PROCESS_MSG_infoLog(enum SubCmdRead etype,uint8_t seatNr,uint8_t seatLeftAux1,uint8_t seatRightAux1,uint32_t res)
{

}

void PROCESS_MSG_ReadMsgReply(uint8_t destAddr,uint8_t sourceAddr,enum comnd msg_id,uint8_t subCmd,uint16_t mlen,uint16_t seqNr,uint16_t xxxxx,infoLog_t log[])
{

}

void PROCESS_MSG_SetProfile(uint8_t destAddr,uint8_t sourceAddr,enum comnd msg_id,uint8_t subCmd,uint16_t mlen,uint16_t seqNr,uint16_t xxxxx,int32_t id,char surname[],enum ename fieldvarname,enum Gender gender,int8_t dlen,char addit[])
{

}

int DEMO_INTL_FUNC_CALL_processDemoCall(uint8_t buff[],int pos,uint16_t vxx1,uint32_t vxx2,infoLog_t infox,uint8_t infoLen,infoLog_t infoarr[])
{

}

void PROCESS_MSG_DemoIntlFuncCall(uint16_t vxx1,uint32_t vxx2,infoLog_t infox,uint8_t infoLen,infoLog_t infoarr[])
{
    
}
