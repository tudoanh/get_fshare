# A Fshare API tool built with Python
-----------------
[![Build Status](https://circleci.com/gh/tudoanh/get_fshare.png?style=shield&circle-token=76fafffc2a4ba9d254a5a1d3ac6583b75daff3c2)](https://circleci.com/gh/tudoanh/get_fshare)
[![forthebadge](http://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)
[![forthebadge](http://forthebadge.com/images/badges/check-it-out.svg)](http://forthebadge.com)  [![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)

## Getting started  

First, install `get_fshare` with `pip`:  
``` bash
$ pip install get_fshare
```  

Then you can use normaly.  

**Example code**  

``` python
from get_fshare import FSAPI

URL = 'https://www.fshare.vn/folder/THFVWDY4YT'

bot = FSAPI(email="Your email", password="Your password")
bot.login()
sillicon_valley_ss1 = bot.get_folder_urls(URL)

for episode in sillicon_valley_ss1:
    print(episode['name'], bot.download("https://www.fshare.vn/file/{}".format(episode['linkcode'])))
```

**Result**  

```
Silicon.Valley.S01.720p.HDTV.E002-PhimVIPvn.net.mp4 http://download003.fshare.vn/dl/DDw36kqC+XtnxDDabH3A9WxhgvC5dnROeIhBefBDTSHwtO-OGzVKi3JVTEHeR4f1YO+1QVBogiKQiHj5/Silicon.Valley.S01.720p.HDTV.E002-PhimVIPvn.net.mp4
Silicon.Valley.S01.720p.HDTV.E001-PhimVIPvn.net.mp4 http://download008.fshare.vn/dl/H709d9NNl-p5kexaSvch+R9NrTzO16qBg2MdecmkU6fp797Y0gUNH6EinO6d0sRd4l4LRC57v6LTefFo/Silicon.Valley.S01.720p.HDTV.E001-PhimVIPvn.net.mp4
Silicon.Valley.S01.720p.HDTV.E003-PhimVIPvn.net.mp4 http://download015.fshare.vn/dl/-PzHlZBIkJBzRY6SpkeoYuiAKOiG004BGeyx35rYSWdsfgX+00sB32oBNZIIpNivmUjR7iYQFA8dPE3p/Silicon.Valley.S01.720p.HDTV.E003-PhimVIPvn.net.mp4
Silicon.Valley.S01.720p.HDTV.E004-PhimVIPvn.net.mp4 http://download019.fshare.vn/dl/4jIObmhjP76LcLvKNaKDVB43F2Y-sSrsirX5fzYPqXPJqi+p180Cv7mcnOAYO00djvUfKJi0tqgys4ar/Silicon.Valley.S01.720p.HDTV.E004-PhimVIPvn.net.mp4
Silicon.Valley.S01.720p.HDTV.E005-PhimVIPvn.net.mp4 http://download016.fshare.vn/dl/c4lknf1YF3VmfZ5Uf6GL6RFDWH-OE+87a6eSCb4S39SKDIaI8ZjVEazwHctkX8I+jBIthKbF69GPpEb-/Silicon.Valley.S01.720p.HDTV.E005-PhimVIPvn.net.mp4
Silicon.Valley.S01.720p.HDTV.E006-PhimVIPvn.net.mp4 http://download014.fshare.vn/dl/W7OsskpPLzZQJniLGOGublqpW7LqX0yRRW0pShFAmqhoXYMU-Qm9xIDMAJo9XNNx00yq+lipJH+vMLMW/Silicon.Valley.S01.720p.HDTV.E006-PhimVIPvn.net.mp4
Silicon.Valley.S01.720p.HDTV.E007-PhimVIPvn.net.mp4 http://download001.fshare.vn/dl/QGxNHPMoPVghhSpiamBqNhrtLnqsjjz3xO1DVMEnkyR4Jd2aBrcuvnhbpSd7iBgOPeZBhCHvEvrcX0yA/Silicon.Valley.S01.720p.HDTV.E007-PhimVIPvn.net.mp4
Silicon.Valley.S01.720p.HDTV.E008-PhimVIPvn.net.mp4 http://download014.fshare.vn/dl/+kYq54+P2Bo6rwx6JmSMDKSdbogsya8dlRPiwxIs6RK2mQ90VCgOv2fgsLyXkA5fBu9XALh6tmmZAmOF/Silicon.Valley.S01.720p.HDTV.E008-PhimVIPvn.net.mp4
```  

## Requirements  
* Python 3.5+
* [requests](https://github.com/request/request)
* [lxml](https://github.com/lxml/lxml)


## Current functions  
* Get Fshare download link
* Extract links from Fshare folder
* Get file name from link
* Get file size from link  
* Upload file to your Fshare account

## Test
Just run `pytest`

## Question?  
Please create issues so I can improve or fix my lib.  


## Enjoy and have fun :)  
*Fork what you can, push ~~nothing~~ something back!*  
<center>  

![](http://24.media.tumblr.com/tumblr_lvnf2zS3Xc1qjhjdwo2_r3_500.gif)  

![](http://25.media.tumblr.com/tumblr_lvnf2zS3Xc1qjhjdwo3_r3_500.gif)
</center>
