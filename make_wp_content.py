#!/usr/bin/env python3
"""Génère le contenu à coller dans le bloc HTML WordPress à partir d'une page du repo.

  python3 make_wp_content.py index.html  > wp-page-content.txt   (LP Stratégie Privée, page WP 1768)
  python3 make_wp_content.py merci.html  > wp-merci-content.txt  (page de remerciement)

Transformation : on retire doctype/html/head/body/meta/title/noscript, les
liens de polices marqués <!-- fonts:github-only --> (le thème WordPress charge
déjà Montserrat), les images passent en URL absolue vers GitHub Pages, et le
tout est enveloppé dans <!-- wp:html -->. La ligne PageView (trackSingle)
est conservée : PixelYourSite n'envoie PageView que sur l'ancien pixel.
"""
import re, sys

src_path = sys.argv[1]
src = open(src_path, encoding='utf-8').read()
head = re.search(r'<head>(.*?)</head>', src, re.S).group(1)
body = re.search(r'<body>(.*?)</body>', src, re.S).group(1)
lines = []
for l in head.split('\n'):
    s = l.strip()
    if s.startswith('<meta') or s.startswith('<title'):
        continue
    if 'fonts:github-only' in l:
        continue
    lines.append(l)
head2 = re.sub(r'<noscript>.*?</noscript>\n?', '', '\n'.join(lines), flags=re.S)
content = (head2 + body).replace('src="assets/', 'src="https://alexyoucompte99-lang.github.io/lp-investisseurs30/assets/')
label = {'index.html': 'Page "Stratégie Privée" : contenu complet de la LP.',
         'merci.html': 'Page "Appel réservé" (remerciement après réservation iClosed).'}.get(src_path, src_path)
sys.stdout.write('<!-- wp:html -->\n<!-- ' + label + ' Modèle : Elementor Canvas. -->' + content + '<!-- /wp:html -->\n')
