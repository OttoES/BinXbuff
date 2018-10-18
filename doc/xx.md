
# BXB definition document

### GGCommsDefinition version 1.0-2
___

## Intoduction
This is the definiton of the message protocol
                  used between the seat units and the master streamer.
                  Messages and tags marked with "DevOnly" should be 
                  ignored and is purly for trouble shooting. 
___
___

## Enumerations
___

### Enum cmd_t
 A list of all the commands. Note that all commands are send to a spesific 
   address except the broadcast command. Most commands have an acknowladge
   but note:
   * each command have a paired acknowldge (ACK) command id
   * there is only one not acknowladge (NAC) command shared by all commands 
   * the debug command is not acknowladged
   * a broadcast command is only acknowladced by one address


|Tag|Value|Comment|
|------|-----|------------------------------|
|CMD_BROADCAST|0x0A|  Broadcast |
|CMD_BROADCAST_ACK|0x03|  An acknowladge if the broadcast command was sucessfull |
|CMD_READ|0x15||
|CMD_READ_REPLY|0x16||
|CMD_WRITE|0x29||
|CMD_WRITE_ACK|0x30|  Acknowladge send on a write|
|CMD_WR_SLAVE|0x3D|  Not used: Reserved to be used to write to a single seat unit.|
|CMD_DEBUG|0x1A|  DevOnly: Debug command only and should be ignored otherwise.|
|CMD_NACK|0x04|  A negative ackowladge used if any command failed  |
|CMD_ACK_HEADER|0x05|  An acknowladge used if the header was recieved withhout error.  |

### Enum SubCmdRead

|Tag|Value|Comment|
|------|-----|------------------------------|
|DINFO_STATUS|1|  DevOnly|
|DINFO_VERSION|2|  DevOnly|
|DINFO_NETSTATS|4||
|DINFO_VERSION|5||
|DINFO_LANG_STATS|6||
|DINFO_HOPONOFF_STATS|7||
|DINFO_EVENT_LOG|8||
|DINFO_EVENT_LOG_WITH_DEL|9||
|DINFO_DEBUG|100|  DevOnly|

### Enum Gender

|Tag|Value|Comment|
|------|-----|------------------------------|
|UNKNOWN|0||
|MALE|1|  set as male|
|FEMLE|0x2|  set as female|
|OTHER|0x3|  if a person identifies with a different gender |

### Enum ename

|Tag|Value|Comment|
|------|-----|------------------------------|
|x1|1||
|x2|2||
|a1|3||
___
___

## Structures
___

### MsgHeader
 
 This is the common header for all messages. 



**Structure locals constants**
* MSG_BASE  =  TRUE
Fields in this structure


|Field|Type|Array|Comment|
|------|-----|-----|------------------------------|
|__magic|uint32|-| This is a magic number that indicates the start of the message.   (This is 0x900DBEEF in bigendian format)|
|destAddr|uint8|-|        The destination address is where the message should be send to.        Devices are allocated a fixed address. The address for the master streamer         is always 0. Seat units are each configured with ther own addresses.        Messages can be either directed to a single device or broadcasted         depending on the command. If it is a broadcast command the destination        will still be for a spesific address and that address should send CMD_BROADCAST_ACK        acknowladges or a CMD_ACK_HEADER on sucess or a CMD_NACK on an error.         When broadcasted the broadcast address is 0xFF     |
|sourceAddr|uint8|-|  The source address.|
|cmd|enum8 [cmd_t](#enum-cmd_t)|-|  This is the message identifier. |
|subCmd|uint8|-|   |
|len|uint16|-|  the lenghth of he data |
|seqNr|uint16|-|  A sequence number send with the request|
|__crc16|CRC16|-|  crc use for integrity checking|
|Total| length|14|4+1+1+1+1+2+2+2|

### ReadMsg

  The read command reads information from the seat units, normally statistics 
  and state changes. The seat unit should respond with a CMD_READ_ACK or 
  CMD_NAC on failure.



**Annotations**
* c_pack  =  
* c_unpack  =  


**Structure locals constants**
* MSG_ID  =  CMD_READ
* MSG_LEN  =  0
* IS_MSG  =  0x55


Structure inherits all fields from **MsgHeader** and add these


|Field|Type|Array|Comment|
|------|-----|-----|------------------------------|
|Parent|[MsgHeader](#msgheader)||This data prepend this structure|
|subCmd|enum8 [read_t](#enum-read_t)|-|  |
|len|uint16|-|  no data send with this message|
|seqNr|uint16|-|       A sequence number assosiated with this message and returned        by the CMD_READ_ACK     |
|__dcrc16|CRC16|-||
|Total| length|21|4+1+1+1+1+2+2+2+ 1+2+2+2|

### ReadMsgReply


**Structure locals constants**
* CASE  =  44
* MSG_ID  =  CMD_READ_REPLY
* MSG_COND  =  (subCmd == DINFO_EVENT_LOG)  


Structure inherits all fields from **MsgHeader** and add these


|Field|Type|Array|Comment|
|------|-----|-----|------------------------------|
|Parent|[MsgHeader](#msgheader)||This data prepend this structure|
|log|infoLog [infoLog](#infolog)|10|  normally|
|__crc16|CRC16|-|  crc use for integrity checking|
|Total| length|variable|4+1+1+1+1+2+2+2+  (10)*-100000+2|

### infoLog


**Annotations**
* STRUCT  =  
Fields in this structure


|Field|Type|Array|Comment|
|------|-----|-----|------------------------------|
|etype|enum8 [SubCmdRead](#enum-subcmdread)|-||
|seatNr|uint8|-||
|seatLeftAux1|uint8|-||
|seatRightAux1|uint8|-||
|res|uint32|-||
|Total| length|8|1+1+1+1+4|

### SetProfile

  This is the message to set the user profile.
  Line 2 of comment



**Annotations**
* c_pack  =  
* CV  =  


**Structure locals constants**
* MSG_ID  =  0x1155
* ARRLEN  =  10


Structure inherits all fields from **MsgHeader** and add these


|Field|Type|Array|Comment|
|------|-----|-----|------------------------------|
|Parent|[MsgHeader](#msgheader)||This data prepend this structure|
|id|int32|-|  the user identificatin number|
|surname|char|20|  the user surname|
|fieldvarname|enum8 [ename](#enum-ename)|-||
|gender|enum8 [Gender](#enum-gender)|-||
|dlen|int8|-||
|hdrCrc2|CRC16|-|  a message calculated crc|
|addit|char|dlen||
|__email|zstring|-||
|Total| length|variable|4+1+1+1+1+2+2+2+ 4+ (20)*1+1+1+1+2+ (dlen)*1+-100000|

### DemoIntlFuncCall


**Annotations**
* cv_call_in_pack  =  
* c_call_after_unpack  =  
Fields in this structure


|Field|Type|Array|Comment|
|------|-----|-----|------------------------------|
|vxx1|uint16|-||
|vxx2|uint32|-||
|Total| length|6|2+4|
