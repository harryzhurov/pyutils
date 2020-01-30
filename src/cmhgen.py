#!/usr/bin/python



#-------------------------------------------------------------------------------    
#
#   Get out handlers info
#

import os
import sys
import re

s0 = '//******************************************************************************'   + os.linesep
s1 = '//*'                                                                                + os.linesep
                                                                                          
s2 = ' exception/intrrupt handlers stuff header file'                                     + os.linesep
s3 = ' vector table'                                                                      + os.linesep
                                                                                          
s4 = \
'//*'                                                                                     + os.linesep +\
'//*      Version 1.2'                                                                    + os.linesep +\
'//*'                                                                                     + os.linesep +\
'//*      Copyright (c) 2016-2020, emb-lib Project Team'                                  + os.linesep +\
'//*'                                                                                     + os.linesep +\
'//*      This file is part of the arm-none-eabi-startup project.'                        + os.linesep +\
'//*      Visit https://github.com/emb-lib/arm-none-eabi-startup for new versions.'       + os.linesep +\
'//*'                                                                                     + os.linesep +\
'//*      Permission is hereby granted, free of charge, to any person'                    + os.linesep +\
'//*      obtaining  a copy of this software and associated documentation'                + os.linesep +\
'//*      files (the "Software"), to deal in the Software without restriction,'           + os.linesep +\
'//*      including without limitation the rights to use, copy, modify, merge,'           + os.linesep +\
'//*      publish, distribute, sublicense, and/or sell copies of the Software,'           + os.linesep +\
'//*      and to permit persons to whom the Software is furnished to do so,'              + os.linesep +\
'//*      subject to the following conditions:'                                           + os.linesep +\
'//*'                                                                                     + os.linesep +\
'//*      The above copyright notice and this permission notice shall be included'        + os.linesep +\
'//*      in all copies or substantial portions of the Software.'                         + os.linesep +\
'//*'                                                                                     + os.linesep +\
'//*      THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,'                + os.linesep +\
'//*      EXPRESS  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF'            + os.linesep +\
'//*      MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.'         + os.linesep +\
'//*      IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY'           + os.linesep +\
'//*      CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,'           + os.linesep +\
'//*      TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH'                  + os.linesep +\
'//*      THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'                     + os.linesep +\
'//*'                                                                                     + os.linesep +\
'//------------------------------------------------------------------------------'        + os.linesep
 
s5 = '//*      '

s6_1 =                                                                                      os.linesep +\
'#ifndef EXHANDLER_H'                                                                     + os.linesep +\
'#define EXHANDLER_H'                                                                     + os.linesep +\
''                                                                                        + os.linesep +\
'//------------------------------------------------------------------------------'        + os.linesep +\
'//'                                                                                      + os.linesep +\
'//   Weak attribute allows to replace default handler with the user\'s one'              + os.linesep +\
'//'                                                                                      + os.linesep +\
'#define WEAK __attribute__ ((weak))'                                                     + os.linesep +\
'//------------------------------------------------------------------------------'        + os.linesep +\
''                                                                                        + os.linesep +\
'//------------------------------------------------------------------------------'        + os.linesep +\
'extern unsigned long __top_of_stack[];'                                                  + os.linesep +\
''                                                                                        + os.linesep +\
'//------------------------------------------------------------------------------'        + os.linesep +\
'//'                                                                                      + os.linesep +\
'//   Vector table item. Can be pointer to function or plain address value'               + os.linesep +\
'//'                                                                                      + os.linesep +\
'typedef void (*intfun_t)();'                                                             + os.linesep +\
'typedef struct'                                                                          + os.linesep +\
'{'                                                                                       + os.linesep +\
'    unsigned long *tos;'                                                                 + os.linesep

s6_2 =                                                                                      os.linesep +\
'}'                                                                                       + os.linesep +\
'__vector_table_t;'                                                                       + os.linesep +\
''                                                                                        + os.linesep +\
'//------------------------------------------------------------------------------'        + os.linesep +\
'//'                                                                                      + os.linesep +\
'//   Startup handler'                                                                    + os.linesep +\
'//'                                                                                      + os.linesep +\
'void Reset_Handler();'                                                                   + os.linesep +\
''                                                                                        + os.linesep +\
'//------------------------------------------------------------------------------'        + os.linesep +\
'//'                                                                                      + os.linesep +\
'//   Cortex-M internal exceptions'                                                       + os.linesep +\
'//'                                                                                      + os.linesep +\
'WEAK void NMI_Handler();'                                                                + os.linesep +\
'WEAK void HardFault_Handler();'                                                          + os.linesep +\
'WEAK void MemManage_Handler();'                                                          + os.linesep +\
'WEAK void BusFault_Handler();'                                                           + os.linesep +\
'WEAK void UsageFault_Handler();'                                                         + os.linesep +\
'WEAK void SVC_Handler();'                                                                + os.linesep +\
'WEAK void DebugMon_Handler();'                                                           + os.linesep +\
'WEAK void PendSV_Handler();'                                                             + os.linesep +\
'WEAK void SysTick_Handler();'                                                            + os.linesep +\
''                                                                                        + os.linesep +\
'//------------------------------------------------------------------------------'        + os.linesep +\
'//'                                                                                      + os.linesep +\
'//   Controller specific peripheral interrupts'                                          + os.linesep +\
'//'                                                                                      + os.linesep
                                                                                          
