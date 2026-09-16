from owlready2 import *

onto = get_ontology("v-idiomV2.rdf").load()

print(list(onto.classes()))
print(list(onto.properties()))
