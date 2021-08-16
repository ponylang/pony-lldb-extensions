"""
Pony LLDB extensions
"""
# pylint: disable=W0613
# pylint: disable=C0103
import lldb


def pony_string_summary(value, *rest):
    """
    Prints the summary for a pony string
    """
    target = lldb.debugger.GetSelectedTarget()
    char_ptr_type = target.FindFirstType('char').GetPointerType()
    str_data = value.GetChildMemberWithName("_ptr").Cast(char_ptr_type)
    if str_data is None:
        return '<error getting `_ptr`>'
    size_vo = value.GetChildMemberWithName("_size")
    size = size_vo.GetValueAsUnsigned(0)
    if size == 0:
        return '""'
    data = str_data.GetPointeeData(0, size)
    error = lldb.SBError()
    bs = data.ReadRawData(error, 0, size)
    if bs is None:
        return '"<bs is stupid>": ' + error.description
    return '"%s"' % (bs.decode('utf-8').encode('utf-8'))


def pony_array_i32_summary(value, *rest):
    """
    Prints the summary for a pony i32 array
    """
    target = lldb.debugger.GetSelectedTarget()
    u32_ptr_type = target.FindFirstType('int').GetPointerType()
    a_data = value.GetChildMemberWithName("_ptr").Cast(u32_ptr_type)
    if a_data is None:
        return '<error getting `_ptr`>'
    size_vo = value.GetChildMemberWithName("_size")
    size = size_vo.GetValueAsUnsigned(0)
    if size == 0:
        return '[]'

    v = []
    for i in range(size):
        d = a_data.GetChildAtIndex(i, 0, 1).GetData()
        e = lldb.SBError()
        x = d.GetSignedInt32(e, 0)
        if x is None:
            return '<error reading item>'
        v.append(x)

    return ' '.join(["[%d]=%d" % (i, x) for (i, x) in enumerate(v)])


def pony_array_u32_summary(value, *rest):
    """
    Prints the summary for a pony u32 array
    """
    target = lldb.debugger.GetSelectedTarget()
    u32_ptr_type = target.FindFirstType('int').GetPointerType()
    a_data = value.GetChildMemberWithName("_ptr").Cast(u32_ptr_type)
    if a_data is None:
        return '<error getting `_ptr`>'
    size_vo = value.GetChildMemberWithName("_size")
    size = size_vo.GetValueAsUnsigned(0)
    if size == 0:
        return '[]'

    v = []
    for i in range(size):
        d = a_data.GetChildAtIndex(i, 0, 1).GetData()
        e = lldb.SBError()
        x = d.GetUnsignedInt32(e, 0)
        if x is None:
            return '<error reading item>'
        v.append(x)

    return ' '.join(["[%d]=%08x" % (i, x) for (i, x) in enumerate(v)])


def pony_array_u8_summary(value, *rest):
    """
    Prints the summary for a pony u8 array
    """
    target = lldb.debugger.GetSelectedTarget()
    u8_ptr_type = target.FindFirstType('char').GetPointerType()
    a_data = value.GetChildMemberWithName("_ptr").Cast(u8_ptr_type)
    if a_data is None:
        return '<error getting `_ptr`>'
    size_vo = value.GetChildMemberWithName("_size")
    size = size_vo.GetValueAsUnsigned(0)
    if size == 0:
        return ''

    data = a_data.GetPointeeData(0, size)
    error = lldb.SBError()
    bs = data.ReadRawData(error, 0, size)
    if bs is None:
        return '"<bs is stupid>": ' + error.description
    return _hex_dump([ord(b) for b in bs])


def _hex_dump(bs):
    columns_per_row = 16
    total_rows = len(bs) / columns_per_row
    rows = []
    for i in range(0, total_rows + 1):
        row_start = i * columns_per_row
        row_data = bs[row_start:(row_start + columns_per_row)]
        row_num = ("%08x" % (row_start,))
        nums = ' '.join(["%02x" % (b,) for b in row_data])
        protected_chars = ''.join([_char_or_dot(chr(b)) for b in row_data])
        rows.append("%s: %s |%s|" % (row_num, nums.ljust(50),
                                     protected_chars.ljust(columns_per_row)))
    return '\n' + '\n'.join(rows)


def _char_or_dot(c):
    if ord(c) < 32:
        return '.'
    return c


def _register_summary(debugger, function_name, type_name):
    print("registering '%s'" % (type_name,))
    summary = lldb.SBTypeSummary.CreateWithFunctionName(function_name)
    summary.SetOptions(lldb.eTypeOptionHideChildren)
    debugger.GetDefaultCategory().AddTypeSummary(
        lldb.SBTypeNameSpecifier(type_name, False), summary )


def __lldb_init_module(debugger, *rest):
    _register_summary(debugger, 'pony_lldb.pony_string_summary', 'String *')

    for refcap in ['ref', 'val', 'box']:
        type_name = "Array_I32_%s *" % (refcap,)
        _register_summary(debugger, 'pony_lldb.pony_array_i32_summary',
                          type_name)

    for refcap in ['ref', 'val', 'box']:
        type_name = "Array_U32_%s *" % (refcap,)
        _register_summary(debugger, 'pony_lldb.pony_array_u32_summary',
                          type_name)

    for refcap in ['ref', 'val', 'box']:
        type_name = "Array_U8_%s *" % (refcap,)
        _register_summary(debugger, 'pony_lldb.pony_array_u8_summary',
                          type_name)
