import json
from rich.console import Console
console = Console()

raw = ""

with open("raw.json","r") as f:
    raw = f.read()

replies = json.loads(raw)

out = []

filte = input("输入过滤词(空字符表示不过滤)\n")

for r in replies:
    if filte in r["content"]["message"]:
        content = {"content":r["content"]["message"]}
        if not  r["replies"] is None:
            sub_rs = r["replies"]
            ref = []
            content["replies"] = ref
            for sub_r in sub_rs:
                sub_content = {"content":sub_r["content"]["message"]}
                ref.append(sub_content)
        out.append(content)
    
console.print(out)
input("----end----")