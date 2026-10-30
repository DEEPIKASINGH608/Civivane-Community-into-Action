import math
from typing import List, Dict, Any

class SmartMatchingEngine:
    @staticmethod
    def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance in kilometers between two coordinates."""
        R = 6371.0  
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c

    @staticmethod
    def rank_volunteers(request_data: Dict[str, Any], volunteers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ranks volunteers using the formula:
        Score = 0.4(Skill Compatibility) + 0.4(Geospatial Proximity) + 0.2(Urgency Match)
        """
        req_category = request_data.get("category", "").lower()
        req_lat = request_data.get("latitude", 0.0)
        req_lon = request_data.get("longitude", 0.0)
        req_urgency = request_data.get("urgency", "MEDIUM")

        urgency_weight_multiplier = 1.2 if req_urgency == "CRITICAL" else 1.0

        scored_volunteers = []
        for vol in volunteers:
            # 1. Skill Match Component (0 to 1)
            vol_skills = [s.lower() for s in vol.get("skills", [])]
            skill_match = 1.0 if req_category in vol_skills or not vol_skills else 0.4

            # 2. Distance Proximity Component (0 to 1, normalized over 50km max radius)
            vol_lat = vol.get("latitude", 0.0)
            vol_lon = vol.get("longitude", 0.0)
            distance_km = SmartMatchingEngine.calculate_haversine_distance(req_lat, req_lon, vol_lat, vol_lon)
            distance_score = max(0.0, 1.0 - (distance_km / 50.0))

            # 3. Urgency / Availability Component
            urgency_score = 1.0 if req_urgency in ["CRITICAL", "HIGH"] else 0.7

            # Final Composite Score Calculation
            composite_score = (0.4 * skill_match) + (0.4 * distance_score) + (0.2 * urgency_score)
            composite_score *= urgency_weight_multiplier

            scored_volunteers.append({
                "volunteer_id": vol.get("id"),
                "full_name": vol.get("full_name"),
                "composite_score": round(min(composite_score, 1.0), 3),
                "breakdown": {
                    "skill_match_40pct": round(skill_match * 0.4, 3),
                    "distance_score_40pct": round(distance_score * 0.4, 3),
                    "urgency_score_20pct": round(urgency_score * 0.2, 3),
                    "distance_km": round(distance_km, 2)
                }
            })

        scored_volunteers.sort(key=lambda x: x["composite_score"], reverse=True)
        return scored_volunteers