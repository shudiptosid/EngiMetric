from typing import Dict, Any, Optional


class PricingEngine:
    """Core pricing calculation engine supporting 5 different pricing models."""

    @staticmethod
    def calculate_hourly(
        hourly_rate: float,
        estimated_hours: float,
        risk_percentage: float = 10.0,
        profit_margin: float = 15.0,
        hardware_costs: float = 0.0,
        software_costs: float = 0.0,
        maintenance_months: int = 0,
        maintenance_monthly_rate: float = 0.0,
    ) -> Dict[str, Any]:
        """Algorithm 1: Cost = Hours × Rate + extras"""
        subtotal = hourly_rate * estimated_hours
        risk_amount = subtotal * (risk_percentage / 100)
        profit_amount = subtotal * (profit_margin / 100)
        maintenance_cost = maintenance_months * maintenance_monthly_rate
        total = subtotal + risk_amount + profit_amount + hardware_costs + software_costs + maintenance_cost

        return {
            "model_type": "hourly",
            "subtotal": round(subtotal, 2),
            "hardware_cost": round(hardware_costs, 2),
            "software_cost": round(software_costs, 2),
            "risk_amount": round(risk_amount, 2),
            "profit_amount": round(profit_amount, 2),
            "maintenance_cost": round(maintenance_cost, 2),
            "total_cost": round(total, 2),
            "breakdown": {
                "hourly_rate": hourly_rate,
                "hours": estimated_hours,
                "base_labor": round(subtotal, 2),
                "risk_pct": risk_percentage,
                "profit_pct": profit_margin,
            },
        }

    @staticmethod
    def calculate_fixed(
        hourly_rate: float,
        estimated_hours: float,
        risk_percentage: float = 10.0,
        profit_margin: float = 15.0,
        hardware_costs: float = 0.0,
        software_costs: float = 0.0,
        maintenance_months: int = 0,
        maintenance_monthly_rate: float = 0.0,
    ) -> Dict[str, Any]:
        """Algorithm 2: Cost = (Hours × Rate) + Hardware + Risk%"""
        labor = hourly_rate * estimated_hours
        subtotal = labor + hardware_costs + software_costs
        risk_amount = subtotal * (risk_percentage / 100)
        profit_amount = subtotal * (profit_margin / 100)
        maintenance_cost = maintenance_months * maintenance_monthly_rate
        total = subtotal + risk_amount + profit_amount + maintenance_cost

        return {
            "model_type": "fixed",
            "subtotal": round(subtotal, 2),
            "hardware_cost": round(hardware_costs, 2),
            "software_cost": round(software_costs, 2),
            "risk_amount": round(risk_amount, 2),
            "profit_amount": round(profit_amount, 2),
            "maintenance_cost": round(maintenance_cost, 2),
            "total_cost": round(total, 2),
            "breakdown": {
                "labor": round(labor, 2),
                "materials": round(hardware_costs + software_costs, 2),
                "risk_pct": risk_percentage,
                "profit_pct": profit_margin,
            },
        }

    @staticmethod
    def calculate_value_based(
        estimated_client_revenue: float,
        value_percentage: float = 10.0,
        risk_percentage: float = 10.0,
        profit_margin: float = 15.0,
        hardware_costs: float = 0.0,
        software_costs: float = 0.0,
        maintenance_months: int = 0,
        maintenance_monthly_rate: float = 0.0,
    ) -> Dict[str, Any]:
        """Algorithm 3: Cost = % of estimated client revenue impact"""
        subtotal = estimated_client_revenue * (value_percentage / 100)
        risk_amount = subtotal * (risk_percentage / 100)
        profit_amount = subtotal * (profit_margin / 100)
        maintenance_cost = maintenance_months * maintenance_monthly_rate
        total = subtotal + risk_amount + profit_amount + hardware_costs + software_costs + maintenance_cost

        return {
            "model_type": "value_based",
            "subtotal": round(subtotal, 2),
            "hardware_cost": round(hardware_costs, 2),
            "software_cost": round(software_costs, 2),
            "risk_amount": round(risk_amount, 2),
            "profit_amount": round(profit_amount, 2),
            "maintenance_cost": round(maintenance_cost, 2),
            "total_cost": round(total, 2),
            "breakdown": {
                "client_revenue": estimated_client_revenue,
                "value_pct": value_percentage,
                "value_amount": round(subtotal, 2),
            },
        }

    @staticmethod
    def calculate_complexity_multiplier(
        hourly_rate: float,
        estimated_hours: float,
        complexity_multiplier: float = 1.0,
        risk_percentage: float = 10.0,
        profit_margin: float = 15.0,
        hardware_costs: float = 0.0,
        software_costs: float = 0.0,
        maintenance_months: int = 0,
        maintenance_monthly_rate: float = 0.0,
    ) -> Dict[str, Any]:
        """Algorithm 4: Base Cost × Complexity Multiplier"""
        base_cost = hourly_rate * estimated_hours
        subtotal = base_cost * complexity_multiplier
        risk_amount = subtotal * (risk_percentage / 100)
        profit_amount = subtotal * (profit_margin / 100)
        maintenance_cost = maintenance_months * maintenance_monthly_rate
        total = subtotal + risk_amount + profit_amount + hardware_costs + software_costs + maintenance_cost

        return {
            "model_type": "complexity_multiplier",
            "subtotal": round(subtotal, 2),
            "hardware_cost": round(hardware_costs, 2),
            "software_cost": round(software_costs, 2),
            "risk_amount": round(risk_amount, 2),
            "profit_amount": round(profit_amount, 2),
            "maintenance_cost": round(maintenance_cost, 2),
            "total_cost": round(total, 2),
            "breakdown": {
                "base_cost": round(base_cost, 2),
                "multiplier": complexity_multiplier,
                "adjusted_cost": round(subtotal, 2),
            },
        }

    @staticmethod
    def calculate_modular(
        hourly_rate: float,
        modules: Dict[str, float],
        risk_percentage: float = 10.0,
        profit_margin: float = 15.0,
        hardware_costs: float = 0.0,
        software_costs: float = 0.0,
        maintenance_months: int = 0,
        maintenance_monthly_rate: float = 0.0,
    ) -> Dict[str, Any]:
        """Algorithm 5: Per-module pricing (Research, Design, Dev, Testing, Docs, Deploy)"""
        default_modules = {
            "research": 0,
            "design": 0,
            "development": 0,
            "testing": 0,
            "documentation": 0,
            "deployment": 0,
        }
        merged = {**default_modules, **(modules or {})}

        module_costs = {}
        subtotal = 0
        for module_name, hours in merged.items():
            cost = hours * hourly_rate
            module_costs[module_name] = {"hours": hours, "cost": round(cost, 2)}
            subtotal += cost

        risk_amount = subtotal * (risk_percentage / 100)
        profit_amount = subtotal * (profit_margin / 100)
        maintenance_cost = maintenance_months * maintenance_monthly_rate
        total = subtotal + risk_amount + profit_amount + hardware_costs + software_costs + maintenance_cost

        return {
            "model_type": "modular",
            "subtotal": round(subtotal, 2),
            "hardware_cost": round(hardware_costs, 2),
            "software_cost": round(software_costs, 2),
            "risk_amount": round(risk_amount, 2),
            "profit_amount": round(profit_amount, 2),
            "maintenance_cost": round(maintenance_cost, 2),
            "total_cost": round(total, 2),
            "breakdown": {
                "modules": module_costs,
                "total_hours": sum(merged.values()),
            },
        }

    def calculate(self, request_data: dict) -> Dict[str, Any]:
        """Route to the correct pricing model based on model_type."""
        model_type = request_data.get("model_type", "hourly")
        common = {
            "risk_percentage": request_data.get("risk_percentage", 10.0),
            "profit_margin": request_data.get("profit_margin", 15.0),
            "hardware_costs": request_data.get("hardware_costs", 0.0),
            "software_costs": request_data.get("software_costs", 0.0),
            "maintenance_months": request_data.get("maintenance_months", 0),
            "maintenance_monthly_rate": request_data.get("maintenance_monthly_rate", 0.0),
        }

        if model_type == "hourly":
            return self.calculate_hourly(
                hourly_rate=request_data.get("hourly_rate", 50.0),
                estimated_hours=request_data.get("estimated_hours", 0.0),
                **common,
            )
        elif model_type == "fixed":
            return self.calculate_fixed(
                hourly_rate=request_data.get("hourly_rate", 50.0),
                estimated_hours=request_data.get("estimated_hours", 0.0),
                **common,
            )
        elif model_type == "value_based":
            return self.calculate_value_based(
                estimated_client_revenue=request_data.get("estimated_client_revenue", 0.0),
                value_percentage=request_data.get("value_percentage", 10.0),
                **common,
            )
        elif model_type == "complexity_multiplier":
            return self.calculate_complexity_multiplier(
                hourly_rate=request_data.get("hourly_rate", 50.0),
                estimated_hours=request_data.get("estimated_hours", 0.0),
                complexity_multiplier=request_data.get("complexity_multiplier", 1.0),
                **common,
            )
        elif model_type == "modular":
            return self.calculate_modular(
                hourly_rate=request_data.get("hourly_rate", 50.0),
                modules=request_data.get("modules", {}),
                **common,
            )
        else:
            raise ValueError(f"Unknown pricing model: {model_type}")


pricing_engine = PricingEngine()
