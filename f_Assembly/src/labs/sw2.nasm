; Arquivo: sw1.nasm
; Curso: Elementos de Sistemas
; Criado por: Rafael Corsi
; Data: 4/2020
;
; Faça os LEDs serem o inverso das chaves
; LED = !SW

leaw $16385, %A
movw (%A), %D
notw %D
leaw $16384, %A
movw %D, (%A)

