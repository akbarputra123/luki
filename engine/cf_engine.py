class CertaintyFactorEngine:
    def hitung_cf(self, cf_user, mb, md):
        return round(cf_user * (mb - md), 2)

    def kombinasi_cf(self, cf_list):
        if not cf_list:
            return 0
        cf_total = cf_list[0]
        for cf in cf_list[1:]:
            cf_total = round(cf_total + cf * (1 - cf_total), 2)
        return cf_total
