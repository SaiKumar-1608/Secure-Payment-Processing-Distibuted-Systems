import socket
import threading
import time

class Client1:
    def __init__(self, host='localhost', port=5000):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.balance = 20000  # Initial Balance

        self.vector_clock = {"Client1": 0, "Client2": 0}
        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        while True:
            try:
                msg = self.client.recv(1024).decode()
                if not msg:
                    print("[Client1] ❌ Server connection lost. Exiting...")
                    break
                
                parts = msg.split("|")
                msg_type = parts[0]

                if msg_type == "TRANSACTION":
                    if len(parts) == 5:
                        _, sender, receiver, amount, timestamp = parts
                        amount = int(amount)
                        self.vector_clock[sender] = max(self.vector_clock[sender], int(timestamp))
                        print(f"\n[Client1] 📩 Received transaction from {sender}: ${amount}")
                        print(f"[Client1] ⏳ Vector Clock: {self.vector_clock}")
                    
                        if self.balance >= amount:
                            print("[Client1] ✅ Voting COMMIT")
                            self.client.send(f"VOTE_COMMIT|{amount}".encode())
                        else:
                            print("[Client1] ❌ Voting ABORT (Insufficient Funds)")
                            self.client.send("VOTE_ABORT".encode())
                    else:
                        print("[Client1 ERROR] Invalid TRANSACTION format received.")

                elif msg_type == "TRANSACTION_SUCCESS":
                    if len(parts) == 2:
                        _, new_balance = parts
                        self.balance = int(new_balance)
                        self.vector_clock["Client1"] += 1
                        print(f"[Client1] ✅ Transaction SUCCESS. New Balance: ${self.balance}")
                        print(f"[Client1] ⏳ Updated Vector Clock: {self.vector_clock}")
                    else:
                        print("[Client1 ERROR] Invalid TRANSACTION_SUCCESS format received.")

                elif msg_type == "TRANSACTION_FAILED":
                    if len(parts) == 2:
                        print(f"[Client1] ❌ Transaction FAILED: {parts[1]}")
                    else:
                        print("[Client1 ERROR] Invalid TRANSACTION_FAILED format received.")

            except Exception as e:
                print(f"[Client1 ERROR] {e}")
                break

    def send_transaction(self, receiver, amount):
        if self.balance >= amount:
            self.vector_clock["Client1"] += 1
            transaction_msg = f"TRANSACTION|Client1|{receiver}|{amount}|{self.vector_clock['Client1']}"
            self.client.send(transaction_msg.encode())
            print(f"\n[Client1] 📤 Sent ${amount} to {receiver}")
            print(f"[Client1] ⏳ Updated Vector Clock: {self.vector_clock}")
        else:
            print("[Client1] ❌ Not enough balance!")

if __name__ == "__main__":
    client = Client1()
    while True:
        try:
            amount = input("Enter amount to send (or type 'exit' to quit): ")
            if amount.lower() == "exit":
                break
            client.send_transaction("Client2", int(amount))
            time.sleep(1)
        except ValueError:
            print("[Client1] ❌ Invalid amount. Please enter a number.")
