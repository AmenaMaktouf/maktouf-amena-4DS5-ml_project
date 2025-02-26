import pytest
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import sys
import os

# Ajouter le répertoire parent au PATH pour que pytest trouve les modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importer les fonctions nécessaires depuis le module pipeline
from pipeline import (
    prepare_data,
    train_model,
)  # Assurez-vous d'importer depuis le bon module


@pytest.fixture
def prepared_data():
    """Fixture pour préparer les données une seule fois pour plusieurs tests."""
    features_pca, target, feature_scaler, pca_transformer = prepare_data()
    return features_pca, target, feature_scaler, pca_transformer


def test_prepare_data(prepared_data):
    """Test si la fonction prepare_data retourne bien les bons types de données."""
    features_pca, target, feature_scaler, pca_transformer = prepared_data

    assert isinstance(
        features_pca, np.ndarray
    ), "Les features PCA doivent être un numpy array"
    assert isinstance(target, pd.Series), "La target doit être une Series"
    assert feature_scaler is not None, "Le StandardScaler ne doit pas être None"
    assert pca_transformer is not None, "Le PCA ne doit pas être None"
    assert (
        features_pca.shape[0] == target.shape[0]
    ), "Les features et la target doivent avoir le même nombre d'échantillons"


def test_train_model(prepared_data):
    """Test si la fonction train_model entraîne un modèle DecisionTreeClassifier."""
    features_pca, target, _, _ = prepared_data

    # Diviser les données pour le test
    X_train, X_test, y_train, y_test = train_test_split(
        features_pca, target, test_size=0.2, random_state=42
    )

    model = train_model(X_train, y_train)

    assert model is not None, "Le modèle ne doit pas être None"
    assert isinstance(
        model, DecisionTreeClassifier
    ), "Le modèle doit être un DecisionTreeClassifier"
    assert hasattr(model, "predict"), "Le modèle doit avoir une méthode predict"
