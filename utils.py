import configparser


def get_config(config_path, config_type):
    all_config = configparser.ConfigParser()
    all_config.read(config_path)
    cfg = all_config[config_type]
    config_dict = {}
    for k, v in cfg.items():
        if k == "api_key":
            with open(v) as f:
                api_key = f.read()
                v = api_key
        config_dict[k] = v
    return config_dict
