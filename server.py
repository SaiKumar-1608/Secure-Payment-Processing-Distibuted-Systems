import socket
import threading

class PaymentServer:
    def __init__(self, host='localhost', port=5000):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)

        self.clients = {}
        self.balances = {}
        self.vector_clock = {}
        self.leader = None
        self.client_order = []

    def display_vector_clock(self):
        print(f"[SERVER] Current Vector Clock: {self.vector_clock}")

    def handle_client(self, client_socket, client_id):
        while True:
            try:
                msg = client_socket.recv(1024).decode()
                if msg.startswith("TRANSACTION"):
                    sender, receiver, amount, timestamp = msg.split("|")[1:]
                    amount = int(amount)
                    self.vector_clock[sender] += 1

                    if self.balances[sender] >= amount:
                        print(f"[SERVER] Transaction Request: {sender} -> {receiver} | ${amount}")
                        self.clients[receiver].send(msg.encode())  # Send to receiver
                    else:
                        self.clients[sender].send("TRANSACTION_FAILED|Insufficient Funds".encode())
                    
                    self.display_vector_clock()
                
                elif msg.startswith("VOTE_COMMIT"):
                    sender = "Client1" if client_id == "Client2" else "Client2"
                    receiver = client_id
                    amount = int(msg.split("|")[1])

                    # Update balances
                    self.balances[sender] -= amount
                    self.balances[receiver] += amount
                    self.vector_clock[receiver] += 1
                    
                    print(f"[SERVER] Transaction SUCCESS: {sender} -> {receiver} | ${amount}")
                    print(f"[SERVER] Updated Balances -> {sender}: ${self.balances[sender]}, {receiver}: ${self.balances[receiver]}")
                    
                    self.clients[sender].send(f"TRANSACTION_SUCCESS|{self.balances[sender]}".encode())
                    self.clients[receiver].send(f"TRANSACTION_SUCCESS|{self.balances[receiver]}".encode())
                    
                    self.display_vector_clock()
                
                elif msg.startswith("VOTE_ABORT"):
                    sender = "Client1" if client_id == "Client2" else "Client2"
                    print(f"[SERVER] Transaction FAILED: {sender} -> {client_id}")
                    self.clients[sender].send("TRANSACTION_FAILED|Verification Failed".encode())
                    
                    self.display_vector_clock()
            except:
                break

    def start(self):
        print("[SERVER] Waiting for clients...")
        
        for i in range(2):
            client_socket, _ = self.server.accept()
            client_id = f"Client{i+1}"
            self.clients[client_id] = client_socket
            self.client_order.append(client_id)
            self.balances[client_id] = 20000 if client_id == "Client1" else 23183
            self.vector_clock[client_id] = 0
            print(f"[SERVER] {client_id} Connected.")
        
        # Assign leader based on who connected first
        self.leader = self.client_order[0]
        print(f"[SERVER] Leader Elected: {self.leader}")

        for client_id in self.clients:
            threading.Thread(target=self.handle_client, args=(self.clients[client_id], client_id)).start()

if __name__ == "__main__":
    PaymentServer().start()
