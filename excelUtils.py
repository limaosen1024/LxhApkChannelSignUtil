import xlrd


def saveFile(filename, contents):
    fh = open(filename, 'w', encoding='utf-8')
    fh.write(contents)
    fh.close()


workBook = xlrd.open_workbook("/Users/lixiaohui/Desktop/技术部/芒果7天会员/给孝辉芒果TV7天会员兑换码.xlsx")
sqlFile = "/Users/lixiaohui/Desktop/技术部/芒果7天会员/redeem.sql"
cp_name="MANGGUO"
cp_product_id="mg_d7_20200331"
expire_time="2020-06-27 23:59:59"

allSheetNames = workBook.sheet_names()
# print(allSheetNames)
sheet1_content1 = workBook.sheet_by_index(0)
cols = sheet1_content1.col_values(0)
# print(cols)
sqlStr = "INSERT INTO `cp_user_redeem` (`cp_name`, `cp_product_id`, `redeem`, `expire_time`, `status`, `user_id`, `order_id`, `promote_code`) \nVALUES";
for inx, col in enumerate(cols):
    if inx == 0:
        continue
    elif inx == len(cols) - 1:
        sqlStr += "\n('"+cp_name+"','"+cp_product_id+"','" + col + "','"+expire_time+"', 'VALID', 0, 0, '');"
    else:
        sqlStr += "\n('"+cp_name+"','"+cp_product_id+"','" + col + "','"+expire_time+"', 'VALID', 0, 0, ''),"
saveFile(sqlFile, sqlStr)
