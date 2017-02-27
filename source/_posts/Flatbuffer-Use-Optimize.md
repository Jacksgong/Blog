title: Flatbuffer Use Optimize
date: 2015-01-05 08:35:03
permalink: 2015/01/05/Flatbuffer-Use-Optimize
categories:
- 开源项目
tags:
- flatbuffer
- optimize
- python
- 项目

---

### 一. Tool Launguage
python.

### 二. Cause
1. `__offset()` method is not fast enough.
2. for get a varaible may need to calls `__offset()` method many times.

### 三. Effect
1. Add has set method for flatbuffer file.
2. Add member variables cache (include array variables).

<!--more-->

### 四. Exp

origin:

```
public int top() { int o = __offset(4); return o != 0 ? bb.getInt(o + bb_pos) : 0; }
```

convert to:

```
  public boolean has_top_cache = false;
  public int top_cache;
  public int top() { if ( has_top_cache ) { return top_cache; }  int o = __offset(4); top_cache = o != 0 ? bb.getInt(o + bb_pos) : 0;  has_top_cache= true; return top_cache; }
  public boolean hasSetValue_top = false;
  public boolean hasSet_top() { if ( hasSetValue_top ) { return true; }  if ( has_top_cache  ) { return top_cache != 0; } int o = __offset(4); if (o == 0) { has_top_cache = true; top_cache = 0; return false; } else { hasSetValue_top = true; return true; } }
 ```

origin:

```
public String fontFamily(int j) { int o = __offset(10); return o != 0 ? __string(__vector(o) + j * 4) : null; }
```

convert to:

```
public int list_fontFamily_offset = -1;
public android.util.SparseArray<String> fontFamily_cache = new android.util.SparseArray<String>();
public String fontFamily(int j) { if ( fontFamily_cache.get(j) != null ) { return fontFamily_cache.get(j); }  int o = list_fontFamily_offset != -1? list_fontFamily_offset : __offset(10); String value =  o != 0 ? __string(__vector(o) + j * 4) : null;  list_fontFamily_offset = o; fontFamily_cache.put( j, value); return value; }
public boolean hasSet_fontFamily() { if ( list_fontFamily_offset != -1 ) { return list_fontFamily_offset != 0; } list_fontFamily_offset = __offset(10); return list_fontFamily_offset!= 0; }
```

### 五. Tips

Flatbuffer is very fast from flatbuffer instream to avaliable object, but `__offset()` is very slow, so very frequently invoked almost not recommended. I tested 100,000 times `__offset()`, consuming greater than 50ms, but Java object directly accesse the same time only need 2~3ms. So such tool is come, but you need to pay attention to the increase of the GC.


### 六. Tool Source

