# routes.py
from flask import Blueprint, request, jsonify
from service import HealthRiskCalculator

risk_bp = Blueprint('health_risk', __name__)
risk_service = HealthRiskCalculator()

@risk_bp.route('/calculate', methods=['POST'])
def calculate_risk_endpoint():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Empty payload"}), 400

        # --- 1. VALIDATION ---
        required_fields = ['systolic_bp', 'diastolic_bp', 'blood_sugar', 'oxygen_level']
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        # --- 2. EXECUTE LOGIC ---
        result = risk_service.compute_risk(data)

        # --- 3. DATABASE (SKIPPED FOR NOW) ---
        # Since Firebase isn't ready, we skip saving.
        # When ready, you can uncomment the DB code here.
        print(f"Calculated risk for patient: {data.get('user_id', 'Guest')}")

        # --- 4. RESPONSE ---
        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
