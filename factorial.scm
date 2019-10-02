; This is an example tiny Scheme program.
; Semicolon to end of line is a comment character (like Scheme).
; It borrows from Scheme syntax, but uses Forth concepts like a data stack.
; It doesn't support features e.g. arbitrary precision arithmetic and macros.

; Examples of vectors creation which can be used to create data tables.
(define data1 (bytes '(1 2 3 4))

(define data2 (words '(1 2 3 4))

(define factorial
  (lambda
  (if (= dup 0) 1
      (* dup (factorial (- dup 1))))))

(define hello_world
  (lambda (display "Hello World!")))

(define print_one
  (lambda (display 1)))

(define main (factorial 5))
