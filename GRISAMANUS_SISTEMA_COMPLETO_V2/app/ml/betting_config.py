import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
class BettingConfig:


    def __init__(self, 
                 conf_alta=0.80,
                 conf_media_min=0.70,
                 conf_media_max=0.79,
                 conf_baixa_min=0.55,
                 conf_baixa_max=0.69,
                 stake_base=20.00,
                 stake_alta_pct=100,
                 stake_media_pct=50,
                 stake_baixa_pct=25):
        
        self.conf_alta = conf_alta
        self.conf_media_min = conf_media_min
        self.conf_media_max = conf_media_max
        self.conf_baixa_min = conf_baixa_min
        self.conf_baixa_max = conf_baixa_max
        
        self.stake_base = stake_base
        self.stake_alta_pct = stake_alta_pct
        self.stake_media_pct = stake_media_pct
        self.stake_baixa_pct = stake_baixa_pct
    
    def calibrar_confianca(self, prob):
        """Determine confidence level based on probability"""
        if prob >= self.conf_alta:
            return 'alta'
        elif prob >= self.conf_media_min:
            return 'média'
        elif prob >= self.conf_baixa_min:
            return 'baixa'
        else:
            return 'fraca'
    
    def calcular_stake(self, confidence_level):
        """Calculate stake amount based on confidence level"""
        if confidence_level == 'alta':
            return self.stake_base * (self.stake_alta_pct / 100)
        elif confidence_level == 'média':
            return self.stake_base * (self.stake_media_pct / 100)
        elif confidence_level == 'baixa':
            return self.stake_base * (self.stake_baixa_pct / 100)
        return 0  # No bet for 'fraca' confidence
    
    def to_dict(self):
        """Serialize config to dictionary"""
        return {
            'conf_alta': self.conf_alta,
            'conf_media_min': self.conf_media_min,
            'conf_media_max': self.conf_media_max,
            'conf_baixa_min': self.conf_baixa_min,
            'conf_baixa_max': self.conf_baixa_max,
            'stake_base': self.stake_base,
            'stake_alta_pct': self.stake_alta_pct,
            'stake_media_pct': self.stake_media_pct,
            'stake_baixa_pct': self.stake_baixa_pct
        }
    
    @classmethod
    def from_dict(cls, config_dict):
        """Robust dictionary conversion that handles both GUI and native formats"""
        # First check if it's a GUI-style config
        if 'niveis_confianca' in config_dict and 'stake' in config_dict:
            gui_config = config_dict
            return cls(
                conf_alta=gui_config['niveis_confianca']['ALTA'],
                conf_media_min=gui_config['niveis_confianca']['MEDIA'],
                conf_media_max=min(gui_config['niveis_confianca']['MEDIA'] + 0.09, 0.99),
                conf_baixa_min=gui_config['niveis_confianca']['BAIXA'],
                conf_baixa_max=min(gui_config['niveis_confianca']['BAIXA'] + 0.14, 0.69),
                stake_base=20.00,  # Default from class
                stake_alta_pct=gui_config['stake']['ALTA'],
                stake_media_pct=gui_config['stake']['MEDIA'],
                stake_baixa_pct=gui_config['stake']['BAIXA']
            )
        # Otherwise assume it's a native config format
        else:
            # Fill missing values with defaults
            defaults = {
                'conf_media_max': min(config_dict.get('conf_media_min', 0.70) + 0.09, 0.99),
                'conf_baixa_max': min(config_dict.get('conf_baixa_min', 0.55) + 0.14, 0.69),
                'stake_base': 20.00
            }
            merged = {**defaults, **config_dict}
            return cls(**merged)
    def save_config(config, path):
        """Save configuration to JSON file"""
        with open(path, 'w') as f:
            json.dump(config.to_dict(), f, indent=2)

    def load_config(path):
        """Load configuration from JSON file"""
        with open(path) as f:
            return BettingConfig.from_dict(json.load(f))