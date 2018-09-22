# BBX document heading generation Testing
### Test BBX version 0.1-4
___
## Intoduction
This is the definiton of the message protocol                   used for bla-bla-bla
___
___
## Enumerations
___
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
### GGheader
   This is the common header for everybody.
Fields in this structure

|Field|Type|Array|Comment|
|------|-----|-----|------------------------------|
|dest|uint8|-| This is to test a very long comment line.         The destination is where the message should be sendto.        Each device should be allocated a fixed address.       Alt dest comment|
|mM|MSGID16|-|  This is to test a very long comment line. Abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz|
|msg_id|uint16|-|  This is to test a very long comment line. Abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz|
|CalcCrc16|CRC16|-|   CRC16     CalcCrc16(dest..msgid); |
|Total| length|7|1+2+2+2|
### SetProfile
   This is the message to set the user profile.   Line 2 of comment
Structure inherits all fields from **GGheader** and add these

|Field|Type|Array|Comment|
|------|-----|-----|------------------------------|
|Parent|[GGheader](#ggheader)||This data prepend this structure|
|id|int32|-|  the user identificatin number|
|surname|char|20|  the user surname|
|fieldvarname|enum8 [ename](#enum-ename)|-||
|gender|enum8 [Gender](#enum-gender)|-||
|dlen|int8|-||
|hdrCrc2|CRC16|-|  a message calculated crc|
|addit|char|dlen||
|email|zstring|-||
|Total| length|variable|1+2+2+2+ 4+ (20)*1+1+1+1+2+ (dlen)*1+-100000|

# BBX document heading generation Testing
### Test BBX version 0.1-4
___
## Intoduction
This is the definiton of the message protocol                   used for bla-bla-bla
___
___
## Enumerations
___
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
### GGheader
   This is the common header for everybody.
Fields in this structure

|Field|Type|Array|Comment|
|------|-----|-----|------------------------------|
|dest|uint8|-| This is to test a very long comment line.         The destination is where the message should be sendto.        Each device should be allocated a fixed address.       Alt dest comment|
|mM|MSGID16|-|  This is to test a very long comment line. Abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz|
|msg_id|uint16|-|  This is to test a very long comment line. Abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz|
|CalcCrc16|CRC16|-|   CRC16     CalcCrc16(dest..msgid); |
|Total| length|7|1+2+2+2|
### SetProfile
   This is the message to set the user profile.   Line 2 of comment
Structure inherits all fields from **GGheader** and add these

|Field|Type|Array|Comment|
|------|-----|-----|------------------------------|
|Parent|[GGheader](#ggheader)||This data prepend this structure|
|id|int32|-|  the user identificatin number|
|surname|char|20|  the user surname|
|fieldvarname|enum8 [ename](#enum-ename)|-||
|gender|enum8 [Gender](#enum-gender)|-||
|dlen|int8|-||
|hdrCrc2|CRC16|-|  a message calculated crc|
|addit|char|dlen||
|email|zstring|-||
|Total| length|variable|1+2+2+2+ 4+ (20)*1+1+1+1+2+ (dlen)*1+-100000|