s7 = '//------------------------------------------------------------------------------'   + os.linesep +\
     ''                                                                                   + os.linesep +\
     '#endif // EXHANDLER_H'                                                              + os.linesep +\
     ''                                                                                   + os.linesep +\
     '//------------------------------------------------------------------------------'   + os.linesep


s8 =                                                                                        os.linesep +\
'#include "exhandler.h"'                                                                  + os.linesep +\
''                                                                                        + os.linesep +\
'//------------------------------------------------------------------------------'        + os.linesep +\
'__attribute__ ((used))'                                                                  + os.linesep +\
'__attribute__ ((section(".isr_vector")))'                                                + os.linesep +\
'const __vector_table_t __vector_table ='                                                 + os.linesep +\
'{'                                                                                       + os.linesep +\
'    __top_of_stack,'                                                                     + os.linesep +\
'    '                                                                                    + os.linesep +\
'    {'                                                                                   + os.linesep +\
'    Reset_Handler,'                                                                      + os.linesep +\
''                                                                                        + os.linesep +\
'    //--------------------------------------------------------------------------'        + os.linesep +\
'    //'                                                                                  + os.linesep +\
'    // Cortex-M core exceptions '                                                        + os.linesep +\
'    // '                                                                                 + os.linesep +\
'    NMI_Handler,'                                                                        + os.linesep +\
'    HardFault_Handler,'                                                                  + os.linesep +\
'    MemManage_Handler,'                                                                  + os.linesep +\
'    BusFault_Handler,'                                                                   + os.linesep +\
'    UsageFault_Handler,'                                                                 + os.linesep +\
'    0,                          // Reserved'                                             + os.linesep +\
'    0,                          // Reserved'                                             + os.linesep +\
'    0,                          // Reserved'                                             + os.linesep +\
'    0,                          // Reserved'                                             + os.linesep +\
'    SVC_Handler,'                                                                        + os.linesep +\
'    DebugMon_Handler,'                                                                   + os.linesep +\
'    0,                          // Reserved'                                             + os.linesep +\
'    PendSV_Handler,             // The OS context switch interrupt'                      + os.linesep +\
'    SysTick_Handler,            // The OS timer'                                         + os.linesep +\
''                                                                                        + os.linesep +\
'    //--------------------------------------------------------------------------'        + os.linesep +\
'    //'                                                                                  + os.linesep +\
'    // Peripheral interrupts'                                                            + os.linesep +\
'    // '                                                                                 + os.linesep
                                                                                    
s9 = \
'};'                                                                                      + os.linesep +\
'//------------------------------------------------------------------------------'        + os.linesep +\
'__attribute__ ((noreturn))'                                                              + os.linesep +\
'static void default_handler() { for(;;) { } }'                                           + os.linesep +\
'#ifndef NDEBUG'                                                                          + os.linesep +\
'static void hf_handler()'                                                                + os.linesep +\
'{'                                                                                       + os.linesep +\
'    volatile int i = 0;         //  debug variable: set non-zero value to '              + os.linesep +\
'    while(!i) { }               //  return from handler - this figures out '             + os.linesep +\
'                                //  an address where HW fault raises'                    + os.linesep +\
'}'                                                                                       + os.linesep +\
'#endif // NDEBUG'                                                                        + os.linesep +\
'//------------------------------------------------------------------------------'        + os.linesep +\
'//'                                                                                      + os.linesep +\
'//   Default exception handlers'                                                         + os.linesep +\
'//'                                                                                      + os.linesep +\
'#ifdef NDEBUG'                                                                           + os.linesep +\
''                                                                                        + os.linesep +\
'#pragma weak NMI_Handler        = default_handler'                                       + os.linesep +\
'#pragma weak HardFault_Handler  = default_handler'                                       + os.linesep +\
'#pragma weak MemManage_Handler  = default_handler'                                       + os.linesep +\
'#pragma weak BusFault_Handler   = default_handler'                                       + os.linesep +\
'#pragma weak UsageFault_Handler = default_handler'                                       + os.linesep +\
'#pragma weak SVC_Handler        = default_handler'                                       + os.linesep +\
'#pragma weak DebugMon_Handler   = default_handler'                                       + os.linesep +\
'#pragma weak PendSV_Handler     = default_handler'                                       + os.linesep +\
'#pragma weak SysTick_Handler    = default_handler'                                       + os.linesep +\
''                                                                                        + os.linesep +\
'#else // NDEBUG'                                                                         + os.linesep +\
''                                                                                        + os.linesep +\
'WEAK void NMI_Handler        ()  { default_handler(); }'                                 + os.linesep +\
'WEAK void HardFault_Handler  ()  { hf_handler();      }'                                 + os.linesep +\
'WEAK void MemManage_Handler  ()  { default_handler(); }'                                 + os.linesep +\
'WEAK void BusFault_Handler   ()  { default_handler(); }'                                 + os.linesep +\
'WEAK void UsageFault_Handler ()  { default_handler(); }'                                 + os.linesep +\
'WEAK void SVC_Handler        ()  { default_handler(); }'                                 + os.linesep +\
'WEAK void DebugMon_Handler   ()  { default_handler(); }'                                 + os.linesep +\
'WEAK void PendSV_Handler     ()  { default_handler(); }'                                 + os.linesep +\
'WEAK void SysTick_Handler    ()  { default_handler(); }'                                 + os.linesep +\
''                                                                                        + os.linesep +\
'#endif // NDEBUG'                                                                        + os.linesep +\
''                                                                                        + os.linesep +\
'//------------------------------------------------------------------------------'        + os.linesep +\
'//'                                                                                      + os.linesep +\
'//   Default interrupt handlers'                                                         + os.linesep +\
'//'                                                                                      + os.linesep


