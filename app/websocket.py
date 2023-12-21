from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # Mantém um dicionário de conexões ativas, onde as chaves são IDs de usuários e os valores são objetos WebSocket.
        self.active_connections: Dict[str, WebSocket] = {}
        
        # Mantém um dicionário de salas de tópicos, onde as chaves são IDs de tópicos e os valores são listas de IDs de usuários.
        self.topic_rooms: Dict[int, List[str]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        # Aceita a conexão WebSocket quando um cliente se conecta e associa o WebSocket ao ID do usuário.
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        # Desconecta um usuário, removendo sua conexão ativa e retirando-o de todas as salas de tópicos.
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            for room in self.topic_rooms.values():
                if user_id in room:
                    room.remove(user_id)

    async def send_private_message(self, message: str, receiver_id: str):
        # Envia uma mensagem privada para um usuário específico, se o usuário estiver conectado.
        receiver = self.active_connections.get(receiver_id)
        if receiver:
            await receiver.send_text(message)

    async def join_topic(self, user_id: str, topic_id: int):
        # Permite que um usuário se junte a uma sala de tópicos, criando a sala se ela não existir.
        if topic_id not in self.topic_rooms:
            self.topic_rooms[topic_id] = []
        self.topic_rooms[topic_id].append(user_id)

    async def send_topic_message(self, message: str, topic_id: int):
        # Envia uma mensagem para todos os usuários em uma sala de tópicos específica.
        if topic_id in self.topic_rooms:
            for user_id in self.topic_rooms[topic_id]:
                user_socket = self.active_connections.get(user_id)
                if user_socket:
                    await user_socket.send_text(message)
