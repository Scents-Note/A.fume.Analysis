from api.src.internal.sql.SqlUtil import SQLUtil


def substitute(tobe_idx, asis_idx):
    update_note_query = "UPDATE IGNORE notes SET ingredient_idx = %s " \
                        "WHERE ingredient_idx = %s"
    sql_util = SQLUtil.instance()
    sql_util.execute(update_note_query, args=[tobe_idx, asis_idx])

    remove_ingredient_query = "UPDATE ingredients SET deleted_at = now() WHERE ingredient_idx = %s"
    sql_util.execute(remove_ingredient_query, args=[asis_idx])


def main():
    splitted = """
    339	23
    345	27
    354	28
    1218	29
    532	33
    596	34
    1219	39
    502	42
    975	48
    264	51
    517	52
    748	55
    838	56
    277	57
    742	58
    245	63
    505	64
    348	65
    714	69
    711	70
    364	72
    333	74
    359	79
    355	80
    892	82
    959	83
    360	84
    993	85
    544	87
    653	88
    607	89
    553	93
    631	95
    971	99
    1119	100
    1231	101
    917	102
    1098	104
    1051	105
    751	107
    980	114
    257	117
    695	118
    976	119
    952	121
    10	151
    748	152
    1154	174
    1190	175
    382	178
    360	179
    751	180
    742	181
    2	184
    733	186
    1182	187
    1344	188
    838	189
    1207	190
    295	191
    563	192
    1206	193
    734	194
    156	196
    77	197
    1392	199
    536	200
    1220	201
    1246	202
    149	204
    1204	205
    975	206
    1199	207
    892	208
    110	209
    67	210
    11	211
    1257	212
    76	213
    1341	216
    852	217
    980	218
    1288	219
    952	220
    1467	221
    1200	222
    633	223
    103	224
    1246	225
    164	226
    81	227
    50	228
    900	238
    323	324
    1183	334
    1281	396
    1362	404
    1612	471
    1203	878
    38	895
    20	912
    149	956
    81	958
    889	1160
    20	1178
    889	1191
    12	1192
    14	1193
    364	1196
    18	1197
    30	1205
    76	1209
    952	1234
    830	1236
    481	1244
    120	1266
    1183	1270
    417	1275
    608	1325
    608	1326
    1203	1336
    469	1340
    14	1355
    837	1365
    448	1404
    37	1420
    504	1429
    549	1466
    1203	1468
    828	1469
    889	1499
    97	1517
    1524	1525
    504	1537
    610	1540
    62	1569
    2	1574
    799	1575
    580	1587
    835	1616
    """.split("\n")
    splitted = list(filter(lambda x: len(x.strip()) > 0, splitted))
    splitted = [list(map(lambda x: int(x.strip()), it.split('\t'))) for it in splitted]

    for tobe, asis in splitted:
        substitute(tobe, asis)


if __name__ == '__main__':
    main()
