"""
Tests for KPI city analytics
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from kpi_city import city_kpi


class TestCityKPI:
    """Test suite for city_kpi function"""
    
    def test_valid_city_returns_kpi(self):
        """
        Happy-path test: calling city_kpi with valid city should return KPI dict
        """
        result = city_kpi("Mumbai")
        
        # Assert result is a dictionary
        assert isinstance(result, dict), "Result should be a dictionary"
        
        # Assert expected keys are present
        assert "city" in result
        assert "total_customers" in result
        assert "avg_spend" in result
        assert "churn_rate" in result
        
        # Assert Mumbai has data
        assert result["total_customers"] > 0, "Mumbai should have customers"
        assert result["city"] == "Mumbai"
    
    def test_sql_injection_attempt_returns_none(self):
        """
        Security test: SQL injection attempt should NOT return all rows.
        Parameterized SQL should safely treat the injection string as a literal value.
        """
        injection_attempt = "Mumbai' OR 1=1 --"
        result = city_kpi(injection_attempt)
        
        # Injection attempt should return None (no matching city with that exact name)
        assert result is None, (
            "SQL injection attempt should return None (no exact match). "
            "Parameterized SQL should prevent injection and not return all rows."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
