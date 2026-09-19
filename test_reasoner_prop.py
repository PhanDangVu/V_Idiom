from owlready2 import *
onto = get_ontology("ontology_protege/v-idiomV5_final.rdf").load()
with onto:
    sync_reasoner(infer_property_values=True)
VN_cls = onto.search_one(iri="*Vietnamese_idiom")
for vi in VN_cls.instances()[:5]:
    print(vi.name, "Có nghĩa:", vi.Có_nghĩa)
