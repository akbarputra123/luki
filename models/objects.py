# models/objects.py
class Gejala:
    def __init__(self, id, kode_gejala, nama_gejala, deskripsi, kategori):
        self.id = id
        self.kode = kode_gejala
        self.nama = nama_gejala
        self.deskripsi = deskripsi
        self.kategori = kategori

class Penyakit:
    def __init__(self, id, kode_penyakit, nama_penyakit, deskripsi, solusi):
        self.id = id
        self.kode = kode_penyakit
        self.nama = nama_penyakit
        self.deskripsi = deskripsi
        self.solusi = solusi

class Aturan:
    def __init__(self, id, penyakit_id, gejala_id, mb, md):
        self.id = id
        self.penyakit_id = penyakit_id
        self.gejala_id = gejala_id
        self.mb = mb
        self.md = md

class HasilDiagnosa:
    def __init__(self, id, user_id, penyakit_id, nilai_cf, tanggal_diagnosa, gejala_terpilih):
        self.id = id
        self.user_id = user_id
        self.penyakit_id = penyakit_id
        self.nilai_cf = nilai_cf
        self.tanggal = tanggal_diagnosa
        self.gejala_terpilih = gejala_terpilih