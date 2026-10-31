import json, random, sys, datetime as dt
from pathlib import Path
run = Path(sys.argv[1]); random.seed(7)
base = dt.datetime(2026, 10, 28, 12, 0, tzinfo=dt.timezone.utc)
def d(i): return base - dt.timedelta(days=i * 6 + random.randint(0, 3))
def w(p, o):
    p = run / "raw" / p; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(o), encoding="utf-8")
def ig(user, n, scale):
    out = []
    for i in range(n):
        vid = i % 3 != 2
        o = {"ownerUsername": user, "shortCode": f"{user[:3]}{i:03d}", "type": "Video" if vid else "Image", "timestamp": d(i).isoformat(),
             "likesCount": int(scale * random.uniform(.02, .08) * (6 if i == 1 else 1)), "commentsCount": random.randint(2, 60),
             "caption": f"{user} post {i}: 3 tips for better results\nsecond line", "displayUrl": "", "url": f"https://www.instagram.com/p/{user[:3]}{i:03d}/"}
        if vid:
            o["videoPlayCount"] = int(scale * random.uniform(.5, 1.5) * (7 if i == 1 else 1)); o["videoDuration"] = random.randint(15, 60)
        out.append(o)
    return out
w("instagram/items.json", ig("rivalone", 12, 20000) + ig("usbrand", 8, 3000))
w("instagram/status.json", {"privateco": "private"})
tt = []
for i in range(10):
    tt.append({"authorMeta": {"name": "rivalone", "fans": 90000}, "id": f"73{i:05d}", "createTimeISO": d(i).isoformat(), "playCount": int(40000 * random.uniform(.3, 2)),
               "diggCount": random.randint(500, 4000), "commentCount": random.randint(5, 90), "shareCount": random.randint(1, 200), "collectCount": random.randint(1, 300),
               "videoMeta": {"duration": random.randint(10, 50), "coverUrl": ""}, "text": f"tiktok {i} behind the scenes hook", "webVideoUrl": f"https://www.tiktok.com/@rivalone/video/73{i:05d}"})
w("tiktok/items.json", tt)
meta = []
for i in range(6):
    meta.append({"pageName": "Rival One", "pageId": "111", "adArchiveID": f"9000{i}", "startDateFormatted": d(i * 3).strftime("%Y-%m-%d"), "isActive": i < 4,
                 "snapshot": {"body": {"text": f"Limited offer {i}: save 20 percent this week"}, "images": [{"original_image_url": ""}]}, "url": f"https://www.facebook.com/ads/library/?id=9000{i}"})
w("meta/items.json", meta)
x = []
for i in range(5):
    x.append({"noteId": f"xn{i}", "user": {"nickname": "Rival One", "userId": "abc123"}, "time": int(d(i * 2).timestamp() * 1000), "likedCount": "1.2万" if i == 0 else str(300 + i),
              "commentCount": str(20 + i), "collectedCount": str(150 + i), "title": f"{i} tips to save time", "cover": "", "url": f"https://www.xiaohongshu.com/explore/xn{i}"})
w("xhs/items.json", x)
w("instagram/followers.json", [{"username": "rivalone", "followersCount": 120000}, {"username": "usbrand", "followersCount": 8000}])
print("fixtures written")
