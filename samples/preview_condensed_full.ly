\version "2.24" 

#(set-default-paper-size "a4" 'landscape)

\paper {
  top-margin = 15\mm
  bottom-margin = 15\mm
  left-margin = 15\mm
  right-margin = 15\mm
  ragged-last-bottom = ##f
  ragged-bottom = ##f
  max-systems-per-page = #4
  min-systems-per-page = #3
  indent = 25\mm
  short-indent = 15\mm
  system-system-spacing.basic-distance = #22
  system-system-spacing.minimum-distance = #18
  system-system-spacing.padding = #4
  system-system-spacing.stretchability = #30
  staff-staff-spacing.basic-distance = #11
  staff-staff-spacing.minimum-distance = #9
  staff-staff-spacing.padding = #1
  print-page-number = ##t
}

\layout {
  \context {
    \Score
    % Uniform horizontal spacing: all bars get similar width regardless of
    % how many notes they contain. This is the main lever against the
    % "some bars tiny, some huge" effect.
    \override SpacingSpanner.uniform-stretching = ##t
    \override SpacingSpanner.strict-note-spacing = ##f
    \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/8)
  }
}
\include "lilypond-book-preamble.ly"
    
color = #(define-music-function (parser location color) (string?) #{
        \once \override NoteHead.color = #(x11-color color)
        \once \override Stem.color = #(x11-color color)
        \once \override Rest.color = #(x11-color color)
        \once \override Beam.color = #(x11-color color)
     #})
    
\header { 
 title = "kronos_kai_kairos"   
  
  } 
 
