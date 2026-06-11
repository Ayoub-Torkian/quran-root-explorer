"""#52 — are the 14 muqaṭṭaʿāt letters a STRUCTURED half of the alphabet (phonetic balance)?
Tests the popular 'half of each phonetic category' claim against a permutation null (random 14-subsets).
NOTE on divine-rootedness control: voicing/articulation are intrinsic properties of the revealed
CONSONANTS (the letter qāf IS a uvular stop regardless of vocalization) — not ḥarakāt. The formal sifa
taxonomy is a human linguistic *description* of intrinsic sounds; flagged, not vocalization-dependent.

RESULT (honest): the 14/28 cardinality is exact; voicing splits EXACTLY half (5/10 voiceless, 9/18
voiced), and emphatic (2/4) & stop (4/8) are also exactly half — individually striking. BUT the AGGREGATE
balance across 6 categories is only modestly better than random (dev 5.0 vs null 9.9, p=0.14, sub-2σ);
throat (4/6) and labial (1/4) deviate. With ~6 features, a few exact halves arise by chance. => the
'half of every phonetic category' claim is PARTIAL and NOT statistically distinctive. The real
muqaṭṭaʿāt signal remains the POSITIONAL pointer (#50/#51), not phonetic structuring.
"""
import numpy as np
rng = np.random.default_rng(52)
ALPHABET = list("ءبتثجحخدذرزسشصضطظعغفقكلمنهوي")  # 28; ا treated as ء for consonant phonetics
MUQ = set("ءلمنركهيعطسحقص")                       # 14 muqaṭṭaʿāt (alif->hamza)
CLASSES = {
 "mahmusa(voiceless)": set("فحثهشخصسكت"),
 "itbaq(emphatic)":    set("صضطظ"),
 "shadida(stop)":      set("ءجدقطبكت"),
 "qalqala":            set("قطبجد"),
 "halqi(throat)":      set("ءهعحغخ"),
 "shafawi(labial)":    set("بفمو"),
}
def balance_dev(S):
    tot = 0.0
    for cls in CLASSES.values():
        comp = set(ALPHABET) - cls
        tot += abs(len(S & cls) - len(cls) / 2) + abs(len(S & comp) - len(comp) / 2)
    return tot

if __name__ == "__main__":
    print("muqaṭṭaʿāt set size:", len(MUQ))
    for nm, cls in CLASSES.items():
        print(f"   {nm:18s}: {len(MUQ&cls)} of {len(cls)} (half={len(cls)/2:.1f})")
    obs = balance_dev(MUQ)
    null = np.array([balance_dev(set(rng.choice(ALPHABET, 14, replace=False))) for _ in range(20000)])
    print(f"balance dev obs={obs:.1f} | null {null.mean():.1f}±{null.std():.1f} | p={np.mean(null<=obs):.4f} z={(obs-null.mean())/null.std():+.2f}")
    mah = len(MUQ & CLASSES["mahmusa(voiceless)"])
    print(f"voicing: {mah}/10 voiceless, {14-mah}/18 voiced (exactly-half: {mah==5})")
