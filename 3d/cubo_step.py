# CUBO DI VIOLA — gli stessi due pezzi di cubo.scad, costruiti come SOLIDI VERI per l'esportazione STEP.
# OpenSCAD non sa scrivere STEP: questo file ripete la geometria di cubo.scad con CadQuery.
# Uso: python cubo_step.py <cartella di uscita> [scritta]   (con «scritta»: fianco destro inciso, file cubo_corpo_scritta.step)
# ⚠️ Le misure sono le stesse di cubo.scad: se cambi un numero la', cambialo anche qui (prova: confronta_step_stl.py).
import math
import sys

import cadquery as cq

# ── cubo
L = 150; R = 14; P = 3
# ── Voice PE
pe_lato = 83; pe_alto = 20; pe_r = 8; gioco = 0.6; affondo = pe_alto; gradino = 5; cavo_l = 50
# ── pannello
pan_vista_l = 77; pan_vista_h = 77; pan_sch_l = 84; pan_sch_h = 84; pan_sch_sp = 2; pan_z = 85
# ── retro e fondo
dc_d = 10.3; f_sp = 3; vite_ins = 4.2; vite_passo = L / 2 - 12
# ── griglia
fess_l = 22; fess_h = 5; fess_passo_x = 30; fess_passo_y = 10; fess_incl = 35
# ── vassoio (v3): il fondo porta Minx, ampli, convertitore e presa DC
dc_x = 51; dc_z = 25; ling_l = 17; ling_h = 33.7
minx_l = 78; minx_p = 83; ala_sp = 2.5; ala_h = 22; ala_lung = 45; ala_gioco = 0.5
minx_y0 = L / 2 - P - 0.5 - minx_p
staf_l = 16; staf_sp = 3; vite_z = 37; asola_l = 6.5; asola_h = 8
amp_x = 46; amp_y = 35; amp_h = 13; amp_cx = -30; amp_cy = -48; amp_ix = 40; amp_iy = 28
buck_x = 46; buck_y = 27; buck_h = 13; buck_cx = 30; buck_cy = -46
culla_h = 6; culla_sp = 1.6; culla_gioco = 0.3; fasc_l = 4.5
col_d = 6; col_h = 5; col_foro = 1.7; bordo_h = 2; bordo_sp = 1.6
scritta_prof = 1
kx0 = dc_x - ling_l / 2 - 4; kx1 = dc_x + ling_l / 2 + 4; kz1 = ling_h + 4
# ── torrette
tor_d = 9; tor_h = 14; mens_h = 16
tor_diag = vite_passo * math.sqrt(2)
par_diag = (L / 2 - R) * math.sqrt(2) + R - P / 2


def tondo(l, h, r, z=0.0):
    """Quadrato di lato l con gli spigoli verticali arrotondati di raggio r, da z a z+h."""
    return cq.Workplane("XY").workplane(offset=z).rect(l, l).extrude(h).edges("|Z").fillet(r)


def scatola(x0, y0, z0, dx, dy, dz):
    return cq.Workplane("XY").box(dx, dy, dz, centered=False).translate((x0, y0, z0))


def rinforzo_torretta():
    """Angolo +X +Y: blocco dalla torretta fin dentro la parete, piu' la mensola inclinata sopra."""
    blocco = scatola(tor_diag, -tor_d / 2, 0, par_diag - tor_diag, tor_d, tor_h)
    mensola = (cq.Workplane("XZ")
               .polyline([(tor_diag - tor_d / 2, tor_h), (par_diag, tor_h), (par_diag, tor_h + mens_h)]).close()
               .extrude(tor_d / 2, both=True))
    return blocco.union(mensola).rotate((0, 0, 0), (0, 0, 1), 45)


