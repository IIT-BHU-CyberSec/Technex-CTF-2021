from Crypto.Util.number import getPrime, inverse

p = 3339170894671744465601628315109082756447958938360359387219
q = 5799472533886432422518977876745006653248415631574097767443
e = 65537
d = inverse(e, (p-1)*(q-1))
flag = b'technex{0r4cl3_i5_4tt4ck_nic3}'