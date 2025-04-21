import ModelSelector as model
import pandas as pd
import PredictionTarget as prediction
# For the best performing model in this case for apple Ridge Regression performed the best
best_model = model.results["Ridge Regression"]["model"]

# Get feature importance
if hasattr(best_model, "feature_importances_"):
    feature_importance = pd.DataFrame({
        'Feature': prediction.X.columns,
        'Importance': best_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance.head(10))