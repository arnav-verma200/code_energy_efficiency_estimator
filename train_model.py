import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import os
import sys

class EnergyModelTrainer:
    def __init__(self, data_path="data/function_metrics.csv", model_type="random_forest"):
        self.data_path = data_path
        self.model_type = model_type
        self.model = None
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def load_data(self):
        """Load training data"""
        print(f"📂 Loading data from: {self.data_path}")
        
        if not os.path.exists(self.data_path):
            print(f"\n❌ Error: {self.data_path} not found!")
            print("   Run 'python collect_data.py' first to generate training data.\n")
            return False
        
        self.data = pd.read_csv(self.data_path)
        print(f"✅ Loaded {len(self.data)} samples\n")
        
        if len(self.data) < 10:
            print("⚠️  Warning: Very small dataset. Consider collecting more data.\n")
        
        # Display summary
        print("📊 Dataset Summary:")
        print("-" * 60)
        print(self.data.describe().round(2))
        print()
        
        return True
    
    def prepare_features(self):
        """Prepare features and split data"""
        print("🔧 Preparing features...")
        
        # Features: cpu_usage, memory_usage, exec_time
        # Target: energy_cost
        self.X = self.data[["cpu_usage", "memory_usage", "exec_time"]].values
        self.y = self.data["energy_cost"].values
        
        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        
        print(f"   Training samples: {len(self.X_train)}")
        print(f"   Testing samples:  {len(self.X_test)}\n")
    
    def train_model(self):
        """Train the selected model"""
        print(f"🤖 Training {self.model_type.replace('_', ' ').title()} model...")
        
        if self.model_type == "random_forest":
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == "gradient_boosting":
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
        elif self.model_type == "linear":
            self.model = LinearRegression()
        else:
            print(f"❌ Unknown model type: {self.model_type}")
            print("   Available: random_forest, gradient_boosting, linear")
            return False
        
        # Train
        self.model.fit(self.X_train, self.y_train)
        print("✅ Training complete!\n")
        
        return True
    
    def evaluate_model(self):
        """Evaluate model performance"""
        print("=" * 60)
        print("📈 MODEL EVALUATION")
        print("=" * 60)
        print()
        
        # Training predictions
        y_train_pred = self.model.predict(self.X_train)
        train_r2 = r2_score(self.y_train, y_train_pred)
        train_mae = mean_absolute_error(self.y_train, y_train_pred)
        
        # Testing predictions
        y_test_pred = self.model.predict(self.X_test)
        test_r2 = r2_score(self.y_test, y_test_pred)
        test_mae = mean_absolute_error(self.y_test, y_test_pred)
        test_rmse = np.sqrt(mean_squared_error(self.y_test, y_test_pred))
        
        print("Training Metrics:")
        print(f"   R² Score:            {train_r2:.4f}")
        print(f"   Mean Absolute Error: {train_mae:.4f}\n")
        
        print("Testing Metrics:")
        print(f"   R² Score:            {test_r2:.4f}")
        print(f"   Mean Absolute Error: {test_mae:.4f}")
        print(f"   Root Mean Sq Error:  {test_rmse:.4f}\n")
        
        # Cross-validation
        if len(self.X) >= 5:
            cv_scores = cross_val_score(self.model, self.X, self.y, cv=min(5, len(self.X)), scoring='r2')
            print(f"Cross-Validation (5-fold):")
            print(f"   Mean R² Score:       {cv_scores.mean():.4f}")
            print(f"   Std Deviation:       {cv_scores.std():.4f}\n")
        
        # Feature importance
        if hasattr(self.model, 'feature_importances_'):
            print("🎯 Feature Importance:")
            features = ["CPU Usage", "Memory Usage", "Execution Time"]
            importances = self.model.feature_importances_
            for feat, imp in sorted(zip(features, importances), key=lambda x: x[1], reverse=True):
                bar = "█" * int(imp * 50)
                print(f"   {feat:20s} {imp:.4f} {bar}")
            print()
        
        # Model quality assessment
        print("📊 Model Quality:")
        if test_r2 > 0.9:
            print("   ✅ EXCELLENT - Model is highly accurate")
        elif test_r2 > 0.8:
            print("   ✔️  GOOD - Model performs well")
        elif test_r2 > 0.6:
            print("   ⚠️  FAIR - Consider collecting more data")
        else:
            print("   🚨 POOR - More training data needed")
        print()
    
    def save_model(self, output_path="models/energy_model.pkl"):
        """Save trained model to disk"""
        # Create models directory
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save model
        joblib.dump(self.model, output_path)
        
        file_size = os.path.getsize(output_path) / 1024
        print(f"💾 Model saved successfully!")
        print(f"   Path: {output_path}")
        print(f"   Size: {file_size:.2f} KB\n")
    
    def run_full_pipeline(self):
        """Execute complete training pipeline"""
        print("=" * 70)
        print("🚀 ENERGY MODEL TRAINING PIPELINE")
        print("=" * 70)
        print()
        
        # Step 1: Load data
        if not self.load_data():
            return False
        
        # Step 2: Prepare features
        self.prepare_features()
        
        # Step 3: Train model
        if not self.train_model():
            return False
        
        # Step 4: Evaluate
        self.evaluate_model()
        
        # Step 5: Save
        self.save_model()
        
        # Success message
        print("=" * 70)
        print("✅ TRAINING COMPLETE!")
        print("=" * 70)
        print()
        print("You can now use the model with:")
        print("   python predict_energy.py <your_script.py>")
        print("   python predict_energy.py <your_script.py> --functions")
        print()
        
        return True

def main():
    """CLI entry point"""
    # Parse arguments
    model_type = "random_forest"
    if len(sys.argv) > 1:
        if sys.argv[1] in ["random_forest", "gradient_boosting", "linear"]:
            model_type = sys.argv[1]
        else:
            print("Usage: python train_model.py [model_type]")
            print("Model types: random_forest, gradient_boosting, linear")
            print("Default: random_forest")
            sys.exit(1)
    
    # Train model
    trainer = EnergyModelTrainer(model_type=model_type)
    success = trainer.run_full_pipeline()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()