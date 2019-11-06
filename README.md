# esrcam
Simple program to scan Swiss payment slips (ESR) with a webcam

## Usage

Start the program and move the payment slip in front of the camera until all four parts are recognized (numbers turn green on the webcam image).
When all four numbers are green, the payment slip code is available in the clipboard and can, e.g., be pasted in your e-banking form.

## Requirements

- python
- numpy
- cv2
- pytesseract
- pyperclip

## Status

This is a quick hack that currently works for me. It can probably be improved quite a bit.

## More information

More information on Swiss payment slips (ESR/ESR+) can be found at https://www.postfinance.ch/esr.
- Check digit calculation: https://www.postfinance.ch/content/dam/pfch/doc/cust/download/modulo_biz_de.pdf
- Handbuch ESR 499.36 https://www.gkb.ch/de/Documents/DC/Beratung-Produkte/Factsheets-Flyers/Handbuch-ESR/ESR-Handbuch-Postfinance-DE.pdf
