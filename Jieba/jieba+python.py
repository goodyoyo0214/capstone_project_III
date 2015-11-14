# coding=utf-8
import MySQLdb
import codecs
import io
import jieba
import time

start = time.time()
BOM = codecs.BOM_UTF8.decode('utf8') #處理編碼的問題
'''------------------以下是每個人自己分類的字典--------------------'''
# 配件字典
dicAcc = {"QX10": "QX10", "QX100": "QX100", "Pad": "Pad", "外掛鏡頭": "外掛鏡頭", "平板": "平板", "外掛相機": "外掛相機", "皮套": "皮套",
          "pad": "pad", "背蓋": "背蓋", "保護套": "保護套", "無線充電": "無線充電", "保護貼": "保護貼", "玻璃保護貼": "玻璃保護貼", "外掛": "外掛",
          "保護殼": "保護殼", "行動電源": "行動電源", "平板基座": "平板基座", "RX10": "RX10", "充電座": "充電座", "保護": "保護", "配件": "配件",
          "透明殼": "透明殼", "電磁筆": "電磁筆", "IMOS": "IMOS", "QX": "QX", "手機平板": "手機平板", "車架": "車架", "PAD": "PAD",
          "玻璃貼": "玻璃貼", "鋁框": "鋁框", "藍芽耳機": "藍芽耳機", "平板手機": "平板手機", "固定夾具": "固定夾具", "觸控筆": "觸控筆", "保貼": "保貼",
          "原廠車架": "原廠車架", "基座": "基座", "HDMI": "HDMI", "mit": "mit", "磁充線": "磁充線", "OTG": "OTG", "合體": "合體", "底座": "底座",
          "悠遊卡": "悠遊卡", "隨身硬碟": "隨身硬碟", "QX鏡頭": "QX鏡頭", "金屬邊框": "金屬邊框", "智慧筆": "智慧筆", "磁充": "磁充", "遙控器": "遙控器",
          "卡榫": "卡榫", "外接": "外接", "座充": "座充", "旅充": "旅充", "副廠": "副廠", "鋼化玻璃": "鋼化玻璃", "轉接頭": "轉接頭", "變壓器": "變壓器",
          "DK32": "DK32", "Q100": "Q100", "ss鏡頭": "ss鏡頭", "手機殼": "手機殼", "包膜": "包膜", "米鍵": "米鍵", "吸式充電": "吸式充電",
          "原廠皮套": "原廠皮套", "單眼鏡頭": "單眼鏡頭", "電池蓋": "電池蓋", "磁線": "磁線", "隨身碟": "隨身碟", "USB充電": "USB充電", "充座": "充座",
          "充電器": "充電器", "相機包": "相機包", "電線": "電線", "Qx10": "Qx10", "手寫筆": "手寫筆", "充電座充": "充電座充", "金屬框": "金屬框",
          "後蓋": "後蓋", "玻璃背蓋": "玻璃背蓋", "套子": "套子", "康寧": "康寧", "強化玻璃貼": "強化玻璃貼", "掛式鏡頭": "掛式鏡頭", "接頭": "接頭",
          "磁力線": "磁力線", "磁扣線": "磁扣線", "磁座": "磁座", "螢幕邊框": "螢幕邊框", "上蓋": "上蓋", "外框": "外框", "吸盤": "吸盤", "尿袋": "尿袋",
          "防護": "防護", "配備": "配備", "插上": "插上", "硬碟": "硬碟", "蓋子": "蓋子", "翻蓋": "翻蓋", "K32座": "K32座", "Y型線": "Y型線",
          "孔位": "孔位", "充電底座": "充電底座", "外掛夾": "外掛夾", "外掛殼": "外掛殼", "行動硬碟": "行動硬碟", "防潮箱": "防潮箱", "玻璃保貼": "玻璃保貼",
          "原廠電池": "原廠電池", "被蓋": "被蓋", "結合平板": "結合平板", "絨布套": "絨布套", "腳架": "腳架", "藍芽喇叭": "藍芽喇叭", "雙料背蓋": "雙料背蓋",
          "平版": "平版", "側翻皮套": "側翻皮套"}
