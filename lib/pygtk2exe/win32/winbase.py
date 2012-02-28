# -*- coding: utf-8 -*-

# Copyright © 2010-2012 pygtk2exe Contributors
#
# This file is part of pygtk2exe.
#
# pygtk2exe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pygtk2exe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pygtk2exe. If not, see <http://www.gnu.org/licenses/>.


import ctypes


NULL        = None
LPVOID      = ctypes.c_void_p
DWORD       = ctypes.c_uint
UINT        = ctypes.c_uint
LPWSTR      = ctypes.c_wchar_p
va_list = ctypes.c_char_p

MAX_PATH    = 260

FORMAT_MESSAGE_ALLOCATE_BUFFER = 0x00000100
FORMAT_MESSAGE_ARGUMENT_ARRAY  = 0x00002000
FORMAT_MESSAGE_FROM_HMODULE    = 0x00000800
FORMAT_MESSAGE_FROM_STRING     = 0x00000400
FORMAT_MESSAGE_FROM_SYSTEM     = 0x00001000
FORMAT_MESSAGE_IGNORE_INSERTS  = 0x00000200
FORMAT_MESSAGE_MAX_WIDTH_MASK  = 0x000000FF
FORMAT_MESSAGE_FROM_HMODULE    = 0x00000800
FORMAT_MESSAGE_FROM_STRING     = 0x00000400


def RaiseIfZero(result, func = None, arguments = ()):
    if not result:
        raise ctypes.WinError()
    return result

def GetLastError():
    _GetLastError = ctypes.windll.kernel32.GetLastError
    _GetLastError.argtypes = []
    _GetLastError.restype  = DWORD

    return _GetLastError()

def FormatMessage(dwMessageId):
    _FormatMessage = ctypes.windll.kernel32.FormatMessageW
    _FormatMessage.argtypes = [DWORD, LPVOID, DWORD, DWORD, LPWSTR, DWORD, va_list]
    _FormatMessage.restype = DWORD
    _FormatMessage.errcheck = RaiseIfZero

    dwFlags = FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS | FORMAT_MESSAGE_MAX_WIDTH_MASK
    lpSource = NULL
    dwLanguageId = 0
    lpBuffer = ctypes.create_unicode_buffer(u'', MAX_PATH)
    nSize = len(lpBuffer)
    Arguments = NULL

    if not _FormatMessage(dwFlags, lpSource, dwMessageId, dwLanguageId, lpBuffer, nSize, Arguments):
        return 'Format message failed with 0x%x\nOriginal error was %s', [GetLastError(), dwMessageId]
    else:
        return lpBuffer.value

def GetSystemDirectory():
    _GetSystemDirectory = ctypes.windll.kernel32.GetSystemDirectoryW
    _GetSystemDirectory.argtypes = [LPWSTR, UINT]
    _GetSystemDirectory.restype = UINT

    lpBuffer = ctypes.create_unicode_buffer(u'', MAX_PATH)
    nSize = len(lpBuffer)

    retval = _GetSystemDirectory(lpBuffer, nSize)
    if retval == 0:
        dwMessageId = GetLastError()
        message = FormatMessage(dwMessageId)
        raise ctypes.WinError(dwMessageId, message)
    elif retval > nSize:
        # Virtually no chance of ever hitting this without Microsoft breaking
        # backward compatibility with every piece of code ever written depending
        # on MAX_PATH, before extended length paths where introduced...
        raise NotImplementedError('Extended length paths are not yet implemented.')
    else:
        return lpBuffer.value
