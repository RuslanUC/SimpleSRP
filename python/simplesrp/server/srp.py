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
from typing import Optional

from ..utils import Hash


class Verifier:
    b: int
    B: int
    K: int
    S: int
    M: int

    def __init__(self, username: str, salt: bytes, vkey: int, hash_func, ng: tuple[int, int]):
        self._username = username
        self._salt = salt
        self._vkey = vkey
        self._hash_func = hash_func
        self.N, self.g = ng
        self.k = int.from_bytes(Hash(hash_func, self.N, self.g), "big")

    def _genB(self) -> None:
        self.b = b = int.from_bytes(urandom(1024), "big")
        self.B = (self.k*self._vkey + pow(self.g, b, self.N)) % self.N

    def getChallenge(self) -> tuple[bytes, int]:
        self._genB()
        return self._salt, self.B

    def calcM(self):
        Hg = Hash(self._hash_func, self.g)
        HN = Hash(self._hash_func, self.N)
        HI = Hash(self._hash_func, self._username)
        Hxor = bytes(map(lambda i: i[0] ^ i[1], zip(Hg, HN)))
        self.M = int.from_bytes(Hash(self._hash_func, Hxor, HI, self._salt, self.A, self.B, self.K), "big")
        return self.M

    def verifyChallenge(self, A: int, M: int) -> Optional[bytes]:
        if A % self.N == 0:
            return
        self.A = A
        u = int.from_bytes(Hash(self._hash_func, A, self.B), "big")
        self.S = pow(A * pow(self._vkey, u, self.N), self.b, self.N)
        self.K = int.from_bytes(Hash(self._hash_func, self.S), "big")
        self.calcM()
        if self.M == M:
            return Hash(self._hash_func, A, self.M, self.K)