# Simula Publications
A python module for programmatically accessing Simula research publications.

```
from simula_publications import Simula
s = Simula()
filter = {
    'status':'accepted,published',
    'owner':'simula',
    'type':'journal_article',
    'year':'2023'
}
for i,pub in enumerate(s.publications(filter)):
    print(i, pub)
```