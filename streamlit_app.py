import streamlit as st
from mnemonic import Mnemonic
import bip32utils
import hashlib
import base58
import ecdsa
import json
import qrcode
from binascii import hexlify
import os
import pyperclip
from typing import Tuple


# Enhanced wallet generation and security functions
class HDWallet:
    def __init__(self, strength: int = 128):
        self.mnemo = Mnemonic("english")
        self.strength = strength
        self.seed_phrase = None
        self.seed = None
        self.master_private_key = None
        self.master_public_key = None
        self.child_private_key = None
        self.child_public_key = None
        self.bitcoin_address = None
        self.ethereum_address = None

    def generate_seed_phrase(self) -> str:
        """Generate the seed phrase (BIP-39)"""
        self.seed_phrase = self.mnemo.generate(strength=self.strength)
        self.seed = self.mnemo.to_seed(self.seed_phrase, passphrase="")
        return self.seed_phrase

    def generate_master_key(self):
        """Generate the master key (Private and Public) (BIP-32)"""
        bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(self.seed)
        self.master_private_key = bip32_root_key_obj.PrivateKey()
        self.master_public_key = bip32_root_key_obj.PublicKey()
        return self.master_private_key, self.master_public_key

    def derive_child_key(self, path: str) -> Tuple[bytes, bytes]:
        """Derive child key using a given BIP-32 path"""
        path_elements = path.split('/')
        bip32_key = bip32utils.BIP32Key.fromEntropy(self.master_private_key)
        for elem in path_elements:
            if "'" in elem:
                index = int(elem[:-1]) + bip32utils.BIP32_HARDEN
            else:
                index = int(elem)
            bip32_key = bip32_key.ChildKey(index)
        self.child_private_key = bip32_key.PrivateKey()
        self.child_public_key = bip32_key.PublicKey()
        return self.child_private_key, self.child_public_key

    def public_key_to_bitcoin_address(self) -> str:
        """Convert the public key to a Bitcoin address (Base58Check)"""
        sha256_public_key = hashlib.sha256(self.child_public_key).digest()
        ripemd160_public_key = hashlib.new('ripemd160', sha256_public_key).digest()
        versioned_payload = b'\x00' + ripemd160_public_key
        checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
        address = versioned_payload + checksum
        self.bitcoin_address = base58.b58encode(address).decode()
        return self.bitcoin_address

    def public_key_to_ethereum_address(self) -> str:
        """Convert the public key to an Ethereum address"""
        keccak_hash = hashlib.new('sha3_256', self.child_public_key).digest()
        self.ethereum_address = '0x' + hex(keccak_hash[12:])[-40:]
        return self.ethereum_address

    def generate_qr_code(self, address: str) -> str:
        """Generate QR code for the address"""
        img = qrcode.make(address)
        qr_path = "/tmp/qr_code.png"
        img.save(qr_path)
        return qr_path

    def save_wallet_info_to_json(self) -> str:
        """Save wallet information to a JSON file"""
        wallet_data = {
            'seed_phrase': self.seed_phrase,
            'master_private_key': hexlify(self.master_private_key).decode(),
            'master_public_key': hexlify(self.master_public_key).decode(),
            'child_private_key': hexlify(self.child_private_key).decode(),
            'child_public_key': hexlify(self.child_public_key).decode(),
            'bitcoin_address': self.bitcoin_address,
            'ethereum_address': self.ethereum_address
        }
        file_path = '/tmp/hd_wallet.json'
        with open(file_path, 'w') as json_file:
            json.dump(wallet_data, json_file)
        return file_path


# Streamlit UI for wallet generation and management
def main():
    st.title("Advanced HD Wallet Generator")

    # Wallet instance
    wallet = HDWallet()

    st.sidebar.header("Wallet Options")
    st.sidebar.text("Select your preferences")

    # Generate Seed Phrase
    if st.sidebar.button('Generate Seed Phrase'):
        seed_phrase = wallet.generate_seed_phrase()
        st.session_state.seed_phrase = seed_phrase
        st.session_state.seed = wallet.seed
        st.subheader("Generated Seed Phrase:")
        st.text(seed_phrase)

    # Display Seed from Seed Phrase (Hexadecimal)
    if 'seed_phrase' in st.session_state:
        seed_phrase = st.session_state.seed_phrase
        seed = st.session_state.seed
        st.subheader("Seed from Seed Phrase:")
        st.text(hexlify(seed).decode())

    # Generate Master Keys
    if 'seed' in st.session_state:
        master_private_key, master_public_key = wallet.generate_master_key()
        st.subheader("Master Private Key:")
        st.text(hexlify(master_private_key).decode())
        st.subheader("Master Public Key:")
        st.text(hexlify(master_public_key).decode())

    # Derive Child Key
    if 'master_private_key' in st.session_state:
        path = st.sidebar.text_input('BIP-32 Path', "44'/0'/0'/0/0")
        if st.sidebar.button('Generate Child Keys'):
            child_private_key, child_public_key = wallet.derive_child_key(path)
            st.subheader("Derived Private Key:")
            st.text(hexlify(child_private_key).decode())
            st.subheader("Derived Public Key:")
            st.text(hexlify(child_public_key).decode())

    # Generate Bitcoin Address
    if 'child_public_key' in st.session_state:
        bitcoin_address = wallet.public_key_to_bitcoin_address()
        st.subheader("Generated Bitcoin Address:")
        st.text(bitcoin_address)

        # Generate Bitcoin QR Code
        qr_path = wallet.generate_qr_code(bitcoin_address)
        st.image(qr_path, caption="Bitcoin Address QR Code")

    # Generate Ethereum Address
    if 'child_public_key' in st.session_state:
        ethereum_address = wallet.public_key_to_ethereum_address()
        st.subheader("Generated Ethereum Address:")
        st.text(ethereum_address)

        # Generate Ethereum QR Code
        qr_path = wallet.generate_qr_code(ethereum_address)
        st.image(qr_path, caption="Ethereum Address QR Code")

    # Save Wallet Information to JSON
    if 'child_public_key' in st.session_state:
        if st.sidebar.button('Save Wallet Info to JSON'):
            json_file_path = wallet.save_wallet_info_to_json()
            st.subheader(f"Wallet Info saved to {json_file_path}")

    # Copy Address to Clipboard
    if 'bitcoin_address' in st.session_state:
        if st.sidebar.button('Copy Bitcoin Address to Clipboard'):
            pyperclip.copy(bitcoin_address)
            st.success("Bitcoin address copied to clipboard.")

    # Footer Section
    st.sidebar.markdown("""
        #### How does this work?
        - This app generates HD wallets using BIP-32 and BIP-44 standards.
        - You can generate a seed phrase, derive private/public keys, and generate Bitcoin or Ethereum addresses from the public key.
        - Wallet information can be saved to a JSON file for backup.
        - QR codes are generated for each address for easy use.
    """)


if __name__ == '__main__':
    main()
