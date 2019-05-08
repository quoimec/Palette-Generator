#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from textwrap import wrap

scrapeURL = "https://colorhunt.co/hunt.php"
scrapeParams = {"step": 0, "sort": "popular"}

userHeader = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive"
}

stillPallets = True
paletteData = []

while stillPallets:
    
    httpResponse = requests.post(scrapeURL, headers = userHeader, data = scrapeParams)
    httpText = httpResponse.text

    if httpText == "<script>arr = [];</script>":
        stillPallets = False
    elif httpText[0:14] == "<script>arr = " and httpText[-10:] == ";</script>":
        
        paletteData += list(map(lambda a: {
            "id": int(a["id"]),
            "date": a["date"],
            "likes": int(a["likes"]),
            "colours": list(map(lambda b: {"r": int(b[0:2], 16), "g": int(b[2:4], 16), "b": int(b[4:6], 16)}, wrap(a["code"], 6)))
        }, json.loads(httpText[14:-13] + "]")))
        
        scrapeParams["step"] += 1
        
    else:
        print("Error: {}".format(httpText))
        stillPallets = False

json.dump(paletteData, open("palette_dump.json", "w"), indent = 4)

