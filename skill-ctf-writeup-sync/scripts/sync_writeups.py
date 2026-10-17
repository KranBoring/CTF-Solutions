#!/usr/bin/env python3
"""Safe write-up index sync: exact mappings only, atomic writes, dry-run support."""
from pathlib import Path
import argparse, html, os, re, tempfile, unicodedata
from urllib.parse import unquote, urlsplit
NAMES={'challenge','name','exercise','bài'}; STATUS={'writeup','solution','writeupstatus'}
PLACE={'todo','tbd','chưa có write-up','coming soon','write-up coming soon'}
def norm(s):
 s=unicodedata.normalize('NFKD',s); s=''.join(c for c in s if not unicodedata.combining(c)).casefold(); return ''.join(c for c in s if c.isalnum())
def meaningful(p):
 try:s=p.read_text(encoding='utf-8-sig')
 except (OSError,UnicodeError): return False
 s=re.sub(r'<!--.*?-->','',s,flags=re.S); keep=[]
 for x in s.splitlines():
  x=x.strip()
  if not x or re.fullmatch(r'#{1,6}\s+.*',x) or x.rstrip('.:').casefold() in PLACE: continue
  keep.append(x)
 return bool(''.join(keep).strip())
def splitrow(line):
 s=line.rstrip('\r\n'); a=1 if s.startswith('|') else 0; b=len(s)-1 if s.endswith('|') else len(s); out=[]; start=a; esc=False
 for i in range(a,b):
  c=s[i]
  if c=='|' and not esc: out.append(s[start:i]); start=i+1
  esc=(c=='\\' and not esc)
  if c!='\\': esc=False
 out.append(s[start:b]); return out
def sep(c): return bool(c) and all(re.fullmatch(r'\s*:?-+:?\s*',x) for x in c)
def name(cell):
 m=re.search(r'\[([^]]+)\]\(',cell); return re.sub(r'<[^>]*>|`','',html.unescape(m.group(1) if m else cell)).strip()
def current(status,base):
 m=re.search(r'\[[^]]*\]\((?:<)?([^)>]*write-up\.md)(?:>)?\)',status)
 if not m or '://' in m.group(1): return None
 p=(base/m.group(1)).resolve()
 try:p.relative_to(base.resolve()); return p
 except ValueError:return None
def candidates(base,root):
 return [p.parent for p in base.rglob('write-up.md') if '.git' not in p.parts and 'skill-ctf-writeup-sync' not in p.parts and p.is_file()]
def choose(n,cell,base,root):
 ds=candidates(base,root); ex=[d for d in ds if norm(d.name)==norm(n)]
 if not ex:
  m=re.search(r'\]\((https?://[^)]+)\)',cell)
  if m:
   seg=unquote(urlsplit(m.group(1)).path.rstrip('/').split('/')[-1]); ex=[d for d in ds if norm(d.name)==norm(seg)]
 return (ex[0] if len(ex)==1 else None), ex
def atomic(p,text):
 fd,tmp=tempfile.mkstemp(dir=p.parent,prefix='.'+p.name+'.');
 try:
  with os.fdopen(fd,'w',encoding='utf-8',newline='') as f:f.write(text)
  os.replace(tmp,p)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
def process(p,root,dry):
 lines=p.read_text(encoding='utf-8').splitlines(True); changed=False; total=done=0; issues=[]
 for i in range(len(lines)-1):
  h=splitrow(lines[i]); s=splitrow(lines[i+1])
  if not h or len(h)!=len(s) or not sep(s):continue
  nh=[norm(x) for x in h]; ci=next((j for j,x in enumerate(nh) if x in NAMES),None); wi=next((j for j,x in enumerate(nh) if x in STATUS),None)
  if ci is None or wi is None:continue
  j=i+2
  while j<len(lines) and lines[j].strip() and '|' in lines[j]:
   c=splitrow(lines[j])
   if len(c)!=len(h):break
   total+=1; n=name(c[ci]); d=current(c[wi],p.parent); amb=[]
   if d is None or not (d/'write-up.md').is_file(): d,amb=choose(n,c[ci],p.parent,root)
   if len(amb)>1: issues.append(f'{n}: ambiguous ({", ".join(str(x.relative_to(p.parent)) for x in amb)})'); d=None
   if d and meaningful(d/'write-up.md'):
    done+=1; new=f' [Đọc write-up]({os.path.relpath(d/"write-up.md",p.parent).replace(os.sep,"/")}) '
   else:
    new=' Chưa có write-up '
    if d is None:issues.append(n)
   if c[wi]!=new:
    c[wi]=new; nl='|'+'|'.join(c)+'|'+ ('\r\n' if lines[j].endswith('\r\n') else '\n'); lines[j]=nl; changed=True
   j+=1
 if changed and not dry:atomic(p,''.join(lines))
 return done,total,issues,changed
def counts(root,totals,dry):
 pat=re.compile(r'(\]\()([^)]*README\.md)(\))\s*\(\s*\d+\s*/\s*\d+\s*\)'); n=0
 for p in root.rglob('README.md'):
  t=p.read_text(encoding='utf-8')
  def sub(m):
   nonlocal n; q=(p.parent/m.group(2)).resolve()
   if q not in totals:return m.group(0)
   n+=1; d,x=totals[q]; return f'{m.group(1)}{m.group(2)}{m.group(3)} ({d}/{x})'
  u=pat.sub(sub,t)
  if u!=t and not dry:atomic(p,u)
 return n
def main():
 a=argparse.ArgumentParser();a.add_argument('root',nargs='?',type=Path,default=Path.cwd());a.add_argument('--dry-run',action='store_true');x=a.parse_args();root=x.root.resolve(); totals={}; changes=0; issues=[]
 for p in sorted(root.rglob('README.md')):
  if '.git' in p.parts or 'skill-ctf-writeup-sync' in p.parts:continue
  d,t,u,c=process(p,root,x.dry_run)
  if t:totals[p.resolve()]=(d,t)
  changes+=int(c);issues += [f'{p.relative_to(root)}: {z}' for z in u]
 print(f'{"Would update" if x.dry_run else "Updated"} {changes} README tables and {counts(root,totals,x.dry_run)} progress links.')
 if issues:
  print('Unresolved:'); print('\n'.join('- '+z for z in issues))
if __name__=='__main__':main()
