import hashlib,json,secrets,struct,math
from Crypto.Util.number import bytes_to_long as B2L,long_to_bytes as L2B,getPrime,inverse
from Crypto.Cipher import AES
EP=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
EN=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
EGx=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
EGy=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
def _add(A,B,p=EP):
    if A is None:return B
    if B is None:return A
    x1,y1=A;x2,y2=B
    if x1==x2:
        if y1!=y2:return None
        l=3*x1*x1*pow(2*y1,-1,p)%p
    else:l=(y2-y1)*pow(x2-x1,-1,p)%p
    x3=(l*l-x1-x2)%p;return x3,(l*(x1-x3)-y1)%p
def _mul(k,T,p=EP):
    R,Q=None,T
    while k:
        if k&1:R=_add(R,Q,p)
        Q=_add(Q,Q,p);k>>=1
    return R
SK=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]
rr=lambda x,n:((x>>n)|(x<<(32-n)))&0xFFFFFFFF
def _sc(st,bl):
    w=list(struct.unpack('>16I',bl))
    for i in range(16,64):w.append((w[i-16]+(rr(w[i-15],7)^rr(w[i-15],18)^(w[i-15]>>3))+w[i-7]+(rr(w[i-2],17)^rr(w[i-2],19)^(w[i-2]>>10)))&0xFFFFFFFF)
    a,b,c,d,e,f,g,h=st
    for i in range(64):
        t1=(h+(rr(e,6)^rr(e,11)^rr(e,25))+((e&f)^(~e&g))+SK[i]+w[i])&0xFFFFFFFF
        t2=((rr(a,2)^rr(a,13)^rr(a,22))+((a&b)^(a&c)^(b&c)))&0xFFFFFFFF
        h=g;g=f;f=e;e=(d+t1)&0xFFFFFFFF;d=c;c=b;b=a;a=(t1+t2)&0xFFFFFFFF
    return[(st[i]+v)&0xFFFFFFFF for i,v in enumerate([a,b,c,d,e,f,g,h])]
def sp(n):return b'\x80'+b'\x00'*((55-n)%64)+struct.pack('>Q',n*8)
def sha_ext(mh,sl,om,ex):
    il=sl+len(om);tot=il+len(sp(il))
    st=[int.from_bytes(bytes.fromhex(mh)[i:i+4],'big') for i in range(0,32,4)]
    bl=ex+sp(tot+len(ex))
    for i in range(0,len(bl),64):st=_sc(st,bl[i:i+64])
    return b''.join(struct.pack('>I',s) for s in st)
LM=2**127-1;La=secrets.randbits(126)|1;Lc=secrets.randbits(126);Ls=secrets.randbits(126)
def lcg():
    global Ls;Ls=(La*Ls+Lc)%LM;return Ls
lo=[lcg() for _ in range(5)];x5=lcg()
k0=hashlib.sha256(L2B(x5,16)).digest()[:16]
s1=secrets.token_bytes(15);Mh=B2L(s1)
Hn=[];Hc=[]
for _ in range(3):
    while True:
        p=getPrime(64);q=getPrime(64);n=p*q
        if n>Mh and math.gcd(3,(p-1)*(q-1))==1:break
    Hn.append(n);Hc.append(pow(Mh,3,n))
bp=b"".join(L2B(v,16) for v in Hn+Hc)
aN=secrets.token_bytes(12);ac=AES.new(k0,AES.MODE_GCM,nonce=aN);aC,aT=ac.encrypt_and_digest(bp)
Kw=hashlib.sha256(s1).digest()[:16]
while True:
    p=getPrime(128);q=getPrime(128);nw=p*q;pw=(p-1)*(q-1)
    dw=secrets.randbelow(int(nw**0.23)+2)
    if dw<2 or math.gcd(dw,pw)!=1:continue
    ew=inverse(dw,pw);break
Gk=secrets.token_bytes(16);GN=secrets.token_bytes(12)
LT=[32,30,26,24];LS2=secrets.randbits(32)|(1<<31)
def lb():
    global LS2;b=LS2&1;fb=0
    for t in LT:fb^=(LS2>>(t-1))&1
    LS2=(LS2>>1)|(fb<<31);return b
