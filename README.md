# Pony LLDB Extensions

This is a collection of LLDB extensions for working with the [Pony programming language](https://ponylang.org).

For more information about using LLDB with Pony programs, see [The Pony LLDB Cheatsheet](https://www.ponylang.org/reference/pony-lldb-cheatsheet/).

## Installing

Installation is a matter of putting the `pony_lldb.py` file somewhere.

## Usage

These scripts work with LLDB. You can load them into LLDB by running the following command at the LLDB prompt:
```
command script import PONY_LLDB_PATH/pony_lldb.py
```
where `PONY_LLDB_PATH` is the path to the directory where you installed the Python file.

Currently the script installs a few summary functions that allow you to print the values of variables of the following types:

```
String
Array[U8] ref
Array[U8] val
Array[U8] box
Array[U32] ref
Array[U32] val
Array[U32] box
Array[I32] ref
Array[I32] val
Array[I32] box
```

To print a value, type `p VARIABLE_NAME` at the LLDB command prompt.

### String

`String` variables are printed as quoted strings. If `s2` is a `String` with the value `"bc"` then you can print it like this:

```
(lldb) p s2
(String *) $7 = 0x0000000100023940 "bc"
```

### Array[U8]

`Array[U8]` variables are printed out using a pretty-printer that looks similar to the output of the `hexdump` command. If `a3` is an `Array[U8]` with the values `0` through `66` the you can print it like this:

```
(lldb) p a3
(Array_U8_val *) $3 = 0x0000000108fd5d20
00000000: 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f    |................|
00000010: 10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f    |................|
00000020: 20 21 22 23 24 25 26 27 28 29 2a 2b 2c 2d 2e 2f    | !"#$%&'()*+,-./|
00000030: 30 31 32 33 34 35 36 37 38 39 3a 3b 3c 3d 3e 3f    |0123456789:;<=>?|
00000040: 40 41 42                                           |@AB             |
```

The first column is the starting index of the row. The second column is the hex values of the array in the given range. The third column is an ASCII representation of the values in the given range, with `.` displayed for unprintable characters.

### Array[U32]

`Array[U32]` variables are printed as the index and the value of each element, with the value printed in hexidecimal form. If `a1` is an `Array[U32]` with the values `0`, `1`, and `2` then you can print it like this:

```
(lldb) p a1
(Array_U32_val *) $8 = 0x0000000108fd5ca0 [0]=00000001 [1]=00000002 [2]=00000003
```

### Array[I32]

`Array[I32]` variables are printed as the index and the value of each element, with the value printed in hexidecimal form. If `a4` is an `Array[I32]` with the values `-20` through `19` then you can print it like this:

```
(lldb) p a4
(Array_I32_val *) $11 = 0x0000000108fd5d60 [0]=-20 [1]=-19 [2]=-18 [3]=-17 [4]=-16 [5]=-15 [6]=-14 [7]=-13 [8]=-12 [9]=-11 [10]=-10 [11]=-9 [12]=-8 [13]=-7 [14]=-6 [15]=-5 [16]=-4 [17]=-3 [18]=-2 [19]=-1 [20]=0 [21]=1 [22]=2 [23]=3 [24]=4 [25]=5 [26]=6 [27]=7 [28]=8 [29]=9 [30]=10 [31]=11 [32]=12 [33]=13 [34]=14 [35]=15 [36]=16 [37]=17 [38]=18 [39]=19
```

## Contributing

Feel free to open PRs against this project.
