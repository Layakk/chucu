#undef amd64
#undef i386
#undef i486
#undef i586
#undef x86_64
                .altmacro
                .intel_syntax noprefix
                .arch   i386, jumps
                .code32
.macro          section name
                .section \name
                .code32
.endm

.macro          ctok32  addvalue, cto8
                local   ckstart, ckmark, ckcount, ckend
                local   ckloop2, ckloop3
// 1st param: effective addvalue (typically 0 or edi; any rvalue)
// 2nd param: where is cto8 (dl, bl, or literal)

section         ctok32.00
        .ifnc   \addvalue, 0
        .ifc    \addvalue, edi
                mov     esi, edi
        .endif
        .endif
                jmp     ckstart
ckloop3:
                mov     al, [edi]
                add     edi, 1
section         ctok32.10                // Jcc only
                cmp     al, 0x80        // lo of 6-byte Jcc
                jb      ckloop2
                cmp     al, 0x8f        // hi of 6-byte Jcc
                ja      ckloop2
                cmpb    [edi -2], 0x0F  // prefix of 6-byte Jcc
                je      ckmark
ckloop2:
section         ctok32.20
                sub     al, 0xE8
                cmp     al, 0xE9 - 0xE8
                ja      ckcount
ckmark:
                cmpb    [edi], \cto8
                jnz     ckcount
                mov     eax, [edi]

                shr     ax, 8
                rol     eax, 16
                xchg    ah, al
// above 3 instr are equivalent to the following 2 instr:
//               mov     al, 0   ; clear cto8  [setup partial-write stall]
//               bswap   eax     ; not on 386: need 486 and up

                sub     eax, edi
        .ifnc   \addvalue, 0
        .ifc    \addvalue, edi
                add     eax, esi
        .else
                add     eax, \addvalue
        .endif
        .endif
                mov     [edi], eax
                add     edi, 4
ckstart:
                sub     ecx, 4
section         ctok32.30   // Jcc only
                mov     al, [edi]
                add     edi, 1
                loop    ckloop2  // prefix cannot overlap previous displacement
section         ctok32.40
ckcount:
                sub     ecx, 1
                jg      ckloop3
ckend:
.endm


