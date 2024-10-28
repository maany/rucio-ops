from rucio.common.types import InternalScope, InternalAccount
from rucio.core import replica

scope = InternalScope('mc15_14TeV')
name = 'HITS.10075481._000435.pool.root.1'
rse_id = 'd22a0465c92d448394b8caa7f06f38f9'

output = replica.declare_bad_file_replicas(replicas=[{'scope': scope, 'name': name, 'rse_id': rse_id}], issuer=InternalAccount('root'), reason="Lost (ATLADDMOPS-5717)")
print(output)