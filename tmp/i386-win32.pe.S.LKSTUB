#include "lk_macros.S"
section         LKSTUB0
                pusha
                mov     esi, offset start_of_compressed
                lea     edi, [esi + start_of_uncompressed]
                jmp     lk_blk0
lk_blk0:
                jmp     start_decrypt_res
start_decrypt_res:
                push    esi
                push    ebx
                push    ecx
                jmp     lk_blk1
lk_blk1:
                push    edx
                mov     ecx, esi
                add     ecx, offset c_len
                jmp     lk_blk2
lk_blk2:
                add     ecx, offset decrypt_key
                add     esi, offset ciphered_resources_offset
                mov     ebx, esi
                jmp     lk_blk3
lk_blk3:
                add     ebx, offset ciphered_resources_size
                xor     edx, edx
                jmp     decrypt_res
decrypt_res:
                cmp     esi, ebx
                je      final_decrypt_res
                xor     al, al
                mov     al, [esi]
                jmp     lk_blk4
lk_blk4:
                xor     al, [ecx + edx]
                mov     [esi], al
                inc     edx
                cmp     edx, offset decrypt_keysize
                jmp     lk_blk5
lk_blk5:
                jne     non_reset_key_res
                xor     edx, edx
                jmp     non_reset_key_res
non_reset_key_res:
                inc     esi
                jmp     decrypt_res
final_decrypt_res:
                pop edx
                pop ecx
                pop ebx
                jmp     lk_blk6
lk_blk6:
                pop esi 
                mov     dword ptr [edi + tls_address], offset tls_value
                push    edi
                jmp     lk_blk7
lk_blk7:
                or      ebp, -1
                jmp     dcl1_n2b
section         LKSTUB1
loopend2_n2b:
                add     ecx, 2
                jmp     decompr_got_mlen_n2b
lk_blk14:
                jb      decompr_ebpeax_n2b
                shl     eax, 8
                jmp     lk_blk15
lk_blk24:
                adc     ebx, ebx
                jmp     l1_9
decompr_got_mlen_n2b:
                cmp     ebp, -0xd00
                adc     ecx, 1
                jmp     lk_blk25
loop3_n2b:
                mov     al, [edx]
                inc     edx
                jmp     lk_blk27
lk_blk27:
                mov     [edi], al
                inc     edi
                jmp     lk_blk28
l1_7:
                adc     ecx, ecx
                add     ebx, ebx
                jnc     loop2_n2b
                jmp     lk_blk23
lk_blk12:
                jnz     loopend1_n2b  
                mov     ebx, [esi]
                sub     esi, -4
                jmp     lk_blk13
lk_blk16:
                xor     eax, -1
                jz      decompr_end_n2b
                jmp     lk_blk17
lk_blk17:
                mov     ebp, eax
                jmp     decompr_ebpeax_n2b
lk_blk26:
                jbe     decompr_copy4_n2b
                jmp     loop3_n2b
lk_blk8:
                inc     edi
                jmp     decompr_loop_n2b
lk_blk18:
                sub     esi, -4
                adc     ebx, ebx
                jmp     l1_5
lk_blk23:
                jnz     loopend2_n2b
                mov     ebx, [esi]
                sub     esi, -4
                jmp     lk_blk24
decompr_loop_n2b:
                add     ebx, ebx
                jnz     dcl2_n2b
                jmp     dcl1_n2b
lk_blk20:
                sub     esi, -4
                adc     ebx, ebx
                jmp     lk_blk21
lk_blk22:
                sub     esi, -4
                adc     ebx, ebx
                jmp     l1_7
lk_blk19:
                jnz     l1_6
                mov     ebx, [esi]
                jmp     lk_blk20
dcl1_n2b:
                mov     ebx, [esi]
                sub     esi, -4
                jmp     lk_blk9
l1_6:
                adc     ecx, ecx
                jnz     decompr_got_mlen_n2b
                inc     ecx
                jmp     loop2_n2b
lk_blk10:
                jmp     loop1_n2b
decompr_literalb_n2b:
                mov     al, [esi]
                inc     esi
                mov     [edi], al
                jmp     lk_blk8
