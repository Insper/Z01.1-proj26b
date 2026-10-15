; Arquivo: led1.nasm
; Curso: Elementos de Sistemas
; Criado por: Rafael Corsi
; Data: 4/2020
;
; Faça o primeiro LED acender
; OFF OFF OFF OFF OFF OFF OFF OFF ON

leaw $16384, %A
movw $1, (%A)

