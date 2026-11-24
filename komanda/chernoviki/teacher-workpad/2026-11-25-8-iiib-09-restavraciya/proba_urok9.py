"""proba_urok9.py — пройти приложение урока 9 в headless Chrome: старт, две сетки, протокол, задачи; скриншоты экранов."""
import pathlib
import sys
from playwright.sync_api import sync_playwright

SOSED = [[8, 8, 4, 0], [8, 4, 0, 0], [4, 0, 0, 4], [0, 0, 4, 8]]


# vvesti: таблица id и функция эталона → ввод цифр в каждую клетку
def vvesti(s, tablica, etalon, n):
    polya = s.locator(f'#{tablica} input')
    for k in range(n * n):
        polya.nth(k).fill(str(etalon(k // n, k % n)))
        polya.nth(k).dispatch_event('input')
    return n * n


# sered: эталон середин
def sered(i, j):
    os_ = lambda x: [x // 2] if x % 2 == 0 else [x // 2, x // 2 + 1]
    v = [SOSED[a][b] for a in os_(i) for b in os_(j)]
    return sum(v) // len(v)


# proba: путь урока → печать хода и ошибок
def proba(url):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome')
        s = b.new_page(viewport={'width': 1366, 'height': 768}); err = []
        s.on('pageerror', lambda e: err.append(str(e))); s.on('console', lambda m: m.type == 'error' and err.append(m.text))
        s.goto(url); s.wait_for_timeout(1500); s.screenshot(path='/tmp/p9/1-start.png', full_page=True)
        s.click('#kody button >> nth=2'); s.click('#gipotezy button >> nth=0'); s.fill('#gipSlovo', 'больше'); s.dispatch_event('#gipSlovo', 'input')
        s.click('#kStart'); s.wait_for_timeout(800)
        vvesti(s, 'tSosed', lambda i, j: SOSED[i // 2][j // 2], 8)
        print('сосед:', s.inner_text('#sSosed'), '| середины видны:', s.is_visible('#blokSerediny'))
        vvesti(s, 'tSerediny', sered, 7)
        print('середины:', s.inner_text('#sSerediny'), '| к студии:', s.is_enabled('#kKStudii'), '| статус:', s.inner_text('#status'))
        s.screenshot(path='/tmp/p9/2-setka.png', full_page=True)
        s.click('#kKStudii'); s.wait_for_timeout(500)
        for k in range(5):
            s.locator('.progon').nth(k).locator('button').first.click()
            pole = s.locator('.progon').nth(k).locator('input[type=text]'); pole.fill('слово'); pole.dispatch_event('change')
        print('вскрыть:', s.is_enabled('#kVskryt')); s.click('#kVskryt')
        for k, o in enumerate([100, 25, 40, 16, 81]):
            pole = s.locator('#obratnaya input').nth(k); pole.fill(str(o)); pole.dispatch_event('input')
        s.fill('#itog', 'формула взяла только исходник а ИИ дорисовал цвет зонта'); s.dispatch_event('#itog', 'input')
        s.check('#chPometka'); s.check('#chSohranil'); s.click('#kGotovo'); s.wait_for_timeout(300)
        print('финал:', s.inner_text('#final').replace('\n', ' '))
        s.screenshot(path='/tmp/p9/3-studiya.png', full_page=True)
        s.reload(); s.wait_for_timeout(1200); print('после перезагрузки экран:', s.evaluate('S.ekran'), '| очки:', s.inner_text('#stOchki'))
        print('ошибки:', err); b.close()
    return True


proba(pathlib.Path(sys.argv[1]).resolve().as_uri())
