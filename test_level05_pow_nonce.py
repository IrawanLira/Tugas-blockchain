import hashlib
import json

import pytest

class Blockchain:
    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.chain = []
        self.new_block([], previous_hash="000")
        
    @staticmethod
    def hash_block(block):
        block_copy = block.copy()
        if "hash" in block_copy:
            del block_copy["hash"]
        return hashlib.sha256(json.dumps(block_copy, sort_keys=True).encode()).hexdigest()
        
    def proof_of_work(self, block):
        block["nonce"] = 0
        attempts = 0
        while True:
            attempts += 1
            h = self.hash_block(block)
            if h.startswith("0" * self.difficulty):
                block["hash"] = h
                return attempts
            block["nonce"] += 1
            
    def new_block(self, transactions, previous_hash=None):
        if not previous_hash and self.chain:
            previous_hash = self.chain[-1]["hash"]
        block = {
            "index": len(self.chain),
            "transactions": transactions,
            "previous_hash": previous_hash,
        }
        self.proof_of_work(block)
        self.chain.append(block)
        return block
        
    def chain_valid(self):
        for i in range(1, len(self.chain)):
            block = self.chain[i]
            prev = self.chain[i-1]
            if block["previous_hash"] != prev["hash"]:
                return False
            if not self.hash_block(block).startswith("0" * self.difficulty):
                return False
            if block.get("hash") != self.hash_block(block):
                return False
        return True
        
    def tambang_ulang_dari(self, index):
        usaha = 0
        for i in range(index, len(self.chain)):
            if i > 0:
                self.chain[i]["previous_hash"] = self.chain[i-1]["hash"]
            usaha += self.proof_of_work(self.chain[i])
        return usaha



@pytest.fixture
def bc():
    b = Blockchain(difficulty=3)
    for tx in (["Ani->Budi 5"], ["Budi->Citra 2"], ["Citra->Dodi 1"]):
        b.new_block(tx)
    return b


def test_hash_block_mengabaikan_key_hash():
    blok = {"index": 1, "nonce": 5, "data": "x"}
    harapan = hashlib.sha256(json.dumps(blok, sort_keys=True).encode()).hexdigest()
    assert Blockchain.hash_block(blok) == harapan
    blok_dengan_hash = dict(blok, hash="apa saja")
    assert Blockchain.hash_block(blok_dengan_hash) == harapan
    assert blok_dengan_hash["hash"] == "apa saja", "dict asli tidak boleh diubah"


def test_proof_of_work_mencari_nonce_terkecil():
    b = Blockchain(difficulty=2)
    blok = {"index": 9, "transactions": [], "previous_hash": "x", "nonce": 123}
    percobaan = b.proof_of_work(blok)
    assert blok["hash"].startswith("00")
    assert blok["hash"] == Blockchain.hash_block(blok)
    assert percobaan == blok["nonce"] + 1
    for n in range(blok["nonce"]):
        uji = dict(blok, nonce=n)
        assert not Blockchain.hash_block(uji).startswith("00")


def test_genesis_ditambang(bc):
    g = bc.chain[0]
    assert g["index"] == 0 and g["hash"].startswith("000")


def test_new_block(bc):
    assert len(bc.chain) == 4
    for i in range(1, 4):
        assert bc.chain[i]["index"] == i
        assert bc.chain[i]["previous_hash"] == bc.chain[i - 1]["hash"]
        assert bc.chain[i]["hash"].startswith("000")
    assert bc.chain[2]["transactions"] == ["Budi->Citra 2"]


def test_chain_valid(bc):
    assert bc.chain_valid() is True


def test_ubah_data_terdeteksi(bc):
    bc.chain[1]["transactions"] = ["Ani->Budi 500"]
    assert bc.chain_valid() is False


def test_ubah_blok_terakhir_juga_terdeteksi(bc):
    # Berbeda dengan Level 3: perubahan blok terakhir pun terdeteksi
    bc.chain[-1]["transactions"] = ["PALSU"]
    assert bc.chain_valid() is False


def test_sambung_ulang_saja_tidak_cukup(bc):
    """Serangan Level 3 (re-link tanpa menambang ulang) GAGAL di sini."""
    bc.chain[1]["transactions"] = ["Ani->Budi 500"]
    bc.chain[1]["hash"] = Blockchain.hash_block(bc.chain[1])
    for i in range(2, len(bc.chain)):
        bc.chain[i]["previous_hash"] = bc.chain[i - 1]["hash"]
        bc.chain[i]["hash"] = Blockchain.hash_block(bc.chain[i])
    assert bc.chain_valid() is False


def test_hash_tidak_memenuhi_difficulty_terdeteksi():
    b = Blockchain(difficulty=2)
    b.new_block(["x"])
    # hash dihitung benar, tapi nonce sengaja dibuat tidak memenuhi target
    blok = b.chain[1]
    n = 0
    while Blockchain.hash_block(dict(blok, nonce=n)).startswith("00"):
        n += 1
    blok["nonce"] = n
    blok["hash"] = Blockchain.hash_block(blok)
    assert b.chain_valid() is False


def test_tambang_ulang_memulihkan_validitas(bc):
    bc.chain[1]["transactions"] = ["Ani->Budi 500"]
    usaha = bc.tambang_ulang_dari(1)
    assert bc.chain_valid() is True
    assert usaha >= 3  # minimal 1 percobaan per blok untuk 3 blok
    assert bc.chain[1]["transactions"] == ["Ani->Budi 500"]
