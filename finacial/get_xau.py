# -*- coding: utf-8 -*-
import eastmoney_api as finacial_api
import finacial_db
import os

if __name__ == "__main__":
    
    current_file_path = os.path.abspath(__file__)
    cache_filename = "%s/XAU.txt" % os.path.dirname(current_file_path)

    '''
    finacial_api.save_all_kline_to_file("XAU", cache_filename)
    '''
    
    tablename = "XAU"
    connection, cursor = finacial_db.connect_db()
    #finacial_db.create_stock_table(connection, cursor, tablename)
    #finacial_db.init_db_with_file(cache_filename, tablename)
    finacial_db.update_all_ma(tablename)

    finacial_db.close_db(connection, cursor)
    
    