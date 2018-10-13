# BinXbuff
While still in its initial phase,the aim of this project is to take a definition file that specifies a message on 
a byte level and translates this into code. 
This tool can generate C, java and python to serialize and deserialize a byte stream of data. The byte stream is 
normally either data that must be stored on a file or serial data, e.g. via RS232 or an RF link.  

The purpose is similar to other tools such as protobuff or flatbuff with the following differences:
- protobuff, etc focus on serialization and deserialization of objects, binXbuff focuses on the byte level definition
- this tool focus on embedded processors with limited memory
- messages are defined on byte level which means that that code can be generated for existing binary protocols 
- the C code generated by this tool will not use the heap (no alloc and free calls)
- the Java and python code is to complement the embedded C code for communicating between the embedded devices and PCs or mobile phones

In addition to the features above, a program that can translate between json and this embedded binary protocol is also in the pipeline.

# Protocol definition

The definition can contain the following elements

## Annotations
Annotations are not stricly part of the definition but mainly used to pass data down to the code generators. Annotations can therefore be used to add information such as copyright, specifying details on code generation, etc 

## BinXbuff Comments  
These are comments that are only relevant to the BinXbuff definition or it can be used to temporarily ignore a part of a definition. These comments start with '#' and end at the end of the line.

e.g.
```# this is a comment
```
## Documentation Comments 
Documentation comments  are comments that explain the data stream. These comment follow the C/CPP style comments and can be used by a documentation generator to generate documentation for the protocol.

e.g.
```
/* 
   This comment explains the message definiton below 
 */
struct msg {
  int16   var;    // this comment goes with the var 
} 
```

## Enumeration
Most protocols have a lot of tags with numeric values that have special meaning. BinXbuff therefore allow the definition of these tags with their assosiated values. (Note that in the structure definitions these enums are declared with a spesific byte size, e.g. enum16)

e.g.
```
enum Gender {
    UNKNOWN = 0;    
    MALE    = 1;   // set as male
    FEMLE   = 0x2;   // set as female
    OTHER   = 0x3;   // if a person identifies with a different gender 
}

enum Command {
    RESERVED   = 0;    
    READ_INFO  = 11;     // request info command from the server
    SEND_INFO  = 12;     // server reply tag
}

``` 
## Structure Definitions
The struture definition declares the final byte layout. The definition is similar to the sructure definitions used in C or definition of messages in Protobuff. The main characteristic of these field definitions is that each field in the structure defines exacly how many bytes it occupies. 

## Fields Structure Definitions
A struture consists of multiple fields. Each field is defined in terms a its size, endianess, optional fixed value nd given a user friendly name.
### Basic definition
The simplest definiton consists of a type and a field name.
e.g.
```
struct msg2 {
  uint32   var2;     
  uint8    var3;     
  enum8    Gender gender;
} 
```

### Constant field value
Field with constant values can be declared as follows:
```
struct msg3 {
  uint32   __magic     = 0x1234567;     
  enum8    Command cmd = READ_INFO;
  uint8    var4;     
  uint8    var5;     
} 
```