# 外觀字典
dicAppear = {"黃色": "黃色", "粉色": "粉色", "邊框": "邊框", "女生": "女生", "設計": "設計", "玻璃": "玻璃", "顏色": "顏色", "材質": "材質", "藍色": "藍色",
             "彎曲": "彎曲", "塑膠": "塑膠", "質感": "質感", "女性": "女性", "背面": "背面", "黑色": "黑色", "金屬": "金屬", "女人": "女人", "曲面": "曲面",
             "色彩": "色彩", "曲線": "曲線", "灰色": "灰色", "漂亮": "漂亮", "弧度": "弧度", "色彩鮮艷": "色彩鮮艷", "防爆膜": "防爆膜", "流行": "流行",
             "髮絲紋": "髮絲紋", "裸機": "裸機", "鏡面": "鏡面", "美感": "美感", "粉紅色": "粉紅色", "設計的": "設計的", "設計師": "設計師", "晶鑽紅": "晶鑽紅",
             "黑色的": "黑色的", "塑料": "塑料", "材料": "材料", "金色": "金色", "紅色": "紅色", "桃紅色": "桃紅色", "綠色": "綠色", "鮮豔": "鮮豔",
             "曲線弧度": "曲線弧度", "有弧度": "有弧度", "設計上": "設計上", "設計出": "設計出", "設計在": "設計在", "塑膠機": "塑膠機", "外觀": "外觀",
             "白色": "白色", "粉色系": "粉色系", "過於陽剛": "過於陽剛", "雙曲面": "雙曲面", "顏色鮮豔": "顏色鮮豔", "彎曲設計": "彎曲設計", "曲面手機": "曲面手機",
             "曲線外型": "曲線外型", "曲線美感": "曲線美感", "科技感": "科技感", "酒紅色": "酒紅色", "產品設計": "產品設計", "塑膠背蓋": "塑膠背蓋", "雙面玻璃": "雙面玻璃",
             "鏡頭突出": "鏡頭突出", "曲面螢幕": "曲面螢幕", "螢幕": "螢幕", "顯示": "顯示", "螢幕亮度": "螢幕亮度", "彎曲螢幕": "彎曲螢幕", "側邊曲面": "側邊曲面",
             "視窗": "視窗", "IPS螢幕": "IPS螢幕", "黑屏": "黑屏", "圓形視窗": "圓形視窗", "側邊螢幕": "側邊螢幕", "側面螢幕": "側面螢幕", "弧形螢幕": "弧形螢幕",
             "螢幕尺寸": "螢幕尺寸", "螢幕顏色": "螢幕顏色", "螢幕顯色": "螢幕顯色", "主畫面": "主畫面", "顯示器": "顯示器", "曲面熒幕": "曲面熒幕", "螢幕顯示": "螢幕顯示",
             "螢幕色調": "螢幕色調"}
#電池字典
dicBattery = {"電池": "電池", "充電": "充電", "耗電": "耗電", "電池容量": "電池容量", "電力": "電力", "電量": "電量", "省電": "省電", "充電電流": "充電電流",
              "電流": "電流", "線材": "線材", "電壓": "電壓", "耗電量": "耗電量", "手機電池": "手機電池", "電源": "電源", "手機充電": "手機充電", "安規": "安規",
              "負載": "負載", "插頭": "插頭", "開開關關": "開開關關", "電流安培": "電流安培", "噴電": "噴電", "電流輸出": "電流輸出", "電源供應": "電源供應",
              "吃電": "吃電", "不耗電": "不耗電", "電池續航": "電池續航", "電源鍵": "電源鍵", "電源管理": "電源管理", "鋰電池": "鋰電池", "平板電池": "平板電池",
              "超耗電": "超耗電", "電源控制": "電源控制", "輸出電流": "輸出電流", "電源輸出": "電源輸出", "好耗電": "好耗電", "電池充電": "電池充電", "電池量": "電池量",
              "電量消耗": "電量消耗", "螢幕耗電": "螢幕耗電", "輸出電壓": "輸出電壓", "用電量": "用電量", "電力耗損": "電力耗損"}
