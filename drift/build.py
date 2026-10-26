#!/usr/bin/env python3
"""seed.json + app.html -> index.html (standalone) and artifact.html (fragment for claude.ai)."""
import json, sys, pathlib
here = pathlib.Path(__file__).parent
seed = json.loads((here / "seed.json").read_text(encoding="utf-8"))
blob = json.dumps(seed, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
frag = (here / "app.html").read_text(encoding="utf-8").replace("__SEED__", blob)
out = sys.argv[1] if len(sys.argv) > 1 else str(here / "artifact.html")
pathlib.Path(out).write_text(frag, encoding="utf-8")
standalone = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
  '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
  '<meta name="apple-mobile-web-app-capable" content="yes">\n'
  '<meta name="apple-mobile-web-app-status-bar-style" content="default">\n'
  '<meta name="theme-color" content="#F2F4F7">\n'
  '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}[hidden]{display:none!important}</style>\n'
  + frag + '\n</head>\n</html>\n')
# the fragment already carries <title>/<style>/<div>/<script>; browsers tolerate body content after head, but keep it explicit:
standalone = standalone.replace('</style>\n\n<div class="app">', '</style>\n</head>\n<body>\n<div class="app">', 1).replace('\n</head>\n</html>\n', '\n</body>\n</html>\n')
(here / "index.html").write_text(standalone, encoding="utf-8")
print("ok", len(frag), "bytes fragment")