GitHub: [https://github.com/Jacksgong/FlatBuffer-Optimize](https://github.com/Jacksgong/FlatBuffer-Optimize)

```
import os

__author__ = 'Jacks gong'
__date__ = 'Jan 4, 2015'


def has_set(line=''):
    has_set_method = ''
    if line.isspace():
        return ''
    return has_set_method


def cache_obj(line=''):
    return ''


def file_list(rootDir):
    list = []
    for root, dirs, files in os.walk(rootDir):
        for filespath in files:
            list.append(os.path.join(root, filespath))
    return list


def is_java(path=''):
    return path.endswith('.java')


def is_valid_deal(line=''):
    return '__offset(' in line and 'public ' in line


def get_type(line=''):
    values = line.split(' ')

    type_index = 0
    for value in values:
        type_index += 1
        if value == 'public':
            break

    if type_index >= len(values):
        return ''

    return values[type_index]


def get_value_name(line=''):
    values = line.split(' ')

    for value in values:
        if not '(' in value:
            continue
        return value[:value.find('(')]

    return ''


def is_list(line=''):
    return 'int j' in line[line.find('('):line.find(')')]


def get_offset(line=''):
    offset_pre = '__offset('
    offset_nums = line[line.find(offset_pre) + len(offset_pre):]
    return offset_nums[:offset_nums.find(')')]


def get_base_type_object(type=''):
    if not type in base_type:
        return type
    return base_type_object[base_type.index(type)]


base_type = ('int', 'float', 'long', 'boolean', 'uint', 'byte', 'ulong')
base_type_object = ('Integer', 'Float', 'Long', 'Boolean', 'Integer', 'Byte', 'Long')


def main():
    flatc_path = raw_input('flatbuffer absolute path: ')

    list = file_list(flatc_path)

    for path in list:
        if not is_java(path):
            continue
        file_read = open(path)
        lines = file_read.readlines()
        file_read.close()

        print(path)
        file_write = open(path, 'w')

        for line in lines:
            while True:
                if line.isspace():
                    break

                if not is_valid_deal(line):
                    break

                type = get_type(line)
                value_name = get_value_name(line)
                if type.isspace() or value_name.isspace():
                    break;

                offset_nums = get_offset(line)

                cache_name = value_name + '_cache'

                if is_list(line):
                    list_offset = 'list_' + value_name + '_offset'
                    has_set_list_def = '  public int ' + list_offset + ' = -1;\n'

                    type_object = get_base_type_object(type);
                    cache_def = '  public android.util.SparseArray<' + type_object + '> ' + cache_name + ' = new android.util.SparseArray<' + type_object + '>();\n'

                    origin_method_pre = line[0:line.index('{') + 1] + \
                                        ' if ( ' + cache_name + '.get(j) != null ) { return ' + cache_name + '.get(j); } '
                    origin_method_mid = line[line.index('{') + 1: line.index('}')]
                    origin_method_mid = origin_method_mid.replace('__offset', list_offset + ' != -1? ' + list_offset + ' : __offset')
                    origin_method_mid = origin_method_mid.replace('return', type + ' value = ')
                    origin_method_end = ' ' + list_offset + ' = o; ' + cache_name + '.put( j, value); return value; }'
                    origin_method_def = origin_method_pre + origin_method_mid + origin_method_end + '\n'

                    has_set_method_pre = '  public boolean hasSet_' + value_name + '() { if ( ' + list_offset + ' != -1 ) { return ' + \
                                         list_offset + ' != 0; } '
                    has_set_method_mid = list_offset + ' = __offset(' + offset_nums + '); '
                    has_set_method_end = 'return ' + list_offset + '!= 0; }'

                    has_set_method_def = has_set_method_pre + has_set_method_mid + has_set_method_end + '\n'

                    line = has_set_list_def + cache_def + origin_method_def + has_set_method_def;
                    print(line)

                    break;

                has_set_value_name = 'hasSetValue_' + value_name
                has_set_value_def = '  public boolean ' + has_set_value_name + ' = false; \n'

                has_cache = 'has_' + value_name + '_cache'
                has_cache_def = '  public boolean ' + has_cache + ' = false;\n'

                cache_def = '  public ' + type + ' ' + cache_name + ';\n'

                origin_method_pre = line[0:line.index('{') + 1] + \
                                    ' if ( ' + has_cache + ' ) { return ' + cache_name + '; } '

                origin_method_mid = line[line.index('{') + 1: line.index('}')]

                origin_method_mid = origin_method_mid.replace('return', cache_name + ' =')

                origin_method_end = ' ' + has_cache + '= true; return ' + cache_name + '; }'

                origin_method_def = origin_method_pre + origin_method_mid + origin_method_end + '\n'

                has_set_method_pre = '  public boolean hasSet_' + value_name + '() { if ( ' + has_set_value_name + ' ) { return true; } '

                has_set_method_mid = ' if ( ' + has_cache + '  ) { return ' + cache_name
                if type in base_type:
                    has_set_method_mid += ' != 0; } int o = __offset(' + offset_nums + '); if (o == 0) { ' + \
                                          has_cache + ' = true; ' + cache_name + ' = 0; return false; } '
                else:
                    has_set_method_mid += ' != null; } int o = __offset( ' + offset_nums + ' ); if (o == 0) { ' + \
                                          has_cache + ' = true; ' + cache_name + ' = null; return false; } '

                has_set_method_end = 'else { ' + has_set_value_name + ' = true; return true; } }';

                has_set_method_def = has_set_method_pre + has_set_method_mid + has_set_method_end + '\n'

                line = has_cache_def + cache_def + origin_method_def + has_set_value_def + has_set_method_def;

                print(line)
                break;
            line += '\n'
            file_write.write(line)

        file_write.close()


main()
```

---

> © 2012 - 2017, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
