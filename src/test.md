# Meddage defiition introdyction
### Spesification version"0.1-4"
___
## Intoduction
"This is the definiton of the message protocoll used for bla-bla-bla"
___
## Enumerations
### Gender

|Tag|Value|Array|Comment|
|------|-----|-----|------------------------------|
|UNKNOWN|0|arrLen||
|MALE|1|arrLen|  set as male|
|FEMLE|0x2|arrLen|  set as female|
|OTHER|0x3|arrLen|  if a person identifies with a different gender |
### yy

|Tag|Value|Array|Comment|
|------|-----|-----|------------------------------|
|x1|1|arrLen||
|x2|2|arrLen||
|a1|3|arrLen||
___
## Structures
### GGheader
   This is the common header for all messages.
Fields in this structure

|Field|Type|Array|Comment|
|------|-----|-----|------------------------------|
|dest|uint8|-| This is to test a very long comment line.         The destination is where the message shoud be send to.        Each device should be allocad a fixed address.       Alt dest comment|
|msgid|MSG_ID16|-|  This is to test a very long comment line. Abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz|
|hdrCrc|CRC16|-||
|Total| length|5|1+2+2|
### SetProfile
   This is the message to set the user profile.   Line 2 of comment
Structure inherits all fields from **GGheader** and add these

|Field|Type|Array|Comment|
|------|-----|-----|------------------------------|
|Parent|[GGheader](#ggheader)||This data prepend this structure|
|id|int32|-|  the user identificatin number|
|surname|char|20|  the user surname|
|yy|enum8|-||
|name|string|-||
|gender|enum8|-||
|dlen|int8|-||
|hdrCrc2|CRC16|-|  a message calculated crc|
|addit|char|dlen||
|email|zstring|-||
|Total| length|variable|1+2+2+ 4+ (20)*1+1+-100000+1+1+2+ (dlen)*1+-100000|