def lB(n):
    v=0
    for _ in range(n*8):v=(v<<1)|lb()
    return v.to_bytes(n,'big')
lf=lB(8);kL=lB(16)
P1=(b"TYPHON::SESSION::v6.0::ts=1724457600::algo=ECDSA::status=OK::").ljust(80,b'\x00')
P2=lf+secrets.token_bytes(72)
g1=AES.new(Gk,AES.MODE_GCM,nonce=GN);C1,T1=g1.encrypt_and_digest(P1)
g2=AES.new(Gk,AES.MODE_GCM,nonce=GN);C2,T2=g2.encrypt_and_digest(P2)
wc=pow(B2L(Gk),ew,nw)
gd=json.dumps({"nw":nw,"ew":ew,"wc":wc,"gn":GN.hex(),"c1":C1.hex(),"t1":T1.hex(),"c2":C2.hex(),"t2":T2.hex(),"p1":P1.hex()}).encode()
gN=secrets.token_bytes(12);gc=AES.new(Kw,AES.MODE_GCM,nonce=gN);gC,gT=gc.encrypt_and_digest(gd)
print("[+] α β γ done",file=__import__("sys").stderr)
PP=10743968325151313008582423583445398294547657746978337143459014709152351170902581
PG=2;Px=secrets.randbelow(1<<128);PH=pow(PG,Px,PP);kP=L2B(Px,16)
pd=json.dumps({"ph_p":PP,"ph_g":PG,"ph_h":PH}).encode()
pN=secrets.token_bytes(12);pc=AES.new(kL,AES.MODE_GCM,nonce=pN);pC,pT=pc.encrypt_and_digest(pd)
KE=hashlib.sha256(kP).digest()[:16]
print("[+] δ ε done",file=__import__("sys").stderr)
SS=secrets.token_bytes(32);SM=b"svc=typhon::uid=observer::op=read"
Sm=hashlib.sha256(SS+SM).hexdigest();Se=b"::uid=root::op=exec"
fM=sha_ext(Sm,len(SS),SM,Se)
assert fM==hashlib.sha256(SS+SM+sp(len(SS)+len(SM))+Se).digest()
kS=fM[:16]
zd=json.dumps({"sha_mac":Sm,"sha_msg":SM.hex(),"secret_len":len(SS)}).encode()
zN=secrets.token_bytes(12);zc=AES.new(KE,AES.MODE_GCM,nonce=zN);zC,zT=zc.encrypt_and_digest(zd)
print("[+] ζ done",file=__import__("sys").stderr)
Ke=hashlib.sha256(kS).digest()[:16]
key_cc=secrets.token_bytes(16)
def make_cc_log(kb):
    hosts=["ws-alpha","ws-bravo","ws-charlie","ws-delta","ws-echo","ws-foxtrot","ws-golf","ws-hotel",
           "ws-india","ws-juliet","ws-kilo","ws-lima","ws-mike","ws-november","ws-oscar","ws-papa"]
    lines=[]
    base_ts=1724457600
    for i,b in enumerate(kb):
        ts=base_ts+i*secrets.randbelow(300)+10
        h=hosts[i%len(hosts)]
        noise_a=secrets.randbelow(65535)
        noise_b=secrets.randbelow(65535)
        lines.append(f"{ts} BEACON #{b} {h} 192.0.2.{secrets.randbelow(200)+10}:{noise_a} -> 198.51.100.{secrets.randbelow(50)+1}:{noise_b} RTT={secrets.randbelow(900)+10}ms")
    extra=[]
    for _ in range(8):
        ts=base_ts+secrets.randbelow(5000)+5000
        h=hosts[secrets.randbelow(len(hosts))]
        extra.append(f"{ts} KEEPALIVE {h} 192.0.2.{secrets.randbelow(200)+10} -> 203.0.113.{secrets.randbelow(50)+1}")
    import random; random.seed(42)
    all_lines=lines+extra; random.shuffle(all_lines)
    header=f"TYPHON C2 SESSION LOG — {secrets.token_hex(8).upper()}\nGENERATED: {base_ts}\n---\n"
    return (header+"\n".join(all_lines)).encode()
