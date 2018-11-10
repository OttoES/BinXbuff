// test

#include "xx.c"
#include "Unity/src/unity.c"

#include "xx_user.h"
#include <stdio.h>

void PROCESS_MSG_MsgHeader(uint8_t destAddr,uint8_t sourceAddr,enum comnd msg_id,uint8_t subCmd,uint16_t mlen,uint16_t seqNr,uint16_t xxxxx)
{

}

#define ADDR_SRC1      111
#define ADDR_DEST1     122
#define SEQ_RD1        108
#define SEQ_RD_REPLY  105
#define V_XX          12345


void PROCESS_MSG_ReadMsg(uint8_t destAddr,uint8_t sourceAddr,enum comnd msg_id,uint8_t subCmd,uint16_t mlen,uint16_t seqNr,uint16_t xxxxx,enum subRead subCmd2,uint16_t rlen,uint16_t seqNr2)
{
    TEST_ASSERT_EQUAL(ADDR_DEST1,destAddr);
    TEST_ASSERT_EQUAL(ADDR_SRC1,sourceAddr);
    TEST_ASSERT_EQUAL(12,subCmd);
    TEST_ASSERT_EQUAL(SEQ_RD1,seqNr);

    TEST_ASSERT_EQUAL(SEQ_RD1+1,seqNr2);

}


void PROCESS_MSG_infoLog(enum SubCmdRead etype,uint8_t seatNr,uint8_t seatLeftAux1,uint8_t seatRightAux1,uint32_t res)
{

}

#define ADDR_SRC   11
#define ADDR_DEST  22
#define V_LEFT        54

void PROCESS_MSG_ReadMsgReply(uint8_t destAddr,uint8_t sourceAddr,enum comnd msg_id,uint8_t subCmd,uint16_t mlen,uint16_t seqNr,uint16_t xxxxx,infoLog_t log[])
{
    TEST_ASSERT_EQUAL(ADDR_DEST,destAddr);
    TEST_ASSERT_EQUAL(ADDR_SRC,sourceAddr);
    TEST_ASSERT_EQUAL(SEQ_RD_REPLY,seqNr);
    TEST_ASSERT_EQUAL(V_XX,xxxxx);
    TEST_ASSERT_EQUAL(V_LEFT,log[0].seatLeftAux1);
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

void read_msg(void)
{
    uint8_t  buff[1000];
    int ret =  READ_MSG_pack(buff,1000, ADDR_DEST1,ADDR_SRC1,12,SEQ_RD1,V_XX,2,SEQ_RD1+1);
    ret = MSG_HEADER_objFactory(buff,ret );
}


void read_msg_reply(void)
{
    uint8_t  buff[1000];
    infoLog_t log[10];
    log[0].seatLeftAux1 = V_LEFT;
    printf("Start\n");
    int ret =  READ_MSG_REPLY_pack(buff,1000, ADDR_DEST,ADDR_SRC,DINFO_EVENT_LOG,SEQ_RD_REPLY,V_XX,log);
    ret = MSG_HEADER_objFactory(buff,ret );

    printf("\n--Done--\n");
    
}

int main(void)
{
  UnityBegin("Verify generated BXB code");
  RUN_TEST(read_msg_reply);
  RUN_TEST(read_msg);
  return (UnityEnd());
}       