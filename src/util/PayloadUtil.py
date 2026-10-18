class PayloadUtil:
    @staticmethod
    def command_payload(
            message_key: str,
            *,
            victim=None,
            targets=None,
            token_factory=None,
            channel: str = "",
            tokens: dict | None = None,
            **extra,
    ) -> dict:
        payload = {"message_key": str(message_key or "")}
        if channel:
            payload["channel"] = channel
        if victim is not None:
            payload["victim"] = victim
        if targets is not None:
            payload["targets"] = list(targets)
        if callable(token_factory):
            payload["token_factory"] = token_factory
        if tokens:
            payload["tokens"] = dict(tokens)
        payload.update(extra)
        return payload
