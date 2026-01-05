# ISO 20022 Payment Fraud Dataset Generator

## 📌 Project Overview
This tool generates synthetic financial transaction data specifically designed for training Machine Learning models to detect payment fraud. 

Unlike generic datasets, this generator structures data according to the **ISO 20022** messaging standard (the global standard for payment interoperability). It simulates realistic user profiles and injects specific fraud typologies based on known financial crime patterns.

## 🚀 Features
* **ISO 20022 Compliance:** Columns map to standard fields (e.g., `Dbtr` for Sender, `Cdtr` for Receiver, `InstdAmt` for Amount).
* **7 Fraud Typologies:** Includes specific injection logic for:
    * Account Takeover (ATO)
    * Wire Fraud
    * Credit/Debit Card Fraud
    * ACH Fraud
    * Check Fraud
    * Chargeback Fraud
* **Contextual Metadata:** Includes IP addresses and Device IDs (`InitgPty`) to enable behavioral analysis.

## 🛠️ Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/iso20022-fraud-generator.git](https://github.com/YOUR_USERNAME/iso20022-fraud-generator.git)
    cd iso20022-fraud-generator
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```


## 🧠 Fraud Logic
The generator does not just randomise numbers; it creates specific patterns:

ATO: A known user suddenly logs in from a new IP/Device and drains high amounts via Wire.

Wire Fraud: High amounts rounded to hundreds (e.g., 50000.00) sent to high-risk jurisdictions.

Card Fraud: High velocity of small transactions or single large transactions from inconsistent locations.

ISO Field,Description,ML Relevance

EndToEndId,Unique Transaction ID,Key

CreDtTm,Creation Date Time,"Velocity checks, Time-of-day analysis"

Dbtr,Debtor (Sender) Name,User profiling

DbtrAcct,Debtor Account (IBAN),History tracking

Cdtr,Creditor (Receiver),Beneficiary analysis

InstdAmt,Instructed Amount,Outlier detection

InitgPty_IP,Initiating Party IP,Location consistency

InitgPty_DeviceId,Initiating Party Device,Device fingerprinting

Label_IsFraud,Target Variable (0/1),Target for Classification

## 💻 Usage

Run the script to generate a CSV file:

```bash
python iso20022_fraud_gen.py



