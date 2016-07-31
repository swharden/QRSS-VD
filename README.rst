# Last Tested

QRSS VD was last tested on 2016-07-30 and confirmed to run on a [stock WinPython 2.7.10.3] (http://winpython.sourceforge.net/) distribution. Note that a slight modification to the code was required to fix some python imaging library imports and that it may have affected saving of images in differnent formats (so pay attention to error codes on saving).

What is QRSS VD?
----------------

QRSS VD is a free, open-source, cross-platform QRSS spectrograph and spectrogram
analyzer written entirely in Python (distributed as source ``.py``'s or compiled
``.exe``'s) by Scott Harden, AJ4VD. I wrote this software because I wanted to
build a 30m QRSS grabber for weak signal extraction experimentation but was
dissatisfied by the limitations placed on my creativity by currently-available
spectrograph software commonly used for QRSS. While I greatly admire and respect
the makers of SpectrumLab and Argo, I simply wanted the flexibility of an open
source option.

    Why shouldn't I be able to create spectrograms spanning thousands of hertz
    (several kilohertz) instead of just 100 hertz? Why shouldn't I be able to
    automatically stitch together hundreds spectrogram images so I can browse
    through them as a single, giant image thousands of pixels in size in each
    directions? Why shouldn't I be able to run the spectrograph on Linux, Mac,
    or Windows, with or without a gui? While questions like these are
    frustrating to many, I saw these challenges as an opportunity to write some
    profound code. It was from my deepest frustration that QRSS VD was born!

What does QRSS VD do?
---------------------

**QRSS VD visualizes sounds in such a way that you can visually see unique
properties of the audio that you could never notice by listening to it
directly.** As far as its application to amateur (ham) radio goes, QRSS VD
allows you to visually distinguish between frequencies (along a vertical axis)
with extremely high resolution. Additionally, by averaging the frequency
readings several-fold with respect to time, extremely weak signals (normally far
below the noise level) begin to emerge. By sending data extremely slowly (the
Morse code Q-code for "slow down" is QRS, and QRSS implies incredibly slow
transmission of information), low power transmitters (perhaps running only a few
milliwatts) can be detected thousands of miles away!

.. image:: https://github.com/QRSS-VD/QRSS-VD/raw/master/img/sample_capture.png

*This is an image created by QRSS VD.* On the vertical axis we have frequency
(with respect to my radio's frequency at the time, 10.140mHz), and on the
horizontal axis we have time (about 2 and a half minutes worth). The signals are
from QRSS transmitters around the world. Whether or not we see certain
transmitters depends on many things, especially atmospheric conditions which
affect propagation. In the image above we see the "flying W" from W1BW in MA,
USA some letters below the W which are from IW4DXW in Italy (putting out a
quarter of a watt!), and the dashed line below that shifts only a few Hz is
AA5CK running a 122mW transmitter in OK, USA, and the two lines which shift up
and down by ~10Hz are KC7VHS and WA5DJJ in NM, USA running ~250 milliwatts.
These signals are interpreted by Morse code, and take a long time to come across
(about 1 letter per minute). Here's an example:

.. image:: https://github.com/QRSS-VD/QRSS-VD/raw/master/img/qrss_kj4ldf.png

However, the image above is only a small, teeny, tiny part of the radio
spectrum. It goes on far in all directions (along both the frequency and time
axis). Although QRSS VD did create the images above, here's the same audio
processed by QRSS VD differently, allowing the creation of a much larger image.
The blue square represents the region where the green image above (with the
flying W) was taken. The quality of this image was greatly reduced to make it
web-friendly. It's over 8,000 pixels wide and over 1,000 pixels high!

.. image:: https://github.com/QRSS-VD/QRSS-VD/raw/master/img/huge_blue_square.jpg
   :width: 500

Note that as large as that image is, it could have been much larger. QRSS VD has
the capability (and yes, I've tried it) to generate spectrograms over 8,000
pixels high (spanning ~4kHz) and many thousands of pixels wide. I intentionally
chose a smaller region to display for the website, and that's okay! The beauty
of QRSS VD is that it lets you make these decisions later, without having to
destroy any data. While QRSS VD is recording you can scroll up, down, left,
and right without messing-up any of the images.

.. image:: https://github.com/QRSS-VD/QRSS-VD/raw/master/img/got_it.jpg
   :height: 500

How does it to everything? It listens to you!  You tell it how much audio to
record, how much to analyze, what region of the band (or the whole thing!), low
pass filters, high pass filters, Fourier transformation methods, frequency-
domain smoothing methods, time-domain smoothing methods, colors, intensity
adjustments, etc. (don't worry, they're all preset for common QRSS use!). While
you analyze, you can adjust most of these settings in real time. The GUI is seen
on the right.

.. image:: https://github.com/QRSS-VD/QRSS-VD/raw/master/img/small_slices.png

While it runs, QRSS VD generates and saves spectrograms in ~10 minute chunks.
Note that you can make it save each chunk as the same filename (good for a web
server QRSS grabber), or you can have it save them all consecutively with
timestamps (seconds since epoch) in the filename. The result is a folder full of
BMP files! (pictured on the left) QRSS VD viewer can then open a folder filled
with these BMP files, assemble them as a giant map, and let you scroll around in
all directions (somewhat like Google maps!, pictured below).

.. image:: https://github.com/QRSS-VD/QRSS-VD/raw/master/img/qrssvd_viewer.png

If you see a cool region you want to extract, Just click on the top left side of
the region, then the bottom right side. The QRSS VD Viewer automatically makes a
new, cropped image, adds scale bars, and opens it for you to save! How
convenient is that?

.. image:: https://github.com/QRSS-VD/QRSS-VD/raw/master/img/qrss_saved.png

Selecting larger regions creates bigger images, such as:

.. image:: https://github.com/QRSS-VD/QRSS-VD/raw/master/img/ts_830s.png
   :width: 500

Here we've captured several QRSS signals. From top to bottom:
 - IQ4DJ (straight CW)
 - G6AVK (Triangles, up is a dot down is a dash)
 - G3ZJO (mountains)
 - AA5CK (3 Hz frequency shift)
 - ??? (10 Hz frequency shift, too weak to copy)
 - WA5DJJ (10 Hz frequency shift)
