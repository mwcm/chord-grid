chord-grid
----------

requires ffmpeg and ffprobe


The goal is to generate a playable grid of samples broken down by beat grid
and ready to be imported to Ableton Live drum rack.

We'll achieve this by analyzing given wav/mp3/flac/midi files using Chordino (for now)
through chord_extractor, then export to wav/mp3/flac/midi using pydub (for now).

Inspired by the chordify grid - which is already doing this very well for most
songs.


Notes:
------

The main difference I'm noticing is that if I give Chordify a relatively simple pop
song it's able to break it down into the expected simple chords. 

In contrast, Chordino seems to get the Chord's root correct - but also adds some
variation that may be there sonically, but is not how a human would generally
notate the audio.

For example, a song with a repeating progression of: [Bm, D, A, G, A]
Whether it is rhythmically complex or not, Chordify's reading gets the simple
chords correct AND places them on the correct beats.

e.g [Bm, D, A, G, A, Bm, D, A, G, A, Bm, D, A, G, A]

While Chordino seems to completely disrespect the BEATS which each chord falls
on, instead combining them seemingly as it pleases.

e.g. [Bm7, Dm, F/A, G/A, Bm, D/A, G7, Am, D/A, G, Am]

Generally ending up with a chord that's more complex than required. I think the
most likely culprits are:

  1. Chordify clearly has a sense of which beats chords fall on, I think that
     probably also informs the chord detection in a way. It seems like
     identifying the repeating pattern of beats & chords for simple songs is
     more important than getting each individual moment transcribed perfectly.

  2. Voices overlapping, e.g. a singer harmozing for an instant can be
     interpreted as part of the backing chord. Any way to fix this without
     damaging specificity in regions where the backing chords actually do change
     momentarily?

The above means that Chordino/chord-extractor isn't going to be super helpful in my aims - unless I can find a way to use it more like a scalpel for specific difficult chords/changes. I think Chordify would likely stumble when it comes to correctly labeling complicated changes, that's generally not what I use it for though, Chordino's likely got the upper hand there.

So, Chordino might still be helpful later for songs or sections of songs which DO NOT BREAK DOWN EASILY INTO SIMPLE, REPEATING, RHYTHM & CHORD BASED SECTIONS. e.g. complex linear or free jazz, edm, prog, weird bridges in any style, etc... 

 
So if we're stuck only using Chordino for specific jobs, wat do for the rest?
  - https://github.com/CPJKU/madmom helpful?

Broken down to a recipe, I think we want to:
  1. find the bpm and where beats land in time during a song
      - This is a task that can get complicated quickly with songs that don't break down easily.
      - That being said, we only care about this working for very simple songs, since we'd use Chordino
        on more complicated songs/sections anyways.
      - it would be very nice if we can then break it down by measure/bar/notes and optionally 
        export detected beat sub-sections as well as chords matched to beats.
  2. asses what the repeating chord patterns of the song are - section by section, or in entirety
      - detect chords with an emphasis on UNIFORM ACCURACY ACROSS THE SONG rather than analyzing EXACTLY
        which tones are playing at a given moment in time. Eg. more important to know that a song is     
        based around a [Bm, D, A, G, A] pattern than knowing that between 0:30 and 0:47 it sounds exactly 
        like e.g [Bm7, D6, A7, G/A, A].
  3. if we can asses what the repeating chord patterns are in a song, or song sections, then we can:
      - best-fit the chords into a beatgrid, again with emphasis on uniformity across the song or song
        section, rather than getting exacty nuances of each bar
      - also important to remember WE ONLY CARE ABOUT WHEN EACH NEW CHORD STARTS, the reader can figure 
        out what happens inbetween, just like a chord sheet. Chordino gives the EXACT CHANGE, but we 
        don't care about that here.

So, next find a way to detect a song or partial song's beatgrid.
Partial song since rhythm could differ between verse/chorus or even change gradually throughout tracks in electronic music.
