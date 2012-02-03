import sys
import os
import re
import doctest
import shutil
import subprocess

subprocess.call([sys.executable, 'setup.py', 'build_ext', '--inplace'])
sys.path.insert(0, os.getcwd())
import bitarray

assert bitarray.test().wasSuccessful()

print 'Backup README.rst'
shutil.copyfile('README.rst', 'README.bak')

print 'Writing new README.rst'
fo = open('README.rst', 'w')

# Copy everything before 'Reference' while substituting the version number
_ver_pat = re.compile(r'(bitarray.+?)(\d+\.\d+\.\d+)')
for line in open('README.bak'):
    if line == 'Reference\n':
        break
    fo.write(_ver_pat.sub(lambda m: m.group(1) + bitarray.__version__, line))

sig_pat = re.compile(r'(\w+\([^()]*\))( -> (.+))?')
def writedoc(name):
    print name,
    doc = eval('bitarray.%s.__doc__' % name)
    lines = doc.splitlines()
    m = sig_pat.match(lines[0])
    if m is None:
        raise Exception("signature line invalid: %r" % lines[0])
    s = '``%s``' %  m.group(1)
    if m.group(3):
        s += ' -> %s' % m.group(3)
    fo.write(s + '\n')
    assert lines[1] == ''
    for line in lines[2:]:
        fo.write('   %s\n' % line)
    fo.write('\n\n')

fo.write("""\
Reference
---------

**The bitarray class:**

""")

writedoc('bitarray')

fo.write("""\
**A bitarray object supports the following methods:**

""")

for method in sorted(dir(bitarray.bitarray)):
    if method.startswith('_'):
        continue
    writedoc('bitarray.%s' % method)

fo.write("""\
**Functions defined in the module:**

""")

writedoc('test')

writedoc('bits2bytes')

fo.close()
print

print 'doctest'
doctest.testfile('README.rst')

# --------- html

print 'Writing html'
os.system('rst2html.py README.rst >README.html')
