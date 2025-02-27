# app/routes/referrals.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.referral_service import get_user_referrals, get_referral_stats

referrals_bp = Blueprint('referrals', __name__)

@referrals_bp.route('/referrals', methods=['GET'])
@jwt_required()
def get_referrals():
    user_id = get_jwt_identity()
    
    referrals = get_user_referrals(user_id)
    
    referral_data = []
    for referral in referrals:
        referral_data.append({
            'id': referral.id,
            'referred_user': {
                'id': referral.referred_user.id,
                'username': referral.referred_user.username
            },
            'date_referred': referral.date_referred.isoformat(),
            'status': referral.status
        })
    
    return jsonify({
        'success': True,
        'referrals': referral_data
    }), 200

@referrals_bp.route('/referral-stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()
    
    stats = get_referral_stats(user_id)
    
    return jsonify({
        'success': True,
        'stats': stats
    }), 200