#相機字典
dicCamera = {"光學變焦": "光學變焦", "感光元件": "感光元件", "拍照": "拍照", "照片": "照片", "效果": "效果", "畫質": "畫質", "手動模式": "手動模式",
             "雷射對焦": "雷射對焦", "拍攝": "拍攝", "相機功能": "相機功能", "自動對焦": "自動對焦", "夜拍": "夜拍", "錄影": "錄影", "光學防手震": "光學防手震",
             "對焦": "對焦", "鏡頭": "鏡頭", "拍照功能": "拍照功能", "夜景模式": "夜景模式", "氙氣閃光燈": "氙氣閃光燈", "畫素": "畫素", "光圈": "光圈",
             "拍照模式": "拍照模式", "特效": "特效", "手機拍照": "手機拍照", "文青相機": "文青相機", "照相功能": "照相功能", "手機相機": "手機相機", "廣角": "廣角",
             "測光": "測光", "照相": "照相", "數位變焦": "數位變焦", "智慧模式": "智慧模式", "場景模式": "場景模式", "曝光": "曝光", "變焦": "變焦",
             "數位相機": "數位相機", "連拍": "連拍", "攝影": "攝影", "近拍": "近拍", "人像": "人像", "手勢自拍": "手勢自拍", "模糊": "模糊", "清晰": "清晰",
             "CMOS": "CMOS", "美顏模式": "美顏模式", "解析度": "解析度", "試拍": "試拍", "白平衡": "白平衡", "油畫感": "油畫感", "相機": "相機",
             "單眼相機": "單眼相機", "隨手拍": "隨手拍", "0倍變焦": "0倍變焦", "像素": "像素", "美肌": "美肌", "光源": "光源", "閃光燈": "閃光燈",
             "曝光值": "曝光值", "防手震": "防手震", "拍照畫質": "拍照畫質", "飽和度": "飽和度", "觸控對焦": "觸控對焦", "拍完": "拍完", "拍到": "拍到",
             "閃光": "閃光", "錄製": "錄製", "錄影功能": "錄影功能", "照相手機": "照相手機", "變焦拍攝": "變焦拍攝", "相機手機": "相機手機", "相機鏡頭": "相機鏡頭",
             "對焦功能": "對焦功能", "拍照品質": "拍照品質", "高ISO": "高ISO", "感光模式": "感光模式", "內建相機": "內建相機", "對焦模式": "對焦模式",
             "全景模式": "全景模式", "色偏": "色偏", "色溫": "色溫", "夜拍模式": "夜拍模式", "相機拍照": "相機拍照", "LED燈": "LED燈", "照相品質": "照相品質",
             "成相": "成相", "成像品質": "成像品質", "拍人": "拍人", "景深相機": "景深相機", "照相機": "照相機", "遠攝": "遠攝", "反差平衡": "反差平衡",
             "手機拍攝": "手機拍攝", "失焦": "失焦", "手動對焦": "手動對焦", "合照": "合照", "自動拍攝": "自動拍攝", "啟動相機": "啟動相機", "焦距": "焦距",
             "開閃光": "開閃光", "感光": "感光", "補光燈": "補光燈", "銳化": "銳化", "鏡片": "鏡片", "失真": "失真", "測光對焦": "測光對焦", "遠景": "遠景",
             "鏡頭設計": "鏡頭設計", "F對焦燈": "F對焦燈", "相機規格": "相機規格", "相機畫質": "相機畫質", "風景模式": "風景模式", "蓋大樓": "蓋大樓",
             "模式實拍": "模式實拍", "OS感光": "OS感光", "十倍變焦": "十倍變焦", "開起相機": "開起相機", "開閃光燈": "開閃光燈", "補光": "補光", "錄影畫面": "錄影畫面",
             "錄影模式": "錄影模式", "隨手亂拍": "隨手亂拍", "隨身拍": "隨身拍", "觸控測光": "觸控測光", "變焦功能": "變焦功能", "手持夜景": "手持夜景",
             "百萬畫素": "百萬畫素", "拍夜景": "拍夜景", "拍照手機": "拍照手機", "拍照需求": "拍照需求", "相機模式": "相機模式", "能自拍": "能自拍", "專業模式": "專業模式",
             "畫素相機": "畫素相機", "照相畫質": "照相畫質", "貓頭鷹模式": "貓頭鷹模式", "光圈鏡頭": "光圈鏡頭", "近拍模式": "近拍模式", "殘影": "殘影",
             "隨意拍拍": "隨意拍拍", "開始播放": "開始播放", "光學": "光學", "快門": "快門", "相片": "相片", "照像": "照像", "像機": "像機", "實拍": "實拍"}
#通信字典
dicComm = {"4GLTE": "4GLTE", "wifi": "wifi", "WIFI": "WIFI", "4G": "4G", "3g": "3g", "3G": "3G", "LTE": "LTE",
           "WiFi": "WiFi", "Wifi": "Wifi", "網路": "網路", "上網": "上網", "訊號": "訊號", "SIM卡": "SIM卡", "MSM": "MSM",
           "Wi-Fi": "Wi-Fi", "通話": "通話", "連線": "連線", "4G訊號": "4G訊號", "GPS": "GPS", "打電話": "打電話", "收訊": "收訊", "傳輸": "傳輸",
           "頻段": "頻段", "4g": "4g", "4G網路": "4G網路", "4G全頻": "4G全頻", "行動通訊": "行動通訊", "基地台": "基地台", "通話品質": "通話品質",
           "熱點": "熱點", "頻寬": "頻寬", "行動網路": "行動網路", "流量": "流量", "斷訊": "斷訊", "斷線": "斷線", "wifi熱點": "wifi熱點", "開台": "開台",
           "資料": "資料", "數據": "數據", "頻率": "頻率", "gps": "gps", "行動數據": "行動數據", "GPS定位": "GPS定位", "WCDMA": "WCDMA",
           "H+": "H+", "sim卡": "sim卡", "網路訊號": "網路訊號", "NFC": "NFC", "通訊": "通訊", "衛星導航": "衛星導航", "導航": "導航", "藍芽": "藍芽",
           "信號": "信號", "4G上網": "4G上網", "簡訊": "簡訊", "導航王": "導航王", "全頻": "全頻", "無線藍芽": "無線藍芽", "開通": "開通", "網路連線": "網路連線",
           "2格": "2格", "3格": "3格", "kbps": "kbps", "MHz": "MHz", "限速": "限速", "衛星定位": "衛星定位", "4G+": "4G+",
           "Hz頻段": "Hz頻段", "漫遊": "漫遊", "藍牙": "藍牙", "4G覆蓋": "4G覆蓋", "WIMAX": "WIMAX", "上傳速度": "上傳速度", "位置資料": "位置資料",
           "衛星訊號": "衛星訊號", "4GS": "4GS", "行動寬頻": "行動寬頻", "降速": "降速", "撥號": "撥號", "3G覆蓋": "3G覆蓋", "Mhz": "Mhz",
           "SIM": "SIM", "wi-fi": "wi-fi", "車用導航": "車用導航", "定位系統": "定位系統", "通訊協定": "通訊協定", "電信網路": "電信網路",
           "衛星系統": "衛星系統", "gsm": "gsm", "MHz-": "MHz-", "MHz+": "MHz+", "WiMax": "WiMax", "WiMAX": "WiMAX",
           "亞太網路": "亞太網路", "波段頻率": "波段頻率", "網內互打": "網內互打"}
