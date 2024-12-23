# -*- coding: utf-8 -*-
from tkinter import messagebox

from data.CaseSql import query_column_all
from data.CaselibUpdataSql import query_caselib, query_casestep, insert_libproduct
from log.LogSql import log_input
def load_commonttest(username,product_id):
    case=query_caselib(username)
    case1 = []
    for i in case:
        caseid = i[0]
        caseteps = tuple(query_casestep(username, caseid))
        ii = (i[1], i[2], i[3], caseteps)
        case1.append(ii)
    case2 = tuple(case1)
    insert_libproduct(username, product_id, case2)
