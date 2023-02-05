import base64

from .provider import SuiJsonRpcProvider
from .rpc_tx_data_serializer import RpcTxDataSerializer
from .wallet import SuiWallet
from .models import MoveCallTransaction
from typing import Optional, List


class SignerWithProvider:

    def __init__(self,
                 provider: SuiJsonRpcProvider,
                 serializer: RpcTxDataSerializer,
                 signer_wallet: SuiWallet,
                 ):
        self.provider = provider
        self.serializer = serializer
        self.signer_wallet = signer_wallet

        self._rpc_minor_version: Optional[int] = None
        self._rpc_major_version: Optional[int] = None
        self._INTENT_BYTES: List[int] = [0, 0, 0]

    def get_address(self):
        return self.signer_wallet.get_address()

    def sign_data(self, data: bytes):
        return self.signer_wallet.sign_data(data)

    def request_sui_from_faucet(self):
        return self.provider.request_tokens_from_faucet(self.get_address())

    def sign_and_execute_transaction(self, tx_bytes: bytes):
        data_to_sign = tx_bytes
        is_rpc_version_valid = isinstance(self._rpc_major_version, int) and isinstance(self._rpc_minor_version, int)
        try:
            if is_rpc_version_valid is False:
                # try to fetch rpc version
                self._fetch_and_update_rpc_version()
        except:
            pass
        is_rpc_version_valid = isinstance(self._rpc_major_version, int) and isinstance(self._rpc_minor_version, int)
        if (is_rpc_version_valid is False) or (self._rpc_major_version == 0 and self._rpc_minor_version >= 19):
            data_to_sign = bytes(self._INTENT_BYTES + list(map(int, data_to_sign)))

        signature_bytes = self.sign_data(data_to_sign)
        return self.provider.execute_transaction(
            tx_bytes_b64_encoded=base64.b64encode(tx_bytes).decode(),
            signature_b64_encoded=base64.b64encode(signature_bytes).decode(),
            pubkey_b64_encoded=self.signer_wallet.get_public_key_as_b64_string(),
        )

    def execute_move_call(self, tx_move_call: MoveCallTransaction):
        tx_bytes_b64 = self.serializer.new_move_call(
            signer_addr=self.signer_wallet.get_address(),
            tx=tx_move_call)["result"]["txBytes"]
        return self.sign_and_execute_transaction(tx_bytes=base64.b64decode(tx_bytes_b64))

    def _fetch_and_update_rpc_version(self):
        rpc_version_res = self.provider.get_rpc_version()
        version_str = rpc_version_res["result"]["info"]["version"]
        if isinstance(version_str, str) and len(version_str.split(".")) == 3:
            version_split = version_str.split(".")
            self._rpc_major_version = int(version_split[0])
            self._rpc_minor_version = int(version_split[1])