#效能硬體字典
dicHardware = {"CPU": "CPU", "處理器": "處理器", "速度": "速度", "跑分": "跑分", "效能": "效能", "順暢": "順暢", "GHz": "GHz", "bps": "bps",
               "分數": "分數", "內核": "內核", "高通": "高通", "晶圓": "晶圓", "雙通": "雙通", "MHz": "MHz", "加速器": "加速器", "很順": "很順",
               "性能": "性能", "卡卡": "卡卡", "四核心": "四核心", "降低": "降低", "比較順": "比較順", "會卡": "會卡", "LAG": "LAG", "卡頓": "卡頓",
               "更順": "更順", "流暢": "流暢", "效率": "效率", "時脈": "時脈", "雙核心": "雙核心", "不順暢": "不順暢", "加快": "加快", "流暢度": "流暢度",
               "頓頓的": "頓頓的", "品質": "品質", "瑕疵": "瑕疵", "中國製": "中國製", "間隙": "間隙", "抱怨文": "抱怨文", "品管": "品管", "大陸製": "大陸製",
               "台灣製": "台灣製", "缺點": "缺點", "麻煩": "麻煩", "證明": "證明", "保證": "保證", "不穩定": "不穩定", "臺灣製造": "臺灣製造",
               "台灣品牌": "台灣品牌", "材質": "材質", "防水機有縫": "防水機有縫", "故障率": "故障率", "組裝不良": "組裝不良", "愛台灣": "愛台灣", "漏水": "漏水",
               "認證": "認證", "雙SIM": "雙SIM", "天線": "天線", "功能鍵": "功能鍵", "晶片": "晶片", "很順暢": "很順暢", "GPU": "GPU",
               "感應器": "感應器", "陀螺儀": "陀螺儀", "四核處理器": "四核處理器"}
#服務購買字典
dicService = {"千元": "千元", "維修": "維修", "退貨": "退貨", "送修": "送修", "中華": "中華", "處理": "處理", "退款": "退款", "神腦": "神腦",
              "客服": "客服", "服務": "服務", "發票": "發票", "保固": "保固", "退費": "退費", "說明": "說明", "申訴": "申訴", "門市": "門市",
              "維修文章": "維修文章", "維修單": "維修單", "送修前": "送修前", "故障維修": "故障維修", "維修單號": "維修單號", "延長保固": "延長保固", "態度": "態度",
              "維修進度": "維修進度", "購買證明": "購買證明", "維修中心": "維修中心", "櫃檯人員": "櫃檯人員", "再送修": "再送修", "廠商": "廠商", "維修單據": "維修單據",
              "送修回來": "送修回來", "維修部門": "維修部門", "欺騙消費": "欺騙消費", "櫃檯小姐": "櫃檯小姐", "客服中心": "客服中心", "騙消費者": "騙消費者",
              "想退": "想退", "線上客服": "線上客服", "退貨退款": "退貨退款", "拆解維修": "拆解維修", "查詢維修": "查詢維修", "手機維修": "手機維修", "損壞": "損壞",
              "詢問客服": "詢問客服", "問題送修": "問題送修", "店家辦理": "店家辦理", "保固部份": "保固部份", "災情不少": "災情不少", "保留發票": "保留發票",
              "客服人員": "客服人員", "維修紀錄": "維修紀錄", "維修人員": "維修人員", "團體訴訟": "團體訴訟", "維修費": "維修費", "維修中": "維修中", "修嗎": "修嗎",
              "換貨": "換貨", "賠償": "賠償", "價格": "價格", "大省方案": "大省方案", "價錢": "價錢", "推出": "推出", "便宜": "便宜", "消費者": "消費者",
              "售價": "售價", "這支": "這支", "發表": "發表", "開賣": "開賣", "方案": "方案", "市場": "市場", "降價": "降價", "空機": "空機",
              "CP值": "CP值", "定價": "定價", "遠傳": "遠傳", "入手": "入手", "推薦": "推薦", "預購": "預購", "大省": "大省", "銷售": "銷售",
              "台哥大": "台哥大", "購買": "購買", "續約": "續約", "電信公司": "電信公司", "消息": "消息", "產品": "產品", "官方": "官方", "排隊": "排隊",
              "想要": "想要", "出貨": "出貨", "多少": "多少", "考慮": "考慮", "超值": "超值", "中華電信": "中華電信", "值得": "值得", "報價": "報價",
              "預算": "預算", "大廠": "大廠", "亞太": "亞太", "想買": "想買", "旗艦": "旗艦", "旗艦機": "旗艦機", "購入": "購入", "中階": "中階",
              "搶購": "搶購", "機種": "機種", "買空機": "買空機", "新機": "新機", "划算": "划算", "優惠": "優惠", "雙卡雙待": "雙卡雙待", "台幣": "台幣",
              "上市": "上市", "低價": "低價", "價位": "價位", "中華大省": "中華大省", "早買早享受": "早買早享受", "高階": "高階", "通訊行": "通訊行",
              "手機廠商": "手機廠商", "台灣大哥大": "台灣大哥大", "高價": "高價", "綁約": "綁約", "資費": "資費", "價差": "價差", "下手": "下手",
              "手機價格": "手機價格", "拍賣": "拍賣", "訂價": "訂價", "降到": "降到", "飢餓行銷": "飢餓行銷", "買手機": "買手機", "萬元": "萬元",
              "電信業者": "電信業者", "平價": "平價", "低階手機": "低階手機", "信用卡": "信用卡", "購物": "購物", "觀望": "觀望", "不要買": "不要買",
              "分期": "分期", "市售": "市售", "行銷": "行銷", "折價卷": "折價卷", "購機": "購機", "00以上": "00以上", "00以下": "00以下",
              "30個月": "30個月", "cp": "cp", "水貨": "水貨", "性價比": "性價比", "品牌價值": "品牌價值", "降得很快": "降得很快", "原價": "原價",
              "特價": "特價", "搶到一隻": "搶到一隻", "新品": "新品", "體驗會": "體驗會", "山寨機": "山寨機", "付款方式": "付款方式", "行情": "行情",
              "折扣": "折扣", "沒貨": "沒貨", "長輩": "長輩", "促銷": "促銷", "首購": "首購", "發售": "發售", "費用": "費用", "預繳": "預繳",
              "賣價": "賣價", "禮卷": "禮卷", "綁手機": "綁手機", "月繳": "月繳", "加價": "加價", "市價": "市價", "生日禮物": "生日禮物", "現貨": "現貨",
              "匯率換算": "匯率換算", "價格跳水": "價格跳水", "禮券": "禮券", "下殺到": "下殺到", "下單": "下單", "跳水": "跳水", "中低階": "中低階",
              "比價": "比價", "市佔率": "市佔率", "孝親": "孝親", "直營店": "直營店", "專案": "專案", "單機價": "單機價", "黃牛價": "黃牛價", "福利品": "福利品",
              "福利機": "福利機", "熱銷": "熱銷", "吃到飽": "吃到飽", "亞太電信": "亞太電信"}
