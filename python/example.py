from hashlib import sha256
from simplesrp.client.srp import Client
from simplesrp.ng_values import NG
from simplesrp.server.srp import Verifier

SALT = b'\xfa\xc0I\x85L\xa3\xfc7\xce]Q,\x1c)\xb2z'
VKEY = 15827888480145372271854914203117663353970591649205157967017813473608838149114825557286700629066352749793025695486150898808924784986811904305629375485400761463453835048645018196754489911506353645843165318351948041911064289599365109441522543932155203095621300836980341915004417659064651658527862984462668023700133302241913456159824478949729658367520957639802899443180949949666811464552524573773776222569130344095659579308198901686213071327371693582155218641912131546949172520689663797219054552747055153775355330428220845483804206329688587822113133886530136862915612298449798783951359000669027335583012526879151302004626

client = Client("testUser", "testPassword", sha256, NG.NG_2048)
ver = Verifier("testUser", SALT, VKEY, sha256, NG.NG_2048)

salt, B = ver.getChallenge()
A = client.genA()

M = client.processChallenge(salt, B)
HAMK = ver.verifyChallenge(A, M)

print(client.verify_HAMK(HAMK))