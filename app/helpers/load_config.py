import yaml


def load_config(file_path):
    try:
        with open(file_path, "r") as f:
            config = yaml.full_load(f)
        return config
    except FileNotFoundError:
        print(f"Configuration file '{file_path}' not found. Exiting program.")
        exit()
    except yaml.YAMLError as e:
        print(f"Error parsing YAML configuration file '{file_path}': {e}")
        exit()
    except Exception as e:
        print(f"Unexpected error while loading configuration file '{file_path}': {e}")
        exit()
