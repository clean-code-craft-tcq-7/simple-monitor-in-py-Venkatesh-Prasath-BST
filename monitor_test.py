import pytest
from unittest.mock import patch
from monitor import vitals_ok, is_temperature_ok, is_pulse_rate_ok, is_spo2_ok


class TestTemperature:
    """Test cases for temperature validation"""
    
    def test_temperature_within_range(self):
        """Test temperature within valid range (95-102)"""
        assert is_temperature_ok(98.6) == True
        assert is_temperature_ok(95) == True
        assert is_temperature_ok(102) == True
        assert is_temperature_ok(100.5) == True
    
    def test_temperature_below_range(self):
        """Test temperature below minimum (95)"""
        with patch('monitor.__display_vital_alert') as mock_alert:
            assert is_temperature_ok(94.9) == False
            mock_alert.assert_called_once_with(6, 'Temperature is out of range!')
        
        with patch('monitor.__display_vital_alert'):
            assert is_temperature_ok(90) == False
    
    def test_temperature_above_range(self):
        """Test temperature above maximum (102)"""
        with patch('monitor.__display_vital_alert') as mock_alert:
            assert is_temperature_ok(102.1) == False
            mock_alert.assert_called_once_with(6, 'Temperature is out of range!')
        
        with patch('monitor.__display_vital_alert'):
            assert is_temperature_ok(105) == False
    
    def test_temperature_boundary_values(self):
        """Test boundary values"""
        assert is_temperature_ok(95.0) == True
        assert is_temperature_ok(102.0) == True
        
        with patch('monitor.__display_vital_alert'):
            assert is_temperature_ok(94.99999) == False
            assert is_temperature_ok(102.00001) == False
    
    def test_temperature_type_error(self):
        """Test type errors for temperature"""
        with pytest.raises(TypeError):
            is_temperature_ok("98.6")
        
        with pytest.raises(TypeError):
            is_temperature_ok(None)
        
        with pytest.raises(TypeError):
            is_temperature_ok([98.6])


class TestPulseRate:
    """Test cases for pulse rate validation"""
    
    def test_pulse_rate_within_range(self):
        """Test pulse rate within valid range (60-100)"""
        assert is_pulse_rate_ok(70) == True
        assert is_pulse_rate_ok(60) == True
        assert is_pulse_rate_ok(100) == True
        assert is_pulse_rate_ok(85) == True
    
    def test_pulse_rate_below_range(self):
        """Test pulse rate below minimum (60)"""
        with patch('monitor.__display_vital_alert') as mock_alert:
            assert is_pulse_rate_ok(59) == False
            mock_alert.assert_called_once_with(6, 'Pulse Rate is out of range!')
        
        with patch('monitor.__display_vital_alert'):
            assert is_pulse_rate_ok(45) == False
    
    def test_pulse_rate_above_range(self):
        """Test pulse rate above maximum (100)"""
        with patch('monitor.__display_vital_alert') as mock_alert:
            assert is_pulse_rate_ok(101) == False
            mock_alert.assert_called_once_with(6, 'Pulse Rate is out of range!')
        
        with patch('monitor.__display_vital_alert'):
            assert is_pulse_rate_ok(120) == False
    
    def test_pulse_rate_boundary_values(self):
        """Test boundary values"""
        assert is_pulse_rate_ok(60) == True
        assert is_pulse_rate_ok(100) == True
        
        with patch('monitor.__display_vital_alert'):
            assert is_pulse_rate_ok(59.9) == False
            assert is_pulse_rate_ok(100.1) == False
    
    def test_pulse_rate_type_error(self):
        """Test type errors for pulse rate"""
        with pytest.raises(TypeError):
            is_pulse_rate_ok("70")
        
        with pytest.raises(TypeError):
            is_pulse_rate_ok(None)
        
        with pytest.raises(TypeError):
            is_pulse_rate_ok([70])


