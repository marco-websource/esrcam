#!/usr/bin/python3
import numpy as np
import cv2
import pytesseract
import re
import pyperclip
from time import sleep

verbose = False

part1 = None
part2 = None
part3 = None
part4 = None
part23 = None

def check_digit(code):
    check_table = [0,9,4,6,8,2,7,1,3,5]
    rem = 0
    for c in code[0:-1]:
        r = rem + int(c)
        rem = check_table[r%10]
    check = (10-rem)%10
    if int(code[-1]) == check:
        return True
    else:
        return False

def capture():
    global part1,part2,part3,part4,part23
    cap = cv2.VideoCapture(0)

    part1 = None
    part2 = None
    part3 = None
    part4 = None
    part23 = None
    framecount = 0
    stop = 0

    while(True):
        ret, frame = cap.read()
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_flip = cv2.flip(frame,1)
        for i,part in enumerate([part1,part2,part3,part4]):
            if part:
                color = (0,255,0)
            else:
                color = (0,0,255)
            cv2.putText(frame_flip,'%d'%(i+1),(10+i*50,460),cv2.FONT_HERSHEY_SIMPLEX,2,color,2)

        cv2.imshow('frame',frame_flip)
        if stop != 0:
            cap.release()
            return stop

        framecount += 1
        if framecount > 20:
            framecount = 0
            detect_esr_code(frame)
            if part1 and part23 and part4:
                stop = 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop = -1

def detect_esr_code(frame):
    global part1,part2,part3,part4,part23
    
    ocr = pytesseract.image_to_string(frame,config='--oem 3 --psm 11')

    if not part1:
        m = re.search('01\d{11}>', ocr)
        if not m:
            m = re.search('04\d>', ocr)
        if m:
            part1 = m.group(0)
            if check_digit(part1[0:-1]):
                if verbose:
                    print('part1 = %s' % part1)
            else:
                print("WARNING: part1 has wrong check digit: %s" % part1)
                part1 = None
    if not part2:
        m = re.search('>\d{14,27}', ocr)
        if m:
            part2 = m.group(0)
            if verbose:
                print('part2 = %s' % part2)
    if not part3:
        m = re.search('\d{14,27}\+', ocr)
        if m:
            part3 = m.group(0)
            if verbose:
                print('part3 = %s' % part3)
    if not part4:
        m = re.search('\+\s*\d{9}>', ocr)
        if m:
            part4 = m.group(0)
            if check_digit(part4[-10:-1]):
                if verbose:
                    print('part4 = %s' % part4)
            else:
                print("WARNING: part4 has wrong check digit: %s" % part4)
                part4 = None

    if part2 and part3 and not part23:
        ## Assemble part2+3
        overlap = len(part2)+len(part3)-(27+2)
        #print('overlap = %d' % overlap)
        part2a = part2[0:-overlap]
        part2b = part2[-overlap:]
        part3a = part3[0:overlap]
        part3b = part3[overlap:]
        #print(' %s | %s' % (part2a,part2b))
        #print(' %s | %s' % (part3a,part3b))
        part23 = '%s%s%s' % (part2a,part2b,part3b)

        if (part2b != part3a):
            print("WARNING: Overlap does not match! Rejecting part2 and part3.")
            part2 = None
            part3 = None
            part23 = None
            return

        if not check_digit(part23[1:-1]):
            print("WARNING: part4 has wrong check digit: %s" % part4)
            part2 = None
            part3 = None
            part23 = None

def main():
    global part1,part2,part3,part4,part23
    while(True):
        ret = capture()
        if ret == -1:
            return
        else:
            code = '%s%s%s' % (part1,part23[1:],part4[1:])
            pyperclip.copy(code)
            print('Copied code to clipboard: %s' % code)
            for i in range(0,20):
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return
                sleep(0.1)
    
main()
cv2.destroyAllWindows()

#EOF
