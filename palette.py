from colour import Color
import random

class Palette:
    def __init__(self, color):
        m = Color(color)
        saturation = m.saturation
        luminance = m.luminance
        self.main = m.hex

        sHue = abs(m.hue+random.uniform(.3, .5))
        sSat = saturation + .07 if saturation < .85 else saturation - .07
        sLum = luminance + .1 if luminance < .9 else luminance - .3
        s = Color(hsl=(sHue, sSat, sLum))
        self.secondary = s.hex

        cHue = abs((m.hue+random.uniform(.5, .6)) - 1)
        cHue = cHue - random.uniform(.13, .3) if cHue > .278 and cHue < .417 else cHue
        cSat = saturation - .05 if saturation > .7 else saturation + .3
        cLum = luminance + .2 if luminance < .8 else luminance - .3
        c = Color(hsl=(cHue, cSat, cLum))
        self.complementary = c.hex

        ccHue = abs((m.hue+random.uniform(.4, .6)) - 1)
        ccHue = ccHue + random.uniform(.13, .2) if ccHue > .278 and ccHue < .417 else cHue
        ccSat = saturation - .05 if saturation > .6 else saturation + .3
        ccLum = sLum
        cc = Color(hsl=(ccHue, ccSat, ccLum))
        self.split_complementary = cc.hex

        nHue = abs(m.hue-random.uniform(.1, .4))
        nSat = cSat
        nLum = cLum
        n = Color(hsl=(nHue, nSat, nLum))
        self.neutral = n.hex