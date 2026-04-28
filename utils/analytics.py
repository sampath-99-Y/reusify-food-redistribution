import pandas as pd

def generate_insights(results):
    df = pd.DataFrame(results)

    total_food = df['food'].sum()
    avg_distance = df['distance_km'].mean()

    top_ngo = df.groupby('ngo')['food'].sum().idxmax()

    return {
        "total_food": total_food,
        "avg_distance": round(avg_distance, 2),
        "top_ngo": top_ngo
    }