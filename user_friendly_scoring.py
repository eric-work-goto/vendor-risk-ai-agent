"""
User-Friendly Assessment Scoring System
=======================================
Enhanced scoring system with letter grades and clear explanations.
"""

from typing import Dict, Tuple, Any, List
from enum import Enum

class LetterGrade(Enum):
    """Letter grade enumeration"""
    A_PLUS = "A+"
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    B_MINUS = "B-"
    C_PLUS = "C+"
    C = "C"
    C_MINUS = "C-"
    D_PLUS = "D+"
    D = "D"
    F = "F"

class GradingSystem:
    """Enhanced grading system for vendor risk assessments"""
    
    def __init__(self):
        # Grade thresholds (higher scores = better security)
        self.grade_thresholds = {
            97: ("A+", "Exceptional", "🏆"),
            93: ("A", "Excellent", "⭐"),
            90: ("A-", "Very Good", "🌟"),
            87: ("B+", "Good", "✅"),
            83: ("B", "Above Average", "👍"),
            80: ("B-", "Satisfactory", "👌"),
            77: ("C+", "Fair", "⚠️"),
            73: ("C", "Needs Attention", "🔍"),
            70: ("C-", "Below Average", "⚡"),
            67: ("D+", "Poor", "🚨"),
            63: ("D", "Very Poor", "❌"),
            60: ("D-", "Failing", "💥"),
            0: ("F", "Critical Failure", "🚫")
        }
        
        # Risk level mappings
        self.risk_levels = {
            "A+": "Minimal", "A": "Minimal", "A-": "Very Low",
            "B+": "Low", "B": "Low", "B-": "Low-Medium",
            "C+": "Medium", "C": "Medium", "C-": "Medium-High",
            "D+": "High", "D": "High", "D-": "Critical", "F": "Critical"
        }
        
        # Score explanations
        self.score_explanations = {
            "A+": "Outstanding security and compliance posture. Industry-leading practices.",
            "A": "Excellent security and compliance. Very minimal risk.",
            "A-": "Very good security practices with minor areas for improvement.",
            "B+": "Good security posture with some room for enhancement.",
            "B": "Above average security with standard industry practices.",
            "B-": "Satisfactory security but several areas need attention.",
            "C+": "Fair security posture requiring moderate improvements.",
            "C": "Average security with significant areas needing attention.",
            "C-": "Below average security requiring substantial improvements.",
            "D+": "Poor security posture with major vulnerabilities identified.",
            "D": "Very poor security requiring immediate attention.",
            "D-": "Failing security posture requiring urgent remediation.",
            "F": "Critical security failures requiring immediate remediation."
        }
        
        # Colors for UI display
        self.grade_colors = {
            "A+": "#10b981", "A": "#059669", "A-": "#047857",  # Green variants
            "B+": "#22c55e", "B": "#16a34a", "B-": "#15803d",  # Light green variants
            "C+": "#eab308", "C": "#ca8a04", "C-": "#a16207",  # Yellow variants
            "D+": "#f97316", "D": "#ea580c", "D-": "#dc2626", "F": "#dc2626"    # Orange to red
        }

    def calculate_letter_grade(self, security_score: float) -> Tuple[str, str, str, str]:
        """
        Calculate letter grade from security score.
        
        Args:
            security_score: Security score from 0-100 (higher = better)
            
        Returns:
            Tuple of (letter_grade, description, emoji, explanation)
        """
        # Find the appropriate grade (start from highest and work down)
        for threshold in sorted(self.grade_thresholds.keys(), reverse=True):
            if security_score >= threshold:
                letter_grade, description, emoji = self.grade_thresholds[threshold]
                explanation = self.score_explanations[letter_grade]
                return letter_grade, description, emoji, explanation
        
        # Fallback to worst grade
        return "F", "Critical Failure", "🚫", self.score_explanations["F"]

    def get_user_friendly_scores(self, security_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Convert technical security scores to user-friendly format.
        
        Args:
            security_scores: Dictionary of security scores by category (0-100, higher = better)
            
        Returns:
            Dictionary with user-friendly scoring information
        """
        friendly_scores = {}
        
        for category, score in security_scores.items():
            grade, description, emoji, explanation = self.calculate_letter_grade(score)
            
            # Keep the original security score for display (higher = better for security)
            display_score = round(score)
            
            friendly_scores[category] = {
                "score": display_score,  # Original security score where higher is better
                "letter_grade": grade,
                "description": description,
                "emoji": emoji,
                "explanation": explanation,
                "risk_level": self.risk_levels[grade],
                "color": self.grade_colors[grade],
                "original_risk_score": score  # Keep original for calculations (actually security score)
            }
        
        return friendly_scores

    def get_overall_assessment(self, component_scores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall assessment from component scores.
        
        Args:
            component_scores: Dictionary of component score data
            
        Returns:
            Overall assessment information
        """
        # Calculate weighted average of original security scores
        weights = {
            "security": 0.3,
            "compliance": 0.25,
            "data_protection": 0.25,
            "operational": 0.2
        }
        
        total_weighted_score = 0
        total_weight = 0
        
        for component, weight in weights.items():
            if component in component_scores:
                score = component_scores[component]["original_risk_score"]  # This is actually security score now
                total_weighted_score += score * weight
                total_weight += weight
        
        overall_security_score = total_weighted_score / total_weight if total_weight > 0 else 50
        
        # Get letter grade for overall
        grade, description, emoji, explanation = self.calculate_letter_grade(overall_security_score)
        
        return {
            "score": round(overall_security_score),  # Security score where higher is better
            "letter_grade": grade,
            "description": description,
            "emoji": emoji,
            "explanation": explanation,
            "risk_level": self.risk_levels[grade],
            "color": self.grade_colors[grade],
            "recommendation": self._get_recommendation(grade)
        }

    def _get_recommendation(self, grade: str) -> str:
        """Get business recommendation based on grade."""
        recommendations = {
            "A+": "✅ **APPROVED** - Excellent vendor choice. Proceed with confidence.",
            "A": "✅ **APPROVED** - Strong vendor with minimal risk. Safe to proceed.",
            "A-": "✅ **APPROVED** - Very good vendor choice with minor considerations.",
            "B+": "⚠️ **APPROVED WITH CONDITIONS** - Good vendor, monitor key areas.",
            "B": "⚠️ **REVIEW REQUIRED** - Acceptable vendor with standard oversight needed.",
            "B-": "⚠️ **REVIEW REQUIRED** - Address identified concerns before proceeding.",
            "C+": "🔍 **DETAILED REVIEW** - Moderate risk requiring management attention.",
            "C": "🔍 **DETAILED REVIEW** - Significant concerns need resolution.",
            "C-": "🚨 **HIGH RISK** - Major improvements required before approval.",
            "D+": "🚫 **NOT RECOMMENDED** - Serious security deficiencies identified.",
            "D": "🚫 **NOT RECOMMENDED** - Critical security issues require resolution.",
            "D-": "🚫 **REJECTED** - Failing security posture, do not proceed.",
            "F": "🚫 **REJECTED** - Unacceptable risk level. Do not proceed."
        }
        
        return recommendations.get(grade, "Further evaluation required.")

    def get_improvement_suggestions(self, scores: Dict[str, Any]) -> List[str]:
        """Get specific improvement suggestions based on scores."""
        suggestions = []
        
        # Check each component and suggest improvements
        for component, data in scores.items():
            grade = data["letter_grade"]
            
            if grade in ["C+", "C", "C-", "D+", "D", "F"]:
                component_name = component.replace("_", " ").title()
                
                if component == "security":
                    suggestions.append(f"🔒 **{component_name}**: Implement stronger encryption and access controls")
                elif component == "compliance":
                    suggestions.append(f"📋 **{component_name}**: Obtain relevant certifications (SOC 2, ISO 27001)")
                elif component == "data_protection":
                    suggestions.append(f"🛡️ **{component_name}**: Enhance privacy policies and data handling procedures")
                elif component == "operational":
                    suggestions.append(f"⚙️ **{component_name}**: Improve incident response and business continuity plans")
        
        if not suggestions:
            suggestions.append("✨ **Excellent work!** Maintain current security practices and stay updated with industry standards.")
        
        return suggestions

# Global grading system instance
grading_system = GradingSystem()

def convert_to_user_friendly(risk_assessment_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert technical risk assessment to user-friendly format.
    
    Args:
        risk_assessment_result: Original risk assessment result
        
    Returns:
        User-friendly assessment result
    """
    # Get assessment mode to determine score categories
    assessment_mode = risk_assessment_result.get("assessment_mode", "business_risk")
    scores = risk_assessment_result.get("scores", {})
    
    # Check if this is a real assessment with scoring_breakdown
    scoring_breakdown = risk_assessment_result.get("scoring_breakdown", {})
    
    # Map different assessment modes to standard categories for grading
    if assessment_mode == "technical_due_diligence":
        if scoring_breakdown:
            # Real assessment - extract from scoring_breakdown
            component_scores = {
                "security": scoring_breakdown.get("breach_assessment", {}).get("score", 50),
                "compliance": scoring_breakdown.get("compliance_assessment", {}).get("score", 50),
                "data_protection": scoring_breakdown.get("privacy_assessment", {}).get("score", 50),
                "operational": scoring_breakdown.get("trust_center_assessment", {}).get("score", 50)
            }
        else:
            # Legacy mock assessment - map technical assessment scores to standard categories
            component_scores = {
                "security": scores.get("technical_security", scores.get("security", 50)),
                "compliance": scores.get("compliance_framework", scores.get("compliance", 50)),
                "data_protection": scores.get("encryption", scores.get("access_controls", scores.get("data_protection", 50))),
                "operational": scores.get("infrastructure", scores.get("operational", 50))
            }
    else:  # business_risk assessment
        if scoring_breakdown:
            # Real assessment - map to business categories
            component_scores = {
                "security": scoring_breakdown.get("breach_assessment", {}).get("score", 50),
                "compliance": scoring_breakdown.get("compliance_assessment", {}).get("score", 50),
                "data_protection": scoring_breakdown.get("privacy_assessment", {}).get("score", 50),
                "operational": scoring_breakdown.get("trust_center_assessment", {}).get("score", 50),
                "ai_governance": scoring_breakdown.get("ai_assessment", {}).get("score", 50),
                "data_flows": scoring_breakdown.get("data_flow_assessment", {}).get("score", 50)
            }
        else:
            # Legacy mock assessment - map business assessment scores to all relevant categories
            component_scores = {
                "business_impact": scores.get("business_impact", 50),
                "operational_risk": scores.get("operational_risk", 50),
                "financial_stability": scores.get("financial_stability", 50),
                "compliance_risk": scores.get("compliance_risk", 50),
                "data_protection_risk": scores.get("data_protection_risk", 50),
                "vendor_reliability": scores.get("vendor_reliability", 50),
                "strategic_alignment": scores.get("strategic_alignment", 50),
                "privacy_compliance": scores.get("privacy_compliance", 50),
                "ai_business_risk": scores.get("ai_business_risk", 50)
            }
    
    # Convert to user-friendly format
    friendly_scores = grading_system.get_user_friendly_scores(component_scores)
    
    # Check if we have an overall_score from real assessment
    if "overall_score" in risk_assessment_result:
        # Use the real overall score instead of calculating from components
        real_overall_score = risk_assessment_result["overall_score"]
        grade, description, emoji, explanation = grading_system.calculate_letter_grade(real_overall_score)
        overall_assessment = {
            "score": round(real_overall_score),
            "letter_grade": grade,
            "description": description,
            "emoji": emoji,
            "explanation": explanation,
            "risk_level": grading_system.risk_levels[grade],
            "color": grading_system.grade_colors[grade],
            "recommendation": grading_system._get_recommendation(grade)
        }
    else:
        # Calculate from component scores (legacy mock assessments)
        overall_assessment = grading_system.get_overall_assessment(friendly_scores)
    
    improvement_suggestions = grading_system.get_improvement_suggestions(friendly_scores)
    
    # Create enhanced result
    enhanced_result = {
        **risk_assessment_result,  # Keep original data
        "user_friendly": {
            "overall": overall_assessment,
            "components": friendly_scores,
            "improvement_suggestions": improvement_suggestions,
            "summary": f"This vendor received a **{overall_assessment['letter_grade']}** grade ({overall_assessment['score']}/100) indicating **{overall_assessment['risk_level']} Risk**. {overall_assessment['explanation']}"
        }
    }
    
    # Add letter grades - ensure consistent structure for frontend
    enhanced_result["letter_grades"] = {
        "overall": overall_assessment["letter_grade"],
        "compliance": friendly_scores.get("compliance", {}).get("letter_grade", "N/A"),
        "security": friendly_scores.get("security", {}).get("letter_grade", "N/A"),
        "data_protection": friendly_scores.get("data_protection", {}).get("letter_grade", "N/A")
    }
    
    # Add any additional dynamic categories for business risk assessments
    if assessment_mode == "business_risk":
        for category, grade_info in friendly_scores.items():
            if category not in enhanced_result["letter_grades"]:
                enhanced_result["letter_grades"][category] = grade_info["letter_grade"]
    
    # Ensure scores structure for frontend compatibility
    enhanced_result["scores"] = {
        "compliance": component_scores.get("compliance", 50),
        "security": component_scores.get("security", 50), 
        "data_protection": component_scores.get("data_protection", 50),
        "overall": overall_assessment["score"]
    }
    
    enhanced_result["risk_description"] = overall_assessment["explanation"]
    enhanced_result["business_recommendation"] = overall_assessment["recommendation"]
    
    return enhanced_result

if __name__ == "__main__":
    # Test the grading system
    test_scores = {
        "security": 85,      # B grade (good security)
        "compliance": 77,    # C+ grade (fair compliance)  
        "data_protection": 92,  # A- grade (very good data protection)
        "operational": 80    # B- grade (satisfactory operational security)
    }
    
    friendly = grading_system.get_user_friendly_scores(test_scores)
    overall = grading_system.get_overall_assessment(friendly)
    suggestions = grading_system.get_improvement_suggestions(friendly)
    
    print("🎯 User-Friendly Scoring Test:")
    print(f"Overall: {overall['letter_grade']} ({overall['score']}/100)")
    print(f"Risk Level: {overall['risk_level']}")
    print(f"Recommendation: {overall['recommendation']}")
    print("\nComponent Scores:")
    for component, data in friendly.items():
        print(f"  {component}: {data['letter_grade']} ({data['score']}/100) - {data['description']}")
