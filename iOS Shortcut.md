<p align="center">
  <a href="https://www.icloud.com/shortcuts/1d48a361d7fd49f296833dd372b92eeb">
    <img src="https://user-images.githubusercontent.com/5026621/83965777-078efd80-a86b-11ea-9cf7-debc677ad785.png">
  </a>
</p>

Link: https://www.icloud.com/shortcuts/1d48a361d7fd49f296833dd372b92eeb

<hr>

Approximate textual representation:
```
1: Get Latest Screenshots (3 Screenshots)
2: Get Items from ⊲1⊳ (Items in Range, 2 to End)
3: Crop Images from ⊲2⊳ (Position Custom, x:680 y:86 w:415 h:2311)
4: Get Item from ⊲1⊳ (First Item)
5: Crop Image from ⊲4⊳ (Position Custom, x:800 y:1690 w:290 h:520)
6: List ⊲3⊳,⊲5⊳
7: Base64 Encode ⊲6⊳ (Encode, Line Breaks None)
8: Get Item from List ⊲7⊳ (Item at Index 1)
9: Get Item from List ⊲7⊳ (Item at Index 3)
10: Get Item from List ⊲7⊳ (Item at Index 2)
11: Get Contents of URL (https://r3plac3m3.execute-api.us-east-1.amazonaws.com/default/ingress-stats-ocr, Method POST, Request Body JSON {now: ⊲8⊳, alltime1: ⊲9⊳, alltime2: ⊲10⊳})
12: Text (⏎)
13: Replace Text ⊲11⊳ (Replace \n with ⊲12⊳, Regex: No, Case Sensitive: Yes)
14: Quick Look ⊲13⊳
15: Delete Photos ⊲1⊳
```

<hr>

Screenshot:
<p align="center">
  <img src="https://user-images.githubusercontent.com/5026621/83966845-8be47f00-a871-11ea-9bce-aa19739ca917.png" width="50%">
</p>
