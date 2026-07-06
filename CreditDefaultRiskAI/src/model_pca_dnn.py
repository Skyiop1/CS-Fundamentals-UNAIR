from .model_dnn import build_dnn_model


def build_pca_dnn_model(input_dim: int):
    return build_dnn_model(input_dim)
