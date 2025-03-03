import argparse
import mlflow
import mlflow.sklearn
from model_pipeline import prepare_data, train_model, save_model, evaluate_model
from sklearn.model_selection import train_test_split

def main():
    global X_train_resampled, X_test, y_train_resampled, y_test, feature_scaler, pca_transformer, model

    parser = argparse.ArgumentParser(description="ML Pipeline CLI")
    parser.add_argument("--prepare", action="store_true", help="Préparer les données")
    parser.add_argument("--train", action="store_true", help="Entraîner le modèle")
    parser.add_argument("--evaluate", action="store_true", help="Évaluer le modèle")
    parser.add_argument("--save", action="store_true", help="Sauvegarder le modèle et les artefacts")

    args = parser.parse_args()

    mlflow.set_experiment("MLflow Experiment")  # Définir l'expérience MLflow

    if args.prepare:
        print("Exécution de prepare_data()...")
        X_train_resampled, X_test, y_train_resampled, y_test, feature_scaler, pca_transformer = prepare_data()
        print("Données préparées avec succès !")

    if args.train:
        with mlflow.start_run():
            print("Exécution de train_model()...")
            if 'X_train_resampled' not in globals():
                print("Données non préparées. Préparation des données avant l'entraînement.")
                X_train_resampled, X_test, y_train_resampled, y_test, feature_scaler, pca_transformer = prepare_data()

            model = train_model(X_train_resampled, y_train_resampled)
            print("Modèle entraîné avec succès !")

            # Enregistrer les hyperparamètres du modèle
            mlflow.log_param("model_type", type(model).__name__)
            if hasattr(model, "criterion"):
                mlflow.log_param("criterion", model.criterion)
            if hasattr(model, "max_depth"):
                mlflow.log_param("max_depth", model.max_depth)
            if hasattr(model, "min_samples_leaf"):
                mlflow.log_param("min_samples_leaf", model.min_samples_leaf)

            # Exemple d'entrée pour la signature du modèle
            input_example = {
                "State": "CA",
                "Account length": 100,
                "Area code": "415",
                "International plan": "Yes",
                "Voice mail plan": "No",
                "Number vmail messages": 0,
                "Total day minutes": 150.0,
                "Total day calls": 200,
                "Total day charge": 25.5,
                "Total eve minutes": 120.0,
                "Total eve calls": 150,
                "Total eve charge": 15.0,
                "Total night minutes": 130.0,
                "Total night calls": 180,
                "Total night charge": 12.0,
                "Total intl minutes": 5.0,
                "Total intl calls": 5,
                "Total intl charge": 2.5,
                "Customer service calls": 1,
            }

            # Enregistrer le modèle avec MLflow
            mlflow.sklearn.log_model(model, "model", input_example=input_example)

            print("Modèle enregistré dans MLflow avec hyperparamètres et exemple d'entrée.")

            if args.save:
                print("Sauvegarde du modèle et des artefacts...")
                save_model(model, feature_scaler, pca_transformer)
                print("Modèle, scaler et PCA sauvegardés avec succès !")

    if args.evaluate:
        print("Évaluation du modèle...")
        if 'model' not in globals():
            print("Modèle non formé. Entraînement du modèle avant l'évaluation.")
            if 'X_train_resampled' not in globals():
                print("Données non préparées. Préparation des données avant l'entraînement.")
                X_train_resampled, X_test, y_train_resampled, y_test, feature_scaler, pca_transformer = prepare_data()
            model = train_model(X_train_resampled, y_train_resampled)

        # Évaluer le modèle et enregistrer les métriques
        metrics = evaluate_model(model, X_test, y_test)
        print("Évaluation terminée !")

        with mlflow.start_run():
            for key, value in metrics.items():
                mlflow.log_metric(key, value)  # Enregistrer chaque métrique
            print("Métriques enregistrées dans MLflow.")
mlflow.set_tracking_uri("sqlite:///mlflow.db")

if __name__ == "__main__":
    main()