loopend1_n2b:
                xor     ecx, ecx
                sub     eax, 3
                jmp     lk_blk14
lk_blk21:
                jmp     l1_6
lk_blk15:
                mov     al, [esi]
                inc     esi
                jmp     lk_blk16
lk_blk13:
                adc     ebx, ebx
                jmp     l1_4
loop2_n2b:
                add     ebx, ebx
                jnz     l1_7
                mov     ebx, [esi]
                jmp     lk_blk22
loop1_n2b:
                add     ebx, ebx
                jnz     l1_2
                mov     ebx, [esi]
                jmp     lk_blk11
lk_blk25:
                lea     edx, [edi+ebp]
                cmp     ebp, -4
                jmp     lk_blk26
lk_blk28:
                dec     ecx
                jnz     loop3_n2b
                jmp     lk_blk29
l1_5:
                adc     ecx, ecx
                add     ebx, ebx
                jmp     lk_blk19
lk_blk11:
                sub     esi, -4
                adc     ebx, ebx
                jmp     l1_2
l1_4:
                jnc     loop1_n2b
                jmp     loopend1_n2b
l1_9:
                jnc     loop2_n2b
                jmp     loopend2_n2b
decompr_ebpeax_n2b:
                add     ebx, ebx
                jnz     l1_5
                mov     ebx, [esi]
                jmp     lk_blk18
l1_2:
                adc     eax, eax
                add     ebx, ebx
                jnc     loop1_n2b
                jmp     lk_blk12
lk_blk9:
                adc     ebx, ebx
                jmp     dcl2_n2b
lk_blk29:
                jmp     decompr_loop_n2b
dcl2_n2b:
                jc      decompr_literalb_n2b
                mov     eax, 1
                jmp     lk_blk10
section         LKSTUB2
lk_blk36:
                mov     [edi], eax
                add     edi, 5
                mov     al, bl
                jmp     lk_blk37
lk_blk49:
                or      eax, eax
                jz      imp_failed
                jmp     lk_blk50
decompr_copy4_n2b:
                mov     eax, [edx]
                add     edx, 4
                mov     [edi], eax
                add     edi, 4
                jmp     lk_blk30
lk_blk64:

                jmp     reloc_end_jmp
next_dll:
                mov     eax, [edi]
                or      eax, eax
                jz      imports_done
                jmp     lk_blk39
reloc_end_jmp:

                jmp    original_entry
                jmp     lk_blk65
lk_blk51:
                jmp     next_func
lk_blk37:
                dec     ecx
                jnz     ct1
                lea     edi, [esi + compressed_imports]
                jmp     lk_blk38
lk_blk41:
                xchg    eax, ebp
                jmp     next_func
lk_blk39:
                mov     ebx, [edi+4]
                lea     eax, [eax + esi + start_of_imports]
                add     ebx, esi
                jmp     lk_blk40
lk_blk52:
                jmp     reloc_main
imp_failed:
                call    [esi + ExitProcess]
                jmp     imports_done
lk_blk45:
                push    eax
                inc     edi
                jmp     lk_blk46
lk_blk33:
                jnz     calltrickloop
                mov     eax, [edi]
                mov     bl, [edi + 4]
                jmp     lk_blk34
lk_blk50:
                jmp     next_imp
lk_blk46:
                mov     ecx, 0xAEF24857
                jmp     lk_mod_1;
next_imp:
                mov     [ebx], eax
                add     ebx, 4
                jmp     lk_blk51
lk_blk55:
                ja      reloc_fx
                jmp     reloc_add
lk_blk30:
                sub     ecx, 4
                ja      decompr_copy4_n2b
                add     edi, ecx
                jmp     decompr_loop_n2b
reloc_endx:
                mov     ebp, [esi + VirtualProtect]
                lea     edi, [esi + vp_base]
                mov     ebx, offset vp_size
                push    eax
                jmp     lk_blk59
lk_blk60:
                call    ebp
                lea     eax, [edi + swri]
                andb    [eax], 0x7f
                andb    [eax + 0x28], 0x7f
                jmp     lk_blk61
lk_blk53:
                inc     edi
                or      eax, eax
                jmp     lk_blk54