#音效字典
dicSound = {"聲音": "聲音", "音效配置": "音效配置", "音量": "音量", "音樂": "音樂", "音質": "音質", "鈴聲": "鈴聲", "來電鈴聲": "來電鈴聲", "音效": "音效",
            "喇叭": "喇叭", "小聲": "小聲", "靜音": "靜音", "擴音": "擴音", "錄音": "錄音", "大聲": "大聲", "多媒體": "多媒體", "電話": "電話",
            "降噪": "降噪", "播放": "播放", "播放音樂": "播放音樂", "雜音": "雜音", "聽筒": "聽筒", "禁音": "禁音", "鬧鈴": "鬧鈴", "低音": "低音",
            "破音": "破音", "語音": "語音", "數位降噪": "數位降噪", "MFX": "MFX", "耳朵": "耳朵", "沒聲": "沒聲", "開音": "開音", "底噪": "底噪",
            "音頻引擎": "音頻引擎", "原音": "原音", "樂效": "樂效", "調校": "調校", "噪音抑制": "噪音抑制", "MP3檔": "MP3檔", "千千動聽": "千千動聽",
            "耳音": "耳音", "耳罩": "耳罩", "知音": "知音", "整音": "整音", "選鈴": "選鈴"}
#儲存空間字典
dicStorage = {"記憶卡": "記憶卡", "記憶體": "記憶體", "16G": "16G", "16GB": "16GB", "28GB": "28GB", "30MB": "30MB", "32G": "32G",
              "32GB": "32GB", "64G": "64G", "64g": "64g", "64GB": "64GB", "Disk": "Disk", "flash": "flash", "GB": "GB",
              "GRAM": "GRAM", "MSD": "MSD", "msd": "msd", "RAM": "RAM", "ROM": "ROM", "SD": "SD", "SDHC": "SDHC",
              "SDSD": "SDSD", "內建空間": "內建空間", "內部儲存": "內部儲存", "容量": "容量", "能存": "能存", "儲存空間": "儲存空間", "儲存裝置": "儲存裝置",
              "總空間": "總空間", "儲存": "儲存", "SDXC": "SDXC"}
