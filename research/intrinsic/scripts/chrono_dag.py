# -*- coding: utf-8 -*-
"""Chronology as a PARTIAL-ORDER DAG. Event backbone ordered by AH (edge iff AH strictly less; same AH =
PARALLEL = contemporaneous). Era prefix + directional developmental threads (gradual rulings, promise->
fulfilment, referent-emergence) weave through as parallel processes. Test DAG, layers (= time strata with
simultaneity), and incomparability (non-linearity)."""
import networkx as nx, itertools
G=nx.DiGraph()
# time coordinate (Meccan negative; AH for Medinan). None = no global coordinate (placed only by edges).
T={'EarlyMecca':-3,'MidMecca':-2,'LateMecca':-1,'Hijra':0,'Badr':2,'Qibla':2,'Uhud':3,
   'BanuNadir/Hashr':4,'Khandaq/Ahzab':5,'Hudaybiyya/Fath':6,'HajjRuling':6,'Conquest/Nasr':8,
   'Tabuk':9,'MasjidDirar':9,'Najran/Mubahala':9.5,'Maida/Farewell':10}
for n in T: G.add_node(n)
# backbone: edge iff strictly earlier AH (same AH -> no edge -> PARALLEL/contemporaneous)
for a,b in itertools.permutations(T,2):
    if T[a]<T[b]: G.add_edge(a,b)
# developmental THREADS (directional, internal evidence) — parallel processes, anchored to windows by <= edges
khamr=['khamr:provision(16:67)','khamr:sin&benefit(2:219)','khamr:no-pray-drunk(4:43)','khamr:prohibition(5:90)']
nx.add_path(G,khamr)
G.add_edge('LateMecca',khamr[0]); G.add_edge(khamr[0],'Hijra')          # provision is late-Meccan
G.add_edge('Hijra',khamr[1]); G.add_edge(khamr[3],'Maida/Farewell')     # prohibition by the farewell window
ref=['ref:deniers','ref:polytheists','ref:peopleOfBook','ref:christians']
G.add_edge('EarlyMecca','ref:deniers'); G.add_edge('ref:deniers','ref:polytheists')
G.add_edge('ref:polytheists','LateMecca'); G.add_edge('Hijra','ref:peopleOfBook')
G.add_edge('ref:peopleOfBook','ref:christians'); G.add_edge('ref:christians','Conquest/Nasr')
G.add_edge('Hijra','ref:hypocrites')
G.add_edge('MidMecca','promise:aD-93:5'); G.add_edge('promise:aD-93:5','fulfil:aK-108:1'); G.add_edge('fulfil:aK-108:1','LateMecca')
print("nodes=%d edges=%d  is_DAG=%s"%(G.number_of_nodes(),G.number_of_edges(),nx.is_directed_acyclic_graph(G)))
layers=list(nx.topological_generations(G))
print("\nTIME STRATA (same layer = temporally PARALLEL / contemporaneous):")
for i,l in enumerate(layers): print(f"  L{i}: {sorted(l)}")
tc=nx.transitive_closure(G); nodes=list(G.nodes()); inc=tot=0
for a,b in itertools.combinations(nodes,2):
    tot+=1
    if not(tc.has_edge(a,b) or tc.has_edge(b,a)): inc+=1
print(f"\nINCOMPARABLE (parallel) pairs: {inc}/{tot} = {inc/tot:.0%}  -> structure is a PARTIAL order, not a line")
print("CONTEMPORANEITY classes (same AH window): {Badr,Qibla}@2 · {Hudaybiyya,HajjRuling}@6 · {Tabuk,MasjidDirar}@9 (+Najran ~9.5)")
print("longest strict chain ('spine') = %d of %d nodes"%(nx.dag_longest_path_length(G)+1,G.number_of_nodes()))
print("parallel developmental THREADS through the windows: event-backbone · khamr ruling · referent-emergence · promise→fulfilment")
