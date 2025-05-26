# vtubestudio.py
import websockets
import json
import asyncio

class VTubeStudio:
    def __init__(self):
        self.websocket = None
        self.auth_token = None
        self.plugin_name = "Iris Assistant"
        self.plugin_developer = "YourName"

    async def connect(self, uri="ws://localhost:8001"):
        self.websocket = await websockets.connect(uri)
        if not self.auth_token:
            await self._request_token()
        await self._authenticate()

    async def _request_token(self):
        request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "TokenRequest1",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": self.plugin_name,
                "pluginDeveloper": self.plugin_developer
            }
        }
        await self.websocket.send(json.dumps(request))
        response = json.loads(await self.websocket.recv())
        self.auth_token = response["data"]["authenticationToken"]

    async def _authenticate(self):
        request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "AuthRequest1",
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": self.plugin_name,
                "pluginDeveloper": self.plugin_developer,
                "authenticationToken": self.auth_token
            }
        }
        await self.websocket.send(json.dumps(request))
        await self.websocket.recv()

    async def trigger_hotkey(self, hotkey_id: str):
        request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "HotkeyTrigger1",
            "messageType": "HotkeyTriggerRequest",
            "data": {"hotkeyID": hotkey_id}
        }
        await self.websocket.send(json.dumps(request))
        await self.websocket.recv()

vts = VTubeStudio()