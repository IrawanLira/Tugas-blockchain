"""
LEVEL 1 — Fungsi Hash SHA-256 (LATIHAN)
==============================================

Tujuan belajar:
  * Memahami bahwa hash adalah "sidik jari digital" berukuran tetap (256 bit).
  * Memahami sifat deterministik: input sama -> hash sama.
  * Mengamati efek avalanche: perubahan 1 karakter mengubah ~50% bit hash.
  * Memahami mengapa dict harus diserialisasi secara kanonik (sort_keys).

Jalankan tes:  python cek_nilai.py 1
"""

import hashlib
import json


def sha256_hex(teks: str) -> str:
    """Kembalikan hash SHA-256 dari `teks` (encoding UTF-8) dalam bentuk heksadesimal (64 karakter)."""
    # TODO: lengkapi fungsi ini
    # Petunjuk: Gunakan hashlib.sha256(...) lalu .hexdigest()
    # Petunjuk: Ingat: hashlib butuh bytes, jadi teks harus di-.encode('utf-8')
    return hashlib.sha256(teks.encode('utf-8')).hexdigest()


def hash_dict(data: dict) -> str:
    """Hash sebuah dict secara KANONIK.

    Dua dict dengan isi sama tetapi urutan key berbeda harus menghasilkan hash yang sama.
    Petunjuk: json.dumps(..., sort_keys=True).
    """
    # TODO: lengkapi fungsi ini
    # Petunjuk: Ubah dict menjadi string JSON dengan json.dumps(data, sort_keys=True)
    # Petunjuk: lalu hash string itu dengan sha256_hex()
    return sha256_hex(json.dumps(data, sort_keys=True))


def bit_berbeda(hash_a: str, hash_b: str) -> int:
    """Hitung jumlah bit yang berbeda antara dua hash heksadesimal (0..256).

    Petunjuk: ubah ke int basis 16, lakukan XOR, lalu hitung jumlah bit '1'.
    """
    # TODO: lengkapi fungsi ini
    # Petunjuk: int(hash_a, 16) ^ int(hash_b, 16) -> XOR
    # Petunjuk: bin(x).count('1') -> jumlah bit 1
    return bin(int(hash_a, 16) ^ int(hash_b, 16)).count('1')


def persen_bit_berbeda(teks_a: str, teks_b: str) -> float:
    """Persentase bit (0..100) yang berbeda antara SHA-256(teks_a) dan SHA-256(teks_b)."""
    # TODO: lengkapi fungsi ini
    # Petunjuk: Hash kedua teks, hitung bit_berbeda, bagi 256, kali 100
    return (bit_berbeda(sha256_hex(teks_a), sha256_hex(teks_b)) / 256) * 100


if __name__ == "__main__":
    a, b = "Teknologi Blockchain", "teknologi Blockchain"
    print(f"SHA256('{a}') = {sha256_hex(a)}")
    print(f"SHA256('{b}') = {sha256_hex(b)}")
    print(f"Bit berbeda: {persen_bit_berbeda(a, b):.1f}%  (efek avalanche)")