class TestSpo2:
    """Test cases for SpO2 validation"""
    
    def test_spo2_within_range(self):
        """Test SpO2 within valid range (90 and above)"""
        assert is_spo2_ok(95) == True
        assert is_spo2_ok(90) == True
        assert is_spo2_ok(100) == True
        assert is_spo2_ok(99.5) == True
        assert is_spo2_ok(150) == True  # No upper limit
    
    def test_spo2_below_range(self):
        """Test SpO2 below minimum (90)"""
        with patch('monitor.__display_vital_alert') as mock_alert:
            assert is_spo2_ok(89) == False
            mock_alert.assert_called_once_with(6, 'Oxygen Saturation is out of range!')
        
        with patch('monitor.__display_vital_alert'):
            assert is_spo2_ok(85) == False
    
    def test_spo2_boundary_values(self):
        """Test boundary values"""
        assert is_spo2_ok(90.0) == True
        assert is_spo2_ok(90.1) == True
        
        with patch('monitor.__display_vital_alert'):
            assert is_spo2_ok(89.9) == False
    
    def test_spo2_type_error(self):
        """Test type errors for SpO2"""
        with pytest.raises(TypeError):
            is_spo2_ok("95")
        
        with pytest.raises(TypeError):
            is_spo2_ok(None)
        
        with pytest.raises(TypeError):
            is_spo2_ok([95])


class TestVitalsOk:
    """Test cases for overall vitals validation"""
    
    def test_all_vitals_ok(self):
        """Test when all vitals are within normal range"""
        assert vitals_ok(98.6, 70, 95) == True
        assert vitals_ok(95, 60, 90) == True
        assert vitals_ok(102, 100, 100) == True
    
    def test_temperature_not_ok(self):
        """Test when only temperature is out of range"""
        with patch('monitor.__display_vital_alert'):
            assert vitals_ok(94, 70, 95) == False
            assert vitals_ok(103, 70, 95) == False
    
    def test_pulse_rate_not_ok(self):
        """Test when only pulse rate is out of range"""
        with patch('monitor.__display_vital_alert'):
            assert vitals_ok(98.6, 59, 95) == False
            assert vitals_ok(98.6, 101, 95) == False
    
    def test_spo2_not_ok(self):
        """Test when only SpO2 is out of range"""
        with patch('monitor.__display_vital_alert'):
            assert vitals_ok(98.6, 70, 89) == False
    
    def test_multiple_vitals_not_ok(self):
        """Test when multiple vitals are out of range"""
        with patch('monitor.__display_vital_alert'):
            assert vitals_ok(94, 59, 89) == False
            assert vitals_ok(103, 101, 89) == False
    
    def test_vitals_ok_with_original_test_cases(self):
        """Test with original test cases from the file"""
        with patch('monitor.__display_vital_alert'):
            assert vitals_ok(99, 102, 70) == False  # pulse rate too high
        
        assert vitals_ok(98.1, 70, 98) == True
    
    def test_vitals_ok_type_errors(self):
        """Test type errors for vitals_ok function"""
        with pytest.raises(TypeError):
            vitals_ok("98.6", 70, 95)
        
        with pytest.raises(TypeError):
            vitals_ok(98.6, "70", 95)
        
        with pytest.raises(TypeError):
            vitals_ok(98.6, 70, "95")
        
        with pytest.raises(TypeError):
            vitals_ok(None, 70, 95)


class TestEdgeCases:
    """Test edge cases and special scenarios"""
    
    def test_zero_values(self):
        """Test with zero values"""
        with patch('monitor.__display_vital_alert'):
            assert is_temperature_ok(0) == False
            assert is_pulse_rate_ok(0) == False
            assert is_spo2_ok(0) == False
    
    def test_negative_values(self):
        """Test with negative values"""
        with patch('monitor.__display_vital_alert'):
            assert is_temperature_ok(-1) == False
            assert is_pulse_rate_ok(-1) == False
            assert is_spo2_ok(-1) == False
    
    def test_very_large_values(self):
        """Test with very large values"""
        with patch('monitor.__display_vital_alert'):
            assert is_temperature_ok(1000) == False
            assert is_pulse_rate_ok(1000) == False
            assert is_spo2_ok(1000) == False
    
    def test_float_precision(self):
        """Test with floating point precision"""
        assert is_temperature_ok(95.000001) == True
        assert is_pulse_rate_ok(60.000001) == True
        assert is_spo2_ok(90.000001) == True


if __name__ == '__main__':
    pytest.main([__file__])