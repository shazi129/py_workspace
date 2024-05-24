# -*- coding: utf-8 -*-
import eastmoney_api as finacial_api
import finacial_db


if __name__ == "__main__":
    #finacial_db.update_all_ma("XAG")
    finacial_db.create_stock_table(None, None, "XAU")
    