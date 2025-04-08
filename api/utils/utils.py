def create_batch_request(method: str, params: dict | None = None) -> str:
    """Создаент батч-запрос из переданных параметров"""
    if params is None:
        params = {}
    batch = f"{method}?"
    for cmd, cmd_params in params.items():
        cmd = f"&{cmd}"
        if isinstance(cmd_params, dict):
            for key, value in cmd_params.items():
                batch += f'{cmd}[{key}]={value}'
        if isinstance(cmd_params, list | tuple):
            for index, item in enumerate(cmd_params):
                batch += f'{cmd}[{index}]={item}'
    return batch