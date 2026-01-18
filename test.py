# import torch

# print("Torch version:", torch.__version__)
# print("CUDA available:", torch.cuda.is_available())

# if torch.cuda.is_available():
#     print("GPU name:", torch.cuda.get_device_name(0))
# else:
#     print("⚠️ Running on CPU")
# import os
# import argparse
# # from src.utils import config_reader 

# def arg_parse():
#     parser = argparse.ArgumentParser(description="Basketball Video Analysis")
#     parser.add_argument(
#         "--config",
#         type=str,
#         default="configs\\configs.yaml",
#         help="Path to the configuration file",
#     )
#     args = parser.parse_args()
#     return args
# def main():
#     argparse = arg_parse()
#     print("Loading config from:", argparse.config)
#     exit()
#     config_path = "configs\\configs.yaml" 
#     config = config_reader.load_config(config_path)
#     print(config["models_dir"]["player_detector"])
#     exit()

# if __name__ == "__main__":
#     main()      