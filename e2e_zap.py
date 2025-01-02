from zapv2 import ZAPv2

# Inisialisasi ZAP
zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

# Target URL
target = 'http://127.0.0.1:5000'

# Akses target
zap.urlopen(target)
print(f"Scanning target: {target}")

# Menunggu hingga spider selesai
while int(zap.spider.status(zap.spider.scan(target))) < 100:
    pass

# Memulai active scan
zap.ascan.scan(target)
while int(zap.ascan.status(0)) < 100:
    pass

# Cetak hasil
print("Active Scan Completed!")
report = zap.core.alerts()
print(report)
