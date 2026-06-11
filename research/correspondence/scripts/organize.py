import json
P='research/intrinsic/latent_features.json'
L=json.load(open(P,encoding='utf-8'))
cat_order=["Lexical baselines","Rhythm / wave","Rhyme / sound","Self-reference / network",
           "Constellation / matrix","Sūra definition","Order / sequence","Optimality / perturbation","Āyah"]
CAT={"L01":"Lexical baselines","L02":"Lexical baselines",
     "L03":"Rhythm / wave","L04":"Rhythm / wave","L05":"Rhythm / wave",
     "L06":"Rhyme / sound","L07":"Rhyme / sound","L08":"Self-reference / network",
     "L09":"Constellation / matrix","L10":"Constellation / matrix",
     "L11":"Sūra definition","L12":"Sūra definition","L15":"Sūra definition","L16":"Sūra definition",
     "L14":"Order / sequence","L13":"Optimality / perturbation","L17":"Āyah"}
L['category_order']=cat_order
for f in L['features']:
    f['category']=CAT[f['id']]
# sort: by category order, then grade desc, then id
oidx={c:i for i,c in enumerate(cat_order)}
L['features'].sort(key=lambda f:(oidx[f['category']], -f['review']['grade'], f['id']))
# upgrade candidate C1 to record the TWO discovered gaps (the user's point)
for c in L.get('candidates',[]):
    if c['id']=='C1':
        c['evidence']=("Canonical MDL cost 30,679 b sits BETWEEN random 40,632 b (gap-to-random = +9,952 b, the L14 order-load) "
                       "and sorted-homogeneous 18,938–23,470 b (gap-to-sorted = 7,209–11,741 b, the text's resistance to trivial sorting). "
                       "Two distinct measurable quantities, not one.")
        c['why_new']=("Sorting the verses compresses BETTER than canonical — but that is meaningless ordering, so it does NOT mean a "
                      "rearrangement is 'better'. Instead the sorting test DISCOVERS new features: (1) gap-to-random = how non-arbitrary "
                      "the order is; (2) gap-to-sorted = how much the order sacrifices compressibility to preserve meaning. The Qur'an "
                      "occupies the intermediate band of meaningful sequences.")
        c['discovered_quantities']={"gap_to_random_bits":9952,"gap_to_sorted_length_bits":11741,"gap_to_sorted_rhyme_bits":7209}
json.dump(L,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print("organized into",len(cat_order),"categories; order:",[CAT[f['id']] for f in L['features']][:6],"...")
print("category sizes:",{c:sum(1 for f in L['features'] if f['category']==c) for c in cat_order})
