import requests as rq
import uuid
from typing import Dict

from .models import TransferSuiTransaction, TransferObjectTransaction, MoveCallTransaction


class RpcTxDataSerializer:
    def __init__(self, rpc_url: str, session_headers: Dict = None):
        self.rpc_url = rpc_url
        self.session = rq.Session()
        self.session.headers.update(session_headers or {})

    def send_request_to_rpc(self,
                            method: str,
                            params: list = None,
                            request_id: str = None):
        return self.session.post(self.rpc_url,
                                 json={
                                     "jsonrpc": "2.0",
                                     "method": method,
                                     "params": params or [],
                                     "id": request_id or str(uuid.uuid4()),
                                 }).json()

    def new_transfer(self, signer_addr: str, tx: TransferObjectTransaction):
        return self.send_request_to_rpc(method="sui_transferObject",
                                        params=[signer_addr, tx.object_id, tx.gas_payment, tx.gas_budget, tx.recipient])

    def new_transfer_sui(self, signer_addr: str, tx: TransferSuiTransaction):
        return self.send_request_to_rpc(method="sui_transferSui",
                                        params=[signer_addr, tx.sui_object_id, tx.gas_budget, tx.recipient, tx.amount])

    def new_move_call(self, signer_addr: str, tx: MoveCallTransaction):
        return self.send_request_to_rpc(
            method="sui_moveCall",
            params=[
                signer_addr,
                tx.package_object_id,
                tx.module,
                tx.function,
                tx.type_arguments,
                tx.arguments,
                tx.gas_payment,
                tx.gas_budget,
            ])
