#!/usr/bin/python

"""
This module defines Python wrapper for iMacros Scripting interface.
(c) Copyright 2009 iOpus Software GmbH - http://www.iopus.com
"""

import ctypes
import os, sys, platform, re


class __FuncTable:
    def __init__(self):

        libiopus = None

        if platform.system() == "Windows":
            try:
                libiopus = ctypes.windll.imtcp
            except OSError, e:
                sys.stderr.write('ERROR: %s\n' % str(e))
                return;
        else:
            try:
                # first try to find it somewhere
                libiopus = ctypes.cdll.LoadLibrary("libimtcp.so")
            except OSError, e:
                # now try to find it in the current directory
                try:
                    libiopus = ctypes.cdll.LoadLibrary("./libimtcp.so")
                except OSError, e:
                    # there is nothing left to do
                    sys.stderr.write('ERROR: %s\n' % str(e))
                    return;

        self.im_Init = libiopus.im_Init
        self.im_Init.argtypes = [ctypes.c_char_p, ctypes.c_char_p, \
                                     ctypes.c_char_p, \
                                     ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.im_Init.restype = ctypes.c_int

        self.im_Exit = libiopus.im_Exit
        self.im_Exit.argtypes = [ctypes.c_int]
        self.im_Exit.restype = ctypes.c_int

        self.im_SetVar = libiopus.im_SetVar
        self.im_SetVar.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.im_SetVar.restype = ctypes.c_int

        self.im_Play = libiopus.im_Play
        self.im_Play.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self.im_Play.restype = ctypes.c_int

        self.im_Display = libiopus.im_Display
        self.im_Display.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self.im_Display.restype = ctypes.c_int

        self.im_GetLastExtract = libiopus.im_GetLastExtract
        self.im_GetLastExtract.argtypes = [ctypes.c_char_p, ctypes.c_int,
                                           ctypes.c_int]
        self.im_GetLastExtract.restype = ctypes.c_int

        self.im_GetLastErrorText = libiopus.im_GetLastErrorText
        self.im_GetLastErrorText.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self.im_GetLastErrorText.restype = ctypes.c_int

        self.im_GetLastErrorNumber = libiopus.im_GetLastErrorNumber
        self.im_GetLastErrorNumber.argtypes = []
        self.im_GetLastErrorNumber.restype = ctypes.c_int

        self.im_TakeBrowserScreenshot = libiopus.im_TakeBrowserScreenshot
        self.im_TakeBrowserScreenshot.argtypes = [ctypes.c_char_p, \
                                                      ctypes.c_int,\
                                                      ctypes.c_int]
        self.im_TakeBrowserScreenshot.restype = ctypes.c_int

        self.im_GetLastPerformance = libiopus.im_GetLastPerformance
        self.im_GetLastPerformance.argtypes = [ctypes.c_int, \
                                          ctypes.c_char_p, ctypes.c_void_p, \
                                          ctypes.c_char_p, ctypes.c_void_p]
        self.im_GetLastPerformance.restype = ctypes.c_int


        

__ftbl = __FuncTable()
    

__port_number = 0               # 0 for pipes-based communication
__browser_location = None



# Error codes
ERR_OK = 1
ERR_FAIL = -1
ERR_TIMEOUT = -3



def enableLog(enable = True, path = "", debug = False):
    """
    Enable or disable output to log file and set log path
    """
    if enable == True:
        if platform.system() == "Windows":
            ctypes.windll.kernel32.SetEnvironmentVariableA("IMACROS_LOG", "ON")
            ctypes.windll.kernel32.SetEnvironmentVariableA("IMACROS_LOGPATH", \
                                                              path)
        else:
            os.environ["IMACROS_LOG"] = "ON"
            os.environ["IMACROS_LOGPATH"] = path
            if debug == True:
                os.environ["IMACROS_LOGLEVEL"] = "DEBUG"
            else:
                os.environ["IMACROS_LOGLEVEL"] = "ERROR"
    else:
        if platform.system() == "Windows":
            ctypes.windll.kernel32.SetEnvironmentVariable("IMACROS_LOG", "OFF")
        else:
            os.environ["IMACROS_LOG"] = "OFF"
    



def setPortNumber(port):
    """
    Set non-default port number for server.
    (Default port number for Google Chrome is 4590)
    Should be called before iimInit()
    """
    global __port_number
    __port_number = port


def setBrowserLocation(location):
    """
    Set non-default browser location.
    (This may be useful for e.g. portable version of browser)
    Should be called before iimInit()
    """
    global __browser_location
    __browser_location = location


# Print error to stderr
def __handle_im_error(rv, name):
    if rv != 0:
        required_size = __ftbl.im_GetLastErrorText(None, 0)
        b = ctypes.create_string_buffer(required_size)
        __ftbl.im_GetLastErrorText(b, len(b))
        e = __ftbl.im_GetLastErrorNumber()
        sys.stderr.write('%s error: %s, error code=%d\n' % (name, b.value, e))
        return e
    else:
        return ERR_OK


def iimInit(commandLine, openNewBrowser = True, timeout = 0):
    """
    Create new browser instance, start browser process if it is not started yet.
    See http://wiki.imacros.net/iimInit%28%29 for more info.
    """

    m = re.match(r'^-(\w+)(?:\s+(.*))?$', commandLine)
    if not m:
        raise RuntimeError('Wrong commandLine for iimInit')
    
    if not(m.group(1) == "cr" or m.group(1) == "fx"):
        raise RuntimeError('Only -cr (Google Chrome) or -fx (Firefox) browsers  supported')

    rv = __ftbl.im_Init(m.group(1), m.group(2),\
                            __browser_location, __port_number, \
                            (1 if openNewBrowser else 0), timeout)
    return __handle_im_error(rv, "iimInit()")


def iimPlay(macro, timeout = 0):
    """
    Replay macro. 
    See http://wiki.imacros.net/iimPlay%28%29 for more info.
    """
    rv = __ftbl.im_Play(macro, timeout)
    return __handle_im_error(rv, "iimPlay()")


def iimSet(var_name, var_value):
    """
    Set user variable for next macro replay.
    Should be called before each iimPlay() call to take effect.
    See http://wiki.imacros.net/iimSet%28%29 for more info.
    """
    rv = __ftbl.im_SetVar(var_name, var_value)
    return __handle_im_error(rv, "iimSet()")
    

def iimDisplay(message, timeout = 0):
    """
    Displays a message in the browser
    See http://wiki.imacros.net/iimDisplay%28%29 for more info.
    """
    rv = __ftbl.im_Display(message, timeout)
    return __handle_im_error(rv, "iimDisplay()")


def iimExit(timeout = 0):
    """
    Closes browser instance.
    See http://wiki.imacros.net/iimExit%28%29 for more info.
    """
    rv = __ftbl.im_Exit(timeout)
    return __handle_im_error(rv, "iimExit()")


def iimGetLastError():
    """
    Returns the text associated with the last error.
    See http://wiki.imacros.net/iimGetLastError%28%29 for more info.
    """
    required_size = __ftbl.im_GetLastErrorText(None, 0)
    b = ctypes.create_string_buffer(required_size)
    __ftbl.im_GetLastErrorText(b, len(b))
    return b.value
    

def iimGetLastExtract(index = 0):
    """
    Returns the contents of the !EXTRACT variable.
    See http://wiki.imacros.net/iimGetLastExtract%28%29 for more info.
    """
    required_size = __ftbl.im_GetLastExtract(None, 0, index)
    if required_size < 0:
        return None
    b = ctypes.create_string_buffer(required_size)
    __ftbl.im_GetLastExtract(b, len(b), index)
    return b.value



def iimTakeBrowserScreenshot(path, img_type, timeout = 0):
    """
    Takes screenshot of browser or web page
    See http://wiki.imacros.net/iimTakeBrowserScreenshot%28%29 for more info.
    """
    rv = __ftbl.im_TakeBrowserScreenshot(path, img_type, timeout)
    return __handle_im_error(rv, "iimTakeBrowserScreenshot")


def iimGetLastPerformance(idx = 0):
    """
    Returns the total runtime and STOPWATCH data for the most recent macro run.
    Returned object is tuple where first value indicates data presence,
    second value is STOPWATCH name, third is STOPWATCH value.
    If index equals 1 then total runtime is returned.

    See http://wiki.imacros.net/iimGetLastPerformance for more info.
    """
    # create int pointers for querying required buffer sizes
    name_sz = ctypes.pointer(ctypes.c_int(0))
    value_sz = ctypes.pointer(ctypes.c_int(0))
    rv = __ftbl.im_GetLastPerformance(idx, None, name_sz, None, value_sz)
    
    if rv < 0:
        return (False, "", "")

    name = ctypes.create_string_buffer(name_sz.contents.value)
    value = ctypes.create_string_buffer(value_sz.contents.value)
    __ftbl.im_GetLastPerformance(idx, name, name_sz, value, value_sz)
    
    return (True, name.value, value.value)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        print "No argument is given. Using Demo-FillForm.iim\n"+\
            "Usage imacros.py <macro>"
        arg = "Demo-FillForm.iim"

    if iimInit("-cr") != 0:
        print "iimInit() failed, error: "+iimGetLastError()
    else:
        rv = iimPlay(arg)
        print "Result of replaying "+arg+":\n"+\
            "Return value="+str(rv)+\
            "\nLast error="+iimGetLastError()+\
            "\nExtracted data="+iimGetLastExtract()
        iimExit()