cc_plain=make_cc_log(key_cc)
import re
beacons=re.findall(r'BEACON #(\d+)',cc_plain.decode())
beacons_sorted=[int(x) for x in beacons]
assert len(beacons_sorted)==16
etaK_enc=secrets.token_bytes(12)
etaC=AES.new(Ke,AES.MODE_GCM,nonce=etaK_enc)
ccC,ccT=etaC.encrypt_and_digest(cc_plain)
Kcc=hashlib.sha256(key_cc).digest()[:16]
key_rat=secrets.token_bytes(16)
def make_rat_config(kb):
    modules=[]
    mnames=["keylogger","screencap","filegrab","shellexec","clipboard","browser_stealer",
            "credential_dump","network_scan","lateral_move","persistence","exfil","c2_rotate",
            "av_evasion","process_inject","memory_scan","log_wipe"]
    for i,b in enumerate(kb):
        modules.append({
            "name":mnames[i%len(mnames)],
            "enabled":bool(secrets.randbits(1)),
            "interval":b,
            "timeout":secrets.randbelow(300)+10,
            "retry":secrets.randbelow(5)+1,
            "params":{"depth":secrets.randbelow(4)+1,"silent":bool(secrets.randbits(1))}
        })
    noise_modules=[]
    for _ in range(6):
        noise_modules.append({
            "name":f"mod_{secrets.token_hex(3)}",
            "enabled":False,
            "interval":secrets.randbelow(256),
            "timeout":secrets.randbelow(300)+10,
            "retry":secrets.randbelow(5)+1
        })
    import random; rng=random.Random(0); all_mods=modules+noise_modules; rng.shuffle(all_mods)
    cfg={
        "schema":"rat-config-v3",
        "build":secrets.token_hex(8),
        "target":"x64-windows",
        "mutex":f"Global\\{secrets.token_hex(8)}",
        "c2":{"host":"192.0.2.1","port":secrets.randbelow(60000)+1024,"proto":"tcp"},
        "crypto":{"algo":"aes256","keyex":"dh2048","cert_pin":secrets.token_hex(32)},
        "modules":all_mods,
        "checksum":hashlib.sha256(json.dumps(all_mods).encode()).hexdigest()
    }
    return json.dumps(cfg,indent=2).encode()
rat_plain=make_rat_config(key_rat)
ratdata=json.loads(rat_plain)
mnames_order=["keylogger","screencap","filegrab","shellexec","clipboard","browser_stealer",
              "credential_dump","network_scan","lateral_move","persistence","exfil","c2_rotate",
              "av_evasion","process_inject","memory_scan","log_wipe"]
extracted_rat=[]
for mn in mnames_order:
    for m in ratdata["modules"]:
        if m["name"]==mn:extracted_rat.append(m["interval"]);break
assert bytes(extracted_rat)==key_rat,f"{bytes(extracted_rat).hex()} != {key_rat.hex()}"
thetaN=secrets.token_bytes(12);thetaC_=AES.new(Kcc,AES.MODE_GCM,nonce=thetaN)
ratC,ratT=thetaC_.encrypt_and_digest(rat_plain)
Krat=hashlib.sha256(key_rat).digest()[:16]
de=secrets.randbelow(EN);Qe=_mul(de,(EGx,EGy))
TX=[]
for i in range(40):
    msg=f"TX_{i:04d}::{secrets.token_hex(8)}".encode()
    z=int.from_bytes(hashlib.sha256(msg).digest(),'big')%EN
    k=secrets.randbelow(1<<128)
    Rx,_=_mul(k,(EGx,EGy));r=Rx%EN;s=pow(k,-1,EN)*(z+de*r)%EN
    TX.append((r,s,z))
