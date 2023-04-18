"""
MIT License

Copyright (c) 2023-present RuslanUC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from os import urandom

from ..utils import Hash


class Client:
    salt: bytes
    x: bytes
    V: bytes
    a: int
    A: int
    B: int
    K: int
    S: int
    M: int
    HAMK: bytes

    def __init__(self, username: str, password: str, hash_func, ng: tuple[int, int]):
        self._username = username
        self._password = password
        self._hash_func = hash_func
        self.N, self.g = ng
        self.k = int.from_bytes(Hash(hash_func, self.N, self.g), "big")

    def genSalt(self) -> bytes:
        self.salt = urandom(32)
        return self.salt

    def genX(self, salt: bytes=None) -> bytes:
        if salt is not None:
            self.salt = salt
        self.x = Hash(self._hash_func, self.salt, Hash(self._hash_func, self._username, ":", self._password))
        return self.x

    def genV(self, salt: bytes=None) -> bytes:
        x = int.from_bytes(self.genX(salt), "big")
        self.V = pow(self.g, x, self.N)
        return self.V

    def genA(self) -> int:
        self.a = int.from_bytes(urandom(128), "big") % self.N
        self.A = pow(self.g, self.a, self.N)
        return self.A

    def calcM(self):
        Hg = Hash(self._hash_func, self.g)
        HN = Hash(self._hash_func, self.N)
        HI = Hash(self._hash_func, self._username)
        Hxor = bytes(map(lambda i: i[0] ^ i[1], zip(Hg, HN)))
        self.M = int.from_bytes(Hash(self._hash_func, Hxor, HI, self.salt, self.A, self.B, self.K), "big")
        return self.M

    def processChallenge(self, salt: bytes, B: int) -> int:
        self.salt = salt
        self.B = B
        u = int.from_bytes(Hash(self._hash_func, self.A, B), "big")
        x = int.from_bytes(self.genX(salt), "big")
        self.S = pow((B - (self.k * pow(self.g, x, self.N))), (self.a + (u * x)), self.N)
        self.K = int.from_bytes(Hash(self._hash_func, self.S), "big")
        self.calcM()
        self.HAMK = Hash(self._hash_func, self.A, self.M, self.K)
        return self.M

    def verify_HAMK(self, HAMK: bytes) -> bool:
        return HAMK == self.HAMK