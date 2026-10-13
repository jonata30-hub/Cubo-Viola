// CUBO DI VIOLA — involucro stampabile (box, 11/10/2026, richiesta di Jonata). Tutte le misure in mm, PARAMETRICHE.
// Pezzi: «corpo» (cubo con il coperchio e l'alloggio del PE, aperto sotto) + «fondo» (VASSOIO avvitato: porta Minx, ampli, convertitore e presa DC; il fondo entra a filo dentro le pareti).
// ⚠️ DA VERIFICARE col righello: misure del PE, del pannello (da scegliere), posizione dei connettori del PE.
parte = "tutto";          // "corpo" | "fondo" | "tutto" (anteprima esplosa)

// ── cubo
L = 150;                  // lato esterno (Jonata: 15 x 15)
R = 14;                   // raggio degli spigoli verticali arrotondati
P = 3;                    // spessore delle pareti
$fn = 64;

// ── Voice PE (alloggio superiore: A FILO del coperchio, appoggiato su un gradino — Jonata 12/10/2026)
pe_lato = 83;             // misurato da Jonata col calibro il 12/10/2026 (83 x 83 x 20)
pe_alto = 20;             // misurato da Jonata il 12/10/2026
pe_r = 8;                 // raggio degli angoli del PE: diagonale misurata 110,5 (Jonata 12/10 22:48) -> raggio 8,3; messo 8 per stare larghi
gioco = 0.6;              // aria fra PE e incavo (per lato)
affondo = pe_alto;        // il PE entra tutto: il suo piano sopra e' a filo del coperchio
gradino = 5;              // larghezza dell'appoggio su cui poggia il PE
cavo_l = 50;              // finestra per le spine USB-C e jack sul lato posteriore (nicchia misurata da Jonata il 12/10: 19 - 45 - 19, centrata)

// ── pannello touch (davanti): Waveshare ESP32-S3-Touch-LCD-4. Vetro 84 x 84 (la parte piu' larga), scheda dietro 75 x 75.
// Si monta DA FUORI: la scheda passa nel foro, il vetro si incolla sulla faccia esterna (Jonata 12/10 22:13)
pan_vista_l = 77; pan_vista_h = 77;   // FORO nella parete: 77 x 77 (Jonata 12/10 22:17; scheda 75, vetro 84 -> appoggio 3,5 per lato)
pan_sch_l = 84;   pan_sch_h = 84;     // vetro del pannello (non usato nel taglio: appoggia fuori)
pan_sch_sp = 2;                       // profondita' della battuta
pan_z = 85;                           // altezza del centro dello schermo da terra

// ── cassa Cambridge Audio Minx Min 12: 78 x 78 x 85, cono 57 mm. Sta contro il RETRO, verso il muro (Jonata 12/10 21:45)
minx_z = 55;              // altezza del centro del cono

// ── retro: presa DC e prese d'aria
dc_d = 10.3;            // presa di alimentazione: diametro 10 (Jonata 12/10/2026) + 0,3 di gioco
dc_x = 51; dc_z = 25;     // presa DC sul retro, nell'angolo in basso accanto alla cassa (Jonata 12/10 21:50)
// ── VASSOIO (v3, Jonata 12/10): tutto si monta sul fondo, poi il cubo ci si cala sopra
ling_l = 17; ling_h = 33.7;         // linguetta del fondo che porta la presa DC ed entra in una tacca del retro
minx_l = 78; minx_p = 83;             // Minx: 78 x 78, profonda 83 (calibro di Jonata 12/10 21:58)
ala_sp = 2.5; ala_h = 22; ala_lung = 45; ala_gioco = 0.5;   // ali che fermano la Minx
staf_l = 16; staf_sp = 3; vite_z = 37; asola_l = 6.5; asola_h = 8;   // staffa sulla vite centrale del retro della Minx (centro a 37 dal piano d'appoggio; fra i morsetti 25 liberi) ; vite quasi 6 mm = M6, asola 6,5
minx_y0 = L/2 - P - 0.5 - minx_p;     // filo anteriore della Minx (il cono guarda la griglia del retro, +Y)
// ampli HW-327A (TPA3118 mono): 46 x 35 misurato da Jonata 12/10; 4 fori agli angoli
amp_x = 46; amp_y = 35; amp_h = 13; amp_cx = -30; amp_cy = -48;
amp_ix = 40; amp_iy = 28;             // interasse dei 4 fori (Jonata 12/10 21:57); componenti piu' alti 13 mm
// convertitore Fulree 12->5 V 3 A: scatoletta 46 x 27 x 13 misurata da Jonata 12/10; alette sui lati corti non misurate ⚠️
buck_x = 46; buck_y = 27; buck_h = 13; buck_cx = 30; buck_cy = -46;
culla_h = 6; culla_sp = 1.6; culla_gioco = 0.3; fasc_l = 4.5;   // culla del convertitore e passaggio della fascetta
col_d = 6; col_h = 5; col_foro = 1.7;                       // colonnine sotto l'ampli: fori della scheda da 2 mm (Jonata 12/10 22:11) -> viti M2, foro 1,7 per autofilettare
bordo_h = 2; bordo_sp = 1.6;                                // cornice bassa che segna il posto della scheda
// ── fondo
f_sp = 3;                 // spessore del fondo
vite_ins = 4.2;           // foro per inserto filettato M3 a caldo
vite_passo = L/2 - 12;    // posizione delle 4 viti

