from datetime import datetime
from typing import Dict, Any

class HealthRiskCalculator:
    """
    Service class responsible for calculating health risks.
    Encapsulates all medical logic.
    """

    def compute_risk(self, vitals: Dict[str, Any]) -> Dict[str, Any]:
        score = 0
        reasons = []

        # Standardized inputs (Clean API Contract)
        sbp = vitals.get('systolic_bp')
        dbp = vitals.get('diastolic_bp')
        sugar = vitals.get('blood_sugar')
        sp02 = vitals.get('oxygen_level')
        hr = vitals.get('heart_rate')
        sleep = vitals.get('sleep_hours')
        prev_score = vitals.get('previous_score')

        # --- LOGIC ENGINE ---
        
        # 1. Hypertension (BP)
        if sbp >= 180 or dbp >= 120:
            score += 40
            reasons.append("Critical: Hypertensive Crisis")
        elif sbp >= 140 or dbp >= 90:
            score += 20
            reasons.append("Stage 2 Hypertension")
        
        # 2. Diabetes (Sugar)
        if sugar > 200:
            score += 30
            reasons.append("Hyperglycemia (High Blood Sugar)")
        elif sugar < 70:
            score += 25
            reasons.append("Hypoglycemia Risk")

        # 3. Hypoxia (Oxygen)
        if sp02 < 90:
            score += 50
            reasons.append("Critical: Hypoxia (Low Oxygen)")
        elif sp02 < 95:
            score += 15
            reasons.append("Low Oxygen Saturation")

        # 4. Heart Rate
        if hr > 100:
            score += 10
            reasons.append("Tachycardia (High Heart Rate)")
        elif hr < 50:
            score += 10
            reasons.append("Bradycardia (Low Heart Rate)")

        # 5. Lifestyle
        if sleep < 5:
            score += 5
            reasons.append("Chronic Sleep Deprivation")

        # Cap score
        final_score = min(score, 100)
        
        return {
            "risk_score": final_score,
            "risk_label": self._classify_score(final_score),
            "reasons": reasons if reasons else ["Vitals within normal limits"],
            "trend": self._calculate_trend(final_score, prev_score),
            "calculated_at": datetime.utcnow().isoformat() + "Z"
        }

    def _classify_score(self, score: int) -> str:
        if score < 30: return "Low"
        elif score < 60: return "Medium"
        else: return "High"

    def _calculate_trend(self, current: int, previous: int) -> str:
        if previous is None: return "New"
        diff = current - previous
        if diff > 5: return "Worsening"
        elif diff < -5: return "Improving"
        else: return "Stable"