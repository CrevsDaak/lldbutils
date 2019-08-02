# Time-stamp: </Users/nico/_code/Python/lldbutils/funcdainfo.py, 2019-08-02 Friday 15:24:10 nico>

from __future__ import print_function
import lldb

def get_mangled_name(fname, target=lldb.target):
    for x in target.FindFunctions(fname):
        return x.GetSymbol().GetMangledName()
