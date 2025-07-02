# models/objects.py
class Gejala:
    def __init__(self, id, kode_gejala, nama, deskripsi, kategori):
        self.id = id
        self.kode = kode_gejala
        self.nama = nama
        self.deskripsi = deskripsi
        self.kategori = kategori

class Penyakit:
    def __init__(self, id, kode_penyakit, nama, deskripsi, solusi):
        self.id = id
        self.kode = kode_penyakit
        self.nama = nama
        self.deskripsi = deskripsi
        self.solusi = solusi

class Aturan:
    def __init__(self, id, penyakitId, gejalaId, mb, md):
        self.id = id
        self.penyakit_id = penyakitId
        self.gejala_id = gejalaId
        self.mb = mb
        self.md = md

class HasilDiagnosa:
    def __init__(self, id, userId, penyakitId, nilai_cf, tanggal, gejala_terpilih):
        self.id = id
        self.user_id = userId
        self.penyakit_id = penyakitId
        self.nilai_cf = nilai_cf
        self.tanggal = tanggal
        self.gejala_terpilih = gejala_terpilih