# HD Wallet Generator

This project implements a Hierarchical Deterministic (HD) wallet generator based on BIP-32 and BIP-44 standards. The wallet allows you to generate a seed phrase, derive private/public keys, and generate Bitcoin or Ethereum addresses from the public key. It also provides QR code generation for each address and the ability to save wallet information to a JSON file for backup. The project uses Streamlit for the UI and several cryptographic libraries for wallet generation and key derivation.

## Features

- **Generate Seed Phrase (BIP-39)**: Securely generate a 12-word mnemonic seed phrase.
- **Generate Master Key (BIP-32)**: Derive master private and public keys from the seed phrase.
- **Derive Child Keys (BIP-32 Path)**: Derive child private and public keys using a specific BIP-32 path.
- **Generate Bitcoin Address**: Convert public key to a Bitcoin address (Base58Check encoding).
- **Generate Ethereum Address**: Convert public key to an Ethereum address.
- **Generate QR Codes**: Automatically generate QR codes for Bitcoin and Ethereum addresses.
- **Save Wallet Info to JSON**: Save all wallet information, including private keys, public keys, addresses, and seed phrase, to a JSON file.
- **Copy Address to Clipboard**: Copy the generated Bitcoin or Ethereum address to the clipboard.

## Prerequisites

Before running this project, make sure you have the following installed on your system:

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/hdwallet.git
   cd hdwallet
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   The required dependencies are:
   - **Streamlit**: For the web interface.
   - **Mnemonic**: For generating the BIP-39 seed phrase.
   - **bip32utils**: For BIP-32 key derivation.
   - **hashlib**: For cryptographic hashing operations.
   - **base58**: For Base58 encoding (Bitcoin address generation).
   - **ecdsa**: For elliptic curve cryptography operations.
   - **qrcode**: For generating QR codes.
   - **pyperclip**: For clipboard operations.

## Running the Application

To run the application, use the following command:

```bash
streamlit run app.py
```

Once the app is running, open a browser and navigate to `http://localhost:8501` to interact with the wallet generator.

## Usage

1. **Generate Seed Phrase**: Click on the "Generate Seed Phrase" button to generate a new 12-word seed phrase (BIP-39).
   
2. **Convert Seed Phrase to Seed**: After generating the seed phrase, the corresponding seed (in hexadecimal format) is automatically displayed.

3. **Generate Master Key**: After obtaining the seed, the app will generate the master private and public keys.

4. **Derive Child Key**: You can enter a BIP-32 path (e.g., `44'/0'/0'/0/0`) to derive child keys (both private and public). 

5. **Generate Bitcoin Address**: Once the child public key is derived, you can generate a Bitcoin address in Base58Check encoding. You can also generate a QR code for this address.

6. **Generate Ethereum Address**: Similarly, you can generate an Ethereum address from the child public key.

7. **Save Wallet Info**: You can save the generated wallet information (seed phrase, master keys, child keys, addresses) to a JSON file for backup.

8. **Copy to Clipboard**: You can copy the generated Bitcoin or Ethereum address to your clipboard by clicking the corresponding button.

## Example Workflow

1. Click on the "Generate Seed Phrase" button to generate a seed phrase.
2. Convert the seed phrase to a seed using the `Seed from Seed Phrase` section.
3. Generate the master private and public keys.
4. Enter a BIP-32 path (e.g., `44'/0'/0'/0/0`) to derive child private and public keys.
5. Generate Bitcoin and Ethereum addresses.
6. Save the wallet information to a JSON file for backup.
7. Use the QR codes for easy scanning of the addresses.

## Screenshots

### Main Interface
![Main Interface Screenshot](screenshots/main_interface.png)

### QR Code for Bitcoin Address
![Bitcoin QR Code Screenshot](screenshots/bitcoin_qr_code.png)

## Security Notice

- **Seed Phrase**: The seed phrase is crucial for recovering your wallet. Store it securely and never share it with anyone.
- **Private Keys**: The private keys generated are highly sensitive. If someone gains access to them, they will have control over your wallet.
- **Backup**: Always keep a backup of your seed phrase and wallet information in a secure location.

## Contributing

We welcome contributions to the project. If you'd like to contribute, follow these steps:

1. Fork the repository.
2. Clone your forked repository.
3. Make your changes.
4. Push your changes to your forked repository.
5. Create a pull request with a description of the changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The code uses libraries like **Mnemonic**, **bip32utils**, **hashlib**, and **base58** for wallet generation and cryptographic operations.
- QR Code generation is handled by the **qrcode** library.
- **Streamlit** is used to provide a user-friendly web interface for interacting with the wallet.
