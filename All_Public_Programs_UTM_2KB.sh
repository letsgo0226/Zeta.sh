command -v python3>/dev/null||exit 127;python3 -c 'import sys,json as j,urllib.request as u,base64 as b;A="letsgo0226";H={"User-Agent":"PUBLIC-UTM"};G=lambda x:j.loads(u.urlopen(u.Request(x,headers=H)).read());R=[];p=1
while 1:
 z=G("https://api.github.com/users/%s/repos?per_page=100&page=%d"%(A,p));R+=z
 if len(z)<100:break
 p+=1
R=sorted(x for x in R if not x["private"] and not x["fork"] and x["name"]!="API",key=lambda x:x["name"]);F=[]
for r in R:
 try:t=G("https://api.github.com/repos/%s/%s/git/trees/%s?recursive=1"%(A,r["name"],r["default_branch"]))["tree"]
 except:continue
 for x in t:
  if x.get("type")=="blob" and x["path"].lower().endswith((".py",".sh",".c",".h",".cpp",".js",".ts",".java",".go",".rs",".rb",".pl",".lua",".hs",".ml")):F.append((r["name"],x["path"],x["sha"]))
S=j.dumps(F,separators=(",",":"),ensure_ascii=False).encode();E=lambda x:int.from_bytes(b"\1"+x,"big");D=lambda n:n.to_bytes((n.bit_length()+7)//8,"big")[1:];g=E(S);print(j.dumps({"model":"ALL_PUBLIC_PROGRAMS_UTM","owner":A,"repos":len(R),"program_blobs":len(F),"state":"canonical(repo,path,blob_sha) corpus","godel_bits":g.bit_length(),"exact_manifest_roundtrip":D(g)==S,"utm":"U(<program,input>) simulates each computable program; manifest is its account corpus","snapshot":0,"programs_embedded":0,"network_required":1,"omega":"formal colim","omega_attained":0,"program_equals_zeta":0,"open":1,"final":0},separators=(",",":")))' "$@"