tb=b"".join(r.to_bytes(32,'big')+s.to_bytes(32,'big')+z.to_bytes(32,'big') for r,s,z in TX)
tN2=secrets.token_bytes(12);tc2=AES.new(kS,AES.MODE_GCM,nonce=tN2);tC2,tT2=tc2.encrypt_and_digest(tb)
to2=json.dumps({"sha_mac":Sm,"sha_msg":SM.hex(),"secret_len":len(SS),"tx_nonce":tN2.hex(),"tx_ct":tC2.hex(),"tx_tag":tT2.hex()}).encode()
to2N=secrets.token_bytes(12);to2c=AES.new(Krat,AES.MODE_GCM,nonce=to2N);to2C,to2T=to2c.encrypt_and_digest(to2)
K_ec=hashlib.sha256(L2B(de,32)).digest()[:16]
while True:
    p_bd=getPrime(256);q_bd=getPrime(256);n_bd=p_bd*q_bd;phi_bd=(p_bd-1)*(q_bd-1)
    d_bd=secrets.randbelow(int(n_bd**0.27))
    if d_bd<3 or math.gcd(d_bd,phi_bd)!=1:continue
    e_bd=inverse(d_bd,phi_bd)
    if e_bd<n_bd//2:continue
    break
bd_msg=secrets.token_bytes(16)
bd_enc=pow(B2L(bd_msg),e_bd,n_bd)
key_bd=hashlib.sha256(bd_msg).digest()[:16]
kd=json.dumps({"n":n_bd,"e":e_bd,"c":bd_enc}).encode()
kdN=secrets.token_bytes(12);kdc=AES.new(K_ec,AES.MODE_GCM,nonce=kdN);kdC,kdT=kdc.encrypt_and_digest(kd)
p_cop=getPrime(256);q_cop=getPrime(256);n_cop=p_cop*q_cop;e_cop=65537
p_top=p_cop>>(256//2)
ld=json.dumps({"n":n_cop,"e":e_cop,"p_top":p_top,"p_bits":256,"known_bits":128}).encode()
ldN=secrets.token_bytes(12);ldc=AES.new(key_bd,AES.MODE_GCM,nonce=ldN);ldC,ldT=ldc.encrypt_and_digest(ld)
key_cop=hashlib.sha256(L2B(p_cop,32)).digest()[:16]
FLAG=b"CSCV2026{REDACTED}"
MASTER=hashlib.sha256(kL+kP+kS+key_cc+key_rat+key_bd+key_cop).digest()
VN=secrets.token_bytes(12);Vc=AES.new(MASTER,AES.MODE_GCM,nonce=VN)
VC,VT=Vc.encrypt_and_digest(FLAG)
rp2=getPrime(256);rq2=getPrime(256);rn2=rp2*rq2
dl2=[secrets.randbits(64) for _ in range(10)]
out={
    "Ψ":"TYPHON v1.0",
    "meta":{"sessions":dl2,"escrow":{"n":rn2,"e":65537,"ct":pow(secrets.randbits(512),65537,rn2)}},
    "α":{"M":LM,"out":lo,"Φ":{"N":aN.hex(),"C":aC.hex(),"T":aT.hex()}},
    "γ":{"Φ":{"N":gN.hex(),"C":gC.hex(),"T":gT.hex()}},
    "δ":{"Φ":{"N":pN.hex(),"C":pC.hex(),"T":pT.hex()}},
    "ζ":{"Φ":{"N":zN.hex(),"C":zC.hex(),"T":zT.hex()}},
    "η":{"Φ":{"N":etaK_enc.hex(),"C":ccC.hex(),"T":ccT.hex()}},
    "θ":{"Φ":{"N":thetaN.hex(),"C":ratC.hex(),"T":ratT.hex()}},
    "ι":{"Φ":{"N":to2N.hex(),"C":to2C.hex(),"T":to2T.hex()}},
    "κ":{"Φ":{"N":kdN.hex(),"C":kdC.hex(),"T":kdT.hex()}},
    "λ":{"Φ":{"N":ldN.hex(),"C":ldC.hex(),"T":ldT.hex()}},
    "pub":{"Qx":Qe[0],"Qy":Qe[1]},
    "Ω":{"N":VN.hex(),"C":VC.hex(),"T":VT.hex()}
}
import sys as _sys
print("[+] TYPHON generated.",file=_sys.stderr)
print(json.dumps(out,indent=2))
