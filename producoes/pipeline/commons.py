import json,sys,urllib.request,urllib.parse
UA={"User-Agent":"LadoSombrioBot/1.0 (canal educativo; contato via github)"}
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
q=sys.argv[1]
d=get("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6&gsrlimit=6&gsrsearch="+urllib.parse.quote(q)+"&prop=imageinfo&iiprop=url|size|extmetadata&iiurlwidth=1920")
for p in (d.get("query",{}).get("pages",{}) or {}).values():
    ii=p["imageinfo"][0]; m=ii.get("extmetadata",{})
    lic=m.get("LicenseShortName",{}).get("value","?"); art=m.get("Artist",{}).get("value","")[:60]
    print(p["title"][:70],"|",lic,"|",ii.get("width"),"x",ii.get("height"),"|",ii.get("thumburl"))
