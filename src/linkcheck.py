import os,re,urllib.parse
import sys; root=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'); bad=[]; n=0
for d,_,fs in os.walk(root):
  for f in fs:
    if not f.endswith('.html'): continue
    p=os.path.join(d,f); s=open(p).read()
    for m in re.finditer(r'(?:href|src|srcset)="([^"]+)"',s):
      for u in m.group(1).split(','):
        u=u.strip().split(' ')[0]
        if not u.startswith('/') or u.startswith('//'): continue
        n+=1; path=urllib.parse.urlparse(u).path
        t=root+path
        if path.endswith('/'): t+='index.html'
        if not os.path.exists(t): bad.append((p.replace(root,''),u))
    # img alt check
    for img in re.findall(r'<img[^>]*>',s):
      if 'alt=' not in img: bad.append((p,'MISSING ALT '+img[:60]))
print(n,'internal refs checked; problems:',bad); sys.exit(1 if bad else 0)
