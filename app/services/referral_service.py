# app/services/referral_service.py
from app.models import db, User, Referral, Reward

def create_referral(referrer_id, referred_user_id):
    """Create a new referral record"""
    referral = Referral(
        referrer_id=referrer_id,
        referred_user_id=referred_user_id,
        status='successful'
    )
    
    db.session.add(referral)
    db.session.commit()
    
    # Optionally process rewards
    process_referral_reward(referral.id)
    
    return referral

def get_user_referrals(user_id):
    """Get all users referred by a specific user"""
    return Referral.query.filter_by(referrer_id=user_id).all()

def get_referral_stats(user_id):
    """Get referral statistics for a user"""
    referrals = Referral.query.filter_by(referrer_id=user_id).all()
    
    stats = {
        'total_referrals': len(referrals),
        'successful_referrals': len([r for r in referrals if r.status == 'successful']),
        'rewards_earned': Reward.query.filter_by(user_id=user_id).count()
    }
    
    return stats

def process_referral_reward(referral_id):
    """Process rewards for a successful referral"""
    referral = Referral.query.get(referral_id)
    
    # Create a reward record
    reward = Reward(
        user_id=referral.referrer_id,
        referral_id=referral.id,
        reward_type='credit',
        amount=10.0  # Example: $10 credit per referral
    )
    
    db.session.add(reward)
    db.session.commit()
    
    return reward