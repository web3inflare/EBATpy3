import requests as rq
import uuid
import base64
from typing import Dict, Optional, Union

from .wallet import SignatureScheme


class ExecuteTransactionRequestType:
    ImmediateReturn = "ImmediateReturn"
    WaitForTxCert = "WaitForTxCert"
    WaitForEffectsCert = "WaitForEffectsCert"
    WaitForLocalExecution = "WaitForLocalExecution"


class SuiJsonRpcProvider:

    def __init__(self,
                 rpc_url: str,
                 faucet_url: str = None,
                 session_headers: Dict = None):
        self.session = rq.Session()
        self.session.headers.update(session_headers or {})

        self.rpc_url = rpc_url
        self.faucet_url = faucet_url

    def request_tokens_from_faucet(self, addr: str):
        return self.session.post(self.faucet_url, json={"FixedAmountRequest": {"recipient": addr}}).json()

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

    def batch_send_request_to_rpc(self,
                                  methods: list,
                                  params: list = None,
                                  request_ids: list = None):
        return self.session.post(self.rpc_url,
                                 json=[{
                                     "jsonrpc": "2.0",
                                     "method": methods[i],
                                     "params": params[i] if (
                                             isinstance(params, list) and params[i] is not None) else [],
                                     "id": request_ids[i] if isinstance(request_ids, list) else str(uuid.uuid4()),
                                 } for i in range(len(methods))
                                 ]
                                 ).json()

    def get_rpc_version(self):
        return self.send_request_to_rpc(method="rpc.discover")

    def get_objects_owned_by_address(self, addr: str):
        return self.send_request_to_rpc(method="sui_getObjectsOwnedByAddress", params=[addr])

    def get_objects_owned_by_object(self, object_id: str):
        return self.send_request_to_rpc(method="sui_getObjectsOwnedByObject", params=[object_id])

    def get_object(self, object_id: str):
        return self.send_request_to_rpc(method="sui_getObject", params=[object_id])

    def get_move_function_arg_types(self, package_id: str, module_name: str, function_name: str):
        return self.send_request_to_rpc(method="sui_getMoveFunctionArgTypes",
                                        params=[package_id, module_name, function_name])

    def get_transactions(self,
                         query: Union[Dict, str] = None,
                         cursor: Optional[Union[Dict, str]] = None,
                         limit: Optional[int] = None,
                         order: str = "Descending"):
        return self.send_request_to_rpc(method="sui_getTransactions", params=[query, cursor, limit, order])

    def get_transaction_with_effects(self, digest: str):
        return self.send_request_to_rpc(method="sui_getTransaction", params=[digest])

    def get_events_by_transaction(self, digest: str, limit: int = 100):
        return self.send_request_to_rpc(method="sui_getEventsByTransaction", params=[digest, limit])

    def get_events_by_module(self, package: str, module: str, limit: int = 100, start_time: int = 0,
                             end_time: int = 2 ** 53 - 1):
        return self.send_request_to_rpc(method="sui_getEventsByModule",
                                        params=[package, module, limit, start_time, end_time])

    def get_events_by_object(self, object_id: str, limit: int = 100, start_time: int = 0, end_time: int = 2 ** 53 - 1):
        return self.send_request_to_rpc(method="sui_getEventsByObject", params=[object_id, limit, start_time, end_time])

    def execute_transaction(self,
                            tx_bytes_b64_encoded: str,
                            signature_b64_encoded: str,
                            pubkey_b64_encoded: str,
                            signature_scheme: SignatureScheme = SignatureScheme.ED25519,
                            executeType: ExecuteTransactionRequestType = ExecuteTransactionRequestType.WaitForEffectsCert):
        # this function actually broadcasts the transaction
        if isinstance(tx_bytes_b64_encoded, bytes):
            tx_bytes_b64_encoded = base64.b64encode(tx_bytes_b64_encoded).decode()
        if isinstance(signature_b64_encoded, bytes):
            signature_b64_encoded = base64.b64encode(signature_b64_encoded).decode()

        signature_scheme_to_flag = {
            SignatureScheme.ED25519: 0x00,
            SignatureScheme.Secp256k1: 0x01,
        }
        signature_scheme_flag = signature_scheme_to_flag[signature_scheme]

        serialized_sig = [signature_scheme_flag] + \
                         list(base64.b64decode(signature_b64_encoded)) + \
                         list(base64.b64decode(pubkey_b64_encoded))

        return self.send_request_to_rpc(method="sui_executeTransactionSerializedSig",
                                        params=[
                                            tx_bytes_b64_encoded,
                                            base64.b64encode(bytes(serialized_sig)).decode(),
                                            executeType])

    def get_total_transaction_number(self):
        return self.send_request_to_rpc(method="sui_getTotalTransactionNumber")

    def get_total_transaction_in_range(self, start_of_range: int, end_of_range: int):
        return self.send_request_to_rpc(method="sui_getTransactionsInRange", params=[start_of_range, end_of_range])
