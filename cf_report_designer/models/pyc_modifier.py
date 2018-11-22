# -*- coding: utf-8 -*-
#
# ========================================================================================
# 根据
# https://blog.csdn.net/ir0nf1st/article/details/61962197
#  文所讲的原理，在bytecode加载code object常量表的第65535项到栈顶（一般的代码中没有这么多的常量，所以加载65536号常量
# 是加载不到的，反编译器会出错），然后用
#  JUMP_ABSOLUTE 6
# 来跳过第二步操作，使得程序可以运行，但反编译时出错，更好地防止反编译器。
# 这种方式的优点是：没有增加额外的代码，也不增加额外的so或dll，保证程序的兼容性
# 这种方式的缺点是：可以防止一般人员使用工具反编译pyc文件，但对于懂字节码的人是无效的。
#
#
#  用法：
#  python pyc_modifier.py -p <start path> -p <Compile python file?(Y/N)>
#  或
#  python pyc_modifier.py --path=<start path> --compile=<Y/N>
#
#  康虎软件工作室
#  QQ: 360026606
#  微信： 360026606
#
# ========================================================================================
import sys, os, getopt
import marshal, dis
import py_compile

def find_files(path, path_list = [], ext = "pyc"):
    files = os.listdir(path);
    for f in files:
        npath = path + '/' + f;
        if(os.path.isfile(npath)):
            if(os.path.splitext(npath)[1] == "."+ext):
                path_list.append(npath);
        if(os.path.isdir(npath)):
            if (f[0] == '.'):
                pass;
            else:
                find_files(npath, path_list, ext)

def compile_py(fname):
    """编译py文件"""


def change_pyc(fname):
    """修改pyc文件，防逆向"""

    with open(fname, 'rb') as fd:  # Read the binary file
        magic = fd.read(4)
        timestamp = fd.read(4)
        code = fd.read()

    code_obj = marshal.loads(code)
    # magic, timestamp, code

    co = code_obj
    bcode = co.co_code
    bcode = list(bcode)

    # #增加   JUMP_ABSOLUTE 3   指令
    # bcode.insert(0, "\x00")
    # bcode.insert(0, "\x03")
    # bcode.insert(0, "\x71")

    #增加  LOAD_CONST  65535   指令（错误指令）
    bcode.insert(0, "\x64")
    bcode.insert(0, "\xFF")
    bcode.insert(0, "\xFF")
    #增加   JUMP_ABSOLUTE 6   指令
    bcode.insert(0, "\x00")
    bcode.insert(0, "\x06")
    bcode.insert(0, "\x71")

    bcode = "".join(bcode)

    import new

    co2 = new.code(co.co_argcount,
                   co.co_nlocals,
                   co.co_stacksize,
                   co.co_flags,
                   bcode,
                   co.co_consts,
                   co.co_names,
                   co.co_varnames,
                   co.co_filename,
                   co.co_name,
                   co.co_firstlineno,
                   co.co_lnotab)

    # code_obj = co2
    # dis(code_obj)

    # 序列化到文件中
    # fd = open(os.path.join( os.getcwd(),'getip_2.pyc'), 'wb')
    with open(os.path.join(os.getcwd(), fname), 'wb') as fd:
        fd.write(magic)
        fd.write(timestamp)
        marshal.dump(co2, fd)

def help():
    print('Usage: pyc_modifier.py -p <start path> -p <Compile python file?(Y/N)>')
    print('   or: pyc_modifier.py --path=<start path> --compile=<Y/N>')

def main(args):
    try:
        """
            options, args = getopt.getopt(args, shortopts, longopts=[])

            参数args：一般是sys.argv[1:]。过滤掉sys.argv[0]，它是执行脚本的名字，不算做命令行参数。
            参数shortopts：短格式分析串。例如："hp:i:"，h后面没有冒号，表示后面不带参数；p和i后面带有冒号，表示后面带参数。
            参数longopts：长格式分析串列表。例如：["help", "ip=", "port="]，help后面没有等号，表示后面不带参数；ip和port后面带冒号，表示后面带参数。

            返回值options是以元组为元素的列表，每个元组的形式为：(选项串, 附加参数)，如：('-i', '192.168.0.1')
            返回值args是个列表，其中的元素是那些不含'-'或'--'的参数。
        """
        opts, args = getopt.getopt(args, "hp:c:", ["help", "path=", "compile="])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    if len(opts)<1:
        help()
        return

    start_path = "."
    is_compile = True
    # 处理 返回值options是以元组为元素的列表。
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit()
        elif opt in ("-p", "--path"):
            start_path = arg
        elif opt in ("-c", "--compile"):
            if arg.lower() == "Y":
                is_compile = True

    f_list = []
    #编译python源文件
    if is_compile:
        find_files(start_path, f_list, "py")
        for f in f_list:
            py_compile.compile(f)

    f_list = []
    find_files(start_path, f_list, "pyc")
    for f in f_list:
        change_pyc(f)

    print(u"Python加密处理完毕！")

if __name__ == "__main__":
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以用sys.argv[1:]过滤掉脚本名。
    main(sys.argv[1:])