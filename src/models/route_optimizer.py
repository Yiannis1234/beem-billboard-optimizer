import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import joblib
import uuid

class BeemRouteOptimizer:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.feature_columns = [
            'temperature', 'precipitation', 'wind_speed',
            'pedestrian_density', 'traffic_flow',
            'hour', 'day_of_week'
        ]

    def train_engagement_model(self, training_data):
        """Train the model using historical data"""
        df = pd.DataFrame(training_data)
        
        # Extract time features
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        
        # Prepare features and target
        X = df[self.feature_columns]
        y = df['engagement_rate']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)

    def predict_optimal_routes(self, current_conditions, zone_conditions):
        """Predict optimal routes based on current conditions"""
        predictions = []
        current_hour = datetime.now().hour
        current_day = datetime.now().weekday()
        
        for zone in zone_conditions:
            features = np.array([
                current_conditions['temperature'],
                current_conditions['precipitation'],
                current_conditions['wind_speed'],
                zone['pedestrian_density'],
                zone['traffic_flow'],
                current_hour,
                current_day
            ]).reshape(1, -1)
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Predict engagement
            predicted_engagement = self.model.predict(features_scaled)[0]
            
            # Calculate route score
            route_score = self._calculate_route_score(
                predicted_engagement,
                zone['pedestrian_density'],
                zone['traffic_flow']
            )
            
            predictions.append({
                'zone_id': zone['zone_id'],
                'predicted_engagement': predicted_engagement,
                'route_score': route_score,
                'coordinates': {
                    'latitude': zone['latitude'],
                    'longitude': zone['longitude']
                }
            })
        
        # Sort by route score
        return sorted(predictions, key=lambda x: x['route_score'], reverse=True)

    def generate_route_recommendations(self, optimal_zones):
        """Generate detailed route recommendations"""
        recommendations = []
        
        for zone in optimal_zones:
            route_id = str(uuid.uuid4())
            estimated_reach = self._estimate_reach(
                zone['predicted_engagement'],
                zone['coordinates']
            )
            
            recommended_times = self._get_recommended_times(
                zone['predicted_engagement']
            )
            
            sustainability_score = self._calculate_sustainability_score(
                zone['coordinates']
            )
            
            recommendations.append({
                'route_id': route_id,
                'zone_id': zone['zone_id'],
                'predicted_engagement': zone['predicted_engagement'],
                'route_score': zone['route_score'],
                'estimated_reach': estimated_reach,
                'recommended_times': recommended_times,
                'sustainability_score': sustainability_score
            })
        
        return recommendations

    def _calculate_route_score(self, engagement, pedestrian_density, traffic_flow):
        """Calculate overall route score considering multiple factors"""
        engagement_weight = 0.4
        density_weight = 0.3
        traffic_weight = 0.3
        
        return (
            engagement * engagement_weight +
            pedestrian_density * density_weight +
            traffic_flow * traffic_weight
        )

    def _estimate_reach(self, engagement_rate, coordinates):
        """Estimate potential reach based on location and engagement"""
        base_reach = 1000  # Base reach per hour
        location_multiplier = self._get_location_multiplier(coordinates)
        engagement_multiplier = 1 + (engagement_rate * 2)  # Higher engagement = higher reach
        
        return int(base_reach * location_multiplier * engagement_multiplier)

    def _get_location_multiplier(self, coordinates):
        """Calculate location-based multiplier for reach estimates"""
        # Simplified example - in reality, would use more sophisticated geo-analysis
        return 1.2  # Default multiplier for urban areas

    def _get_recommended_times(self, engagement_rate):
        """Generate recommended time slots based on predicted engagement"""
        current_hour = datetime.now().hour
        times = []
        
        # Morning slot (if applicable)
        if current_hour <= 10:
            times.append({
                'start': '08:00',
                'end': '10:00',
                'priority': 'High' if engagement_rate > 0.15 else 'Medium'
            })
        
        # Lunch slot (if applicable)
        if current_hour <= 14:
            times.append({
                'start': '12:00',
                'end': '14:00',
                'priority': 'High' if engagement_rate > 0.2 else 'Medium'
            })
        
        # Evening slot (if applicable)
        if current_hour <= 18:
            times.append({
                'start': '16:00',
                'end': '18:00',
                'priority': 'High' if engagement_rate > 0.18 else 'Medium'
            })
        
        return times

    def _calculate_sustainability_score(self, coordinates):
        """Calculate sustainability score for the route"""
        # Simplified example - would consider factors like:
        # - Route elevation changes
        # - Traffic patterns
        # - Air quality
        # - Weather conditions
        base_score = 75
        return min(100, base_score)

    def save_model(self, filepath):
        """Save the trained model to disk"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }, filepath)

    def load_model(self, filepath):
        """Load a trained model from disk"""
        saved_model = joblib.load(filepath)
        self.model = saved_model['model']
        self.scaler = saved_model['scaler']
        self.feature_columns = saved_model['feature_columns'] 