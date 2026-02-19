from typing import Dict, Optional
from config import settings


class AIService:
    """AI-powered complexity analysis and project estimation using OpenAI or fallback heuristics."""

    WEIGHT_MAP = {
        "hardware": 1.5,
        "ai_ml": 2.0,
        "cloud": 1.2,
        "realtime": 1.8,
        "safety_critical": 2.5,
    }

    COMPLEXITY_LEVELS = [
        (3.0, "Basic", 1.0, "standard"),
        (5.0, "Medium", 1.5, "professional"),
        (7.5, "Advanced", 2.0, "senior"),
        (10.0, "Industrial", 3.0, "expert"),
    ]

    def _calculate_base_score(
        self,
        has_hardware: bool,
        has_ai_ml: bool,
        has_cloud: bool,
        is_realtime: bool,
        is_safety_critical: bool,
    ) -> Dict[str, float]:
        """Calculate weighted complexity score from project flags."""
        breakdown = {}
        score = 1.0  # Base complexity

        if has_hardware:
            breakdown["hardware"] = self.WEIGHT_MAP["hardware"]
            score += self.WEIGHT_MAP["hardware"]
        if has_ai_ml:
            breakdown["ai_ml"] = self.WEIGHT_MAP["ai_ml"]
            score += self.WEIGHT_MAP["ai_ml"]
        if has_cloud:
            breakdown["cloud"] = self.WEIGHT_MAP["cloud"]
            score += self.WEIGHT_MAP["cloud"]
        if is_realtime:
            breakdown["realtime"] = self.WEIGHT_MAP["realtime"]
            score += self.WEIGHT_MAP["realtime"]
        if is_safety_critical:
            breakdown["safety_critical"] = self.WEIGHT_MAP["safety_critical"]
            score += self.WEIGHT_MAP["safety_critical"]

        # Normalize to 1-10 scale
        max_possible = 1.0 + sum(self.WEIGHT_MAP.values())
        normalized = min((score / max_possible) * 10, 10.0)

        return {
            "score": round(normalized, 1),
            "breakdown": breakdown,
            "raw_score": round(score, 2),
        }

    def _get_complexity_level(self, score: float):
        for threshold, level, multiplier, rate_cat in self.COMPLEXITY_LEVELS:
            if score <= threshold:
                return level, multiplier, rate_cat
        return "Industrial", 3.0, "expert"

    def _estimate_hours(self, score: float) -> tuple:
        """Estimate hour range based on complexity score."""
        base_min = int(20 + (score * 8))
        base_max = int(40 + (score * 16))
        return base_min, base_max

    def _estimate_risk(self, score: float) -> float:
        """Estimate risk percentage based on complexity."""
        return round(min(5 + (score * 3.5), 40), 1)

    async def analyze_complexity(
        self,
        project_description: str,
        has_hardware: bool = False,
        has_ai_ml: bool = False,
        has_cloud: bool = False,
        is_realtime: bool = False,
        is_safety_critical: bool = False,
    ) -> Dict:
        """Full complexity analysis combining heuristic scoring with optional AI analysis."""
        # Calculate base heuristic score
        base = self._calculate_base_score(
            has_hardware, has_ai_ml, has_cloud, is_realtime, is_safety_critical
        )
        score = base["score"]

        # Get complexity classification
        level, multiplier, rate_category = self._get_complexity_level(score)

        # Estimate hours and risk
        hours_min, hours_max = self._estimate_hours(score)
        risk_pct = self._estimate_risk(score)

        # Try AI analysis if OpenAI key is available
        ai_analysis = None
        if settings.OPENAI_API_KEY:
            try:
                ai_analysis = await self._get_ai_analysis(
                    project_description, has_hardware, has_ai_ml,
                    has_cloud, is_realtime, is_safety_critical
                )
            except Exception:
                ai_analysis = None

        if ai_analysis is None:
            # Fallback analysis based on description length and keywords
            ai_analysis = self._generate_fallback_analysis(
                project_description, level, score
            )

        return {
            "complexity_score": score,
            "complexity_level": level,
            "pricing_multiplier": multiplier,
            "suggested_hours_min": hours_min,
            "suggested_hours_max": hours_max,
            "risk_percentage": risk_pct,
            "rate_category": rate_category,
            "ai_analysis": ai_analysis,
            "breakdown": base["breakdown"],
        }

    async def _get_ai_analysis(
        self,
        description: str,
        has_hardware: bool,
        has_ai_ml: bool,
        has_cloud: bool,
        is_realtime: bool,
        is_safety_critical: bool,
    ) -> str:
        """Get AI-powered analysis from OpenAI."""
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        features = []
        if has_hardware:
            features.append("hardware/embedded systems")
        if has_ai_ml:
            features.append("AI/ML components")
        if has_cloud:
            features.append("cloud infrastructure")
        if is_realtime:
            features.append("real-time requirements")
        if is_safety_critical:
            features.append("safety-critical systems")

        feature_text = ", ".join(features) if features else "standard software"

        prompt = f"""Analyze this engineering project for complexity and provide a brief professional assessment:

Project Description: {description}
Technical Features: {feature_text}

Provide a concise 3-4 sentence analysis covering:
1. Key technical challenges
2. Recommended approach
3. Risk factors to consider
4. Suggested project phases"""

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert engineering project estimator. Be concise and professional."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.7,
        )

        return response.choices[0].message.content

    def _generate_fallback_analysis(
        self, description: str, level: str, score: float
    ) -> str:
        """Generate a heuristic-based analysis when OpenAI is unavailable."""
        desc_len = len(description)
        complexity_text = {
            "Basic": "straightforward implementation with standard components",
            "Medium": "moderate complexity requiring careful planning and some specialized skills",
            "Advanced": "significant technical challenges requiring senior engineering expertise",
            "Industrial": "highly complex, safety-critical implementation requiring expert-level engineering",
        }

        analysis = (
            f"This project is classified as {level} complexity (score: {score}/10). "
            f"It involves {complexity_text.get(level, 'standard development')}. "
        )

        if score > 6:
            analysis += "Consider breaking the project into smaller milestones with dedicated testing phases. "
            analysis += "Risk mitigation strategies and thorough documentation are strongly recommended."
        elif score > 3:
            analysis += "A phased approach with regular client check-ins is recommended. "
            analysis += "Standard testing and code review processes should be sufficient."
        else:
            analysis += "This can be handled with a straightforward development approach. "
            analysis += "Standard practices should yield reliable results within the estimated timeframe."

        return analysis


ai_service = AIService()
