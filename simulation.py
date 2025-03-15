import random
import time

def generate_invoices(num_rounds=5):
    reminders = [
       {
         "name": "Loss Aversion",
         "principle": "loss aversion",
         "message": "Alert: Your account is at risk of service interruption if the invoice is not paid by tomorrow. Avoid extra fees by paying now."
       },
       {
         "name": "Reciprocity",
         "principle": "reciprocity",
         "message": "Thank you for your loyalty! As a token of our appreciation, settle your invoice today and receive a discount on your next service."
       },
       {
         "name": "Social Proof",
         "principle": "social proof",
         "message": "Notice: 80% of your peers have already paid their invoices. Join them to continue enjoying uninterrupted service."
       },
       {
         "name": "Combined: Loss Aversion & Social Proof",
         "principle": "loss aversion, social proof",
         "message": "Urgent: Most clients have already paid, and if you delay, you risk additional charges and service interruption."
       },
       {
         "name": "Combined: Reciprocity & Social Proof",
         "principle": "reciprocity, social proof",
         "message": "We value your business and many of your peers have paid promptly. Settle this invoice now and receive an exclusive discount on your next order."
       }
    ]
    invoices = []
    for i in range(num_rounds):
        reminder = random.choice(reminders)
        invoice = {
            "round": i + 1,
            "name": reminder["name"],
            "principle": reminder["principle"],
            "message": reminder["message"],
            "open_time": None,
            "response_time": None,
            "response": None,
            "relationship_rating": None,
        }
        invoices.append(invoice)
    return invoices