s10 = '//------------------------------------------------------------------------------'  + os.linesep
                       
print 'process file: ' + sys.argv[1]
                                                             
with open( sys.argv[1], 'rb') as f:                                                 
    src = f.readlines()
    
filename_pattern = '.*startup_(\w+)\.[sS]'

filename = re.match(filename_pattern, sys.argv[1]).groups()[0]
                                                                                        
#-------------------------------------------------------------------------------    
#
#   Get out handlers info
#
begin_pattern   = '\s*; External Interrupts'
handler_pattern = '\s+\w+\s+(\w+)\s+;\s(.+)'
end_pattern     = '__Vectors_End'

ProcessData = False
Handlers    = []
HLengths    = []

for i in src:
    if re.match(begin_pattern, i):
        ProcessData = True
        continue
        
    if re.match(end_pattern, i):
        break

    if ProcessData:
        if i.strip() == '':
            continue
        hrec = re.match( handler_pattern, i).groups()
        Handlers.append( hrec )
        HLengths.append( len( hrec[0] ) )
    
#-------------------------------------------------------------------------------    
#
#   Create output
#
#-----------------------------------------------------
#
#   Generate contents
#
header  = ''
source  = ''
weaks0  = '#ifdef NDEBUG' + os.linesep*2
weaks1  = os.linesep + '#else // NDEBUG' + os.linesep*2

handler_count = len(Handlers) + 15
max_hlen      = max(HLengths)

header += s0 + s1 + s5 + filename.upper() + s2 + s4 + s6_1 + '    intfun_t      vectors[' + str(handler_count) +'];' + s6_2
source += s0 + s1 + s5 + filename.upper() + s3 + s4 + s8 


for idx, i in enumerate(Handlers, start=1):
    if idx == len(Handlers):  # last element
        sep = ' '
    else:
        sep = ','
    
    if i[0] != '0':
        header += 'WEAK void ' + i[0] + '();' + os.linesep
        weaks0  += '#pragma weak ' + i[0] + ' '*(max_hlen-len(i[0])) + ' = default_handler' + os.linesep
        weaks1  += 'WEAK void ' + i[0] + ' '*(max_hlen-len(i[0])) + ' ()  { default_handler(); }' + os.linesep
        
    source += ' '*4 + i[0]  + sep + ' '*(max_hlen-len(i[0])) + ' '*4 + '// ' + i[1] + os.linesep
    if sep == ' ':
        source += ' '*4 + '}' + os.linesep
    
header += s7
source += s9 + weaks0 + weaks1 + os.linesep + '#endif // NDEBUG' + os.linesep + s10    
    
#-----------------------------------------------------
#
#   Save results
#
dirname = filename.lower()

stm32_proper_name = os.path.join( os.path.dirname(sys.argv[1]), '../stm32-proper-name.txt' )

if os.path.exists(stm32_proper_name):
    with open( stm32_proper_name, 'rt' ) as stm32_names_f:
        stm32_names = stm32_names_f.read().splitlines()
        
        lowercase_list = [n.lower() for n in stm32_names]
        if dirname in lowercase_list:
            idx = lowercase_list.index(dirname)
            dirname = stm32_names[idx]
        else:
            dirname = dirname.upper()
else:
    dirname = dirname.upper()


if not  os.path.exists(dirname):
    os.mkdir(dirname)

with open( dirname + os.sep + 'exhandler.h', 'wb' ) as hf:
    hf.write( header )

with open( dirname + os.sep + 'vectable.c', 'wb' ) as sf:
    sf.write( source )

#-------------------------------------------------------------------------------    

