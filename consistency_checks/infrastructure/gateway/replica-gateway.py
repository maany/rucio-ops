from typing import List
from rucio.core import replica
from rucio.common.types import InternalScope, InternalAccount

from consistency_checks.core.entity import Replica
import logging

class RucioReplicaGateway:
    def __init__(self, account: str):
        self.account = InternalAccount(account)

    def declare_bad_replica(self, replica: Replica, ticket_numer: str) -> str:
        scope = InternalScope(replica.scope)
        name = replica.name
        rse_id = replica.rse_id
        replica = {
            'scope': scope,
            'name': name,
            'rse_id': rse_id
        }
        replica.declare_bad_file_replicas(replicas=[replica], issuer=self.account, reason=f"Lost ({ticket_numer})")
        output =  replica.declare_bad_file()
    

    def declare_bad_replicas(self, replicas: List[Replica], ticket_numer: str):
        for replica in replicas:
            self.declare_bad_replica(replica, ticket_numer)