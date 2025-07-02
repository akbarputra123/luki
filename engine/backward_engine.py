class BackwardChainingEngine:
    def __init__(self, aturan_list):
        self.aturan_list = aturan_list

    def inferensi(self, penyakit_list, gejala_jawab):
        penyakit_ditemukan = []
        for penyakit in penyakit_list:
            pid = penyakit['id']
            aturan_penyakit = [a for a in self.aturan_list if a['penyakit_id'] == pid]
            semua_gejala_terpenuhi = True
            for aturan in aturan_penyakit:
                if str(aturan['gejala_id']) not in gejala_jawab:
                    semua_gejala_terpenuhi = False
                    break
            if semua_gejala_terpenuhi:
                penyakit_ditemukan.append(penyakit)
        return penyakit_ditemukan
