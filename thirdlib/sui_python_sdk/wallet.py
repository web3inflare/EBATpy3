import base64
import bip_utils
import hashlib
import nacl


class SignatureScheme:
    ED25519 = 'ED25519'
    Secp256k1 = 'Secp256k1'


class SuiWallet:
    def __init__(self, mnemonic: str, derivation_path="m/44'/784'/0'/0'/0'"):
        self.mnemonic = mnemonic
        self.derivation_path = derivation_path

        self.bip39_seed = bip_utils.Bip39SeedGenerator(self.mnemonic).Generate()  # or = bip39.phrase_to_seed(mnemonic)
        self.bip32_ctx = bip_utils.Bip32Slip10Ed25519.FromSeed(self.bip39_seed)
        self.bip32_der_ctx = self.bip32_ctx.DerivePath(derivation_path)

        self.private_key: bytes = self.bip32_der_ctx.PrivateKey().Raw().ToBytes()
        self.public_key: bytes = self.bip32_der_ctx.PublicKey().RawCompressed().ToBytes()
        self.full_private_key = self.private_key[:32] + self.public_key[1:]

    @staticmethod
    def create_random_wallet():
        return SuiWallet(
            mnemonic=bip_utils.Bip39MnemonicGenerator().FromWordsNumber(bip_utils.Bip39WordsNum.WORDS_NUM_24).ToStr())

    def get_address(self) -> str:
        return "0x" + hashlib.sha3_256(self.bip32_der_ctx.PublicKey().RawCompressed().ToBytes()).digest().hex()[:40]

    def sign_data(self, data: bytes) -> bytes:
        return nacl.signing.SigningKey(self.private_key).sign(data)[:64]  # Todo: support secp256k1 key and signature

    def get_public_key_as_b64_string(self) -> str:
        return base64.b64encode(self.public_key[1:]).decode()
