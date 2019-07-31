# Time-stamp: </Users/nico/_code/Python/lldbutils/structoffset.py, 2019-07-30 Tuesday 17:40:47 nico>

from __future__ import print_function
import lldb

def get_member_offset(ptype, m_name, target=lldb.target):
    if isinstance(ptype, basestring):
        ptype = target.FindFirstType(ptype)
    for mtype in ptype.get_fields_array():
        if mtype.GetName() == m_name:
            return hex(mtype.GetOffsetInBytes())

def get_struct_offsets(ttype, target=lldb.target):
    if isinstance(ttype, basestring):
        ttype = target.FindFirstType(ttype)
    offlist = list()
    for i in range(ttype.GetNumberOfFields()):
        mtype = ttype.GetFieldAtIndex(i)
        offlist.append((hex(mtype.GetOffsetInBytes()),
                           mtype.GetType().GetDisplayTypeName(),
                           mtype.GetType().GetByteSize(),
                           mtype.GetName()))
        if cmp(ttype.GetNumberOfFields(), i):
            poff = ttype.GetFieldAtIndex(i+1).GetOffsetInBytes() - (mtype.GetOffsetInBytes() + mtype.GetType().GetByteSize())
            if poff > 0:
                offlist.append((hex(mtype.GetOffsetInBytes()+mtype.GetType().GetByteSize()), 'char *[' + str(poff) + ']', poff, 'PADDING'))
    return offlist
            
            
def print_offsets(ttype, target=lldb.target):
    if isinstance(ttype, basestring):
        ttype = get_struct_offsets(ttype, target)
    for typeinfo in ttype:
        if typeinfo[1].endswith('*'):
            spc = ""
        else:
            spc = ' '
        print(typeinfo[0], '\t', typeinfo[2], '\t', typeinfo[1], spc, typeinfo[3], sep="")
