from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.topic_rooms: Dict[int, List[str]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            for room in self.topic_rooms.values():
                if user_id in room:
                    room.remove(user_id)

    async def send_private_message(self, message: str, receiver_id: str):
        receiver = self.active_connections.get(receiver_id)
        if receiver:
            await receiver.send_text(message)

    async def join_topic(self, user_id: str, topic_id: int):
        if topic_id not in self.topic_rooms:
            self.topic_rooms[topic_id] = []
        self.topic_rooms[topic_id].append(user_id)

    async def send_topic_message(self, message: str, topic_id: int):
        if topic_id in self.topic_rooms:
            for user_id in self.topic_rooms[topic_id]:
                user_socket = self.active_connections.get(user_id)
                if user_socket:
                    await user_socket.send_text(message)
