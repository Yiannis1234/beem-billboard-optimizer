from models.route_optimizer import BeemRouteOptimizer
from data.data_collector import BeemDataCollector
from datetime import datetime, timedelta
import json

def main():
    # Configuration
    config = {
        'weather_api_key': 'demo_key',  # Using simulated data for demo
        'traffic_api_key': 'demo_key'   # Using simulated data for demo
    }
    
    # Initialize components
    data_collector = BeemDataCollector(config)
    route_optimizer = BeemRouteOptimizer()
    
    # Define sample zones (London areas)
    zones = [
        {
            'zone_id': 'central_london_1',
            'name': 'Soho',
            'latitude': 51.5137,
            'longitude': -0.1349
        },
        {
            'zone_id': 'central_london_2',
            'name': 'Covent Garden',
            'latitude': 51.5117,
            'longitude': -0.1240
        },
        {
            'zone_id': 'central_london_3',
            'name': 'Oxford Street',
            'latitude': 51.5152,
            'longitude': -0.1418
        }
    ]
    
    # Prepare training data
    print("\n🔄 Preparing historical training data...")
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()
    training_data = data_collector.prepare_training_data(start_date, end_date, zones)
    print(f"✓ Generated {len(training_data)} historical data points")
    
    # Train the model
    print("\n🧠 Training route optimization model...")
    route_optimizer.train_engagement_model(training_data)
    print("✓ Model training complete")
    
    # Get current conditions for each zone
    print("\n🌍 Analyzing current conditions for each zone...")
    current_time = datetime.now()
    zone_conditions = []
    
    for zone in zones:
        print(f"\n📍 Analyzing: {zone['name']}")
        integrated_data = data_collector.integrate_data(zone, current_time)
        
        if integrated_data['weather'] and integrated_data['traffic']:
            zone_data = {
                'zone_id': zone['zone_id'],
                'name': zone['name'],
                'latitude': zone['latitude'],
                'longitude': zone['longitude'],
                'pedestrian_density': integrated_data['pedestrian_density'],
                'traffic_flow': 1 - integrated_data['traffic']['congestion_level']  # Invert congestion for flow
            }
            zone_conditions.append(zone_data)
            
            print(f"🌤  Weather: {integrated_data['weather']['condition']}, {integrated_data['weather']['temperature']:.1f}°C")
            print(f"🚗 Traffic Flow: {zone_data['traffic_flow']:.2f}")
            print(f"👥 Pedestrian Density: {zone_data['pedestrian_density']:.2f}")
    
    # Get route recommendations
    print("\n📊 Generating route recommendations...")
    current_conditions = {
        'temperature': integrated_data['weather']['temperature'],
        'precipitation': integrated_data['weather']['precipitation'],
        'wind_speed': integrated_data['weather']['wind_speed']
    }
    
    optimal_zones = route_optimizer.predict_optimal_routes(current_conditions, zone_conditions)
    recommendations = route_optimizer.generate_route_recommendations(optimal_zones)
    
    # Display recommendations
    print("\n🚲 Beem Billboard Bike Route Recommendations")
    print("==========================================")
    
    for i, route in enumerate(recommendations, 1):
        zone_name = next(z['name'] for z in zones if z['zone_id'] == route['zone_id'])
        print(f"\n📍 Route {i}: {zone_name}")
        print(f"🆔 Route ID: {route['route_id']}")
        print(f"📈 Predicted Engagement: {route['predicted_engagement']:.1%}")
        print(f"⭐ Route Score: {route['route_score']:.2f}")
        print(f"👥 Estimated Reach: {route['estimated_reach']} impressions")
        print(f"🌱 Sustainability Score: {route['sustainability_score']}/100")
        
        print("\n⏰ Recommended Times:")
        for time_slot in route['recommended_times']:
            priority_emoji = "🔴" if time_slot['priority'] == "High" else "🟡"
            print(f"{priority_emoji} {time_slot['start']} to {time_slot['end']} ({time_slot['priority']} Priority)")
            
    # Save the trained model
    print("\n💾 Saving model...")
    route_optimizer.save_model('route_optimizer_model.joblib')
    print("✓ Model saved successfully")
    print("\n✨ Demo complete! The system is ready for real-world deployment.")

if __name__ == "__main__":
    main() 