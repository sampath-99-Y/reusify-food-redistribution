from geopy.distance import geodesic

def allocate(restaurants, ngos):
    allocations = []

    for r in restaurants:
        best = None
        best_score = float('inf')
        best_dist = 0

        for n in ngos:
            dist = geodesic((r['lat'], r['lon']), (n['lat'], n['lon'])).km

            # smarter scoring
            demand_weight = n['demand'] * 0.08
            distance_weight = dist * 1.2

            score = distance_weight - demand_weight

            if score < best_score:
                best_score = score
                best = n
                best_dist = dist

        allocations.append({
            "restaurant": r['name'],
            "ngo": best['name'],
            "distance_km": round(best_dist, 2),
            "food": r['food']
        })

    return allocations