\score  { 
 
      << \new Staff  = Reedsgx \with  { 
         \autoBeamOff 
          } 
          { \partial 32*16 
             \pageBreak
             \clef "treble" 
             \key d \major 
             \time 4/4
             r 4.  
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             ees' 16 [  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             e' 16 ]  
             \bar "|"  %{ end measure 0 %} 
             < fis'  ees'  > 4   
             < e'  b  > 4   
             < ees'  bes  > 4   
             < des'  aes  > 4   
             \bar "|"  %{ end measure 1 %} 
             r 2..  
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             a' 16 [  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             b' 16 ]  
             \bar "|"  %{ end measure 2 %} 
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             cis'' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             b' 8 ]  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             aes' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             e' 8 ]  
             < ees'  b  > 4  ~   
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             dis' 8 [  ~  
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < ees'  b  > 8   
             \bar "|"  %{ end measure 3 %} 
             < cis'  b  > 1   
             \bar "|"  %{ end measure 4 %} 
             < fis'  cis'  > 1   
             \bar "|"  %{ end measure 5 %} 
             < g'  e'  > 1   
             \bar "|"  %{ end measure 6 %} 
             < g'  e'  > 1   
             \bar "||"  %{ end measure 7 %} 
             \time 5/4
             r 1  
             r 4  
             \bar "|"  %{ end measure 8 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 9 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 10 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 11 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 12 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 13 %} 
             g' 1  ~  
             g' 16.  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             a' 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             b' 16. ]  
             \bar "|"  %{ end measure 14 %} 
             < c''  g'  > 4.  ~   
             g' 2  ~  
             g' 8..  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < g'  f'  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < g'  e'  > 16.   
             \bar "|"  %{ end measure 15 %} 
             < g'  d'  > 4.  ~   
             < g'  e'  > 2..   
             \bar "|"  %{ end measure 16 %} 
             < gis'  e'  > 1  ~   
             < gis'  e'  > 4   
             \bar "|"  %{ end measure 17 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 18 %} 
             r 4.  
             e'' 4  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             c'' 8  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             aes' 8  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             g' 8  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             e' 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             c' 8 ]  
             \bar "||"  %{ end measure 19 %} 
             \pageBreak
             < g'  c'  > 1  ~   
             < g'  c'  > 4   
             \bar "|"  %{ end measure 20 %} 
             aes 4.  
             e' 2..  
             \bar "|"  %{ end measure 21 %} 
             d' 4.  
             c' 8  
             r 8  
             e 2  ~  
             e 8  
             \bar "|"  %{ end measure 22 %} 
             e 2.  
             r 4  
             g 4  
             \bar "|"  %{ end measure 23 %} 
             a 1  ~  
             a 16.  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             g 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             f 16. ]  
             \bar "|"  %{ end measure 24 %} 
             e 4.  
             b 2..  
             \bar "|"  %{ end measure 25 %} 
             c' 4.  
             d' 8  
             r 8  
             e' 2  ~  
             e' 8  
             \bar "|"  %{ end measure 26 %} 
             e' 2  
             r 2.  
             \bar "||"  %{ end measure 27 %} 
             \pageBreak
             r 2.  
             c'' 4  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             b' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             g' 8 ]  
             \bar "|"  %{ end measure 28 %} 
             g' 2.  
             r 4  
             r 16.  
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             b' 16 [  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             c'' 16. ]  
             \bar "|"  %{ end measure 29 %} 
             d'' 4.  
             c'' 8  
             r 4  
             e'' 4  
             c'' 4  
             \bar "|"  %{ end measure 30 %} 
             c'' 2.  
             r 4.  
             < f'  f  > 8   
             \bar "|"  %{ end measure 31 %} 
             < e'  e  > 4.   
             < c''  c'  > 4.   
             < d''  d'  > 4   
             < g''  g'  > 4   
             \bar "|"  %{ end measure 32 %} 
             < e''  e'  > 4.   
             < b'  b  > 2  ~   
             < b'  b  > 8..   
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < c''  c'  > 16   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < b'  b  > 16.   
             \bar "|"  %{ end measure 33 %} 
             < c''  c'  > 4   
             < g'  g  > 1   
             \bar "|"  %{ end measure 34 %} 
             r 1  
             r 8  
             aes' 8  
             \bar "||"  %{ end measure 35 %} 
             \pageBreak
             g' 4.  
             bes' 4.  
             f'' 4  
             ees'' 4  
             \bar "|"  %{ end measure 36 %} 
             d'' 4.  
             c'' 8  
             r 4  
             g' 2  
             \bar "|"  %{ end measure 37 %} 
             f' 4.  
             c' 2..  
             \bar "|"  %{ end measure 38 %} 
             b 2.  
             r 2  
             \bar "|"  %{ end measure 39 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 40 %} 
             < a'  f'  > 2   
             r 4.  
             < a'  f'  > 8   
             r 4  
             \bar "|"  %{ end measure 41 %} 
             < b'  f'  > 4   
             < c''  g'  > 1   
             \bar "||"  %{ end measure 42 %} 
             \pageBreak
             < b'  e'  > 1  ~   
             < b'  e'  > 4   
             \bar "|"  %{ end measure 43 %} 
             aes 4.  
             e' 2..  
             \bar "|"  %{ end measure 44 %} 
             d' 4.  
             c' 8  
             r 8  
             e 2  ~  
             e 8  
             \bar "|"  %{ end measure 45 %} 
             r 1  
             g 4  
             \bar "|"  %{ end measure 46 %} 
             a 1  ~  
             a 16.  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             g 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             f 16. ]  
             \bar "|"  %{ end measure 47 %} 
             e 4.  
             b 2  ~  
             b 8  
             < aes'  d'  > 4   
             \bar "|"  %{ end measure 48 %} 
             < a'  e'  > 4.   
             < b'  e'  > 8   
             r 8  
             < b'  e'  > 2  ~   
             < b'  e'  > 8   
             \bar "|"  %{ end measure 49 %} 
             < c''  g'  > 1  ~   
             < c''  g'  > 4   
             \bar "||"  %{ end measure 50 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 51 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 52 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 53 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 54 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 55 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 56 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 57 %} 
             r 1  
             r 4  
             \bar "||"  %{ end measure 58 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 59 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 60 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 61 %} 
             g 1  ~  
             g 16.  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             f 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             e 16. ]  
             \bar "|"  %{ end measure 62 %} 
             d 4.  
             < c''  c'  > 2  ~   
             < c''  c'  > 8..   
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < b'  b  > 16   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < beses'  a  > 16.   
             \bar "|"  %{ end measure 63 %} 
             < aes'  gis  > 4.   
             < e'  e  > 2..   
             \bar "|"  %{ end measure 64 %} 
             < g'  c'  > 1  ~   
             < g'  c'  > 4   
             \bar "|"  %{ end measure 65 %} 
             < aes'  b  > 1  ~   
             < aes'  b  > 4   
             \bar "||"  %{ end measure 66 %} 
             \pageBreak
             < g'  ees'  > 2.   
             r 2  
             \bar "|"  %{ end measure 67 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 68 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 69 %} 
             r 1  
             e' 4  
             \bar "|"  %{ end measure 70 %} 
             f' 4.  
             g' 2..  
             \bar "|"  %{ end measure 71 %} 
             aes' 2  
             r 4  
             r 8  
             r 32  
             g' 8  ~  
             g' 32  
             r 32  
             f' 8  ~  
             f' 32  
             \bar "|"  %{ end measure 72 %} 
             < g'  d'  > 4   
             r 1  
             r 4  
             \bar "||"  %{ end measure 73 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 74 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 75 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 76 %} 
             g 1  ~  
             g 16.  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             g' 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             aes' 16. ]  
             \bar "|"  %{ end measure 77 %} 
             a' 1  ~  
             a' 16.  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             f' 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             fes' 16. ]  
             \bar "|"  %{ end measure 78 %} 
             ees' 4.  
             aes, 2..  
             \bar "|"  %{ end measure 79 %} 
             < ges'  d'  > 4.   
             < b'  fis'  > 8   
             r 2.  
             \bar "|"  %{ end measure 80 %} 
             < g'  d'  > 4.   
             < g'  c'  > 8   
             r 8  
             < c''  f'  > 2  ~   
             < c''  f'  > 8   
             \bar "||"  %{ end measure 81 %} 
             \time 3/4
             < d''  g'  > 4.   
             < b'  fis'  > 4.   
             \bar "|"  %{ end measure 82 %} 
             < bes'  ees'  > 4.   
             < ges'  des'  > 8   
             r 4  
             \bar "||"  %{ end measure 83 %} 
             \pageBreak
             \time 4/4
             < f'  c'  > 1   
             \bar "|"  %{ end measure 84 %} 
             r 1  
             \bar "|"  %{ end measure 85 %} 
             r 1  
             \bar "|"  %{ end measure 86 %} 
             r 1  
             \bar "|"  %{ end measure 87 %} 
             r 1  
             \bar "|"  %{ end measure 88 %} 
             r 1  
             \bar "|"  %{ end measure 89 %} 
             r 1  
             \bar "|"  %{ end measure 90 %} 
             r 1  
             \bar "||"  %{ end measure 91 %} 
             \pageBreak
             c' 2  ~  
             c' 8  ~  
             c' 32  
             bes 8  ~  
             bes 32  
             r 32  
             a 8  ~  
             a 32  
             \bar "|"  %{ end measure 92 %} 
             f 4.  ~  
             < a  f  > 2  ~   
             < a  f  > 8   
             \bar "|"  %{ end measure 93 %} 
             d' 2  ~  
             d' 8  ~  
             d' 32  
             c' 8  ~  
             c' 32  
             g 32  
             bes 8  ~  
             bes 32  
             \bar "|"  %{ end measure 94 %} 
             f' 1  
             \bar "|"  %{ end measure 95 %} 
             < c'  f,  > 2.  ~   
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             f, 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             g' 8 ]  
             \bar "|"  %{ end measure 96 %} 
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             a' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             d' 8 ]  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             cis' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             d' 2 ]  ~  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             d' 8 ]  
             \bar "|"  %{ end measure 97 %} 
             < f'  d'  > 4.   
             < d'  bes  > 2  ~   
             < d'  bes  > 8   
             \bar "|"  %{ end measure 98 %} 
             < a'  ges'  > 2..   
             < c''  f'  > 8   
             \bar "||"  %{ end measure 99 %} 
             \pageBreak
             < c''  f'  > 1   
             \bar "|"  %{ end measure 100 %} 
             r 1  
             \bar "|"  %{ end measure 101 %} 
             r 2..  
             aes' 8  
             \bar "|"  %{ end measure 102 %} 
             g' 4.  
             c'' 2  
             f'' 8  
             \bar "|"  %{ end measure 103 %} 
             f'' 8  
             ees'' 4.  
             d'' 4  
             c'' 4  
             \bar "|"  %{ end measure 104 %} 
             bes' 4.  
             < g'  d'  > 4.   
             r 8  
             < f'  c'  > 8   
             \bar "|"  %{ end measure 105 %} 
             < f'  c'  > 2..   
             a, 8  
             \bar "||"  %{ end measure 106 %} 
             \pageBreak
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             a, 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             b' 8 ]  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             a' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             e' 2 ]  ~  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             e' 8 ]  
             \bar "|"  %{ end measure 107 %} 
             r 4.  
             b 4  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             a' 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             b' 16 ]  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             a' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             e' 8 ]  
             \bar "|"  %{ end measure 108 %} 
             e' 4.  
             < g'  e'  > 2  ~   
             < g'  e'  > 8   
             \bar "|"  %{ end measure 109 %} 
             < g'  ees'  > 2   
             r 16.  
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             f' 16 [  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             g' 16. ]  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             f' 8 [  
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < c''  g'  > 8   
             \bar "|"  %{ end measure 110 %} 
             < c''  g'  > 8  ~   
             < c''  g'  > 32   
             a' 8  ~  
             a' 32  
             r 32  
             g' 8  ~  
             g' 32  
             < c''  a'  > 4.   
             < b'  fis'  > 8   
             \bar "|"  %{ end measure 111 %} 
             < b'  fis'  > 2   
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             aes, 8 [  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             b' 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             beses' 16 ]  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             aes' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             e'' 8 ]  
             \bar "|"  %{ end measure 112 %} 
             e'' 8  ~  
             e'' 32  
             d'' 8  ~  
             d'' 32  
             a, 32  
             c'' 8  ~  
             c'' 32  
             e' 8  ~  
             e' 32  
             d' 8  ~  
             d' 32  
             a, 32  
             c' 8  ~  
             c' 32  
             \bar "|"  %{ end measure 113 %} 
             b 4  
             g, 2.  
             \bar "||"  %{ end measure 114 %} 
             \pageBreak
             \time 5/4
             g' 4.  
             bes' 4.  
             f'' 4  
             ees'' 4  
             \bar "|"  %{ end measure 115 %} 
             d'' 4.  
             c'' 8  
             r 4  
             g' 2  
             \bar "|"  %{ end measure 116 %} 
             f' 4.  
             c' 2..  
             \bar "|"  %{ end measure 117 %} 
             b 2.  
             r 2  
             \bar "|"  %{ end measure 118 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 119 %} 
             < c''  g'  > 4.   
             < b'  f'  > 8   
             r 4.  
             < a'  e'  > 8   
             r 4  
             \bar "|"  %{ end measure 120 %} 
             < a'  f'  > 4   
             < c''  g'  > 1   
             \bar "||"  %{ end measure 121 %} 
             \pageBreak
             < b'  e'  > 1  ~   
             < b'  e'  > 4   
             \bar "|"  %{ end measure 122 %} 
             aes 4.  
             e' 2  ~  
             e' 8  
             r 4  
             \bar "|"  %{ end measure 123 %} 
             d' 4.  
             c' 8  
             r 8  
             e 2  ~  
             e 8  
             \bar "|"  %{ end measure 124 %} 
             e 2.  
             r 4  
             g 4  
             \bar "|"  %{ end measure 125 %} 
             a 1  ~  
             a 16.  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             g 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             f 16. ]  
             \bar "|"  %{ end measure 126 %} 
             e 4.  
             b 2  ~  
             b 8  
             r 4  
             \bar "|"  %{ end measure 127 %} 
             c' 4.  
             d' 8  
             r 8  
             e' 4.  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             a' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             b' 8 ]  
             \bar "||"  %{ end measure 128 %} 
             \pageBreak
             c'' 4.  
             g' 8  
             r 8  
             < f'  c'  > 2  ~   
             < f'  c'  > 8   
             \bar "|"  %{ end measure 129 %} 
             < e'  c'  > 1  ~   
             < e'  c'  > 4   
             \bar "|"  %{ end measure 130 %} 
             c' 4  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             b 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             g 8 ]  
             r 8  
             d 4...  
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             b' 16 [  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             a' 16. ]  
             \bar "|"  %{ end measure 131 %} 
             aes' 4.  
             e' 8  
             r 8  
             < b'  aes'  > 2  ~   
             < b'  aes'  > 8   
             \bar "|"  %{ end measure 132 %} 
             r 2  
             r 8  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             g' 8 [  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             a' 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             b' 8 ]  
             r 4  
             \bar "|"  %{ end measure 133 %} 
             < b'  e'  > 4.   
             < a'  e'  > 8   
             r 8  
             < b'  fis'  > 8   
             r 4.  
             e 8  
             \bar "|"  %{ end measure 134 %} 
             e 2.  
             r 4.  
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             aes' 16 [  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             a' 16 ]  
             \bar "|"  %{ end measure 135 %} 
             \pageBreak
             \time 4/4
             < b'  fis'  > 4   
             < a'  e'  > 4   
             < g'  d'  > 4   
             < fis'  cis'  > 4   
             \bar "|"  %{ end measure 136 %} 
             r 2..  
             \set stemRightBeamCount = #2
             \set stemRightBeamCount = #2
             < d''  d'  > 16   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < e''  e'  > 16   
             \bar "|"  %{ end measure 137 %} 
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < fis''  fis'  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < e''  e'  > 8   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < ees''  ees'  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < des''  des'  > 8   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < c''  c'  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < bes'  bes  > 8   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < aes'  aes  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < g'  g  > 8   
             \bar "|"  %{ end measure 138 %} 
             < fis'  d'  > 2.   
             r 8  
             \set stemRightBeamCount = #2
             \set stemRightBeamCount = #2
             < b'  b  > 16   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < c''  c'  > 16   
             \bar "|"  %{ end measure 139 %} 
             < d''  g'  > 4   
             < c''  f'  > 4   
             < e''  e'  > 4  ~   
             < c''  e'  > 4   
             \bar "|"  %{ end measure 140 %} 
             < b'  f'  > 4  ~   
             < b'  e'  > 2.   
             \bar "||"  %{ end measure 141 %} 
              } 
            
 
       \new Staff  = Reedsgy \with  { 
         \autoBeamOff 
          } 
          { \partial 32*16 
             \pageBreak
             \clef "bass" 
             \key d \major 
             \time 4/4
             r 4.  
             \set stemRightBeamCount = #2
             \set stemRightBeamCount = #2
             < ees'  ees  > 16   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < e'  e  > 16   
             \bar "|"  %{ end measure 0 %} 
             < b  aes  des  > 4   
             < a  ges  b,  > 4   
             < aes  f  bes,  > 4   
             < fis  e  a,  > 4   
             \bar "|"  %{ end measure 1 %} 
             r 2..  
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             a 16 [  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             b 16 ]  
             \bar "|"  %{ end measure 2 %} 
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < cis'  fis  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < b  fis  > 8   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < gis  e  > 8  ~   
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             e 8 ]  
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < gis  cis  > 4  ~   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < b  gis  cis  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < gis  cis  > 8   
             \bar "|"  %{ end measure 3 %} 
             < a  fis  g,  > 1   
             \bar "|"  %{ end measure 4 %} 
             < b  e  gis,  > 1   
             \bar "|"  %{ end measure 5 %} 
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < d'  a  f  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < d'  a  c  > 8  ~   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < d'  a  f,  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < d'  a  bes,  > 2  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < d'  a  bes,  > 8   
             \bar "|"  %{ end measure 6 %} 
             < d'  a  bes,  > 1   
             \bar "||"  %{ end measure 7 %} 
             \time 5/4
             r 1  
             r 4  
             \bar "|"  %{ end measure 8 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 9 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 10 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 11 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 12 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 13 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 14 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 15 %} 
             g 4.  ~  
             < g  e  > 2  ~   
             < g  e  > 8..   
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < a  e  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < b  e  > 16.   
             \bar "|"  %{ end measure 16 %} 
             < c'  fis  > 1  ~   
             < c'  fis  > 4   
             \bar "|"  %{ end measure 17 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 18 %} 
             r 1  
             r 4  
             \bar "||"  %{ end measure 19 %} 
             \pageBreak
             r 4.  
             c' 2  ~  
             c' 8..  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             b 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             a 16. ]  
             \bar "|"  %{ end measure 20 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 21 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 22 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 23 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 24 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 25 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 26 %} 
             r 1  
             r 4  
             \bar "||"  %{ end measure 27 %} 
             \pageBreak
             r 2.  
             c' 4  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             b 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             g 8 ]  
             \bar "|"  %{ end measure 28 %} 
             g 2.  
             r 4  
             r 16.  
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             b 16 [  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             c' 16. ]  
             \bar "|"  %{ end measure 29 %} 
             d' 4.  
             c' 8  
             r 4  
             e' 4  
             c' 4  
             \bar "|"  %{ end measure 30 %} 
             c' 2.  
             r 2  
             \bar "|"  %{ end measure 31 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 32 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 33 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 34 %} 
             r 1  
             r 8  
             aes 8  
             \bar "||"  %{ end measure 35 %} 
             \pageBreak
             g 4.  
             bes 4.  
             f' 4  
             ees' 4  
             \bar "|"  %{ end measure 36 %} 
             d' 4.  
             c' 8  
             r 4  
             g 2  
             \bar "|"  %{ end measure 37 %} 
             f 4.  
             c 2..  
             \bar "|"  %{ end measure 38 %} 
             < g  e  > 2.   
             r 2  
             \bar "|"  %{ end measure 39 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 40 %} 
             < c'  f  g,  > 2   
             r 4.  
             < c'  f  g,  > 8   
             r 4  
             \bar "|"  %{ end measure 41 %} 
             < d'  a  ces  > 4   
             < d'  aes  bes,  > 1   
             \bar "||"  %{ end measure 42 %} 
             \pageBreak
             < c'  g  > 1  ~   
             < c'  g  > 16.   
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < c'  b  g  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < c'  a  g  > 16.   
             \bar "|"  %{ end measure 43 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 44 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 45 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 46 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 47 %} 
             r 1  
             b 4  
             \bar "|"  %{ end measure 48 %} 
             < c'  g  > 2   
             r 8  
             < c'  g  > 2  ~   
             < c'  g  > 8   
             \bar "|"  %{ end measure 49 %} 
             < d'  aes  > 1  ~   
             < d'  aes  > 4   
             \bar "||"  %{ end measure 50 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 51 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 52 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 53 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 54 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 55 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 56 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 57 %} 
             r 1  
             r 4  
             \bar "||"  %{ end measure 58 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 59 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 60 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 61 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 62 %} 
             r 4.  
             < c'  f  > 2  ~   
             < c'  f  > 8..   
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < b  f  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < a  f  > 16.   
             \bar "|"  %{ end measure 63 %} 
             < gis  e  > 4.   
             e 2..  
             \bar "|"  %{ end measure 64 %} 
             < f  a,  > 1  ~   
             < f  a,  > 4   
             \bar "|"  %{ end measure 65 %} 
             < f  g,  > 1  ~   
             < f  g,  > 4   
             \bar "||"  %{ end measure 66 %} 
             \pageBreak
             < bes  c  > 2.   
             r 2  
             \bar "|"  %{ end measure 67 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 68 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 69 %} 
             r 1  
             e 4  
             \bar "|"  %{ end measure 70 %} 
             f 4.  
             g 2..  
             \bar "|"  %{ end measure 71 %} 
             aes 2  
             r 4  
             r 8  
             r 32  
             g 8  ~  
             g 32  
             r 32  
             f 8  ~  
             f 32  
             \bar "|"  %{ end measure 72 %} 
             < aes  bes,  > 4   
             r 1  
             r 4  
             \bar "||"  %{ end measure 73 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 74 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 75 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 76 %} 
             r 1  
             r 16.  
             \set stemRightBeamCount = #2
             \set stemRightBeamCount = #2
             < g'  g  > 16   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < gis'  ges  > 16.   
             \bar "|"  %{ end measure 77 %} 
             < a'  f  > 1  ~   
             < a'  f  > 16.   
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < f'  f  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < fes'  f  > 16.   
             \bar "|"  %{ end measure 78 %} 
             < ees'  e  > 4  ~   
             ees' 8  
             r 2..  
             \bar "|"  %{ end measure 79 %} 
             < b  a,  > 4.   
             < d'  a,  > 8   
             r 2.  
             \bar "|"  %{ end measure 80 %} 
             < aes  bes,  > 4.   
             < aes  d  > 8   
             r 8  
             < d'  aes  > 2  ~   
             < d'  aes  > 8   
             \bar "||"  %{ end measure 81 %} 
             \time 3/4
             < fis'  d'  > 4.   
             < d'  ces'  > 4.   
             \bar "|"  %{ end measure 82 %} 
             < des'  bes  > 4.   
             < b  ges  > 8   
             r 4  
             \bar "||"  %{ end measure 83 %} 
             \pageBreak
             \time 4/4
             < bes  f  > 1   
             \bar "|"  %{ end measure 84 %} 
             r 1  
             \bar "|"  %{ end measure 85 %} 
             r 1  
             \bar "|"  %{ end measure 86 %} 
             r 1  
             \bar "|"  %{ end measure 87 %} 
             r 1  
             \bar "|"  %{ end measure 88 %} 
             r 1  
             \bar "|"  %{ end measure 89 %} 
             r 1  
             \bar "|"  %{ end measure 90 %} 
             r 1  
             \bar "||"  %{ end measure 91 %} 
             \pageBreak
             r 1  
             \bar "|"  %{ end measure 92 %} 
             r 4.  
             f 2  ~  
             f 8  
             \bar "|"  %{ end measure 93 %} 
             g 2  ~  
             g 4  ~  
             g 16  
             r 32  
             g 8  ~  
             g 32  
             \bar "|"  %{ end measure 94 %} 
             f 4.  
             < f'  ges,  > 2  ~   
             < f'  ges,  > 8   
             \bar "|"  %{ end measure 95 %} 
             r 2..  
             < g'  f,  > 8   
             \bar "|"  %{ end measure 96 %} 
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             a' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             d' 8 ]  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             cis' 8 [  
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < d'  fis,  > 2  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < d'  fis,  > 8   
             \bar "|"  %{ end measure 97 %} 
             < bes  ees  g,  > 4.   
             < g  f  ees  > 2  ~   
             < g  f  ees  > 8   
             \bar "|"  %{ end measure 98 %} 
             < des'  a  f  > 4  ~   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < des'  a  ees  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < des'  a  f,  > 2   
             < des'  aes  bes,  > 8   
             \bar "||"  %{ end measure 99 %} 
             \pageBreak
             < des'  aes  bes,  > 1   
             \bar "|"  %{ end measure 100 %} 
             r 1  
             \bar "|"  %{ end measure 101 %} 
             r 2..  
             aes 8  
             \bar "|"  %{ end measure 102 %} 
             g 4.  
             c' 2  
             f' 8  
             \bar "|"  %{ end measure 103 %} 
             f' 8  
             ees' 4.  
             d' 4  
             c' 4  
             \bar "|"  %{ end measure 104 %} 
             bes 4.  
             < bes  g  ees  > 4.   
             r 8  
             < bes  ges  aes,  > 8   
             \bar "|"  %{ end measure 105 %} 
             < bes  ges  aes,  > 2..   
             r 8  
             \bar "||"  %{ end measure 106 %} 
             \pageBreak
             r 8  
             < b  a,  > 8  ~   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < a  a,  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < e  a,  > 2  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < e  a,  > 8   
             \bar "|"  %{ end measure 107 %} 
             r 2  
             r 8  
             \set stemRightBeamCount = #2
             \set stemRightBeamCount = #2
             < a'  b  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < b'  b  > 16  ~   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < a'  b  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < e'  c'  > 8   
             \bar "|"  %{ end measure 108 %} 
             < e'  c'  > 4.   
             < c'  f  d  > 2  ~   
             < c'  f  d  > 8   
             \bar "|"  %{ end measure 109 %} 
             < c'  bes  aes,  > 2   
             r 16.  
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             f' 16 [  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             g' 16. ]  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             f' 8 [  
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < e'  a  g,  > 8   
             \bar "|"  %{ end measure 110 %} 
             < e'  a  g,  > 8  ~   
             < e'  a  g,  > 32   
             a 8  ~  
             a 32  
             r 32  
             g 8  ~  
             g 32  
             < f'  c'  g,  > 4.   
             < b  e  aes,  > 8   
             \bar "|"  %{ end measure 111 %} 
             < b  e  aes,  > 2   
             r 8  
             \set stemRightBeamCount = #2
             \set stemRightBeamCount = #2
             < b  aes,  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < a  aes,  > 16  ~   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < gis  aes,  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < e'  a,  > 8   
             \bar "|"  %{ end measure 112 %} 
             < e'  a,  > 8  ~   
             < e'  a,  > 32   
             < d'  a,  > 8  ~   
             < d'  a,  > 32   
             r 32  
             < c'  a,  > 8  ~   
             < c'  a,  > 32   
             < e'  a,  > 8  ~   
             < e'  a,  > 32   
             < d'  a,  > 8  ~   
             < d'  a,  > 32   
             r 32  
             < c'  a,  > 8  ~   
             < c'  a,  > 32   
             \bar "|"  %{ end measure 113 %} 
             < b  g,  > 4   
             r 2.  
             \bar "||"  %{ end measure 114 %} 
             \pageBreak
             \time 5/4
             g 4.  
             bes 4.  
             f' 4  
             ees' 4  
             \bar "|"  %{ end measure 115 %} 
             d' 4.  
             c' 8  
             r 4  
             g 2  
             \bar "|"  %{ end measure 116 %} 
             f 4.  
             c 2..  
             \bar "|"  %{ end measure 117 %} 
             < g  e  c  > 2.   
             r 2  
             \bar "|"  %{ end measure 118 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 119 %} 
             < a  f  g,  > 2   
             r 4.  
             < c'  f  g,  > 8   
             r 4  
             \bar "|"  %{ end measure 120 %} 
             < d'  a  ces  > 4   
             < d'  aes  bes,  > 1   
             \bar "||"  %{ end measure 121 %} 
             \pageBreak
             < c'  g  > 1  ~   
             < c'  g  > 16.   
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < c'  b  g  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < c'  a  g  > 16.   
             \bar "|"  %{ end measure 122 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 123 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 124 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 125 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 126 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 127 %} 
             r 1  
             r 4  
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < e'  a  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < e'  b  > 8   
             \bar "||"  %{ end measure 128 %} 
             \pageBreak
             c' 4.  
             g 8  
             r 8  
             < aes  d  > 2  ~   
             < aes  d  > 8   
             \bar "|"  %{ end measure 129 %} 
             < b  g  > 1   
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             < b  a  g  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < b  g  > 8   
             \bar "|"  %{ end measure 130 %} 
             r 1  
             r 16.  
             \set stemRightBeamCount = #2
             \set stemRightBeamCount = #2
             < b  d  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < a  d  > 16.   
             \bar "|"  %{ end measure 131 %} 
             gis 4.  
             e 8  
             r 8  
             < a  des  > 2  ~   
             < a  des  > 8   
             \bar "|"  %{ end measure 132 %} 
             r 2  
             r 8  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             g 8 [  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             a 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             b 8 ]  
             r 4  
             \bar "|"  %{ end measure 133 %} 
             < cis'  a  e  > 2   
             r 8  
             < cis'  a  e  > 8   
             r 2  
             \bar "|"  %{ end measure 134 %} 
             r 1  
             r 8  
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             aes 16 [  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             a 16 ]  
             \bar "|"  %{ end measure 135 %} 
             \pageBreak
             \time 4/4
             < cis'  a  e  > 4   
             < b  g  d  > 4   
             < a  f  c  > 4   
             < gis  e  b,  > 4   
             \bar "|"  %{ end measure 136 %} 
             r 2..  
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             d' 16 [  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             e' 16 ]  
             \bar "|"  %{ end measure 137 %} 
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < fis'  b,  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < e'  b,  > 8   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < ees'  bes,  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < des'  bes,  > 8   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < c'  aes,  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < bes  aes,  > 8  ~   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < aes  aes,  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < g  aes,  > 8   
             \bar "|"  %{ end measure 138 %} 
             < b  fis  g,  > 2.   
             r 8  
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             b 16 [  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             c' 16 ]  
             \bar "|"  %{ end measure 139 %} 
             < e'  g  a,  > 4   
             < c'  f  g,  > 4   
             < c'  g  c  > 2   
             \bar "|"  %{ end measure 140 %} 
             < d'  b  g  > 1   
             \bar "||"  %{ end measure 141 %} 
              } 
            
 
       \new Staff  = Brassgx \with  { 
         \autoBeamOff 
          } 
          { \partial 32*16 
             \pageBreak
             \clef "treble" 
             \key d \major 
             \time 4/4
             r 2  
             \bar "|"  %{ end measure 0 %} 
             r 2..  
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             a' 16 [  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             b' 16 ]  
             \bar "|"  %{ end measure 1 %} 
             < cis''  a'  gis'  e'  > 4   
             < b'  aes'  e'  ees'  > 4   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < a'  e'  ees'  cis'  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < a'  fis'  ees'  cis'  > 8   
             < gis'  e'  dis'  b  > 4   
             \bar "|"  %{ end measure 2 %} 
             < gis'  e'  dis'  b  > 4  ~   
             < gis'  e'  dis'  cis'  b  a  > 4   
             < fis'  ees'  des'  b  gis  > 2   
             \bar "|"  %{ end measure 3 %} 
             < e'  cis'  b  a  fis  > 1   
             \bar "|"  %{ end measure 4 %} 
             < fis'  ees'  cis'  b  gis  fis  > 1   
             \bar "|"  %{ end measure 5 %} 
             < c''  g'  f'  e'  d'  a  > 1   
             \bar "|"  %{ end measure 6 %} 
             < c''  g'  f'  e'  d'  a  > 1   
             \bar "||"  %{ end measure 7 %} 
             \time 5/4
             r 1  
             r 4  
             \bar "|"  %{ end measure 8 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 9 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 10 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 11 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 12 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 13 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 14 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 15 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 16 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 17 %} 
             < g'  e'  > 4.  ~   
             < g'  e'  b  > 2  ~   
             < g'  e'  b  > 8..   
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < a'  f'  e'  b  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < b'  g'  e'  b  > 16.   
             \bar "|"  %{ end measure 18 %} 
             < c''  aes'  c'  g  > 1  ~   
             < c''  aes'  c'  g  > 4   
             \bar "||"  %{ end measure 19 %} 
             \pageBreak
             < b'  g'  e'  c'  g  > 1  ~   
             < b'  g'  e'  c'  g  > 4   
             \bar "|"  %{ end measure 20 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 21 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 22 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 23 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 24 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 25 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 26 %} 
             r 1  
             r 4  
             \bar "||"  %{ end measure 27 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 28 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 29 %} 
             r 1  
             f' 4  
             \bar "|"  %{ end measure 30 %} 
             g' 4.  
             f' 4.  
             c' 2  
             \bar "|"  %{ end measure 31 %} 
             c' 1  ~  
             c' 4  
             \bar "|"  %{ end measure 32 %} 
             r 4.  
             < aes'  b  > 2..   
             \bar "|"  %{ end measure 33 %} 
             < e'  c'  > 1  ~   
             < e'  c'  > 4   
             \bar "|"  %{ end measure 34 %} 
             < f'  b  > 1   
             r 4  
             \bar "||"  %{ end measure 35 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 36 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 37 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 38 %} 
             r 2  
             r 8  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             e' 8 [  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             a' 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             b' 4. ]  
             \bar "|"  %{ end measure 39 %} 
             < g'  e'  d'  c'  > 4.   
             < c''  g'  e'  c'  > 8   
             r 4  
             e'' 4  
             < d''  g'  e'  c'  > 4   
             \bar "|"  %{ end measure 40 %} 
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < e''  a'  e'  c'  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             < f''  a'  e'  c'  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             < g''  a'  e'  c'  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < e''  a'  e'  c'  > 8   
             r 8  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             f'' 8 [  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             c'' 8  
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < d''  a'  e'  c'  > 8   
             r 4  
             \bar "|"  %{ end measure 41 %} 
             < d''  a'  f'  d'  > 4   
             < e''  c''  aes'  g'  d'  > 1   
             \bar "||"  %{ end measure 42 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 43 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 44 %} 
             b' 1  ~  
             b' 16.  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             a' 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             g' 16. ]  
             \bar "|"  %{ end measure 45 %} 
             f' 4.  
             < g'  c'  > 4.   
             c' 4  ~  
             c' 16.  ~  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < dis'  c'  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < e'  c'  > 16.   
             \bar "|"  %{ end measure 46 %} 
             < f'  c'  > 4.  ~   
             < c''  f'  c'  > 2  ~   
             < c''  f'  c'  > 8..   
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < c''  g'  c'  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < c''  a'  c'  > 16.   
             \bar "|"  %{ end measure 47 %} 
             < b'  gis'  d'  > 4.  ~   
             < b'  e'  d'  > 2   
             r 8  
             < b'  gis'  e'  d'  b  > 4   
             \bar "|"  %{ end measure 48 %} 
             < c''  a'  g'  e'  c'  > 4.   
             < d''  b'  g'  e'  c'  > 8   
             r 8  
             < e''  b'  g'  e'  c'  > 2  ~   
             < e''  b'  g'  e'  c'  > 8   
             \bar "|"  %{ end measure 49 %} 
             < e''  c''  aes'  g'  d'  > 1  ~   
             < e''  c''  aes'  g'  d'  > 4   
             \bar "||"  %{ end measure 50 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 51 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 52 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 53 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 54 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 55 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 56 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 57 %} 
             r 1  
             r 4  
             \bar "||"  %{ end measure 58 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 59 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 60 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 61 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 62 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 63 %} 
             b 4.  ~  
             < d'  b  > 2..   
             \bar "|"  %{ end measure 64 %} 
             < e'  c'  a  > 1  ~   
             < e'  c'  a  > 4   
             \bar "|"  %{ end measure 65 %} 
             < aes'  ees'  b  aes  f  > 4.  ~   
             < ees''  aes'  ees'  b  aes  f  > 2..   
             \bar "||"  %{ end measure 66 %} 
             \pageBreak
             < f''  c''  g'  ees'  bes  > 2.   
             r 2  
             \bar "|"  %{ end measure 67 %} 
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < c''  g'  ees'  c'  a  > 4   
             r 8  
             < c''  g'  ees'  c'  a  > 8   
             r 2  
             r 8  
             < c''  g'  ees'  c'  a  > 8   
             \bar "|"  %{ end measure 68 %} 
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < bes'  f'  c'  bes  g  > 4   
             r 8  
             < bes'  f'  c'  bes  g  > 8   
             r 2  
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < bes'  f'  c'  bes  g  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < c''  g'  ees'  c'  ais  > 8   
             \bar "|"  %{ end measure 69 %} 
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < d''  g'  e'  d'  b  > 4   
             r 8  
             < d''  g'  e'  d'  b  > 8   
             r 2  
             < d''  b'  g'  e'  > 4   
             \bar "|"  %{ end measure 70 %} 
             < e''  c''  a'  g'  > 2   
             r 2.  
             \bar "|"  %{ end measure 71 %} 
             < f''  d''  aes'  ees'  b  aes  > 2   
             r 2.  
             \bar "|"  %{ end measure 72 %} 
             < e''  c''  aes'  g'  d'  c'  > 4.   
             < g''  e''  c''  aes'  g'  e'  > 2..   
             \bar "||"  %{ end measure 73 %} 
             \pageBreak
             < g''  d''  b'  g'  e'  c'  > 1  ~   
             < g''  d''  b'  g'  e'  c'  > 4   
             \bar "|"  %{ end measure 74 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 75 %} 
             d' 1  ~  
             d' 16.  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             e' 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             f' 16. ]  
             \bar "|"  %{ end measure 76 %} 
             < g'  e'  > 1   
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             e' 16. [  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #UP 
             d' 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #UP 
             des' 16. ]  
             \bar "|"  %{ end measure 77 %} 
             < a'  f'  c'  > 1  ~   
             < a'  f'  c'  > 4   
             \bar "|"  %{ end measure 78 %} 
             < b'  gis'  dis'  b  > 4.   
             r 2..  
             \bar "|"  %{ end measure 79 %} 
             < b'  g'  ges'  e'  d'  b  > 2   
             r 2.  
             \bar "|"  %{ end measure 80 %} 
             < d''  bes'  aes'  g'  d'  c'  > 4.   
             < e''  c''  aes'  g'  d'  c'  > 8   
             r 8  
             < g''  e''  c''  aes'  f'  d'  > 2  ~   
             < g''  e''  c''  aes'  f'  d'  > 8   
             \bar "||"  %{ end measure 81 %} 
             \time 3/4
             < fis''  d''  b'  g'  d'  b  > 4.  ~   
             < d''  b'  a'  ges'  d'  b  > 4.   
             \bar "|"  %{ end measure 82 %} 
             < des''  bes'  fis'  ees'  des'  bes  > 4.   
             < b'  fis'  ees'  des'  c'  bes  > 8   
             r 4  
             \bar "||"  %{ end measure 83 %} 
             \pageBreak
             \time 4/4
             < bes'  f'  d'  c'  bes  a  > 1   
             \bar "|"  %{ end measure 84 %} 
             r 1  
             \bar "|"  %{ end measure 85 %} 
             r 1  
             \bar "|"  %{ end measure 86 %} 
             r 1  
             \bar "|"  %{ end measure 87 %} 
             r 1  
             \bar "|"  %{ end measure 88 %} 
             r 1  
             \bar "|"  %{ end measure 89 %} 
             r 1  
             \bar "|"  %{ end measure 90 %} 
             r 1  
             \bar "||"  %{ end measure 91 %} 
             \pageBreak
             c'' 2  ~  
             c'' 8  ~  
             c'' 32  
             bes' 8  ~  
             bes' 32  
             r 32  
             a' 8  ~  
             a' 32  
             \bar "|"  %{ end measure 92 %} 
             f' 1  
             \bar "|"  %{ end measure 93 %} 
             < d''  d'  > 2  ~   
             < d''  d'  > 8  ~   
             < d''  d'  > 32   
             < c''  c'  > 8  ~   
             < c''  c'  > 32   
             r 32  
             < bes'  bes  > 8  ~   
             < bes'  bes  > 32   
             \bar "|"  %{ end measure 94 %} 
             < f''  f'  c'  > 4  ~   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < ees''  f'  c'  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < bes'  f'  c'  > 4.  ~   
             bes' 4  
             \bar "|"  %{ end measure 95 %} 
             < d''  bes'  g'  f'  c'  bes  > 1   
             \bar "|"  %{ end measure 96 %} 
             r 1  
             \bar "|"  %{ end measure 97 %} 
             r 4.  
             < d''  d'  > 4  ~   
             < d''  d'  > 32   
             < ees''  ees'  > 8  ~   
             < ees''  ees'  > 32   
             r 32  
             < f''  f'  > 8  ~   
             < f''  f'  > 32   
             \bar "|"  %{ end measure 98 %} 
             < ges''  des''  a'  ges'  > 2..   
             < f''  c''  f'  ees'  des'  c'  > 8   
             \bar "||"  %{ end measure 99 %} 
             \pageBreak
             < f''  c''  f'  ees'  des'  c'  > 1   
             \bar "|"  %{ end measure 100 %} 
             r 4.  
             < f''  des''  c''  bes'  des'  > 8   
             r 4  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             des' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             bes 8 ]  
             \bar "|"  %{ end measure 101 %} 
             bes 1  
             \bar "|"  %{ end measure 102 %} 
             < g'  d'  > 2   
             r 4  
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < g'  d'  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < bes'  g'  f'  ees'  d'  > 8   
             \bar "|"  %{ end measure 103 %} 
             < bes'  g'  f'  ees'  d'  > 1   
             \bar "|"  %{ end measure 104 %} 
             < d''  bes'  g'  ees'  d'  > 2   
             r 8  
             < d''  bes'  g'  ees'  > 8   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < ees''  c''  a'  f'  ees'  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < f''  d''  bes'  fis'  c'  > 8   
             \bar "|"  %{ end measure 105 %} 
             < f''  d''  bes'  fis'  c'  > 2..   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < g''  c''  b'  g'  c'  > 8   
             \bar "||"  %{ end measure 106 %} 
             \pageBreak
             r 4.  
             < e''  b'  e'  > 4  ~   
             < e''  b'  e'  > 32   
             < e''  a'  d'  > 8  ~   
             < e''  a'  d'  > 32  ~   
             e'' 32  ~  
             < e''  g'  c'  > 8  ~   
             < e''  g'  c'  > 32   
             \bar "|"  %{ end measure 107 %} 
             < a''  d''  a'  e'  > 4.  ~   
             < a''  d''  a'  g'  e'  > 8  ~   
             < a''  a'  > 4.   
             < c'''  c''  > 8   
             \bar "|"  %{ end measure 108 %} 
             < c'''  c''  > 4  ~   
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             c''' 8 [  ~  
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < c'''  g''  g'  > 4  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < c'''  g''  g'  > 32  ~   
             < c'''  f''  f'  > 8  ~   
             < c'''  f''  f'  > 32  ~   
             c''' 32  ~  
             < c'''  e''  e'  > 8  ~   
             < c'''  e''  e'  > 32   
             \bar "|"  %{ end measure 109 %} 
             < f''  c''  g'  ees'  c'  > 2   
             r 4  
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < c''  bes'  g'  ees'  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < e''  c''  g'  e'  c'  a  > 8   
             \bar "|"  %{ end measure 110 %} 
             < e''  c''  g'  e'  c'  a  > 2  ~   
             < e''  c''  g'  e'  > 8  ~   
             < e''  c''  g'  f'  e'  c'  > 4   
             < ces''  fis'  ees'  b  > 8   
             \bar "|"  %{ end measure 111 %} 
             < ces''  fis'  ees'  b  > 8  ~   
             < ces''  fis'  ees'  b  > 32   
             < des''  fis'  ees'  b  > 8  ~   
             < des''  fis'  ees'  b  > 32   
             < fis'  ees'  b  > 32  ~   
             < ees''  fis'  ees'  b  > 8  ~   
             < ees''  fis'  ees'  b  > 32   
             < fis''  b'  fis'  ees'  b  > 4.   
             < g''  e''  g'  f'  e'  c'  > 8   
             \bar "|"  %{ end measure 112 %} 
             < g''  e''  g'  f'  e'  c'  > 8  ~   
             < g''  e''  g'  f'  e'  c'  > 32  ~   
             < g''  d''  g'  f'  e'  c'  > 8  ~   
             < g''  d''  g'  f'  e'  c'  > 32  ~   
             < g''  g'  f'  e'  c'  > 32  ~   
             < g''  c''  g'  f'  e'  c'  > 8  ~   
             < g''  c''  g'  f'  e'  c'  > 32  ~   
             < g''  e''  g'  f'  e'  c'  > 2   
             \bar "|"  %{ end measure 113 %} 
             < ees''  b'  bes'  f'  ees'  b  > 8  ~   
             < ees''  b'  bes'  f'  ees'  b  > 32   
             < f''  des''  ces''  aes'  ees'  b  > 8  ~   
             < f''  des''  ces''  aes'  ees'  b  > 32   
             < ees'  b  > 32  ~   
             < g''  ees''  des''  b'  ees'  b  > 8  ~   
             < g''  ees''  des''  b'  ees'  b  > 32   
             < aes''  f''  ees''  cis''  ees'  b  > 8  ~   
             < aes''  f''  ees''  cis''  ees'  b  > 32   
             < bes''  g''  f''  b'  ees'  b  > 8  ~   
             < bes''  g''  f''  b'  ees'  b  > 32   
             \set stemRightBeamCount = #3
             \set stemRightBeamCount = #3
             < ees'  b  > 32  ~   
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #1
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #1
             < b''  gis''  ees''  cis''  ees'  b  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < cis'''  a''  fis''  d''  ees'  b  > 16.   
             \bar "||"  %{ end measure 114 %} 
             \pageBreak
             \time 5/4
             < d'''  bes''  g''  ees''  d'  bes  > 1  ~   
             < d'''  bes''  g''  ees''  d'  bes  > 4   
             \bar "|"  %{ end measure 115 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 116 %} 
             r 1  
             f' 4  
             \bar "|"  %{ end measure 117 %} 
             e' 4.  
             b 4  ~  
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < e'  b  > 8   
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             < a'  b  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < b'  b  > 4.   
             \bar "|"  %{ end measure 118 %} 
             < g'  e'  d'  c'  f  > 4.   
             < c''  g'  e'  c'  f  > 8   
             r 4  
             e'' 4  
             < d''  g'  e'  c'  f  > 4   
             \bar "|"  %{ end measure 119 %} 
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < e''  a'  e'  c'  f  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             < f''  a'  e'  c'  f  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             < g''  a'  e'  c'  f  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < e''  a'  e'  c'  f  > 8   
             r 8  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             f'' 8 [  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             c'' 8  
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < d''  a'  e'  c'  f  > 8   
             r 4  
             \bar "|"  %{ end measure 120 %} 
             < d''  a'  f'  d'  a  > 4   
             < e''  c''  g'  d'  aes  > 1   
             \bar "||"  %{ end measure 121 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 122 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 123 %} 
             < b'  g'  > 1  ~   
             < b'  g'  > 16.   
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < c''  a'  > 16   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < d''  g'  > 16.   
             \bar "|"  %{ end measure 124 %} 
             < e''  e'  > 4.   
             < c''  c'  > 8  ~   
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             c' 8 [  ~  
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < g'  c'  > 4...   
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < g'  c'  ces'  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < g'  c'  bes  > 16.   
             \bar "|"  %{ end measure 125 %} 
             < c''  a'  e'  c'  a  > 4.  ~   
             < c''  a'  g'  e'  c'  > 2  ~   
             < c''  a'  g'  e'  c'  > 8..   
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < b'  g'  e'  c'  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < a'  g'  f'  e'  c'  > 16.   
             \bar "|"  %{ end measure 126 %} 
             < gis'  e'  d'  > 2..   
             r 8  
             < b'  gis'  d'  b  > 4   
             \bar "|"  %{ end measure 127 %} 
             < c''  a'  g'  e'  c'  > 4.   
             < d''  b'  g'  e'  c'  > 8   
             r 8  
             < e''  b'  g'  e'  c'  > 2  ~   
             < e''  b'  g'  e'  c'  > 8   
             \bar "||"  %{ end measure 128 %} 
             \pageBreak
             < f''  c''  aes'  g'  d'  > 1  ~   
             < f''  c''  aes'  g'  d'  > 4   
             \bar "|"  %{ end measure 129 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 130 %} 
             r 2  
             r 8  
             < e'  c'  > 2  ~   
             < e'  c'  > 8   
             \bar "|"  %{ end measure 131 %} 
             < gis'  e'  > 2  ~   
             < gis'  e'  > 8  ~   
             < b'  gis'  e'  > 4...   
             \set stemRightBeamCount = #2
             \set stemRightBeamCount = #2
             < ees''  b'  gis'  e'  ees'  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < e''  b'  gis'  e'  > 16.   
             \bar "|"  %{ end measure 132 %} 
             < b''  e''  d''  g'  e'  b  > 4.   
             < a''  e''  d''  a'  e'  b  > 8   
             r 8  
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < g''  g'  > 8   
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             < a''  a'  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < b''  b'  > 8   
             r 4  
             \bar "|"  %{ end measure 133 %} 
             < gis''  e''  cis''  b'  gis'  e'  > 4.   
             < a''  e''  cis''  a'  e'  > 8   
             r 8  
             < b''  fis''  cis''  gis'  e'  > 8   
             r 4.  
             < d''  a'  fis'  e'  d'  b  > 8   
             \bar "|"  %{ end measure 134 %} 
             < d''  a'  fis'  e'  d'  b  > 1  ~   
             < d''  a'  fis'  e'  d'  b  > 4   
             \bar "|"  %{ end measure 135 %} 
             \pageBreak
             \time 4/4
             r 2..  
             \set stemRightBeamCount = #2
             \set stemRightBeamCount = #2
             < d''  d'  > 16   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < e''  e'  > 16   
             \bar "|"  %{ end measure 136 %} 
             < fis''  d''  cis''  a'  > 4   
             < e''  b'  a'  fis'  > 4   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < d''  a'  fis'  e'  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < d''  b'  fis'  e'  > 8   
             < cis''  a'  fis'  d'  > 4   
             \bar "|"  %{ end measure 137 %} 
             < cis''  a'  fis'  d'  cis'  b  > 4   
             < c''  aes'  f'  des'  c'  bes  > 4   
             < bes'  g'  ees'  c'  bes  > 2   
             \bar "|"  %{ end measure 138 %} 
             < a'  fis'  e'  d'  b  fis  > 2.   
             r 8  
             \set stemRightBeamCount = #2
             \set stemRightBeamCount = #2
             < b'  b  > 16   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < c''  c'  > 16   
             \bar "|"  %{ end measure 139 %} 
             < d''  a'  g'  e'  d'  c'  > 4   
             < c''  g'  f'  c'  a  g  > 4   
             < e''  g'  e'  c'  bes  g  > 4  ~   
             < c''  g'  e'  c'  bes  g  > 4   
             \bar "|"  %{ end measure 140 %} 
             < b'  g'  f'  d'  b  f  > 4  ~   
             < b'  g'  e'  d'  b  e  > 2.   
             \bar "||"  %{ end measure 141 %} 
              } 
            
 
       \new Staff  = Brassgy \with  { 
         \autoBeamOff 
          } 
          { \partial 32*16 
             \pageBreak
             \clef "bass" 
             \key d \major 
             \time 4/4
             r 2  
             \bar "|"  %{ end measure 0 %} 
             r 1  
             \bar "|"  %{ end measure 1 %} 
             r 1  
             \bar "|"  %{ end measure 2 %} 
             < fis  cis  > 4   
             < e  b,  > 4   
             < cis  fis,  > 2   
             \bar "|"  %{ end measure 3 %} 
             < e  g,  > 1   
             \bar "|"  %{ end measure 4 %} 
             < e  gis,  > 1   
             \bar "|"  %{ end measure 5 %} 
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             f 8 [  ~  
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < f  c  > 8  ~   
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < f  f,  > 8  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < f  bes,,  > 2  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < f  bes,,  > 8   
             \bar "|"  %{ end measure 6 %} 
             < f  bes,,  > 1   
             \bar "||"  %{ end measure 7 %} 
             \time 5/4
             r 1  
             r 4  
             \bar "|"  %{ end measure 8 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 9 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 10 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 11 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 12 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 13 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 14 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 15 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 16 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 17 %} 
             r 4.  
             c 2..  
             \bar "|"  %{ end measure 18 %} 
             gis, 1  ~  
             gis, 4  
             \bar "||"  %{ end measure 19 %} 
             \pageBreak
             a, 4.  ~  
             < c'  a,  > 2  ~   
             < c'  a,  > 8..   
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             < b  a,  > 16  ~   
             \set stemLeftBeamCount = #2
             \set stemLeftBeamCount = #2
             < a  a,  > 16.   
             \bar "|"  %{ end measure 20 %} 
             gis 4.  
             e' 2..  
             \bar "|"  %{ end measure 21 %} 
             d' 4.  
             c' 8  
             r 8  
             e 2  ~  
             e 8  
             \bar "|"  %{ end measure 22 %} 
             e 2.  
             r 4  
             g 4  
             \bar "|"  %{ end measure 23 %} 
             a 1  ~  
             a 16.  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             g 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             f 16. ]  
             \bar "|"  %{ end measure 24 %} 
             e 4.  
             b 2..  
             \bar "|"  %{ end measure 25 %} 
             c' 4.  
             d' 8  
             r 8  
             e' 2  ~  
             e' 8  
             \bar "|"  %{ end measure 26 %} 
             e' 2  
             r 2.  
             \bar "||"  %{ end measure 27 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 28 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 29 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 30 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 31 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 32 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 33 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 34 %} 
             r 1  
             r 8  
             aes 8  
             \bar "||"  %{ end measure 35 %} 
             \pageBreak
             g 4.  
             bes 4.  
             f' 4  
             ees' 4  
             \bar "|"  %{ end measure 36 %} 
             d' 4.  
             c' 8  
             r 4  
             g 2  
             \bar "|"  %{ end measure 37 %} 
             f 4.  
             c 2..  
             \bar "|"  %{ end measure 38 %} 
             c 2.  
             r 2  
             \bar "|"  %{ end measure 39 %} 
             < f  d  > 2   
             r 2  
             < f  d  > 4   
             \bar "|"  %{ end measure 40 %} 
             < f  g,  > 2   
             r 4.  
             < f  g,  > 8   
             r 4  
             \bar "|"  %{ end measure 41 %} 
             < a  b,  > 4   
             < aes  bes,  > 1   
             \bar "||"  %{ end measure 42 %} 
             \pageBreak
             r 4.  
             c' 2  ~  
             c' 8..  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             b 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             a 16. ]  
             \bar "|"  %{ end measure 43 %} 
             gis 4.  
             e' 2..  
             \bar "|"  %{ end measure 44 %} 
             d' 4.  
             c' 8  
             r 8  
             e 2  ~  
             e 8  
             \bar "|"  %{ end measure 45 %} 
             r 1  
             g 4  
             \bar "|"  %{ end measure 46 %} 
             a 1  ~  
             a 16.  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             g 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             f 16. ]  
             \bar "|"  %{ end measure 47 %} 
             e 4.  
             b 2  ~  
             b 8  
             < e  gis,  > 4   
             \bar "|"  %{ end measure 48 %} 
             < g  a,  > 2   
             r 8  
             < g  a,  > 2  ~   
             < g  a,  > 8   
             \bar "|"  %{ end measure 49 %} 
             < aes  bes,  > 1  ~   
             < aes  bes,  > 4   
             \bar "||"  %{ end measure 50 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 51 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 52 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 53 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 54 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 55 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 56 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 57 %} 
             r 1  
             r 4  
             \bar "||"  %{ end measure 58 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 59 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 60 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 61 %} 
             g 1  ~  
             g 16.  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             f 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             e 16. ]  
             \bar "|"  %{ end measure 62 %} 
             d 4.  
             g, 2..  
             \bar "|"  %{ end measure 63 %} 
             gis, 1  ~  
             gis, 4  
             \bar "|"  %{ end measure 64 %} 
             a, 1  ~  
             a, 4  
             \bar "|"  %{ end measure 65 %} 
             g, 1  ~  
             g, 4  
             \bar "||"  %{ end measure 66 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 67 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 68 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 69 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 70 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 71 %} 
             < f  g,  > 2   
             r 2.  
             \bar "|"  %{ end measure 72 %} 
             < aes  bes,  > 4.   
             < d'  bes,  > 2..   
             \bar "||"  %{ end measure 73 %} 
             \pageBreak
             < g  a,  > 1  ~   
             < g  a,  > 4   
             \bar "|"  %{ end measure 74 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 75 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 76 %} 
             g 1  ~  
             g 8  ~  
             g 32  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             ges 16. ]  
             \bar "|"  %{ end measure 77 %} 
             f 1  ~  
             f 4  
             \bar "|"  %{ end measure 78 %} 
             e 4.  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             gis, 2.. ]  
             \bar "|"  %{ end measure 79 %} 
             < g  a,  > 2   
             r 2.  
             \bar "|"  %{ end measure 80 %} 
             < aes  bes,  > 2   
             r 8  
             < c'  bes,  > 2  ~   
             < c'  bes,  > 8   
             \bar "||"  %{ end measure 81 %} 
             \time 3/4
             < g  a,  > 2.   
             \bar "|"  %{ end measure 82 %} 
             < ges  aes,  > 2   
             r 4  
             \bar "||"  %{ end measure 83 %} 
             \pageBreak
             \time 4/4
             < f  g,  > 1   
             \bar "|"  %{ end measure 84 %} 
             r 1  
             \bar "|"  %{ end measure 85 %} 
             r 1  
             \bar "|"  %{ end measure 86 %} 
             r 1  
             \bar "|"  %{ end measure 87 %} 
             r 1  
             \bar "|"  %{ end measure 88 %} 
             r 1  
             \bar "|"  %{ end measure 89 %} 
             r 1  
             \bar "|"  %{ end measure 90 %} 
             r 1  
             \bar "||"  %{ end measure 91 %} 
             \pageBreak
             r 1  
             \bar "|"  %{ end measure 92 %} 
             r 4.  
             a 2  ~  
             a 8  
             \bar "|"  %{ end measure 93 %} 
             g 1  
             \bar "|"  %{ end measure 94 %} 
             f 4.  
             < f  ges,  > 2  ~   
             < f  ges,  > 8   
             \bar "|"  %{ end measure 95 %} 
             < ees  f,  > 1   
             \bar "|"  %{ end measure 96 %} 
             r 4.  
             fis, 2  ~  
             fis, 8  
             \bar "|"  %{ end measure 97 %} 
             g, 4.  
             ees 2  ~  
             ees 8  
             \bar "|"  %{ end measure 98 %} 
             f 4  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             ees 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             f, 2 ]  
             < aes  bes,  > 8   
             \bar "||"  %{ end measure 99 %} 
             \pageBreak
             < aes  bes,  > 1   
             \bar "|"  %{ end measure 100 %} 
             r 4.  
             < f  g,  > 8   
             r 4  
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < f  g,  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < f  ges,  > 8   
             \bar "|"  %{ end measure 101 %} 
             < f  ges,  > 1   
             \bar "|"  %{ end measure 102 %} 
             < a  bes,  > 2   
             r 4  
             \set stemRightBeamCount = #1
             \set stemRightBeamCount = #1
             < a  bes,  > 8   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < bes  c  > 8   
             \bar "|"  %{ end measure 103 %} 
             < bes  c  > 1   
             \bar "|"  %{ end measure 104 %} 
             < bes  f,  > 2   
             r 8  
             < bes  f,  > 4   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < ges  aes,  > 8   
             \bar "|"  %{ end measure 105 %} 
             < ges  aes,  > 2..   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < g  a,  > 8   
             \bar "||"  %{ end measure 106 %} 
             \pageBreak
             a, 1  
             \bar "|"  %{ end measure 107 %} 
             r 4.  
             < b  c  > 2   
             < c'  d  > 8   
             \bar "|"  %{ end measure 108 %} 
             < c'  d  > 4.   
             < f  d,  > 2  ~   
             < f  d,  > 8   
             \bar "|"  %{ end measure 109 %} 
             < g  aes,  > 2   
             r 4.  
             < f  g,  > 8   
             \bar "|"  %{ end measure 110 %} 
             < f  g,  > 2   
             r 8  
             < a  g,  > 4   
             < e  gis,  > 8   
             \bar "|"  %{ end measure 111 %} 
             < e  gis,  > 2..   
             < f  a,  > 8   
             \bar "|"  %{ end measure 112 %} 
             < f  a,  > 1   
             \bar "|"  %{ end measure 113 %} 
             < f  g,  > 1   
             \bar "||"  %{ end measure 114 %} 
             \pageBreak
             \time 5/4
             < ees  c,  > 1  ~   
             < ees  c,  > 4   
             \bar "|"  %{ end measure 115 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 116 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 117 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 118 %} 
             d 2  
             r 2  
             d 4  
             \bar "|"  %{ end measure 119 %} 
             g, 2  
             r 4.  
             g, 8  
             r 4  
             \bar "|"  %{ end measure 120 %} 
             b, 4  
             bes, 1  
             \bar "||"  %{ end measure 121 %} 
             \pageBreak
             r 4.  
             c' 2  ~  
             c' 8..  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             b 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             a 16. ]  
             \bar "|"  %{ end measure 122 %} 
             gis 4.  
             e' 2  ~  
             e' 8  
             r 4  
             \bar "|"  %{ end measure 123 %} 
             d' 4.  
             c' 8  
             r 8  
             e 2  ~  
             e 8  
             \bar "|"  %{ end measure 124 %} 
             e 2.  
             r 4  
             g 4  
             \bar "|"  %{ end measure 125 %} 
             a 1  ~  
             a 16.  
             \set stemLeftBeamCount = #2
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             g 16  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             f 16. ]  
             \bar "|"  %{ end measure 126 %} 
             e 4.  
             b 2  ~  
             b 8  
             < e  gis,  > 4   
             \bar "|"  %{ end measure 127 %} 
             < g  a,  > 2   
             r 8  
             < g  a,  > 2  ~   
             < g  a,  > 8   
             \bar "||"  %{ end measure 128 %} 
             \pageBreak
             < aes  bes,  > 1  ~   
             < aes  bes,  > 4   
             \bar "|"  %{ end measure 129 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 130 %} 
             r 2  
             r 8  
             g 2  ~  
             g 8  
             \bar "|"  %{ end measure 131 %} 
             < a  cis  > 1  ~   
             < a  cis  > 4   
             \bar "|"  %{ end measure 132 %} 
             < g  c  > 2   
             r 2.  
             \bar "|"  %{ end measure 133 %} 
             < a  b,  > 2   
             r 8  
             < a  b,  > 8   
             r 4.  
             < e  c,  > 8   
             \bar "|"  %{ end measure 134 %} 
             < e  c,  > 1  ~   
             < e  c,  > 4   
             \bar "|"  %{ end measure 135 %} 
             \pageBreak
             \time 4/4
             r 1  
             \bar "|"  %{ end measure 136 %} 
             r 1  
             \bar "|"  %{ end measure 137 %} 
             < a  b,  > 4   
             < aes  bes,  > 4   
             < g  aes,  > 2   
             \bar "|"  %{ end measure 138 %} 
             < d  g,  > 2.   
             r 4  
             \bar "|"  %{ end measure 139 %} 
             < g  a,  > 4   
             < f  g,  > 4   
             < c  aes,,  > 2   
             \bar "|"  %{ end measure 140 %} 
             < g,  c,  > 1   
             \bar "||"  %{ end measure 141 %} 
              } 
            
 
       \new Staff  = Guitar \with  { 
         \autoBeamOff 
          } 
          { \partial 32*16 
             \pageBreak
             \clef "treble" 
             \key c \major 
             \time 4/4
             r 2  
             \bar "|"  %{ end measure 0 %} 
             r 1  
             \bar "|"  %{ end measure 1 %} 
             r 1  
             \bar "|"  %{ end measure 2 %} 
             r 1  
             \bar "|"  %{ end measure 3 %} 
             r 1  
             \bar "|"  %{ end measure 4 %} 
             r 1  
             \bar "|"  %{ end measure 5 %} 
             r 1  
             \bar "|"  %{ end measure 6 %} 
             r 1  
             \bar "||"  %{ end measure 7 %} 
             \time 5/4
             r 1  
             r 4  
             \bar "|"  %{ end measure 8 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 9 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 10 %} 
             r 4  
             r 8  
             \once \override Stem.direction = #DOWN 
             e''' 4  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             c''' 8 ]  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             aes'' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             g'' 8 ]  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             e'' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             c'' 8 ]  
             \bar "|"  %{ end measure 11 %} 
             \pageBreak
             \once \override Stem.direction = #DOWN 
             b' 4.  
             \once \override Stem.direction = #DOWN 
             a'' 8  
             r 8  
             < b'  e''  b''  > 2  ~   
             < b'  e''  b''  > 8  ~   
             \bar "|"  %{ end measure 12 %} 
             < b'  e''  b''  > 1  ~   
             < b'  e''  b''  > 4   
             \bar "|"  %{ end measure 13 %} 
             < c''  g''  c'''  > 1  ~   
             < c''  g''  c'''  > 4  ~   
             \bar "|"  %{ end measure 14 %} 
             < c''  g''  c'''  > 1  ~   
             < c''  g''  c'''  > 4   
             \bar "|"  %{ end measure 15 %} 
             \once \override Stem.direction = #DOWN 
             b'' \breve  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             a'' 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             g'' 8 ]  
             \bar "|"  %{ end measure 16 %} 
             \once \override Stem.direction = #DOWN 
             e'' 1  ~  
             \once \override Stem.direction = #DOWN 
             e'' 4  ~  
             \bar "|"  %{ end measure 17 %} 
             \once \override Stem.direction = #DOWN 
             e'' 1  ~  
             \once \override Stem.direction = #DOWN 
             e'' 4  
             \bar "|"  %{ end measure 18 %} 
             r 1  
             r 4  
             \bar "||"  %{ end measure 19 %} 
             \pageBreak
             < c''  g''  a''  d'''  > 1  ~   
             < c''  g''  a''  d'''  > 4   
             \bar "|"  %{ end measure 20 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 21 %} 
             < g'  d''  g''  b''  > 1  ~   
             < g'  d''  g''  b''  > 4   
             \bar "|"  %{ end measure 22 %} 
             r 2.  
             r 4  
             \once \override Stem.direction = #UP 
             g' 4  
             \bar "|"  %{ end measure 23 %} 
             \once \override Stem.direction = #UP 
             a' \breve  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             g' 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             f' 8 ]  
             \bar "|"  %{ end measure 24 %} 
             \once \override Stem.direction = #UP 
             e' 4.  
             \once \override Stem.direction = #DOWN 
             b' 2..  
             \bar "|"  %{ end measure 25 %} 
             \once \override Stem.direction = #DOWN 
             c'' 4.  
             \once \override Stem.direction = #DOWN 
             d'' 8  
             r 8  
             \once \override Stem.direction = #DOWN 
             e'' 2  ~  
             \once \override Stem.direction = #DOWN 
             e'' 8  
             \bar "|"  %{ end measure 26 %} 
             \once \override Stem.direction = #DOWN 
             e'' 1  ~  
             \once \override Stem.direction = #DOWN 
             e'' 4  
             \bar "||"  %{ end measure 27 %} 
             \pageBreak
             < b'  g''  a''  d'''  > 1  ~   
             < b'  g''  a''  d'''  > 4   
             \bar "|"  %{ end measure 28 %} 
             r 4.  
             < d''  d'''  > 4.   
             < c''  c'''  > 4   
             < g'  g''  > 4  ~   
             \bar "|"  %{ end measure 29 %} 
             < g'  g''  > 1  ~   
             < g'  g''  > 4   
             \bar "|"  %{ end measure 30 %} 
             r 1  
             r 8  
             \once \override Stem.direction = #UP 
             f' 8  
             \bar "|"  %{ end measure 31 %} 
             \once \override Stem.direction = #UP 
             e' 4.  
             \once \override Stem.direction = #DOWN 
             c'' 4.  
             \once \override Stem.direction = #DOWN 
             d'' 4  
             \once \override Stem.direction = #DOWN 
             g'' 4  
             \bar "|"  %{ end measure 32 %} 
             \once \override Stem.direction = #DOWN 
             e'' 4.  
             \once \override Stem.direction = #DOWN 
             b' 1  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             c'' 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             b' 8 ]  
             \bar "|"  %{ end measure 33 %} 
             \once \override Stem.direction = #DOWN 
             c'' 4  
             \once \override Stem.direction = #UP 
             g' 1  
             \bar "|"  %{ end measure 34 %} 
             r 1  
             r 4  
             \bar "||"  %{ end measure 35 %} 
             \pageBreak
             < bes'  f''  g''  d'''  > 1  ~   
             < bes'  f''  g''  d'''  > 4   
             \bar "|"  %{ end measure 36 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 37 %} 
             < aes'  c''  g''  bes''  > 1  ~   
             < aes'  c''  g''  bes''  > 4   
             \bar "|"  %{ end measure 38 %} 
             r 4  
             r 4  
             r 8  
             \once \override Stem.direction = #UP 
             e' 8  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             a' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             b' 4. ]  
             \bar "|"  %{ end measure 39 %} 
             \once \override Stem.direction = #UP 
             g' 4.  
             \once \override Stem.direction = #DOWN 
             c'' 8  
             r 4  
             \once \override Stem.direction = #DOWN 
             e'' 4  
             \once \override Stem.direction = #DOWN 
             d'' 4  
             \bar "|"  %{ end measure 40 %} 
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             e'' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             f'' 8 ]  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             g'' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             e'' 8 ]  
             r 8  
             \once \override Stem.direction = #DOWN 
             f'' 8  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             c'' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             d'' 8 ]  
             r 4  
             \bar "|"  %{ end measure 41 %} 
             \once \override Stem.direction = #DOWN 
             d'' 4  
             \once \override Stem.direction = #DOWN 
             e'' 1  
             \bar "||"  %{ end measure 42 %} 
             \pageBreak
             r 4.  
             \once \override Stem.direction = #DOWN 
             c'' 1  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             b' 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             a' 8 ]  
             \bar "|"  %{ end measure 43 %} 
             \once \override Stem.direction = #UP 
             gis' 4.  
             \once \override Stem.direction = #DOWN 
             e'' 2..  
             \bar "|"  %{ end measure 44 %} 
             \once \override Stem.direction = #DOWN 
             d'' 4.  
             \once \override Stem.direction = #DOWN 
             c'' 8  
             r 8  
             \once \override Stem.direction = #UP 
             e' 2  ~  
             \once \override Stem.direction = #UP 
             e' 8  
             \bar "|"  %{ end measure 45 %} 
             r 2.  
             r 4  
             \once \override Stem.direction = #UP 
             g' 4  
             \bar "|"  %{ end measure 46 %} 
             \once \override Stem.direction = #UP 
             a' \breve  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             g' 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             f' 8 ]  
             \bar "|"  %{ end measure 47 %} 
             \once \override Stem.direction = #UP 
             e' 4.  
             \once \override Stem.direction = #DOWN 
             b' 2  ~  
             \once \override Stem.direction = #DOWN 
             b' 8  
             r 4  
             \bar "|"  %{ end measure 48 %} 
             \once \override Stem.direction = #DOWN 
             c'' 4.  
             \once \override Stem.direction = #DOWN 
             d'' 8  
             r 8  
             \once \override Stem.direction = #DOWN 
             e'' 2  ~  
             \once \override Stem.direction = #DOWN 
             e'' 8  ~  
             \bar "|"  %{ end measure 49 %} 
             \once \override Stem.direction = #DOWN 
             e'' 1  ~  
             \once \override Stem.direction = #DOWN 
             e'' 4  
             \bar "||"  %{ end measure 50 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 51 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 52 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 53 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 54 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 55 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 56 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 57 %} 
             r 1  
             r 4  
             \bar "||"  %{ end measure 58 %} 
             \pageBreak
             < b'  d''  > 4   
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             e'' 8 [  
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < g'  c''  > 2  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < g'  c''  > 8   
             r 8  
             < g'  c''  > 8   
             \bar "|"  %{ end measure 59 %} 
             < g'  b'  > 4   
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             e' 8 [  
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < g'  b'  > 2..   
             \bar "|"  %{ end measure 60 %} 
             < g'  c''  > 4   
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             f'' 8 [  
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < g'  c''  > 2  ~   
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < g'  c''  > 8   
             r 8  
             < g'  c''  > 8   
             \bar "|"  %{ end measure 61 %} 
             < g'  c''  > 4   
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             f' 8 [  
             \set stemLeftBeamCount = #1
             \set stemLeftBeamCount = #1
             < g'  c''  > 2..   
             \bar "|"  %{ end measure 62 %} 
             \bar "|"  %{ end measure 63 %} 
             \bar "|"  %{ end measure 64 %} 
             \bar "|"  %{ end measure 65 %} 
             \bar "||"  %{ end measure 66 %} 
             \pageBreak
             \bar "|"  %{ end measure 67 %} 
             \bar "|"  %{ end measure 68 %} 
             \bar "|"  %{ end measure 69 %} 
             \bar "|"  %{ end measure 70 %} 
             \bar "|"  %{ end measure 71 %} 
             \bar "|"  %{ end measure 72 %} 
             \bar "||"  %{ end measure 73 %} 
             \pageBreak
             \bar "|"  %{ end measure 74 %} 
             \bar "|"  %{ end measure 75 %} 
             \bar "|"  %{ end measure 76 %} 
             \bar "|"  %{ end measure 77 %} 
             \bar "|"  %{ end measure 78 %} 
             < gis'  e''  b''  dis'''  > 1  ~   
             < gis'  e''  b''  dis'''  > 4   
             \bar "|"  %{ end measure 79 %} 
             < g'  d''  fis''  b''  > 2   
             r 4  
             r 2  
             \bar "|"  %{ end measure 80 %} 
             < g'  aes'  bes'  d''  > 4.   
             < g'  c''  e''  > 8   
             r 8  
             < g'  e''  g''  > 2  ~   
             < g'  e''  g''  > 8   
             \bar "||"  %{ end measure 81 %} 
             \time 3/4
             r 2.  
             \bar "|"  %{ end measure 82 %} 
             r 2.  
             \bar "||"  %{ end measure 83 %} 
             \pageBreak
             \time 4/4
             \bar "|"  %{ end measure 84 %} 
             \bar "|"  %{ end measure 85 %} 
             \bar "|"  %{ end measure 86 %} 
             \bar "|"  %{ end measure 87 %} 
             \bar "|"  %{ end measure 88 %} 
             \bar "|"  %{ end measure 89 %} 
             \bar "|"  %{ end measure 90 %} 
             \bar "||"  %{ end measure 91 %} 
             \pageBreak
             \bar "|"  %{ end measure 92 %} 
             \bar "|"  %{ end measure 93 %} 
             \bar "|"  %{ end measure 94 %} 
             \bar "|"  %{ end measure 95 %} 
             \bar "|"  %{ end measure 96 %} 
             \bar "|"  %{ end measure 97 %} 
             \bar "|"  %{ end measure 98 %} 
             \bar "||"  %{ end measure 99 %} 
             \pageBreak
             \bar "|"  %{ end measure 100 %} 
             \bar "|"  %{ end measure 101 %} 
             \bar "|"  %{ end measure 102 %} 
             \bar "|"  %{ end measure 103 %} 
             \bar "|"  %{ end measure 104 %} 
             \bar "|"  %{ end measure 105 %} 
             \bar "||"  %{ end measure 106 %} 
             \pageBreak
             r 1  
             \bar "|"  %{ end measure 107 %} 
             \bar "|"  %{ end measure 108 %} 
             \once \override Stem.direction = #DOWN 
             g'' 4.  
             \once \override Stem.direction = #DOWN 
             c''' 2  ~  
             \once \override Stem.direction = #DOWN 
             c''' 8  
             \bar "|"  %{ end measure 109 %} 
             \once \override Stem.direction = #DOWN 
             bes'' 2  
             r 4  
             r 8  
             \once \override Stem.direction = #DOWN 
             a'' 8  ~  
             \bar "|"  %{ end measure 110 %} 
             \once \override Stem.direction = #DOWN 
             a'' 2..  
             \once \override Stem.direction = #DOWN 
             gis'' 8  ~  
             \bar "|"  %{ end measure 111 %} 
             \once \override Stem.direction = #DOWN 
             gis'' 2..  
             \once \override Stem.direction = #DOWN 
             e'' 8  ~  
             \bar "|"  %{ end measure 112 %} 
             e'' 1  
             \bar "|"  %{ end measure 113 %} 
             \times 2/3 { \once \override Stem.direction = #DOWN 
                ees'' 4  
                \once \override Stem.direction = #DOWN 
                f'' 4  
                \once \override Stem.direction = #DOWN 
                g'' 4  
                 } 
                
             \times 2/3 { \once \override Stem.direction = #DOWN 
                aes'' 4  
                \once \override Stem.direction = #DOWN 
                bes'' 4  
                \set stemRightBeamCount = #1
                \once \override Stem.direction = #DOWN 
                b'' 8 [  
                \set stemLeftBeamCount = #1
                \once \override Stem.direction = #DOWN 
                cis''' 8 ]  
                 } 
                
             \bar "||"  %{ end measure 114 %} 
             \pageBreak
             \time 5/4
             \once \override Stem.direction = #DOWN 
             d''' 1  ~  
             \once \override Stem.direction = #DOWN 
             d''' 4  
             \bar "|"  %{ end measure 115 %} 
             \once \override Stem.direction = #DOWN 
             d'' 4.  
             \once \override Stem.direction = #DOWN 
             g'' 4.  
             \once \override Stem.direction = #DOWN 
             d''' 4  
             \once \override Stem.direction = #DOWN 
             c''' 4  
             \bar "|"  %{ end measure 116 %} 
             < aes'  c''  g''  bes''  > 1  ~   
             < aes'  c''  g''  bes''  > 4   
             \bar "|"  %{ end measure 117 %} 
             \bar "|"  %{ end measure 118 %} 
             \bar "|"  %{ end measure 119 %} 
             \bar "|"  %{ end measure 120 %} 
             \bar "||"  %{ end measure 121 %} 
             \pageBreak
             r 4.  
             \once \override Stem.direction = #DOWN 
             c'' 1  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             b' 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             a' 8 ]  
             \bar "|"  %{ end measure 122 %} 
             \once \override Stem.direction = #UP 
             gis' 4.  
             \once \override Stem.direction = #DOWN 
             e'' 2  ~  
             \once \override Stem.direction = #DOWN 
             e'' 8  
             r 4  
             \bar "|"  %{ end measure 123 %} 
             \once \override Stem.direction = #DOWN 
             d'' 4.  
             \once \override Stem.direction = #DOWN 
             c'' 8  
             r 8  
             \once \override Stem.direction = #UP 
             e' 2  ~  
             \once \override Stem.direction = #UP 
             e' 8  ~  
             \bar "|"  %{ end measure 124 %} 
             \once \override Stem.direction = #UP 
             e' 2.  
             r 4  
             \once \override Stem.direction = #UP 
             g' 4  
             \bar "|"  %{ end measure 125 %} 
             \once \override Stem.direction = #UP 
             a' \breve  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             g' 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             f' 8 ]  
             \bar "|"  %{ end measure 126 %} 
             \once \override Stem.direction = #UP 
             e' 4.  
             \once \override Stem.direction = #DOWN 
             b' 2  ~  
             \once \override Stem.direction = #DOWN 
             b' 8  
             r 4  
             \bar "|"  %{ end measure 127 %} 
             \once \override Stem.direction = #DOWN 
             c'' 4.  
             \once \override Stem.direction = #DOWN 
             d'' 8  
             r 8  
             \once \override Stem.direction = #DOWN 
             e'' 2  ~  
             \once \override Stem.direction = #DOWN 
             e'' 8  
             \bar "||"  %{ end measure 128 %} 
             \pageBreak
             r 2.  
             r 4  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             e'' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             f'' 8 ]  
             \bar "|"  %{ end measure 129 %} 
             \once \override Stem.direction = #DOWN 
             g'' 4.  
             \once \override Stem.direction = #DOWN 
             e'' 8  
             r 8  
             \once \override Stem.direction = #DOWN 
             c'' 2  ~  
             \once \override Stem.direction = #DOWN 
             c'' 8  
             \bar "|"  %{ end measure 130 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 131 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 132 %} 
             r 2  
             r 8  
             \once \override Stem.direction = #UP 
             g' 8  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             a' 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             b' 8 ]  
             r 4  
             \bar "|"  %{ end measure 133 %} 
             \once \override Stem.direction = #DOWN 
             gis'' 4.  
             \once \override Stem.direction = #DOWN 
             a'' 8  
             r 8  
             \once \override Stem.direction = #DOWN 
             b'' 8  
             r 4  
             r 8  
             \once \override Stem.direction = #DOWN 
             d'' 8  ~  
             \bar "|"  %{ end measure 134 %} 
             \bar "|"  %{ end measure 135 %} 
             \pageBreak
             \time 4/4
             r 1  
             \bar "|"  %{ end measure 136 %} 
             r 1  
             \bar "|"  %{ end measure 137 %} 
             r 1  
             \bar "|"  %{ end measure 138 %} 
             r 2  
             r 4  
             r 8  
             \set stemRightBeamCount = #2
             \once \override Stem.direction = #DOWN 
             b' 16 [  
             \set stemLeftBeamCount = #2
             \once \override Stem.direction = #DOWN 
             c'' 16 ]  
             \bar "|"  %{ end measure 139 %} 
             \once \override Stem.direction = #DOWN 
             d'' 4  
             \once \override Stem.direction = #DOWN 
             c'' 4  
             \once \override Stem.direction = #DOWN 
             e'' 4  
             \once \override Stem.direction = #DOWN 
             c'' 4  
             \bar "|"  %{ end measure 140 %} 
             b' 1  \fermata  
             \bar "||"  %{ end measure 141 %} 
              } 
            
 
       \new Staff  = Bass \with  { 
         \autoBeamOff 
          } 
          { \partial 32*16 
             \pageBreak
             \clef "bass" 
             \key c \major 
             \time 4/4
             r 2  
             \bar "|"  %{ end measure 0 %} 
             r 1  
             \bar "|"  %{ end measure 1 %} 
             r 1  
             \bar "|"  %{ end measure 2 %} 
             \once \override Stem.direction = #UP 
             cis 4  
             \once \override Stem.direction = #UP 
             b, 4  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             fis, 8 [  \fermata  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             cis 8  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             gis 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             dis' 8 ]  
             \bar "|"  %{ end measure 3 %} 
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             g 8 [  \fermata  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             g, 8  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             d 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             a 2 ]  ~  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             a 8 ]  
             \bar "|"  %{ end measure 4 %} 
             gis 1  \fermata  
             \bar "|"  %{ end measure 5 %} 
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             f 8 [  \fermata  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             c 8  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #UP 
             f, 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             bes, 2 ]  ~  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             bes, 8 ]  ~  
             \bar "|"  %{ end measure 6 %} 
             bes, 1  
             \bar "||"  %{ end measure 7 %} 
             \time 5/4
             r 1  
             r 4  
             \bar "|"  %{ end measure 8 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 9 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 10 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 11 %} 
             \pageBreak
             r 1  
             r 4  
             \bar "|"  %{ end measure 12 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 13 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 14 %} 
             r 2.  
             \once \override Stem.direction = #DOWN 
             ees 4  
             \once \override Stem.direction = #UP 
             aes, 4  
             \bar "|"  %{ end measure 15 %} 
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 16 %} 
             \once \override Stem.direction = #DOWN 
             d 4.  
             \once \override Stem.direction = #DOWN 
             fis 2  ~  
             \once \override Stem.direction = #DOWN 
             fis 8  
             \once \override Stem.direction = #DOWN 
             d 4  
             \bar "|"  %{ end measure 17 %} 
             \once \override Stem.direction = #UP 
             e, 1  ~  
             \once \override Stem.direction = #UP 
             e, 4  
             \bar "|"  %{ end measure 18 %} 
             \once \override Stem.direction = #UP 
             aes, 4.  
             \once \override Stem.direction = #DOWN 
             f 2  ~  
             \once \override Stem.direction = #DOWN 
             f 8  
             \once \override Stem.direction = #UP 
             aes, 4  
             \bar "||"  %{ end measure 19 %} 
             \pageBreak
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 20 %} 
             \once \override Stem.direction = #DOWN 
             d 4.  
             \once \override Stem.direction = #DOWN 
             fis 2  ~  
             \once \override Stem.direction = #DOWN 
             fis 8  
             \once \override Stem.direction = #DOWN 
             d 4  
             \bar "|"  %{ end measure 21 %} 
             \once \override Stem.direction = #UP 
             e, 1  ~  
             \once \override Stem.direction = #UP 
             e, 4  
             \bar "|"  %{ end measure 22 %} 
             \once \override Stem.direction = #UP 
             aes, 4.  
             \once \override Stem.direction = #DOWN 
             f 2  ~  
             \once \override Stem.direction = #DOWN 
             f 8  
             \once \override Stem.direction = #UP 
             aes, 4  
             \bar "|"  %{ end measure 23 %} 
             \once \override Stem.direction = #UP 
             g, 1  ~  
             \once \override Stem.direction = #UP 
             g, 4  
             \bar "|"  %{ end measure 24 %} 
             \once \override Stem.direction = #UP 
             gis, 4.  
             \once \override Stem.direction = #DOWN 
             e 2  ~  
             \once \override Stem.direction = #DOWN 
             e 8  
             \once \override Stem.direction = #UP 
             gis, 4  
             \bar "|"  %{ end measure 25 %} 
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 26 %} 
             \once \override Stem.direction = #UP 
             b, 4.  
             \once \override Stem.direction = #UP 
             bes, 2..  
             \bar "||"  %{ end measure 27 %} 
             \pageBreak
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 28 %} 
             \once \override Stem.direction = #UP 
             c 1  ~  
             \once \override Stem.direction = #UP 
             c 4  
             \bar "|"  %{ end measure 29 %} 
             \once \override Stem.direction = #DOWN 
             d 1  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 30 %} 
             \once \override Stem.direction = #UP 
             aes, 4.  
             \once \override Stem.direction = #DOWN 
             f 2  ~  
             \once \override Stem.direction = #DOWN 
             f 8  
             \once \override Stem.direction = #UP 
             aes, 4  
             \bar "|"  %{ end measure 31 %} 
             \once \override Stem.direction = #UP 
             g, 1  ~  
             \once \override Stem.direction = #UP 
             g, 4  
             \bar "|"  %{ end measure 32 %} 
             \once \override Stem.direction = #UP 
             gis, 4.  
             \once \override Stem.direction = #DOWN 
             e 2  ~  
             \once \override Stem.direction = #DOWN 
             e 8  
             \once \override Stem.direction = #UP 
             gis, 4  
             \bar "|"  %{ end measure 33 %} 
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 34 %} 
             \once \override Stem.direction = #UP 
             g, 4.  
             \once \override Stem.direction = #DOWN 
             f 2  ~  
             \once \override Stem.direction = #DOWN 
             f 8  
             \once \override Stem.direction = #UP 
             g, 4  
             \bar "||"  %{ end measure 35 %} 
             \pageBreak
             \once \override Stem.direction = #UP 
             c 1  ~  
             \once \override Stem.direction = #UP 
             c 4  
             \bar "|"  %{ end measure 36 %} 
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 37 %} 
             \once \override Stem.direction = #UP 
             aes, 1  ~  
             \once \override Stem.direction = #UP 
             aes, 4  
             \bar "|"  %{ end measure 38 %} 
             \once \override Stem.direction = #UP 
             c 1  ~  
             \once \override Stem.direction = #UP 
             c 4  
             \bar "|"  %{ end measure 39 %} 
             \once \override Stem.direction = #DOWN 
             d 1  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 40 %} 
             \once \override Stem.direction = #UP 
             g, 4.  
             \once \override Stem.direction = #DOWN 
             f 8  
             r 4  
             r 8  
             \once \override Stem.direction = #UP 
             g, 8  
             r 4  
             \bar "|"  %{ end measure 41 %} 
             \once \override Stem.direction = #UP 
             b, 4  
             bes, 1  
             \bar "||"  %{ end measure 42 %} 
             \pageBreak
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 43 %} 
             \once \override Stem.direction = #DOWN 
             d 4.  
             \once \override Stem.direction = #DOWN 
             fis 2  ~  
             \once \override Stem.direction = #DOWN 
             fis 8  
             \once \override Stem.direction = #DOWN 
             d 4  
             \bar "|"  %{ end measure 44 %} 
             \once \override Stem.direction = #UP 
             e, 1  ~  
             \once \override Stem.direction = #UP 
             e, 4  
             \bar "|"  %{ end measure 45 %} 
             \once \override Stem.direction = #UP 
             aes, 4.  
             \once \override Stem.direction = #DOWN 
             f 2  ~  
             \once \override Stem.direction = #DOWN 
             f 8  
             \once \override Stem.direction = #UP 
             aes, 4  
             \bar "|"  %{ end measure 46 %} 
             \once \override Stem.direction = #UP 
             g, 1  ~  
             \once \override Stem.direction = #UP 
             g, 4  
             \bar "|"  %{ end measure 47 %} 
             \once \override Stem.direction = #UP 
             gis, 4.  
             \once \override Stem.direction = #DOWN 
             e 2  ~  
             \once \override Stem.direction = #DOWN 
             e 8  
             \once \override Stem.direction = #UP 
             gis, 4  
             \bar "|"  %{ end measure 48 %} 
             \once \override Stem.direction = #UP 
             a, 2  
             r 8  
             \once \override Stem.direction = #UP 
             a, 2  ~  
             \once \override Stem.direction = #UP 
             a, 8  
             \bar "|"  %{ end measure 49 %} 
             \once \override Stem.direction = #UP 
             bes, 1  ~  
             \once \override Stem.direction = #UP 
             bes, 4  
             \bar "||"  %{ end measure 50 %} 
             \pageBreak
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 51 %} 
             \once \override Stem.direction = #DOWN 
             d 4.  
             \once \override Stem.direction = #DOWN 
             fis 2  ~  
             \once \override Stem.direction = #DOWN 
             fis 8  
             \once \override Stem.direction = #DOWN 
             d 4  
             \bar "|"  %{ end measure 52 %} 
             \once \override Stem.direction = #UP 
             e, 1  ~  
             \once \override Stem.direction = #UP 
             e, 4  
             \bar "|"  %{ end measure 53 %} 
             \once \override Stem.direction = #UP 
             aes, 4.  
             \once \override Stem.direction = #DOWN 
             f 2  ~  
             \once \override Stem.direction = #DOWN 
             f 8  
             \once \override Stem.direction = #UP 
             aes, 4  
             \bar "|"  %{ end measure 54 %} 
             \once \override Stem.direction = #UP 
             g, 1  ~  
             \once \override Stem.direction = #UP 
             g, 4  
             \bar "|"  %{ end measure 55 %} 
             \once \override Stem.direction = #UP 
             gis, 4.  
             \once \override Stem.direction = #DOWN 
             e 2  ~  
             \once \override Stem.direction = #DOWN 
             e 8  
             \once \override Stem.direction = #UP 
             gis, 4  
             \bar "|"  %{ end measure 56 %} 
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 57 %} 
             \once \override Stem.direction = #UP 
             bes, 1  
             r 8  
             \once \override Stem.direction = #UP 
             bes, 8  
             \bar "||"  %{ end measure 58 %} 
             \pageBreak
             \once \override Stem.direction = #UP 
             a, 4.  
             \once \override Stem.direction = #DOWN 
             e 4.  
             \once \override Stem.direction = #DOWN 
             a 4  
             \once \override Stem.direction = #DOWN 
             g 4  
             \bar "|"  %{ end measure 59 %} 
             \once \override Stem.direction = #UP 
             c 1  ~  
             \once \override Stem.direction = #UP 
             c 4  
             \bar "|"  %{ end measure 60 %} 
             \once \override Stem.direction = #DOWN 
             d 4.  
             \once \override Stem.direction = #UP 
             a, 4.  
             \once \override Stem.direction = #DOWN 
             d 4  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 61 %} 
             \once \override Stem.direction = #UP 
             aes, 4.  
             \once \override Stem.direction = #DOWN 
             f 2  ~  
             \once \override Stem.direction = #DOWN 
             f 8  
             \once \override Stem.direction = #UP 
             aes, 4  
             \bar "|"  %{ end measure 62 %} 
             \once \override Stem.direction = #UP 
             g, 4.  
             \once \override Stem.direction = #UP 
             c 4.  
             \once \override Stem.direction = #DOWN 
             f 4  
             \once \override Stem.direction = #DOWN 
             g 4  
             \bar "|"  %{ end measure 63 %} 
             \once \override Stem.direction = #DOWN 
             gis 4.  
             \once \override Stem.direction = #DOWN 
             e 4.  
             \once \override Stem.direction = #UP 
             gis, 2  
             \bar "|"  %{ end measure 64 %} 
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 65 %} 
             \once \override Stem.direction = #UP 
             g, 4.  
             \once \override Stem.direction = #DOWN 
             f 2  ~  
             \once \override Stem.direction = #DOWN 
             f 8  
             \once \override Stem.direction = #UP 
             g, 4  
             \bar "||"  %{ end measure 66 %} 
             \pageBreak
             \once \override Stem.direction = #UP 
             c 1  ~  
             \once \override Stem.direction = #UP 
             c 4  
             \bar "|"  %{ end measure 67 %} 
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 68 %} 
             \once \override Stem.direction = #UP 
             aes, 1  ~  
             \once \override Stem.direction = #UP 
             aes, 4  
             \bar "|"  %{ end measure 69 %} 
             \once \override Stem.direction = #UP 
             c 1  ~  
             \once \override Stem.direction = #UP 
             c 4  
             \bar "|"  %{ end measure 70 %} 
             \once \override Stem.direction = #DOWN 
             d 1  
             \once \override Stem.direction = #UP 
             aes, 4  
             \bar "|"  %{ end measure 71 %} 
             \once \override Stem.direction = #UP 
             g, 4.  
             \once \override Stem.direction = #DOWN 
             f 8  
             r 4  
             r 8  
             \once \override Stem.direction = #UP 
             g, 8  
             r 4  
             \bar "|"  %{ end measure 72 %} 
             \once \override Stem.direction = #UP 
             bes, 1  ~  
             \once \override Stem.direction = #UP 
             bes, 4  
             \bar "||"  %{ end measure 73 %} 
             \pageBreak
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 74 %} 
             \once \override Stem.direction = #DOWN 
             d 4.  
             \once \override Stem.direction = #DOWN 
             fis 2  ~  
             \once \override Stem.direction = #DOWN 
             fis 8  
             \once \override Stem.direction = #DOWN 
             d 4  
             \bar "|"  %{ end measure 75 %} 
             \once \override Stem.direction = #UP 
             e, 1  ~  
             \once \override Stem.direction = #UP 
             e, 4  
             \bar "|"  %{ end measure 76 %} 
             \once \override Stem.direction = #UP 
             aes, 4.  
             \once \override Stem.direction = #DOWN 
             f 2  ~  
             \once \override Stem.direction = #DOWN 
             f 8  
             \once \override Stem.direction = #UP 
             aes, 4  
             \bar "|"  %{ end measure 77 %} 
             \once \override Stem.direction = #UP 
             g, 1  ~  
             \once \override Stem.direction = #UP 
             g, 4  
             \bar "|"  %{ end measure 78 %} 
             \once \override Stem.direction = #DOWN 
             e 4  
             r 8  
             \once \override Stem.direction = #UP 
             gis, 2..  
             \bar "|"  %{ end measure 79 %} 
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 80 %} 
             \once \override Stem.direction = #UP 
             bes, 2  
             r 8  
             \once \override Stem.direction = #UP 
             bes, 4.  
             r 8  
             \once \override Stem.direction = #UP 
             bes, 8  
             \bar "||"  %{ end measure 81 %} 
             \time 3/4
             \once \override Stem.direction = #UP 
             a, 2.  
             \bar "|"  %{ end measure 82 %} 
             \once \override Stem.direction = #UP 
             aes, 2  
             r 4  
             \bar "||"  %{ end measure 83 %} 
             \pageBreak
             \time 4/4
             g, 1  
             \bar "|"  %{ end measure 84 %} 
             \once \override Stem.direction = #UP 
             c 2.  
             r 8  
             \once \override Stem.direction = #UP 
             b, 8  
             \bar "|"  %{ end measure 85 %} 
             \once \override Stem.direction = #UP 
             bes, 4.  
             \once \override Stem.direction = #DOWN 
             f 2  ~  
             \once \override Stem.direction = #DOWN 
             f 8  
             \bar "|"  %{ end measure 86 %} 
             \once \override Stem.direction = #DOWN 
             ges 1  
             \bar "|"  %{ end measure 87 %} 
             \once \override Stem.direction = #DOWN 
             f 4.  
             \once \override Stem.direction = #UP 
             f, 2  ~  
             \once \override Stem.direction = #UP 
             f, 8  
             \bar "|"  %{ end measure 88 %} 
             \once \override Stem.direction = #UP 
             fis, 1  
             \bar "|"  %{ end measure 89 %} 
             \once \override Stem.direction = #UP 
             g, 4.  
             \once \override Stem.direction = #DOWN 
             ees 2  ~  
             \once \override Stem.direction = #DOWN 
             ees 8  
             \bar "|"  %{ end measure 90 %} 
             \once \override Stem.direction = #UP 
             aes, 4.  
             \once \override Stem.direction = #DOWN 
             ees 4.  
             \once \override Stem.direction = #DOWN 
             aes 4  
             \bar "||"  %{ end measure 91 %} 
             \pageBreak
             \once \override Stem.direction = #DOWN 
             g 4.  
             \once \override Stem.direction = #UP 
             g, 2  ~  
             \once \override Stem.direction = #UP 
             g, 8  
             \bar "|"  %{ end measure 92 %} 
             \once \override Stem.direction = #UP 
             bes, 1  
             \bar "|"  %{ end measure 93 %} 
             \once \override Stem.direction = #UP 
             c 4.  
             \once \override Stem.direction = #UP 
             g, 2  ~  
             \once \override Stem.direction = #UP 
             g, 8  
             \bar "|"  %{ end measure 94 %} 
             \once \override Stem.direction = #UP 
             ges, 1  
             \bar "|"  %{ end measure 95 %} 
             \once \override Stem.direction = #UP 
             f, 1  
             \bar "|"  %{ end measure 96 %} 
             \once \override Stem.direction = #UP 
             fis, 1  
             \bar "|"  %{ end measure 97 %} 
             \once \override Stem.direction = #UP 
             g, 4.  
             \once \override Stem.direction = #DOWN 
             ees 2  ~  
             \once \override Stem.direction = #DOWN 
             ees 8  
             \bar "|"  %{ end measure 98 %} 
             \bar "||"  %{ end measure 99 %} 
             \pageBreak
             \bar "|"  %{ end measure 100 %} 
             \bar "|"  %{ end measure 101 %} 
             \bar "|"  %{ end measure 102 %} 
             \bar "|"  %{ end measure 103 %} 
             \bar "|"  %{ end measure 104 %} 
             \bar "|"  %{ end measure 105 %} 
             \bar "||"  %{ end measure 106 %} 
             \pageBreak
             \once \override Stem.direction = #UP 
             a, 2  ~  
             \once \override Stem.direction = #UP 
             a, 4  ~  
             \once \override Stem.direction = #UP 
             a, 16  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             bes, 8. ]  
             \bar "|"  %{ end measure 107 %} 
             \once \override Stem.direction = #UP 
             c 2..  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #UP 
             d 8 ]  ~  
             \bar "|"  %{ end measure 108 %} 
             \once \override Stem.direction = #DOWN 
             d 1  
             \bar "|"  %{ end measure 109 %} 
             \once \override Stem.direction = #UP 
             aes, 2  
             r 4  
             r 8  
             \once \override Stem.direction = #UP 
             g, 8  ~  
             \bar "|"  %{ end measure 110 %} 
             \once \override Stem.direction = #UP 
             g, 2..  
             \once \override Stem.direction = #UP 
             gis, 8  ~  
             \bar "|"  %{ end measure 111 %} 
             \once \override Stem.direction = #UP 
             gis, 2..  
             \once \override Stem.direction = #UP 
             a, 8  ~  
             \bar "|"  %{ end measure 112 %} 
             \once \override Stem.direction = #UP 
             a, 1  
             \bar "|"  %{ end measure 113 %} 
             \once \override Stem.direction = #UP 
             g, 1  
             \bar "||"  %{ end measure 114 %} 
             \pageBreak
             \time 5/4
             \once \override Stem.direction = #UP 
             c 1  ~  
             \once \override Stem.direction = #UP 
             c 4  
             \bar "|"  %{ end measure 115 %} 
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 116 %} 
             \once \override Stem.direction = #UP 
             aes, 1  ~  
             \once \override Stem.direction = #UP 
             aes, 4  
             \bar "|"  %{ end measure 117 %} 
             \once \override Stem.direction = #UP 
             c 1  ~  
             \once \override Stem.direction = #UP 
             c 4  
             \bar "|"  %{ end measure 118 %} 
             \once \override Stem.direction = #DOWN 
             d 1  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 119 %} 
             \once \override Stem.direction = #UP 
             g, 4.  
             \once \override Stem.direction = #DOWN 
             f 8  
             r 4  
             r 8  
             \once \override Stem.direction = #UP 
             g, 8  
             r 4  
             \bar "|"  %{ end measure 120 %} 
             \once \override Stem.direction = #UP 
             b, 4  
             bes, 1  
             \bar "||"  %{ end measure 121 %} 
             \pageBreak
             \once \override Stem.direction = #UP 
             a, 1  ~  
             \once \override Stem.direction = #UP 
             a, 4  
             \bar "|"  %{ end measure 122 %} 
             \once \override Stem.direction = #DOWN 
             d 4.  
             \once \override Stem.direction = #DOWN 
             fis 2  ~  
             \once \override Stem.direction = #DOWN 
             fis 8  
             \once \override Stem.direction = #DOWN 
             d 4  
             \bar "|"  %{ end measure 123 %} 
             \once \override Stem.direction = #UP 
             e, 1  ~  
             \once \override Stem.direction = #UP 
             e, 4  
             \bar "|"  %{ end measure 124 %} 
             \once \override Stem.direction = #UP 
             aes, 4.  
             \once \override Stem.direction = #DOWN 
             f 2  ~  
             \once \override Stem.direction = #DOWN 
             f 8  
             \once \override Stem.direction = #UP 
             aes, 4  
             \bar "|"  %{ end measure 125 %} 
             \once \override Stem.direction = #UP 
             g, 1  ~  
             \once \override Stem.direction = #UP 
             g, 4  
             \bar "|"  %{ end measure 126 %} 
             \once \override Stem.direction = #UP 
             gis, 4.  
             \once \override Stem.direction = #DOWN 
             e 2  ~  
             \once \override Stem.direction = #DOWN 
             e 8  
             \once \override Stem.direction = #UP 
             gis, 4  
             \bar "|"  %{ end measure 127 %} 
             \once \override Stem.direction = #UP 
             a, 2  
             r 8  
             \once \override Stem.direction = #UP 
             a, 2  ~  
             \once \override Stem.direction = #UP 
             a, 8  
             \bar "||"  %{ end measure 128 %} 
             \pageBreak
             \once \override Stem.direction = #UP 
             bes, 2  
             r 8  
             \once \override Stem.direction = #UP 
             bes, 2  ~  
             \once \override Stem.direction = #UP 
             bes, 8  
             \bar "|"  %{ end measure 129 %} 
             \once \override Stem.direction = #UP 
             a, 2  
             r 8  
             \once \override Stem.direction = #UP 
             a, 8  
             r 8  
             \once \override Stem.direction = #DOWN 
             g 8  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             a 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             b 8 ]  
             \bar "|"  %{ end measure 130 %} 
             \once \override Stem.direction = #DOWN 
             c' 4  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             b 8 [  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             g 8 ]  
             r 8  
             \once \override Stem.direction = #DOWN 
             d 2  ~  
             \once \override Stem.direction = #DOWN 
             d 8  
             \bar "|"  %{ end measure 131 %} 
             \once \override Stem.direction = #UP 
             cis 2  
             r 8  
             \once \override Stem.direction = #UP 
             cis 2  ~  
             \once \override Stem.direction = #UP 
             cis 8  
             \bar "|"  %{ end measure 132 %} 
             \once \override Stem.direction = #UP 
             c 2  
             r 8  
             \once \override Stem.direction = #UP 
             c 2  ~  
             \once \override Stem.direction = #UP 
             c 8  
             \bar "|"  %{ end measure 133 %} 
             \once \override Stem.direction = #UP 
             b, 2  
             r 8  
             \once \override Stem.direction = #UP 
             b, 8  
             r 4  
             r 8  
             \once \override Stem.direction = #UP 
             c 8  ~  
             \bar "|"  %{ end measure 134 %} 
             \once \override Stem.direction = #UP 
             c 1  ~  
             \once \override Stem.direction = #UP 
             c 4  \fermata  
             \bar "|"  %{ end measure 135 %} 
             \pageBreak
             \time 4/4
             r 1  
             \bar "|"  %{ end measure 136 %} 
             r 1  
             \bar "|"  %{ end measure 137 %} 
             \once \override Stem.direction = #UP 
             b, 4  
             \once \override Stem.direction = #UP 
             bes, 4  
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             aes, 8 [  \fermata  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             ees 8  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             bes 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             ees' 8 ]  
             \bar "|"  %{ end measure 138 %} 
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             g 8 [  \fermata  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             g, 8  
             \set stemLeftBeamCount = #1
             \set stemRightBeamCount = #1
             \once \override Stem.direction = #DOWN 
             d 8  
             \set stemLeftBeamCount = #1
             \once \override Stem.direction = #DOWN 
             a 4. ]  
             r 4  
             \bar "|"  %{ end measure 139 %} 
             \once \override Stem.direction = #DOWN 
             a 4  
             \once \override Stem.direction = #DOWN 
             g 4  
             \once \override Stem.direction = #UP 
             aes, 2  
             \bar "|"  %{ end measure 140 %} 
             c 1  \fermata  
             \bar "||"  %{ end measure 141 %} 
              } 
            
 
       \new Staff  = Drums \with  { 
         \autoBeamOff 
          } 
          { \partial 32*16 
             \pageBreak
             \clef "percussion" 
             \key c \major 
             \time 4/4
             r 2  
             \bar "|"  %{ end measure 0 %} 
             r 1  
             \bar "|"  %{ end measure 1 %} 
             r 1  
             \bar "|"  %{ end measure 2 %} 
             
               << \new Voice {  } 
                     
 
                \new Voice { r 1  
                       } 
                     
 
                 >>
               
             \bar "|"  %{ end measure 3 %} 
             \bar "|"  %{ end measure 4 %} 
             \bar "|"  %{ end measure 5 %} 
             \bar "|"  %{ end measure 6 %} 
             r 1  
             \bar "||"  %{ end measure 7 %} 
             \time 5/4
             r 1  
             r 4  
             \bar "|"  %{ end measure 8 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 9 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 10 %} 
             
               << \new Voice { r 4  
                      r 8  
                       } 
                     
 
                \new Voice { r 1  
                      r 4  
                       } 
                     
 
                 >>
               
             \bar "|"  %{ end measure 11 %} 
             \pageBreak
             r 8  
             \bar "|"  %{ end measure 12 %} 
             r 4  
             \bar "|"  %{ end measure 13 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 14 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 15 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 16 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 17 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 18 %} 
             r 1  
             r 4  
             \bar "||"  %{ end measure 19 %} 
             \pageBreak
             r 8  
             \bar "|"  %{ end measure 20 %} 
             r 4  
             \bar "|"  %{ end measure 21 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 22 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 23 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 24 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 25 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 26 %} 
             \bar "||"  %{ end measure 27 %} 
             \pageBreak
             r 8  
             \bar "|"  %{ end measure 28 %} 
             r 4  
             \bar "|"  %{ end measure 29 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 30 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 31 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 32 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 33 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 34 %} 
             r 1  
             r 4  
             \bar "||"  %{ end measure 35 %} 
             \pageBreak
             r 8  
             \bar "|"  %{ end measure 36 %} 
             r 4  
             \bar "|"  %{ end measure 37 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 38 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 39 %} 
             r 4  
             r 4  
             \bar "|"  %{ end measure 40 %} 
             r 4  
             r 8  
             r 4  
             \bar "|"  %{ end measure 41 %} 
             \bar "||"  %{ end measure 42 %} 
             \pageBreak
             r 8  
             \bar "|"  %{ end measure 43 %} 
             r 4  
             \bar "|"  %{ end measure 44 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 45 %} 
             r 4  
             r 4  
             r 4  
             r 4  
             \bar "|"  %{ end measure 46 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 47 %} 
             r 4  
             r 4  
             r 4  
             r 4  
             \bar "|"  %{ end measure 48 %} 
             r 8  
             \bar "|"  %{ end measure 49 %} 
             \bar "||"  %{ end measure 50 %} 
             \pageBreak
             r 8  
             \bar "|"  %{ end measure 51 %} 
             r 4  
             \bar "|"  %{ end measure 52 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 53 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 54 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 55 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 56 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 57 %} 
             r 1  
             r 4  
             \bar "||"  %{ end measure 58 %} 
             \pageBreak
             r 8  
             \bar "|"  %{ end measure 59 %} 
             r 4  
             \bar "|"  %{ end measure 60 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 61 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 62 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 63 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 64 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 65 %} 
             r 1  
             r 4  
             \bar "||"  %{ end measure 66 %} 
             \pageBreak
             r 8  
             \bar "|"  %{ end measure 67 %} 
             r 4  
             \bar "|"  %{ end measure 68 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 69 %} 
             r 4  
             r 4  
             r 4  
             r 4  
             \bar "|"  %{ end measure 70 %} 
             r 8  
             \bar "|"  %{ end measure 71 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 72 %} 
             \bar "||"  %{ end measure 73 %} 
             \pageBreak
             r 8  
             \bar "|"  %{ end measure 74 %} 
             r 4  
             \bar "|"  %{ end measure 75 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 76 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 77 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 78 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 79 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 80 %} 
             r 8  
             \bar "||"  %{ end measure 81 %} 
             \time 3/4
             \bar "|"  %{ end measure 82 %} 
             r 4  
             \bar "||"  %{ end measure 83 %} 
             \pageBreak
             \time 4/4
             r 1  
             \bar "|"  %{ end measure 84 %} 
             r 1  
             \bar "|"  %{ end measure 85 %} 
             r 1  
             \bar "|"  %{ end measure 86 %} 
             
               << \new Voice { r 2  
                       } 
                     
 
                \new Voice { r 1  
                       } 
                     
 
                 >>
               
             \bar "|"  %{ end measure 87 %} 
             
               << \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   {  } 
                     
 
                \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   { r 4  
                       } 
                     
 
                 >>
               
             \bar "|"  %{ end measure 88 %} 
             
               << \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   {  } 
                     
 
                \new Voice { r 8  
                       } 
                     
 
                 >>
               
             \bar "|"  %{ end measure 89 %} 
             r 1  
             \bar "|"  %{ end measure 90 %} 
             r 1  
             \bar "||"  %{ end measure 91 %} 
             
               << \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   {  } 
                     
 
                \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   {  } 
                     
 
                 >>
               
             \pageBreak
             \bar "|"  %{ end measure 92 %} 
             
               << \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   {  } 
                     
 
                \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   { r 8  
                       } 
                     
 
                 >>
               
             \bar "|"  %{ end measure 93 %} 
             r 1  
             \bar "|"  %{ end measure 94 %} 
             r 1  
             \bar "|"  %{ end measure 95 %} 
             r 1  
             \bar "|"  %{ end measure 96 %} 
             r 1  
             \bar "|"  %{ end measure 97 %} 
             r 1  
             \bar "|"  %{ end measure 98 %} 
             r 8  
             \bar "||"  %{ end measure 99 %} 
             
               << \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   {  } 
                     
 
                \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   { r 16  
                       } 
                     
 
                 >>
               
             \pageBreak
             \bar "|"  %{ end measure 100 %} 
             
               << \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   {  } 
                     
 
                \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   { r 8  
                      r 16  
                       } 
                     
 
                 >>
               
             \bar "|"  %{ end measure 101 %} 
             
               << \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   {  } 
                     
 
                \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   { r 16  
                       } 
                     
 
                 >>
               
             \bar "|"  %{ end measure 102 %} 
             
               << \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   {  } 
                     
 
                \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   { r 8  
                      r 16  
                       } 
                     
 
                 >>
               
             \bar "|"  %{ end measure 103 %} 
             r 1  
             \bar "|"  %{ end measure 104 %} 
             r 8  
             \bar "|"  %{ end measure 105 %} 
             r 8  
             \bar "||"  %{ end measure 106 %} 
             
               << \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   {  } 
                     
 
                \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   { r 16  
                       } 
                     
 
                 >>
               
             \pageBreak
             \bar "|"  %{ end measure 107 %} 
             
               << \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   {  } 
                     
 
                \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   { r 8  
                      r 16  
                       } 
                     
 
                 >>
               
             \bar "|"  %{ end measure 108 %} 
             
               << \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   {  } 
                     
 
                \new Voice \with  { 
                  \autoBeamOff 
                   } 
                   { r 16  
                       } 
                     
 
                 >>
               
             \bar "|"  %{ end measure 109 %} 
             r 4  
             r 8  
             \bar "|"  %{ end measure 110 %} 
             \bar "|"  %{ end measure 111 %} 
             \bar "|"  %{ end measure 112 %} 
             
               << \new Voice {  } 
                     
 
                \new Voice { r 2.  
                       } 
                     
 
                 >>
               
             \bar "|"  %{ end measure 113 %} 
             \bar "||"  %{ end measure 114 %} 
             \pageBreak
             \time 5/4
             r 8  
             \bar "|"  %{ end measure 115 %} 
             r 4  
             \bar "|"  %{ end measure 116 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 117 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 118 %} 
             r 4  
             r 4  
             \bar "|"  %{ end measure 119 %} 
             r 4  
             r 8  
             r 4  
             \bar "|"  %{ end measure 120 %} 
             \bar "||"  %{ end measure 121 %} 
             \pageBreak
             r 8  
             \bar "|"  %{ end measure 122 %} 
             r 4  
             \bar "|"  %{ end measure 123 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 124 %} 
             r 4  
             r 4  
             r 4  
             r 4  
             \bar "|"  %{ end measure 125 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 126 %} 
             r 4  
             r 4  
             r 4  
             r 4  
             \bar "|"  %{ end measure 127 %} 
             r 8  
             \bar "||"  %{ end measure 128 %} 
             \pageBreak
             r 8  
             \bar "|"  %{ end measure 129 %} 
             r 8  
             \bar "|"  %{ end measure 130 %} 
             r 1  
             r 4  
             \bar "|"  %{ end measure 131 %} 
             r 8  
             \bar "|"  %{ end measure 132 %} 
             r 8  
             \bar "|"  %{ end measure 133 %} 
             r 8  
             r 4  
             r 8  
             \bar "|"  %{ end measure 134 %} 
             \bar "|"  %{ end measure 135 %} 
             \pageBreak
             \time 4/4
             r 1  
             \bar "|"  %{ end measure 136 %} 
             r 1  
             \bar "|"  %{ end measure 137 %} 
             r 1  
             \bar "|"  %{ end measure 138 %} 
             r 1  
             \bar "|"  %{ end measure 139 %} 
             r 1  
             \bar "|"  %{ end measure 140 %} 
             
               << \new Voice {  } 
                     
 
                \new Voice { r 1  
                       } 
                     
 
                 >>
               
             \bar "||"  %{ end measure 141 %} 
              } 
            
 
        >>
      
  } 
 

\layout {
  \context {
    \RemoveEmptyStaves
    \override VerticalAxisGroup.remove-first = ##t
  }
 }
 
