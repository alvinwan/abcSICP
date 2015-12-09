;;;
; Chapter 5 : Implicit Sequences
;
; @author: Alvin Wan
; @site: alvinwan.com
;;;


;;;
; UTILITIES
;;;

(define (naturals n)
  (cons-stream n (naturals (+ n 1))))

(define (slice stream start end)
  (cond
    ((or (null? stream) (= end 0)) nil)
      ((> start 0) (slice (cdr-stream stream)
      (- start 1)
      (- end 1)))
    (else (cons (car stream) (slice (cdr-stream stream)
      (- start 1)
      (- end 1))))
  )
)

;;;
; STREAMS
;;;


;;;
; Returns a stream that contains over every other term of another stream.
;
; >>> (define nats (naturals 1))
; nats
; >>> (slice (every-other nats) 0 10)
; (1 3 5 7 9 11 13 15 17 19)
;;;
(define (every-other stream)
  (cons-stream (car stream) (every-other (cdr-stream (cdr-stream stream)))))


;;;
; For two streams stream1 and stream2, combine the first term of stream1 with
; the second term of stream2 using a combiner function f.
;
; >>> (define nats (naturals 1))
; nats
; >>> (slice (combiner nats nats (lambda (x y) (+ x y))) 0 10)
; (3 6 9 12 15 18 21 24 27 30)
;;;
(define (combiner stream1 stream2 f)
  (cons-stream (f (car stream1) (car (cdr-stream stream2)))
    (combiner (cdr-stream stream1) (cdr-stream (cdr-stream stream2)) f)))
)


;;;
; Takes three streams and a list indicating the order with which the streams are
; interpolated. If order is (1 3 2), stream1 is the naturals, stream2 is the
; naturals starting from 2, and stream3 is the naturals starting from 3, the
; first three elements of the alt-sequences stream would be 1, 3, 2.
;
; >>> (define nats1 (naturals 1))
; nats1
; >>> (define nats2 (naturals 2))
; nats2
; >>> (define nats3 (naturals 3))
; nats3
; >>> (slice (alt-sequences nats1 nats2 nats3 '(1 3 2)) 0 10)
; (1 3 2 2 4 3 3 5 4 4)
;;;
(define (alt-sequences stream1 stream2 stream3 order)
  (define (stm order stream)
    (cond ((null? order) (force stream))
      ((eq? (car order) 1) (cons-stream (car stream1) (stm (cdr order) stream)))
      ((eq? (car order) 2) (cons-stream (car stream2) (stm (cdr order) stream)))
      ((eq? (car order) 3) (cons-stream (car stream3) (stm (cdr order) stream)))
    ))
  (stm order (delay (alt-sequences
    (cdr-stream stream1) (cdr-stream stream2) (cdr-stream stream3) order))))
