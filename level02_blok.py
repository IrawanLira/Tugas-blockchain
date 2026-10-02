"""
LEVEL 2 — Blockchain Dasar ala GeeksforGeeks, tanpa Flask (LATIHAN)
=========================================================================

Kode ini adalah port dari artikel:
https://www.geeksforgeeks.org/python/create-simple-blockchain-using-python/
dengan dua perubahan: (1) tanpa Flask agar bisa dijalankan di terminal,
(2) tingkat kesulitan (difficulty) dijadikan parameter, bukan '00000' tetap.

Tujuan belajar:
  * Struktur blok: index, timestamp, proof, previous_hash.
  * Menghubungkan blok dengan hash blok sebelumnya.
  * Proof of Work sederhana dan validasi rantai.

Jalankan tes:  python cek_nilai.py 2
"""

import datetime
import hashlib
import json


class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        self.chain = []
        # Blok genesis (blok pertama)
        self.create_block(proof=1, previous_hash="0")

    # ---------- SUDAH DISEDIAKAN ----------
    def create_block(self, proof: int, previous_hash: str) -> dict:
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
        }
        self.chain.append(block)
        return block

    def last_block(self) -> dict:
        """(Di artikel GfG bernama print_previous_block)."""
        return self.chain[-1]

    # ---------- BAGIAN YANG DIKERJAKAN (isi semua TODO) ----------
    def hash(self, block: dict) -> str:
        """SHA-256 dari blok yang diserialisasi JSON dengan sort_keys=True."""
        # TODO: lengkapi fungsi ini
        # Petunjuk: Lihat fungsi hash() di artikel GfG
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def valid_proof(self, previous_proof: int, proof: int) -> bool:
        """True jika SHA-256(str(proof**2 - previous_proof**2)) diawali `difficulty` angka nol."""
        # TODO: lengkapi fungsi ini
        # Petunjuk: Hitung hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
        # Petunjuk: Bandingkan awalan hash dengan '0' * self.difficulty (pakai .startswith)
        guess = str(proof**2 - previous_proof**2).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash.startswith('0' * self.difficulty)

    def proof_of_work(self, previous_proof: int) -> int:
        """Cari bilangan bulat terkecil mulai dari 1 yang lolos valid_proof()."""
        # TODO: lengkapi fungsi ini
        # Petunjuk: Mulai new_proof = 1, naikkan terus selama valid_proof() masih False
        new_proof = 1
        while not self.valid_proof(previous_proof, new_proof):
            new_proof += 1
        return new_proof

    def mine_block(self) -> dict:
        """Tambang blok baru: cari proof, hitung hash blok terakhir, lalu create_block()."""
        # TODO: lengkapi fungsi ini
        # Petunjuk: 1. ambil blok terakhir  2. proof_of_work(proof blok terakhir)
        # Petunjuk: 3. hash blok terakhir  4. create_block(proof, previous_hash)
        previous_block = self.last_block()
        previous_proof = previous_block['proof']
        proof = self.proof_of_work(previous_proof)
        previous_hash = self.hash(previous_block)
        return self.create_block(proof, previous_hash)

    def chain_valid(self, chain: list) -> bool:
        """Periksa setiap blok (mulai blok ke-2):
        1. previous_hash == hash(blok sebelumnya)
        2. valid_proof(proof blok sebelumnya, proof blok ini) bernilai True
        """
        # TODO: lengkapi fungsi ini
        # Petunjuk: Loop i dari 1 sampai len(chain)-1, bandingkan chain[i] dengan chain[i-1]
        # Petunjuk: Kembalikan False segera jika ada yang salah, True di akhir
        for i in range(1, len(chain)):
            prev_block = chain[i-1]
            curr_block = chain[i]
            
            if curr_block['previous_hash'] != self.hash(prev_block):
                return False
                
            if not self.valid_proof(prev_block['proof'], curr_block['proof']):
                return False
                
        return True


if __name__ == "__main__":
    bc = Blockchain(difficulty=4)
    for _ in range(4):
        b = bc.mine_block()
        print(f"Blok #{b['index']} ditambang, proof={b['proof']}")
    print(json.dumps(bc.chain, indent=2))
    print("Rantai valid?", bc.chain_valid(bc.chain))