#-*- coding:utf-8 -*-
##
##  0xBAADF00D
##
##  Filename : qrcode.py
##  Comment  : Useful class to generate custom QR
##             code easily. See example below.
##
import Image
import qrencode
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
Image.init()


class   QRCode(object):
    def __init__(self):
        self._stream = StringIO.StringIO()
        self._text = None
        self._picture = None

    def genQR(self, text, size = 500, mask = None, icon = None):
        # Create QRCode
        self._text = text
        hQR = qrencode.encode_scaled(unicode(text), size, level=3)

        # Merge colored mask with QRCode
        if mask is not None:
            hQR = hQR[2]
            try:
                foreground = Image.open(mask)
            except:
                foreground = Image.new('RGB', (size, size), (0, 0, 0))

            # Resize mask if size is not equal to qrcode size
            if foreground.size[0] != size:
                foreground = foreground.resize((size, size), Image.ANTIALIAS)
            mask = Image.new('L', (size, size), color=255)  # color=255 -> keep white pixel
            hQR = Image.composite(mask, foreground, hQR)
        else:
            hQR = hQR[2]

        # Add icon
        if icon is not None:
            hIcon = Image.open(icon)

            # Resize icon if too big
            if hIcon.size[0] > int(size * 0.30):
                new_size = int(size * 0.30)
                hIcon = hIcon.resize((new_size, new_size), Image.ANTIALIAS)
            posX = (size / 2) - (hIcon.size[0] / 2)
            posY = (size / 2) - (hIcon.size[1] / 2)
            try:
                hQR.paste(hIcon, (posX, posY), mask=hIcon)
            except:
                hQR.paste(hIcon, (posX, posY))

        # Save QRCode to stream and keep into class
        self._stream.seek(0)
        hQR.save(self._stream, 'png')
        self._picture = hQR

    def saveToFile(self, fileName):
        self._picture.save(fileName)

    def getStream(self):
        self._stream.seek(0)
        return self.stream

    def getText(self):
        return self._text

    def __str__(self):
        return self._text


# Example
#if __name__ == '__main__':
#    hCode = QRCode()
#    hCode.genQR(text = "Hello World (www.0xbaadf00d.com)",
#                size = 500,
#                mask = "color2.png",
#                icon = "icon_a.png")
#    hCode.saveToFile("QRCode_1.png")
#    print hCode
#    hCode.genQR(text = "Hello World",
#                size = 256)
#    hCode.saveToFile("QRCode_2.png")
#    print hCode
