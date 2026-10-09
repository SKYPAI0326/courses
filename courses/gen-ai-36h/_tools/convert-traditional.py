import ctypes
from pathlib import Path
c=ctypes.CDLL('/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation');ptr=ctypes.c_void_p;idx=ctypes.c_long
c.CFStringCreateWithCString.argtypes=[ptr,ctypes.c_char_p,ctypes.c_uint32];c.CFStringCreateWithCString.restype=ptr
c.CFStringCreateMutableCopy.argtypes=[ptr,idx,ptr];c.CFStringCreateMutableCopy.restype=ptr
c.CFStringTransform.argtypes=[ptr,ptr,ptr,ctypes.c_bool];c.CFStringTransform.restype=ctypes.c_bool
c.CFStringGetLength.argtypes=[ptr];c.CFStringGetLength.restype=idx
c.CFStringGetMaximumSizeForEncoding.argtypes=[idx,ctypes.c_uint32];c.CFStringGetMaximumSizeForEncoding.restype=idx
c.CFStringGetCString.argtypes=[ptr,ptr,idx,ctypes.c_uint32];c.CFStringGetCString.restype=ctypes.c_bool
c.CFRelease.argtypes=[ptr]
def trad(text):
 a=c.CFStringCreateWithCString(None,text.encode(),0x08000100);b=c.CFStringCreateMutableCopy(None,0,a);t=c.CFStringCreateWithCString(None,b'Simplified-Traditional',0x08000100);assert c.CFStringTransform(b,None,t,False);n=c.CFStringGetMaximumSizeForEncoding(c.CFStringGetLength(b),0x08000100)+1;out=ctypes.create_string_buffer(n);assert c.CFStringGetCString(b,out,n,0x08000100)
 for x in [a,b,t]:c.CFRelease(x)
 return out.value.decode()
assert trad('这门课引导学员')=='這門課引導學員'
root=Path(__file__).resolve().parents[1]
paths=list((root/'_repair/2026-10-09/lesson-plans').glob('*.md'))+list((root/'assets').glob('*.md'))+list((root/'assets').glob('*.txt'))+list((root/'assets').glob('*.csv'))+[root/'_repair/2026-10-09/lesson-meta.json']
for p in paths:p.write_text(trad(p.read_text()))
print('Traditional Chinese normalization:',len(paths),'text files')
