# python為直譯程式，import即可執行networkd

import networkd
import yhttpd

# 移除除執行過的網路連線程式networkd
if 'networkd' in globals():
    del globals()['networkd']
if 'yuri' in globals():
    del globals()['yuri']