#觸控按鍵
dicTouch = {"觸控": "觸控", "觸控問題": "觸控問題", "觸控失靈": "觸控失靈", "觸控不良": "觸控不良", "鉛筆觸控": "鉛筆觸控", "感應": "感應", "靈敏": "靈敏",
            "觸發": "觸發", "觸控不靈": "觸控不靈", "發生斷觸": "發生斷觸", "觸控位置": "觸控位置", "多點觸控": "多點觸控", "觸碰": "觸碰", "觸控感應": "觸控感應",
            "大幅降低": "大幅降低", "觸點": "觸點", "觸控韌體": "觸控韌體", "觸控異常": "觸控異常", "觸控手感": "觸控手感", "接觸": "接觸", "非常靈敏": "非常靈敏",
            "接觸螢幕": "接觸螢幕"}
#使用者操作
dicUser = {"更新": "更新", "使用": "使用", "設定": "設定", "開啟": "開啟", "安裝": "安裝", "下載": "下載", "功能": "功能", "操作": "操作", "關閉": "關閉",
           "移除": "移除", "原廠設定": "原廠設定", "生存模式": "生存模式", "復原廠設": "復原廠設", "模式": "模式", "通知": "通知", "步驟": "步驟", "備份": "備份",
           "權限": "權限", "選項": "選項", "鍵盤": "鍵盤", "修正": "修正", "lock": "lock", "喚醒": "喚醒", "解除": "解除", "調整": "調整",
           "裝置管理": "裝置管理", "點擊": "點擊", "設置": "設置", "打字": "打字", "搜尋": "搜尋", "長按": "長按", "按鍵": "按鍵", "清除資料": "清除資料",
           "雙擊喚醒": "雙擊喚醒", "查詢": "查詢", "重置": "重置", "解壓縮": "解壓縮", "使用者": "使用者", "匯入": "匯入", "刷回原廠": "刷回原廠",
           "回復原廠": "回復原廠", "輸入密碼": "輸入密碼", "輸入法": "輸入法", "重新設定": "重新設定", "通知列": "通知列", "登入": "登入", "選取": "選取",
           "編輯": "編輯", "點開": "點開", "手勢": "手勢", "切換": "切換", "飛航模式": "飛航模式", "安全模式": "安全模式", "撥出": "撥出", "選單": "選單",
           "觸控震動": "觸控震動", "振動模式": "振動模式", "展示模式": "展示模式", "偵錯模式": "偵錯模式", "日文輸入": "日文輸入", "解壓縮檔": "解壓縮檔",
           "語音輸入": "語音輸入", "壓縮檔案": "壓縮檔案", "無法解壓": "無法解壓", "截圖選項": "截圖選項", "聲音選擇": "聲音選擇", "彈出": "彈出", "搜尋功能": "搜尋功能",
           "偵測模式": "偵測模式"}
#其他手機型號
dicModule ={}
with io.open("E:/project/projectData/etl/module/allModule.txt", 'r', encoding='utf-8') as f: #做字典的檔案
    for line in f: #一行為單位
        line = line.lstrip(BOM) #處理編碼問題
        dicModule[line.strip().encode("utf-8")] = 0

'''---------------把字典合併----------------'''
dicMerge = {}
dicMerge.update(dicAcc)
dicMerge.update(dicAppear)
dicMerge.update(dicBattery)
dicMerge.update(dicCamera)
dicMerge.update(dicComm)
dicMerge.update(dicHardware)
dicMerge.update(dicService)
dicMerge.update(dicSound)
dicMerge.update(dicStorage)
dicMerge.update(dicTouch)
dicMerge.update(dicUser)
dicMerge.update(dicModule)

'''--------SQL--------'''
cnx = MySQLdb.connect(host="10.120.28.14", user="dale", passwd="iii", db="project", charset='utf8')
cursor = cnx.cursor()
select = "SELECT %s FROM %s"
insert_classResult = "INSERT IGNORE INTO classResult (contentNo, titleNo, sourceWeb, classNo) values (%s,%s,%s,%s)"
insert_keyword = "INSERT IGNORE INTO keyword (contentNo, titleNo, sourceWeb, classNo,keyWord) values (%s,%s,%s,%s,%s)"
'''---------檢查寫出去的檔案----------'''
resultURL = "E:/project/projectData/result/new/{0}{1}"

