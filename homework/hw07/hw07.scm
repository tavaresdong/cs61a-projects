(define (cddr s)
  (cdr (cdr s)))

(define (cadr s)
  (car (cdr s))
)

(define (caddr s)
  (car (cdr (cdr s)))
)


(define (sign x)
  (cond
      ((< x 0) -1)
      ((> x 0) 1)
      (else 0))
)


(define (square x) (* x x))

(define (pow b n)
  (cond
      ((<= n 0) 1)
      ((even? n) (square (pow b (quotient n 2))))
      (else (* b (square (pow b (quotient (- n 1) 2)))))
  ) 
)



(define (ordered? s)
  (cond
      ((null? s) true)
      ((null? (cdr s)) true)
      (else (and 
              (ordered? (cdr s)) 
              (<= (car s) (cadr s))
            )
      )
  )
)


(define (nodots s)
  (cond
      ((null? s) s)
      ((number? s) (list s))
      ((number? (car s)) (cons (car s) (nodots (cdr s))))
      ((pair? (car s)) (cons (nodots (car s)) (nodots (cdr s))))
  )
)


; Sets as sorted lists

(define (empty? s) (null? s))

(define (contains? s v)
    (cond ((empty? s) false)
          ((> (car s) v) false)
          ((= (car s) v) true)
          (else (contains? (cdr s) v))
    )
)

; Equivalent Python code, for your reference:
;
; def empty(s):
;     return len(s) == 0
;
; def contains(s, v):
;     if empty(s):
;         return False
;     elif s.first > v:
;         return False
;     elif s.first == v:
;         return True
;     else:
;         return contains(s.rest, v)

(define (add s v)
    (cond ((empty? s) (list v))
          ((contains? s v) s)
          ((> (car s) v) (cons v s))
          (else (cons (car s) (add (cdr s) v)))
    )
)

(define (intersect s t)
    (cond ((or (empty? s) (empty? t)) nil)
          'YOUR-CODE-HERE
          (else nil) ; replace this line
          ))

; Equivalent Python code, for your reference:
;
; def intersect(set1, set2):
;     if empty(set1) or empty(set2):
;         return Link.empty
;     else:
;         e1, e2 = set1.first, set2.first
;         if e1 == e2:
;             return Link(e1, intersect(set1.rest, set2.rest))
;         elif e1 < e2:
;             return intersect(set1.rest, set2)
;         elif e2 < e1:
;             return intersect(set1, set2.rest)

(define (union s t)
    (cond ((empty? s) t)
          ((empty? t) s)
          'YOUR-CODE-HERE
          (else nil) ; replace this line
          ))