def griglia():
    """Fessure a parallelogramma del retro (+Y), come griglia_diagonale() di cubo.scad; niente fessure attorno alla tacca DC."""
    w = L - 2 * R + 6; h = L - 26
    t = math.tan(math.radians(fess_incl))
    u0, u1, v0, v1 = -w / 2, w / 2, 13, 13 + h
    disegno = cq.Workplane("XZ")
    r = 0
    while r <= L:
        c = -L
        while c <= L:
            ox = c + ((r // fess_passo_y) % 2) * fess_passo_x / 2
            pts = [(ox, r), (ox + fess_l, r), (ox + fess_l + fess_h * t, r + fess_h), (ox + fess_h * t, r + fess_h)]
            vietata = ox < kx1 and ox + fess_l + fess_h * t > kx0 and r < kz1
            if not vietata and max(p[0] for p in pts) > u0 and min(p[0] for p in pts) < u1 and r + fess_h > v0 and r < v1:
                disegno = disegno.polyline(pts).close()
            c += fess_passo_x
        r += fess_passo_y
    fessure = disegno.extrude(P + 2, both=True).translate((0, L / 2 - P / 2, 0))
    limite = scatola(u0, L / 2 - P - 1, v0, w, P + 2, h)
    return fessure.intersect(limite)


def scritta(testo, corpo_car, grassetto, centro, zc):
    """Scritta incisa sul fianco destro (+X), come text() di cubo.scad: corpo_car e centro sono tarati sull'ingombro che da' OpenSCAD."""
    fp = "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf" % ("Bold" if grassetto else "Regular")
    t = cq.Workplane("XY").text(testo, corpo_car, scritta_prof + 1, fontPath=fp, halign="center", valign="center")
    b = t.val().BoundingBox()
    t = t.translate((centro[0] - (b.xmin + b.xmax) / 2, centro[1] - (b.ymin + b.ymax) / 2, 0))
    return t.rotate((0, 0, 0), (1, 0, 0), 90).rotate((0, 0, 0), (0, 0, 1), 90).translate((L / 2 - scritta_prof, 0, zc))


def corpo(con_scritta=False):
    s = tondo(L, L, R).cut(tondo(L - 2 * P, L - P + 1, R - P, z=-1))
    lato_pe = pe_lato + 2 * gioco + 2 * gradino + 8
    s = s.union(tondo(lato_pe, affondo, pe_r + 4, z=L - P - affondo))
    for sx in (-1, 1):
        for sy in (-1, 1):
            s = s.union(cq.Workplane("XY").circle(tor_d / 2).extrude(tor_h).translate((sx * vite_passo, sy * vite_passo, f_sp)))
    rinf = rinforzo_torretta().translate((0, 0, f_sp))
    rinf4 = rinf.union(rinf.mirror("YZ")).union(rinf.mirror("XZ")).union(rinf.mirror("YZ").mirror("XZ"))
    s = s.union(rinf4.intersect(tondo(L, L, R)))
    # alloggio del PE
    s = s.cut(tondo(pe_lato + 2 * gioco, affondo + 1, pe_r + gioco, z=L - affondo))
    s = s.cut(tondo(pe_lato - 2 * gradino, 21, max(pe_r - gradino, 2), z=L - affondo - 20))
    s = s.cut(scatola(-cavo_l / 2, pe_lato / 2 - gradino - 1, L - affondo - 20, cavo_l, 2 * gradino + 8, 20 + affondo - P))
    # pannello: foro passante davanti (-Y), il vetro appoggia fuori
    finestra = (cq.Workplane("XZ").center(0, pan_z).rect(pan_vista_l, pan_vista_h).extrude(-(P + 2))
                .edges("|Y").fillet(2).translate((0, -L / 2 - 1, 0)))
    s = s.cut(finestra)
    # retro (+Y) tutto a griglia; tacca per la linguetta della presa DC
    s = s.cut(griglia())
    s = s.cut(scatola(dc_x - (ling_l + 0.4) / 2, L / 2 - P - 1, -1, ling_l + 0.4, P + 2, ling_h + 0.3 + 1))
    if con_scritta:   # variante «scritta»: Viola (30) e Villa alle Rane (9), come nell'anteprima approvata da Jonata
        s = s.cut(scritta("Viola", 41.664, True, (0.546, 0.352), 78))
        s = s.cut(scritta("Villa alle Rane", 12.499, False, (-0.169, 0.106), 40))
    # fori per gli inserti filettati
    for sx in (-1, 1):
        for sy in (-1, 1):
            s = s.cut(cq.Workplane("XY").workplane(offset=f_sp - 1).circle(vite_ins / 2).extrude(12)
                      .translate((sx * vite_passo, sy * vite_passo, 0)))
    return s


def posto_scheda(cx, cy, lx, ly, ix, iy):
    """Cornice bassa che segna il posto della scheda + 4 colonnine con foro."""
    cornice = (scatola(-lx / 2 - bordo_sp, -ly / 2 - bordo_sp, 0, lx + 2 * bordo_sp, ly + 2 * bordo_sp, bordo_h)
               .cut(scatola(-lx / 2, -ly / 2, -1, lx, ly, bordo_h + 2)))
    s = cornice
    for sx in (-1, 1):
        for sy in (-1, 1):
            col = (cq.Workplane("XY").circle(col_d / 2).extrude(col_h)
                   .cut(cq.Workplane("XY").workplane(offset=1).circle(col_foro / 2).extrude(col_h)))
            s = s.union(col.translate((sx * ix / 2, sy * iy / 2, 0)))
    return s.translate((cx, cy, f_sp))


def culla(cx, cy, lx, ly):
    """Culla del convertitore: parete lunga dietro, fermo corto davanti."""
    s = scatola(-lx / 2, ly / 2 + culla_gioco, 0, lx, culla_sp, culla_h)
    s = s.union(scatola(-6, -ly / 2 - culla_gioco - culla_sp, 0, 12, culla_sp, culla_h))
    return s.translate((cx, cy, f_sp))


def fondo():
    mezza = minx_l / 2 + ala_gioco
    s = tondo(L - 2 * P - 0.6, f_sp, R - P)
    # Minx: due ali ai fianchi e staffa centrale sulla vite del retro
    ya = minx_y0 - ala_gioco - ala_sp
    ys = minx_y0 - ala_gioco - staf_sp
    s = s.union(scatola(-staf_l / 2, ys, f_sp, staf_l, staf_sp, vite_z + 9))
    for x0 in (-staf_l / 2, staf_l / 2 - 2):
        nerv = (cq.Workplane("YZ").polyline([(ys + 0.01, f_sp), (ys + 0.01 - 12, f_sp), (ys + 0.01, f_sp + 25)]).close().extrude(2)
                .translate((x0, 0, 0)))
        s = s.union(nerv)
    s = s.union(scatola(mezza, ya, f_sp, ala_sp, ala_lung, ala_h))
    s = s.union(scatola(-mezza - ala_sp, ya, f_sp, ala_sp, ala_lung, ala_h))
    s = s.union(posto_scheda(amp_cx, amp_cy, amp_x, amp_y, amp_ix, amp_iy))
    s = s.union(culla(buck_cx, buck_cy, buck_x, buck_y))
    # linguetta della presa DC con due nervature basse
    s = s.union(scatola(dc_x - ling_l / 2, L / 2 - P - 3, 0, ling_l, P + 3, f_sp))
    s = s.union(scatola(dc_x - ling_l / 2, L / 2 - P, 0, ling_l, P, ling_h))
    for x0 in (dc_x - ling_l / 2, dc_x + ling_l / 2 - 4):
        y1 = L / 2 - P + 0.01
        nerv = (cq.Workplane("YZ").polyline([(y1, f_sp), (y1 - 12, f_sp), (y1, f_sp + 12)]).close().extrude(2)
                .translate((x0, 0, 0)))
        s = s.union(nerv)
    for sx in (-1, 1):
        for sy in (-1, 1):
            foro = cq.Workplane("XY").workplane(offset=-1).circle(3.4 / 2).extrude(f_sp + 2)
            svaso = cq.Workplane("XY").workplane(offset=-1).circle(6.5 / 2).extrude(1.8)
            s = s.cut(foro.union(svaso).translate((sx * vite_passo, sy * vite_passo, 0)))
    for x in range(-12, 13, 6):
        s = s.cut(scatola(amp_cx + x - 1.5, amp_cy - 10, -1, 3, 20, f_sp + 2))
    s = s.cut(scatola(-asola_l / 2, ys - 1, f_sp + vite_z - asola_h / 2, asola_l, staf_sp + 2, asola_h))
    # passaggio della fascetta del convertitore
    y1 = buck_y / 2 + culla_gioco + culla_sp
    s = s.cut(scatola(buck_cx - fasc_l / 2, buck_cy + y1, -1, fasc_l, 2, f_sp + 2))
    s = s.cut(scatola(buck_cx - fasc_l / 2, buck_cy - y1 - 2, -1, fasc_l, 2, f_sp + 2))
    s = s.cut(scatola(buck_cx - fasc_l / 2, buck_cy - y1 - 2, -1, fasc_l, 2 * y1 + 4, 2.2))
    s = s.cut(cq.Workplane("XZ").center(dc_x, dc_z).circle(dc_d / 2).extrude(-(P + 2)).translate((0, L / 2 - P - 1, 0)))
    return s


if __name__ == "__main__":
    dest = sys.argv[1] if len(sys.argv) > 1 else "."
    con_scritta = len(sys.argv) > 2 and sys.argv[2] == "scritta"
    c, f = corpo(con_scritta), fondo()

    def vol(w):
        return sum(x.Volume() for x in w.solids().vals()) if w.vals() else 0.0

    # cose montate sul VASSOIO: Minx, i suoi due morsetti (sporgono 12, alti fino a 24, 25 liberi in mezzo; larghezza 12 stimata), ampli, convertitore
    sul_vassoio = (scatola(-minx_l / 2, minx_y0, f_sp, minx_l, minx_p, minx_l)
                   .union(scatola(amp_cx - amp_x / 2, amp_cy - amp_y / 2, f_sp + col_h, amp_x, amp_y, amp_h))
                   .union(scatola(buck_cx - buck_x / 2, buck_cy - buck_y / 2, f_sp, buck_x, buck_y, buck_h)))
    for x0 in (12.5, -24.5):
        sul_vassoio = sul_vassoio.union(scatola(x0, minx_y0 - 12, f_sp + 6, 12, 12, 18))
    # cose montate sul CUBO: PE nel coperchio; pannello (scheda 75 x 75 nel foro, 17 mm dal vetro appoggiato fuori)
    sul_cubo = tondo(pe_lato, pe_alto, pe_r, z=L - pe_alto).union(scatola(-37.5, -L / 2, pan_z - 37.5, 75, 17, 75))

    print(f"cubo contro vassoio: volume in comune = {vol(c.intersect(f)):.2f} mm3 (deve essere 0)")
    print(f"cubo contro Minx, morsetti, ampli, convertitore, PE, pannello: {vol(c.intersect(sul_vassoio.union(sul_cubo))):.2f} mm3 (deve essere 0)")
    print(f"vassoio contro gli stessi ingombri: {vol(f.intersect(sul_vassoio.union(sul_cubo))):.2f} mm3 (deve essere 0)")
    print(f"PE e pannello contro Minx, ampli, convertitore: {vol(sul_cubo.intersect(sul_vassoio)):.2f} mm3 (deve essere 0)")
    urti = 0
    for dz in range(10, 101, 10):
        v = vol(c.union(sul_cubo).translate((0, 0, dz)).intersect(f.union(sul_vassoio)))
        if v > 0.001:
            urti += 1
            print(f"URTO calando il cubo (con PE e pannello) a {dz} mm: {v:.2f} mm3")
    print(f"calata del cubo con PE e pannello a 10 altezze (10..100 mm): urti = {urti}")
    for nome, pezzo in (("cubo_corpo_scritta" if con_scritta else "cubo_corpo", c), ("cubo_fondo", f)):
        solido = pezzo.val()
        cq.exporters.export(pezzo, f"{dest}/{nome}.step")
        bb = solido.BoundingBox()
        print(f"{nome}: solidi={len(pezzo.solids().vals())} valido={solido.isValid()} volume={solido.Volume():.1f} mm3 "
              f"ingombro={bb.xlen:.2f} x {bb.ylen:.2f} x {bb.zlen:.2f}")