'''--------結巴初始設定----------'''
wordCount = {}
#jieba.initialize()
jieba.set_dictionary('E:/project/projectData/dic/dict.txt.big.txt')  # 設定結巴主要字典(你要分類的別)
jieba.load_userdict('E:/project/projectData/dic//dicAcc.txt')  # 加入其他配件字典
jieba.load_userdict('E:/project/projectData/dic/dicAppear.txt')  # 加入外觀字典
jieba.load_userdict('E:/project/projectData/dic/dicBattery.txt')  # 加入電池字典
jieba.load_userdict('E:/project/projectData/dic/dicCamera.txt')  # 加入相機字典
jieba.load_userdict('E:/project/projectData/dic/dicComm.txt')  # 加入通信字典
jieba.load_userdict('E:/project/projectData/dic/dicHardware.txt')  # 加入硬體字典
jieba.load_userdict('E:/project/projectData/dic/dicService.txt')  # 加入服務與購買字典
jieba.load_userdict('E:/project/projectData/dic/dicSound.txt')  # 加入音效字典
jieba.load_userdict('E:/project/projectData/dic/dicStorage.txt')  # 加入儲存字典
jieba.load_userdict('E:/project/projectData/dic/dicTouch.txt')  # 加入觸控字典
jieba.load_userdict('E:/project/projectData/dic/dicUser.txt')  # 加入使用及操作字典
jieba.load_userdict('E:/project/projectData/dic/dicModule.txt')# 加入其他配件字典
'''---------------------開始斷詞-----------------------'''
cursor.execute("select contentNo,titleNo,sourceWeb,content from `content`")
for (contentNo, titleNo, sourceWeb, content) in cursor:
    print  contentNo, titleNo, sourceWeb, content
    contentNo =str(contentNo)
    titleNo = str(titleNo)

    # result = open(resultURL.format(cellModule, "/" + cellModule + "_Result.txt"), "w")  # wordOut = open(resultURL.format(cellModule, "/" + cellModule + "_result_Word.txt"), "w")
    # notPic = open(resultURL.format(cellModule, "/" + cellModule + "_result_NotPick.txt"), "w")

    words = jieba.cut(content, cut_all=False)  #叫jieba依照字典(.txt那個)斷詞
    #print content
    #outPut.write(line.encode('utf-8'))
    #print words
    check = 0  #處理同一關鍵字重複出現的問題的判斷變數 0表未出現 1表出現
    cheDic = {}  #對照是否重複出現的字典
    cheDicWord = {} #判斷
    for word in words:
        #print word + "/" #觀看斷詞結果
        #outPut.write(word.encode('utf-8')+'/') #寫出斷詞結果

        if word.encode('utf-8').strip() in dicMerge:  #該字若在我們的字庫中的話
            #以下是各字屬於哪個字庫的判斷
            if word.encode('utf-8').strip() in dicBattery:
                if 1 not in cheDic:
                    #print word + " 1"
                    #result.write(str(1) + '\t')
                    check = 1
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"1"
                    cursor.execute(insert_classResult,(contentNo,titleNo,sourceWeb,"1"))
                if word not in cheDicWord:
                    cheDicWord[word] = 1
                    #wordOut.write(word.encode('utf-8').strip() + "\t")
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"1"+word
                    cursor.execute(insert_keyword,(contentNo,titleNo,sourceWeb,"1",word))
                    #print word+" cl=1"
                cheDic[1] = 1

            elif word in dicUser:
                if 2 not in cheDic:
                    #print word + " 2"
                    #result.write(str(2) + '\t')
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"2"
                    cursor.execute(insert_classResult,(contentNo,titleNo,sourceWeb,"2"))
                    check = 1
                if word.encode('utf-8').strip() not in cheDicWord:
                    cheDicWord[word] = 1
                    #wordOut.write(word.encode('utf-8').strip() + "\t")
                    #print word+" cl=2"
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"2"+word
                    cursor.execute(insert_keyword,(contentNo,titleNo,sourceWeb,"2",word))
                cheDic[2] = 2

            elif word.encode('utf-8').strip() in dicCamera:
                if 3 not in cheDic:
                    #print word + " 3"
                    #result.write(str(3) + '\t')
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"3"
                    cursor.execute(insert_classResult,(contentNo,titleNo,sourceWeb,"3"))
                    check = 1
                if word not in cheDicWord:
                    cheDicWord[word] = 1
                    #wordOut.write(word.encode('utf-8').strip() + "\t")
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"3"+word
                    cursor.execute(insert_keyword,(contentNo,titleNo,sourceWeb,"3",word))
                    #print word+" cl=3"
                cheDic[3] = 3
            elif word.encode('utf-8').strip() in dicHardware:
                if 4 not in cheDic:
                    #print word + " 4"
                    #result.write(str(4) + '\t')
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"4"
                    cursor.execute(insert_classResult,(contentNo,titleNo,sourceWeb,"4"))
                    check = 1
                if word not in cheDicWord:
                    cheDicWord[word] = 1
                    #wordOut.write(word.encode('utf-8').strip() + "\t")
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"4"+word
                    cursor.execute(insert_keyword,(contentNo,titleNo,sourceWeb,"4",word))
                    #print word+" cl=4"
                cheDic[4] = 4
            elif word.encode('utf-8').strip() in dicStorage:
                if 5 not in cheDic:
                    #print word + " 5"
                    #result.write(str(5) + '\t')
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"5"
                    cursor.execute(insert_classResult,(contentNo,titleNo,sourceWeb,"5"))

                    check = 1
                if word not in cheDicWord:
                    cheDicWord[word] = 1
                    #wordOut.write(word.encode('utf-8').strip() + "\t")
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"5"+word
                    #print word+" cl=5"
                    cursor.execute(insert_keyword,(contentNo,titleNo,sourceWeb,"5",word))
                cheDic[5] = 5
            elif word.encode('utf-8').strip() in dicService:
                if 6 not in cheDic:
                    #print word + " 6"
                    #result.write(str(6) + '\t')
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"6"
                    cursor.execute(insert_classResult,(contentNo,titleNo,sourceWeb,"6"))
                    check = 1
                if word not in cheDicWord:
                    cheDicWord[word] = 1
                    #wordOut.write(word.encode('utf-8').strip() + "\t")
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"6"+word
                    cursor.execute(insert_keyword,(contentNo,titleNo,sourceWeb,"6",word))
                    #print word+" cl=6"

                cheDic[6] = 6
            elif word.encode('utf-8').strip() in dicAppear:
                if 7 not in cheDic:
                    #print word + " 7"
                    #result.write(str(7) + '\t')
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"7"
                    cursor.execute(insert_classResult,(contentNo,titleNo,sourceWeb,"7"))
                    check = 1
                if word not in cheDicWord:
                    cheDicWord[word] = 1
                    #wordOut.write(word.encode('utf-8').strip() + "\t")
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"7"+word
                    cursor.execute(insert_keyword,(contentNo,titleNo,sourceWeb,"7",word))
                    #print word+" cl=7"

                cheDic[7] = 7
            elif word.encode('utf-8').strip() in dicSound:
                if 8 not in cheDic:
                    #print word + " 8"
                    #result.write(str(8) + '\t')
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"8"
                    cursor.execute(insert_classResult,(contentNo,titleNo,sourceWeb,"8"))
                    check = 1
                if word not in cheDicWord:
                    cheDicWord[word] = 1
                    #wordOut.write(word.encode('utf-8').strip() + "\t")
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"8"+word
                    cursor.execute(insert_keyword,(contentNo,titleNo,sourceWeb,"8",word))
                    #print word+" cl=8"
                cheDic[8] = 8
            elif word.encode('utf-8').strip() in dicComm:
                if 9 not in cheDic:
                    #print word + " 9"
                    #result.write(str(9) + '\t')
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"9"
                    cursor.execute(insert_classResult,(contentNo,titleNo,sourceWeb,"9"))
                    check = 1
                if word not in cheDicWord:
                    cheDicWord[word] = 1
                    #wordOut.write(word.encode('utf-8').strip() + "\t")
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"9"+word
                    cursor.execute(insert_keyword,(contentNo,titleNo,sourceWeb,"9",word))
                    #print word+" cl=9"

                cheDic[9] = 9
            elif word.encode('utf-8').strip() in dicTouch:
                if 10 not in cheDic:
                    #print word + " 10"
                    #result.write(str(10) + '\t')
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"10"
                    cursor.execute(insert_classResult,(contentNo,titleNo,sourceWeb,"10"))
                    check = 1
                if word not in cheDicWord:
                    cheDicWord[word] = 1
                    #wordOut.write(word.encode('utf-8').strip() + "\t")
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"10"+word
                    cursor.execute(insert_keyword,(contentNo,titleNo,sourceWeb,"10",word))
                    #print word+" cl=10"

                cheDic[10] = 10
            elif word.encode('utf-8').strip() in dicAcc:
                if 11 not in cheDic:
                    #print word + " 11"
                    #result.write(str(11) + '\t')
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"11"
                    cursor.execute(insert_classResult,(contentNo,titleNo,sourceWeb,"11"))
                    check = 1
                if word.encode('utf-8').strip() not in cheDicWord:
                    cheDicWord[word] = 1
                    #wordOut.write(word.encode('utf-8').strip() + "\t")
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"11"+word
                    cursor.execute(insert_keyword,(contentNo,titleNo,sourceWeb,"11",word))
                    #print word+" cl=11"
                cheDic[11] = 11
            #手機
            elif word.encode('utf-8').strip() in dicModule:
                if 12 not in cheDic:
                    #print word + " 11"
                    #result.write(str(11) + '\t')
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"12"
                    cursor.execute(insert_classResult,(contentNo,titleNo,sourceWeb,"12"))
                    check = 1
                if word.encode('utf-8').strip() not in cheDicWord:
                    cheDicWord[word] = 1
                    #wordOut.write(word.encode('utf-8').strip() + "\t")
                    print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"12"+word
                    cursor.execute(insert_keyword,(contentNo,titleNo,sourceWeb,"12",word))
                    #print word+" cl=12"
                cheDic[12] = 12
    if check == 1:
        print cheDic
        #result.write("\n")
        #wordOut.write("\n")


    if check == 0:
        print '-----------------reOut--------------------------'
        print contentNo+"\t"+titleNo+"\t"+sourceWeb+"\t"+"0"
        cursor.execute(insert_classResult,(contentNo,titleNo,sourceWeb,"0"))
        print 0
        #result.write(str(0) + '\n')
        #wordOut.write("notPick\t" + line.encode('utf-8'))
        #notPic.write(line.encode('utf-8'))
    #outPut.write('\n--------------------------\n')
    print '-------------endLine----------------'  #result.close()
#wordOut.close()
#notPic.close()
'''-----commitsql指令-----'''
cnx.commit()
cursor.close()
cnx.close()
'''-------印執行時間-------'''
end = time.time()
totalTime = end - start
print totalTime
#outPut.close()