module tondo(l, h, r) { linear_extrude(h) offset(r) square(l - 2*r, center=true); }

// griglia: fessure a parallelogramma inclinate, ritagliate dentro il rettangolo della faccia
fess_l = 22; fess_h = 5; fess_passo_x = 30; fess_passo_y = 10; fess_incl = 35;
// zona senza fessure attorno alla tacca della presa DC
kx0 = dc_x - ling_l/2 - 4; kx1 = dc_x + ling_l/2 + 4; kz1 = ling_h + 4;
fianchi_rilievo = false;   // SOLO ANTEPRIMA: fianchi incisi (non bucati). NON e' in cubo_step.py.
scritta_fianco = ""; scritta_sotto = "";   // VARIANTE «scritta» (Jonata 12/10 22:33): -D 'scritta_fianco="Viola"' -D 'scritta_sotto="Villa alle Rane"', incise sul fianco destro. In cubo_step.py: argomento «scritta».
scritta_prof = 1;          // profondita' dell'incisione
fianchi_griglia = false;   // SOLO ANTEPRIMA (dubbio di Jonata 12/10 22:17): fessure anche sui due fianchi. NON e' in cubo_step.py.
module griglia_diagonale(w, h, libera=false) {
  intersection() {
    translate([-w/2, 13]) square([w, h]);
    for (r=[0 : fess_passo_y : L], c=[-L : fess_passo_x : L]) {
      ox = c + (r/fess_passo_y % 2) * fess_passo_x/2;
      if (libera || !(ox < kx1 && ox + fess_l + fess_h*tan(fess_incl) > kx0 && r < kz1))
        translate([ox, r]) multmatrix([[1, tan(fess_incl), 0, 0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]) square([fess_l, fess_h]);
    }
  }
}

// torretta -> parete: un blocco largo quanto la torretta fino dentro la parete d'angolo, e sopra una
// mensola inclinata (meno di 45 gradi) perche' si stampi senza supporti con il coperchio sul piatto
tor_d = 9; tor_h = 14; mens_h = 16;
tor_diag = vite_passo * sqrt(2);                 // distanza della torretta dal centro, lungo la diagonale
par_diag = (L/2 - R) * sqrt(2) + R - P/2;        // meta' spessore della parete d'angolo, lungo la diagonale
module rinforzo_torretta() {
  rotate(45) {
    translate([tor_diag, -tor_d/2, 0]) cube([par_diag - tor_diag, tor_d, tor_h]);
    rotate([90,0,0]) translate([0,0,-tor_d/2]) linear_extrude(tor_d)
      polygon([[tor_diag - tor_d/2, tor_h], [par_diag, tor_h], [par_diag, tor_h + mens_h]]);
  }
}

module corpo() {
  difference() {
    union() {
      difference() {
        tondo(L, L, R);
        translate([0,0,-1]) tondo(L - 2*P, L - P + 1, R - P);        // vuoto interno, aperto sotto
      }
      // spessore extra sotto il coperchio dove sta il PE
      translate([0,0,L - P - affondo]) tondo(pe_lato + 2*gioco + 2*gradino + 8, affondo, pe_r + 4);
      // torrette agli angoli per le viti del fondo, ATTACCATE alla parete d'angolo (12/10: prima erano sospese)
      for (sx=[-1,1], sy=[-1,1]) translate([sx*vite_passo, sy*vite_passo, f_sp]) cylinder(d=tor_d, h=tor_h);
      intersection() {
        tondo(L, L, R);
        for (sx=[0,1], sy=[0,1]) mirror([sx,0,0]) mirror([0,sy,0]) translate([0,0,f_sp]) rinforzo_torretta();
      }
    }
    // ALLOGGIO PE: incavo della sagoma del PE + foro passante piu' piccolo (resta il gradino)
    translate([0,0,L - affondo]) tondo(pe_lato + 2*gioco, affondo + 1, pe_r + gioco);
    translate([0,0,L - affondo - 20]) tondo(pe_lato - 2*gradino, 21, max(pe_r - gradino, 2));
    // finestra per le spine del PE (verso il retro, +Y): attraversa la parete dell'alloggio, sotto il coperchio
    translate([-cavo_l/2, pe_lato/2 - gradino - 1, L - affondo - 20]) cube([cavo_l, 2*gradino + 8, 20 + affondo - P]);
    // PANNELLO: foro passante davanti (-Y); niente battuta, il vetro appoggia sulla faccia esterna
    translate([0, -L/2 - 1, pan_z]) rotate([-90,0,0]) linear_extrude(P + 2) offset(2) square([pan_vista_l - 4, pan_vista_h - 4], center=true);
    // RETRO (+Y) TUTTO A GRIGLIA, fessure diagonali: dietro c'e' la Minx, e da li' esce anche l'aria calda. Fianchi chiusi.
    translate([0, L/2 + 1, 0]) rotate([90,0,0]) linear_extrude(P + 2) griglia_diagonale(L - 2*R + 6, L - 26);
    // SOLO ANTEPRIMA: stesso disegno delle fessure ma INCISO per 1 mm, senza bucare (fianchi chiusi ma non lisci)
    if (fianchi_rilievo) for (sx=[0,1]) mirror([sx,0,0]) translate([L/2 - 1, 0, 0]) rotate([90,0,90]) linear_extrude(2) griglia_diagonale(L - 2*R + 6, L - 26, true);
    if (scritta_fianco != "") translate([L/2 - scritta_prof, 0, 78]) rotate([90,0,90]) linear_extrude(scritta_prof + 1) text(scritta_fianco, size=30, font="Liberation Sans:style=Bold", halign="center", valign="center");
    if (scritta_sotto != "") translate([L/2 - scritta_prof, 0, 40]) rotate([90,0,90]) linear_extrude(scritta_prof + 1) text(scritta_sotto, size=9, font="Liberation Sans", halign="center", valign="center");
    if (fianchi_griglia) for (sx=[0,1]) mirror([sx,0,0]) translate([L/2 - P - 1, 0, 0]) rotate([90,0,90]) linear_extrude(P + 2) griglia_diagonale(L - 2*R + 6, L - 26, true);
    // tacca aperta verso il basso: ci entra la linguetta del fondo con la presa DC
    translate([dc_x - (ling_l + 0.4)/2, L/2 - P - 1, -1]) cube([ling_l + 0.4, P + 2, ling_h + 0.3 + 1]);
    // fori per gli inserti filettati
    for (sx=[-1,1], sy=[-1,1]) translate([sx*vite_passo, sy*vite_passo, f_sp - 1]) cylinder(d=vite_ins, h=12);
  }
}

// posto di una scheda: cornice bassa + 4 colonnine con foro (centro cx,cy; ingombro lx x ly; interasse fori ix x iy)
module posto_scheda(cx, cy, lx, ly, ix, iy) {
  translate([cx, cy, f_sp]) {
    difference() {
      translate([-lx/2 - bordo_sp, -ly/2 - bordo_sp, 0]) cube([lx + 2*bordo_sp, ly + 2*bordo_sp, bordo_h]);
      translate([-lx/2, -ly/2, -1]) cube([lx, ly, bordo_h + 2]);
    }
    for (sx=[-1,1], sy=[-1,1]) translate([sx*ix/2, sy*iy/2, 0])
      difference() { cylinder(d=col_d, h=col_h); translate([0,0,1]) cylinder(d=col_foro, h=col_h); }
  }
}

// culla del convertitore (scatoletta senza fori): parete lunga dietro, fermo corto davanti (li' escono i cavi)
module culla(cx, cy, lx, ly) {
  translate([cx, cy, f_sp]) {
    translate([-lx/2, ly/2 + culla_gioco, 0]) cube([lx, culla_sp, culla_h]);
    translate([-6, -ly/2 - culla_gioco - culla_sp, 0]) cube([12, culla_sp, culla_h]);
  }
}
// passaggio della fascetta: due asole nel fondo e un canale sotto che le unisce
module passaggio_fascetta(cx, cy, ly) {
  y1 = ly/2 + culla_gioco + culla_sp;
  for (sy=[-1,1]) translate([cx - fasc_l/2, cy + (sy > 0 ? y1 : -y1 - 2), -1]) cube([fasc_l, 2, f_sp + 2]);
  translate([cx - fasc_l/2, cy - y1 - 2, -1]) cube([fasc_l, 2*y1 + 4, 1 + 1.2]);
}

module fondo() {
  mezza = minx_l/2 + ala_gioco;
  difference() {
    union() {
      tondo(L - 2*P - 0.6, f_sp, R - P);
      // MINX: due ali ai fianchi e una STAFFA centrale che sale fra i due morsetti fino alla vite del retro (la vite tiene la cassa anche verso l'alto)
      translate([-staf_l/2, minx_y0 - ala_gioco - staf_sp, f_sp]) cube([staf_l, staf_sp, vite_z + 9]);
      for (x0=[-staf_l/2, staf_l/2 - 2]) translate([x0, minx_y0 - ala_gioco - staf_sp + 0.01, f_sp]) rotate([90,0,90]) linear_extrude(2) polygon([[0,0],[-12,0],[0,25]]);
      for (sx=[-1,1]) translate([sx > 0 ? mezza : -mezza - ala_sp, minx_y0 - ala_gioco - ala_sp, f_sp]) cube([ala_sp, ala_lung, ala_h]);
      // AMPLI su 4 colonnine, CONVERTITORE nella sua culla
      posto_scheda(amp_cx, amp_cy, amp_x, amp_y, amp_ix, amp_iy);
      culla(buck_cx, buck_cy, buck_x, buck_y);
      // LINGUETTA DELLA PRESA DC: sale dal fondo nel piano della parete posteriore, con due nervature basse
      translate([dc_x - ling_l/2, L/2 - P - 3, 0]) cube([ling_l, P + 3, f_sp]);
      translate([dc_x - ling_l/2, L/2 - P, 0]) cube([ling_l, P, ling_h]);
      for (x0=[dc_x - ling_l/2, dc_x + ling_l/2 - 4]) translate([x0, L/2 - P + 0.01, f_sp]) rotate([90,0,90]) linear_extrude(2) polygon([[0,0],[-12,0],[0,12]]);
    }
    for (sx=[-1,1], sy=[-1,1]) translate([sx*vite_passo, sy*vite_passo, -1]) { cylinder(d=3.4, h=f_sp + 2); cylinder(d=6.5, h=1.8); }
    for (x=[-12:6:12]) translate([amp_cx + x - 1.5, amp_cy - 10, -1]) cube([3, 20, f_sp + 2]);   // aria dal basso, sotto l'ampli
    passaggio_fascetta(buck_cx, buck_cy, buck_y);
    translate([-asola_l/2, minx_y0 - ala_gioco - staf_sp - 1, f_sp + vite_z - asola_h/2]) cube([asola_l, staf_sp + 2, asola_h]);   // asola per la vite della Minx
    translate([dc_x, L/2 - P - 1, dc_z]) rotate([-90,0,0]) cylinder(d=dc_d, h=P + 2);     // foro della presa DC
  }
}

if (parte == "corpo") corpo();
else if (parte == "corpo_grigio") color("gainsboro") corpo();   // solo per le viste: un colore solo, cosi' i tagli non sembrano fori
else if (parte == "fondo") fondo();
else if (parte == "fondo_grigio") color("gainsboro") fondo();
else if (parte == "chiuso") { color("gainsboro") corpo(); color("orange") fondo(); }   // solo per le viste: cubo calato sul vassoio (vassoio in arancione)
else if (parte == "vassoio_montato") {   // solo per le viste: il vassoio con gli ingombri dei pezzi montati
  color("gainsboro") fondo();
  color("white", 0.85) translate([-minx_l/2, minx_y0, f_sp]) cube([minx_l, minx_p, minx_l]);                    // cassa Minx
  color("silver") for (x0=[12.5, -24.5]) translate([x0, minx_y0 - 12, f_sp + 12]) cube([12, 12, 12]);            // morsetti
  color("royalblue") translate([amp_cx - amp_x/2, amp_cy - amp_y/2, f_sp + col_h]) cube([amp_x, amp_y, amp_h]);  // ampli
  color("dimgray") translate([buck_cx - buck_x/2, buck_cy - buck_y/2, f_sp]) cube([buck_x, buck_y, buck_h]);     // convertitore
  color("orange") translate([dc_x, L/2 - P - 14, dc_z]) rotate([-90,0,0]) cylinder(d=10, h=20);                  // presa di alimentazione
}
else { corpo(); translate([0,0,-40]) color("gray") fondo(); }
