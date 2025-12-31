from flask import Blueprint, request, jsonify
from .service import HealthRiskCalculator

risk_bp = Blueprint('health_risk', __name__)
risk_service = HealthRiskCalculator()

@risk_bp.route('/calculate', methods=['POST'])
def calculate_risk_endpoint():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Empty payload"}), 400

        # --- 1. CONTEXT EXTRACTION ---
        # Hackathon Note: Auth is handled by gateway, we just log the context
        user_id = data.get('user_id', 'UNKNOWN_PATIENT')
        nurse_id = data.get('updated_by', 'SYSTEM')

        # --- 2. INPUT VALIDATION (Sanity Checks) ---
        required_fields = ['systolic_bp', 'diastolic_bp', 'blood_sugar', 'oxygen_level']
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        # Range Validations (Impossible Medical Values)
        if not (0 <= data['oxygen_level'] <= 100):
            return jsonify({"error": "Invalid oxygen_level (must be 0-100)"}), 400
        if not (0 <= data['systolic_bp'] <= 300):
             return jsonify({"error": "Invalid systolic_bp range"}), 400

        # --- 3. EXECUTE LOGIC ---
        result = risk_service.compute_risk(data)

        # --- 4. DATA PERSISTENCE ---
        # TODO: Save vitals & risk_score to patient_health_records collection in MongoDB
        # Example: db.records.insert_one({ "patient_id": user_id, "nurse_id": nurse_id, ...result })

        # --- 5. RESPONSE ---
        return jsonify({
            "status": "success",
            "meta": {
                "patient_id": user_id,
                "nurse_id": nurse_id,
                "version": "v2.0-stable"
            },
            "data": result
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500