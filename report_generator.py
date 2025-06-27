def generate_report(
    user,
    regime_probs,
    stability,
    coherence,
    velocity,
    fragility_flag,
    phase_shift_flag,
    flow_notes,
    macro_score,
    risk_weight,
    personalized_alloc
):
    print("\n🧠 Regime Summary:")
    top_regime = max(regime_probs, key=regime_probs.get)
    confidence = int(regime_probs[top_regime] * 100)
    print(f"• Regime: {top_regime} ({confidence}% confidence)")
    print(f"• Stability: {stability:.2f}")
    print(f"• Coherence: {coherence:.2f}")
    print(f"• Narrative Velocity: {velocity:.2f}")

    if fragility_flag:
        print("⚠️ Flow Stress Detected:", flow_notes)
    if phase_shift_flag:
        print("🔺 Phase Shift Risk: Consider tactical caution")

    print(f"\n🧭 Risk Budget Modulated to: {int(risk_weight * 100)}%")
    print(f"🎯 {user.name}'s Equity Target: {int(user.equity_target(2025) * 100)}%")

    print("\n📊 Personalized Allocation:")
    for fund, weight in personalized_alloc.items():
        print(f"• {fund} Fund: {weight}%")
