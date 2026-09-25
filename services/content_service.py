def clinic_details() -> dict[str, str]:
    return {
        "name": "ProCare Physiotherapy",
        "tagline": "Community health and rehabilitation",
        "location": "Naranpura, Ahmedabad, Gujarat",
        "lead_physio": "Dr Vishva Shah (MPT)",
        "phone": "9662341549",
        "phone_display": "+91 96623 41549",
        "email": "procare.vishva@gmail.com",
        "address": "F-107 Celestia, Madhav Pride Road, near Satya 2, Shastrinagar, Naranpura, Ahmedabad 380063",
        "hours": "Mon-Sat: 7:00 AM - 10:00 PM | Sun: 7:00 AM - 10:00 AM",
        "instagram": "https://www.instagram.com/procarephysio.vishva/",
        "home_visit": "Home visit available",
        "service_area": "Naranpura, Ahmedabad and nearby areas",
    }


def service_catalog() -> list[dict[str, str]]:
    return [
        {
            "name": "Manual Therapy",
            "benefit": "Hands-on treatment for joint and soft-tissue restrictions.",
            "conditions": "Neck pain, back pain, stiff joints, sports injuries",
        },
        {
            "name": "Exercise Therapy",
            "benefit": "Personalized movement plans to restore strength and mobility.",
            "conditions": "Post-operative rehab, weakness, mobility loss",
        },
        {
            "name": "Electrotherapy",
            "benefit": "Pain relief and muscle activation support for recovery.",
            "conditions": "Chronic pain, muscle spasm, arthritis flare-ups",
        },
        {
            "name": "Posture Correction",
            "benefit": "Targeted correction for desk-related strain and imbalance.",
            "conditions": "Forward head posture, rounded shoulders, tech neck",
        },
        {
            "name": "Sports Rehabilitation",
            "benefit": "Return to sport with safer movement and improved resilience.",
            "conditions": "Ligament injuries, tendon pain, recurrent sprains",
        },
        {
            "name": "Neurological Rehab",
            "benefit": "Guided therapy for better coordination, balance, and function.",
            "conditions": "Stroke recovery, balance issues, gait concerns",
        },
    ]


def testimonials() -> list[dict[str, str]]:
    return [
        {
            "name": "Google review",
            "story": "I would highly recommend ProCare Physiotherapy for the home visit.",
            "highlight": "Home visit care",
        },
        {
            "name": "Google review",
            "story": "Got treated effectively. Good doctor to be treated.",
            "highlight": "Effective treatment",
        },
        {
            "name": "Google review",
            "story": "Good service, kind nature and very polite.",
            "highlight": "Polite, caring staff",
        },
        {
            "name": "Google review",
            "story": "Very professional physiotherapy care with a patient-centered approach and clear guidance.",
            "highlight": "Professional care",
        },
        {
            "name": "Google review",
            "story": "Helpful for pain relief and recovery, especially for home-based rehabilitation support.",
            "highlight": "Pain relief",
        },
        {
            "name": "Google review",
            "story": "Excellent treatment, respectful communication, and helpful follow-up throughout the process.",
            "highlight": "Recovery support",
        },
    ]


def stat_cards() -> list[dict[str, str]]:
    return [
        {"value": "8+", "label": "years of care"},
        {"value": "4,500+", "label": "patient sessions"},
        {"value": "95%", "label": "recovery satisfaction"},
    ]


def process_steps() -> list[dict[str, str]]:
    return [
        {"step": "1", "title": "Comprehensive assessment", "text": "We understand your pain pattern, movement limits, and treatment goals."},
        {"step": "2", "title": "Personalized plan", "text": "You receive a structured program built around your daily routine and condition."},
        {"step": "3", "title": "Hands-on therapy", "text": "We combine manual techniques, guidance, and targeted exercises for better results."},
        {"step": "4", "title": "Progressive recovery", "text": "We track goals, reduce pain, and improve strength with long-term confidence."},
    ]
