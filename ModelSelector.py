from sklearn.metrics import mean_squared_error

def evaluate_model(model, X_train, X_test, y_train, y_test):
    # Align X and y to ensure they have the same number of rows
    X_train, y_train = X_train.align(y_train, join='inner', axis=0)
    X_test, y_test = X_test.align(y_test, join='inner', axis=0)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    predictions = model.predict(X_test)
    
    # Calculate Mean Squared Error
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")
    
    return model, predictions
