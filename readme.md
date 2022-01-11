chord-grid
----------

requires ffmpeg and ffprobe


The goal is to generate a playable grid of samples broken down by chord change
and ready to be imported to Ableton Live drum rack.

We'll achieve this by analyzing given wav/mp3/flac/midi files using Chordino
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

I think Chordify might stumble when it comes to more complicated progressions,
that's generally not what I use it for.

So, next find a way to:
  1. detect a song's beat grid
  2. detect chords in audio segments cut up by GRID BEATS/BARS rather than letting
     Chordino detect the chord changes across whole song?