lk_blk44:
                movzxw  eax, word ptr [edi]
                inc     edi
                jmp     lk_blk45
lk_blk35:
                sub     eax, edi
                sub     bl, 0xE8
                add     eax, esi
                jmp     lk_blk36
reloc_add:
                add     ebx, eax
                mov     eax, [ebx]
                xchg    ah, al
                jmp     lk_blk56
loop_cs:
                push    0
                cmp     esp, eax
                jnz     loop_cs
                sub     esp, -128
                jmp     lk_blk64
next_func:
                mov     al, [edi]
                inc     edi
                jmp     lk_blk42
reloc_fx:
                and     al, 0x0F
                shl     eax, 16
                mov     ax, [edi]
                jmp     lk_blk58
ct1:
                cmp     al, 1
                ja      calltrickloop
                cmpb    [edi], offset filter_cto
                jmp     lk_blk33
lk_blk32:
                jmp     ct1
lk_mod_1:
                push    ebp
                call    [esi + GetProcAddress]
                jmp     lk_blk49
lk_blk31:
                mov     ecx, offset filter_length
                jmp     calltrickloop
lk_blk59:
                push    esp
                push    4
                push    ebx
                push    edi
                jmp     lk_blk60
lk_blk54:
                jz      reloc_endx
                cmp     al, 0xEF
                jmp     lk_blk55
lk_blk62:
                push    ebx
                push    edi
                call    ebp
                jmp     pedep9
reloc_main:
                xor     eax, eax
                mov     al, [edi]
                jmp     lk_blk53
lk_blk63:
                jmp     loop_cs
lk_blk42:
                or      al, al
                jz      next_dll
                jmp     lk_blk43
lk_blk40:
                push    eax
                add     edi, 8
                call    [esi + LoadLibraryA]
                jmp     lk_blk41
lk_blk56:
                rol     eax, 16
                xchg    ah, al
                add     eax, esi
                jmp     lk_blk57
lk_blk47:
                repne
                scasb
                jmp     lk_blk48
lk_blk38:
                jmp     next_dll
lk_blk34:
                shr     ax, 8
                rol     eax, 16
                xchg    ah, al
                jmp     lk_blk35
calltrickloop:
                mov     al, [edi]
                inc     edi
                sub     al, 0xE8
                jmp     lk_blk32
lk_blk57:
                mov     [ebx], eax
                jmp     reloc_main
lk_blk48:
                jmp     lk_mod_1
lk_blk65:

byname:
                push    edi
                dec     eax
                jmp     lk_blk47
pedep9:
                pop     eax

                popa
                lea     eax, [esp - 128]
                jmp     lk_blk63
decompr_end_n2b:
                pop     esi

                mov     edi, esi
                jmp     lk_blk31
lk_blk61:
                pop     eax
                push    eax
                push    esp
                push    eax
                jmp     lk_blk62
imports_done:
                add     edi, 4
                lea     ebx, [esi - 4]
                jmp     lk_blk52
lk_blk43:
                mov     ecx, edi
                jns     byname
                jmp     lk_blk44
lk_blk58:
                add     edi, 2
                jmp     reloc_add
section         UPX1HEAD
                .byte   85,80,88,33     //  0  UPX_MAGIC_LE32
                .byte   161,216,208,213 //     UPX_MAGIC2_LE32
                .long   0               //  8  uncompressed adler32
                .long   0               // 12  compressed adler32
#ifdef COM
                .short  0               // 16  uncompressed len
                .short  0               // 18  compressed len
                .byte   0               // 20  filter
                .byte   45              // 21  header checksum
#elif defined(EXE)
                .byte   0,0,0           // 16  uncompressed len
                .byte   0,0,0           // 19  compressed len
                .byte   0,0,0           // 22  original file size
                .byte   0               // 25  filter
                .byte   45              // 26  header checksum
#else
                .long   0               // 16  uncompressed len
                .long   0               // 20  compressed len
                .long   0               // 24  original file size
                .byte   0               // 28  filter id
                .byte   0               // 29  filter cto
                .byte   0               //  unused
                .byte   45              // 31  header checksum
#endif

