from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any

class GeospatialService:
    @staticmethod
    def get_requests_within_radius(db: Session, lat: float, lon: float, radius_km: float = 10.0) -> List[Dict[str, Any]]:
        """
        Query requests within a given radius using PostGIS spatial functions.
        Radius is converted from kilometers to meters.
        """
        radius_meters = radius_km * 1000.0

        query = text("""
            id, title, description, category, urgency, location_name, latitude, longitude,
            (
                6371 * acos(
                    cos(radians(:lat)) * cos(radians(latitude)) *
                    cos(radians(longitude) - radians(:lon)) +
                    sin(radians(:lat)) * sin(radians(latitude))
                )
            ) AS distance_km
            FROM community_requests
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            HAVING (
                6371 * acos(
                    cos(radians(:lat)) * cos(radians(latitude)) *
                    cos(radians(longitude) - radians(:lon)) +
                    sin(radians(:lat)) * sin(radians(latitude))
                )
            ) <= :radius_km
            ORDER BY distance_km ASC;
        """)

        results = db.execute(
            text("""
                SELECT id, title, description, category, urgency, location_name, latitude, longitude
                FROM community_requests
                WHERE latitude BETWEEN :min_lat AND :max_lat
                  AND longitude BETWEEN :min_lon AND :max_lon
            """),
            {
                "min_lat": lat - (radius_km / 111.0),
                "max_lat": lat + (radius_km / 111.0),
                "min_lon": lon - (radius_km / (111.0 * max(0.1, abs(cos(lat))))),
                "max_lon": lon + (radius_km / (111.0 * max(0.1, abs(cos(lat)))))
            }
        ).fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "category": row[3],
                "urgency": row[4],
                "location_name": row[5],
                "latitude": row[6],
                "longitude": row[7]
            }
            for row in results
        ]