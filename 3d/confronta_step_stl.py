# Prova: gli STL di OpenSCAD e gli STEP di CadQuery sono lo stesso pezzo? Volume, ingombro e numero di corpi separati.
# Uso: python confronta_step_stl.py <file.stl> [<file.step>]
import re
import sys


def leggi_stl(p):
    num = re.compile(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)")
    v = [tuple(round(float(x), 4) for x in m.groups()) for m in num.finditer(open(p, errors="ignore").read())]
    return [v[i:i + 3] for i in range(0, len(v), 3)]


def misura_stl(p):
    tri = leggi_stl(p)
    vol = 0.0
    padre = {}

    def trova(a):
        while padre.setdefault(a, a) != a:
            padre[a] = padre[padre[a]]
            a = padre[a]
        return a

    for a, b, c in tri:
        vol += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6
        padre[trova(a)] = trova(b)
        padre[trova(b)] = trova(c)
    corpi = len({trova(a) for a in list(padre)})
    pts = [q for t in tri for q in t]
    ing = [max(q[i] for q in pts) - min(q[i] for q in pts) for i in range(3)]
    return abs(vol), corpi, ing


if __name__ == "__main__":
    vol, corpi, ing = misura_stl(sys.argv[1])
    print(f"STL  {sys.argv[1].split('/')[-1]}: corpi separati={corpi} volume={vol:.1f} mm3 ingombro={ing[0]:.2f} x {ing[1]:.2f} x {ing[2]:.2f}")
    if len(sys.argv) > 2:
        import cadquery as cq
        s = cq.importers.importStep(sys.argv[2])
        sol = s.solids().vals()
        v2 = sum(x.Volume() for x in sol)
        bb = s.val().BoundingBox()
        print(f"STEP {sys.argv[2].split('/')[-1]}: solidi={len(sol)} volume={v2:.1f} mm3 ingombro={bb.xlen:.2f} x {bb.ylen:.2f} x {bb.zlen:.2f}")
        print(f"differenza di volume: {100 * (v2 - vol) / vol:+.3f} %")
